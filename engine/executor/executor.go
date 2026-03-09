package executor

import (
	"context"
	"errors"
	"fmt"
	"log"
	"time"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"princeton-trading/engine/db"
	"princeton-trading/engine/models"
)

const PriceUpdateMessage = "PRICE_UPDATE"

// Dispatch routes a queue message to the appropriate handler.
func Dispatch(ctx context.Context, msg string) {
	if msg == PriceUpdateMessage {
		handlePriceUpdate(ctx)
	} else {
		handleOrderPlaced(ctx, msg)
	}
}

// handleOrderPlaced loads the order, checks eligibility, and executes if conditions are met.
func handleOrderPlaced(ctx context.Context, orderID string) {
	order, err := loadOrder(ctx, orderID)
	if err != nil {
		log.Printf("load order %s: %v", orderID, err)
		return
	}

	price, err := loadPrice(ctx, order.Symbol)
	if err != nil {
		log.Printf("load price %s: %v", order.Symbol, err)
		return
	}

	if !isEligible(order, price) {
		return
	}

	if err := executeOrder(ctx, order, price); err != nil {
		log.Printf("execute order %s: %v", order.ID, err)
	}
}

// handlePriceUpdate re-evaluates all open limit orders against the latest prices.
func handlePriceUpdate(ctx context.Context) {
	orders, err := loadOpenLimitOrders(ctx)
	if err != nil {
		log.Printf("load open limit orders: %v", err)
		return
	}

	for _, order := range orders {
		price, err := loadPrice(ctx, order.Symbol)
		if err != nil {
			log.Printf("load price %s: %v", order.Symbol, err)
			continue
		}

		if !isEligible(order, price) {
			continue
		}

		if err := executeOrder(ctx, order, price); err != nil {
			log.Printf("execute order %s: %v", order.ID, err)
		}
	}
}

// isEligible returns true if an order should execute at the given price.
// Market orders always execute. Limit BUY fills when price <= limit; SELL when price >= limit.
func isEligible(order *models.Order, price *models.Price) bool {
	if order.Type == models.OrderTypeMarket {
		return true
	}

	if order.LimitPrice == nil {
		return false
	}

	switch order.Side {
	case models.OrderSideBuy:
		return price.Price <= *order.LimitPrice
	case models.OrderSideSell:
		return price.Price >= *order.LimitPrice
	}

	return false
}

// executeOrder opens a transaction and delegates to executeBuy or executeSell.
func executeOrder(ctx context.Context, order *models.Order, price *models.Price) error {
	tx, err := db.Pool.Begin(ctx)
	if err != nil {
		return fmt.Errorf("begin tx: %w", err)
	}
	defer tx.Rollback(ctx)

	switch order.Side {
	case models.OrderSideBuy:
		if err := executeBuy(ctx, tx, order, price.Price); err != nil {
			return err
		}
	case models.OrderSideSell:
		if err := executeSell(ctx, tx, order, price.Price); err != nil {
			return err
		}
	default:
		return fmt.Errorf("unknown order side: %s", order.Side)
	}

	return tx.Commit(ctx)
}

// executeBuy verifies the account has sufficient cash, then settles the trade.
func executeBuy(ctx context.Context, tx pgx.Tx, order *models.Order, price float64) error {
	balance, err := loadBalanceTx(ctx, tx, order.AccountID)
	if err != nil {
		return fmt.Errorf("load balance: %w", err)
	}

	totalCost := float64(order.Quantity) * price
	if balance.AvailableAmount < totalCost {
		return fmt.Errorf("insufficient funds: need %.2f, have %.2f", totalCost, balance.AvailableAmount)
	}

	if err := updateBalance(ctx, tx, order.AccountID, -totalCost); err != nil {
		return fmt.Errorf("update balance: %w", err)
	}
	if err := upsertPosition(ctx, tx, order.AccountID, order.Symbol, order.Quantity); err != nil {
		return fmt.Errorf("upsert position: %w", err)
	}
	if err := insertTrade(ctx, tx, order, price); err != nil {
		return fmt.Errorf("insert trade: %w", err)
	}
	if err := markOrderFilled(ctx, tx, order.ID); err != nil {
		return fmt.Errorf("mark order filled: %w", err)
	}

	return nil
}

// executeSell verifies the account holds enough shares, then settles the trade.
func executeSell(ctx context.Context, tx pgx.Tx, order *models.Order, price float64) error {
	position, err := loadPositionTx(ctx, tx, order.AccountID, order.Symbol)
	if err != nil {
		return fmt.Errorf("load position: %w", err)
	}

	if position.Quantity < order.Quantity {
		return fmt.Errorf("insufficient shares: need %d, have %d", order.Quantity, position.Quantity)
	}

	proceeds := float64(order.Quantity) * price

	if err := updateBalance(ctx, tx, order.AccountID, proceeds); err != nil {
		return fmt.Errorf("update balance: %w", err)
	}
	if err := upsertPosition(ctx, tx, order.AccountID, order.Symbol, -order.Quantity); err != nil {
		return fmt.Errorf("upsert position: %w", err)
	}
	if err := insertTrade(ctx, tx, order, price); err != nil {
		return fmt.Errorf("insert trade: %w", err)
	}
	if err := markOrderFilled(ctx, tx, order.ID); err != nil {
		return fmt.Errorf("mark order filled: %w", err)
	}

	return nil
}

// --- DB read helpers ---

// loadOrder fetches a single OPEN order by ID.
func loadOrder(ctx context.Context, orderID string) (*models.Order, error) {
	row := db.Pool.QueryRow(ctx, `
		SELECT id, account_id, competition_id, symbol, side, type, quantity,
		       status, limit_price, filled_at, canceled_at, created_at
		FROM orders
		WHERE id = $1 AND status = 'OPEN'
	`, orderID)

	var o models.Order
	err := row.Scan(
		&o.ID, &o.AccountID, &o.CompetitionID,
		&o.Symbol, &o.Side, &o.Type, &o.Quantity,
		&o.Status, &o.LimitPrice, &o.FilledAt, &o.CanceledAt, &o.CreatedAt,
	)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, fmt.Errorf("order %s not found or not OPEN", orderID)
	}
	return &o, err
}

// loadOpenLimitOrders fetches all OPEN limit orders across all accounts.
func loadOpenLimitOrders(ctx context.Context) ([]*models.Order, error) {
	rows, err := db.Pool.Query(ctx, `
		SELECT id, account_id, competition_id, symbol, side, type, quantity,
		       status, limit_price, filled_at, canceled_at, created_at
		FROM orders
		WHERE status = 'OPEN' AND type = 'LIMIT'
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var orders []*models.Order
	for rows.Next() {
		var o models.Order
		if err := rows.Scan(
			&o.ID, &o.AccountID, &o.CompetitionID,
			&o.Symbol, &o.Side, &o.Type, &o.Quantity,
			&o.Status, &o.LimitPrice, &o.FilledAt, &o.CanceledAt, &o.CreatedAt,
		); err != nil {
			return nil, err
		}
		orders = append(orders, &o)
	}

	return orders, rows.Err()
}

// loadPrice fetches the latest cached price for a symbol.
func loadPrice(ctx context.Context, symbol string) (*models.Price, error) {
	row := db.Pool.QueryRow(ctx, `
		SELECT symbol, price, updated_at FROM prices WHERE symbol = $1
	`, symbol)

	var p models.Price
	err := row.Scan(&p.Symbol, &p.Price, &p.UpdatedAt)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, fmt.Errorf("no price found for symbol %s", symbol)
	}
	return &p, err
}

// loadBalanceTx fetches and locks the balance row for an account within a transaction.
func loadBalanceTx(ctx context.Context, tx pgx.Tx, accountID uuid.UUID) (*models.Balance, error) {
	row := tx.QueryRow(ctx, `
		SELECT id, account_id, available_amount, reserved_amount, updated_at
		FROM balances
		WHERE account_id = $1
		FOR UPDATE
	`, accountID)

	var b models.Balance
	err := row.Scan(&b.ID, &b.AccountID, &b.AvailableAmount, &b.ReservedAmount, &b.UpdatedAt)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, fmt.Errorf("no balance found for account %s", accountID)
	}
	return &b, err
}

// loadPositionTx fetches and locks the position row for an account+symbol within a transaction.
func loadPositionTx(ctx context.Context, tx pgx.Tx, accountID uuid.UUID, symbol string) (*models.Position, error) {
	row := tx.QueryRow(ctx, `
		SELECT id, account_id, symbol, quantity, reserved_quantity, updated_at
		FROM positions
		WHERE account_id = $1 AND symbol = $2
		FOR UPDATE
	`, accountID, symbol)

	var p models.Position
	err := row.Scan(&p.ID, &p.AccountID, &p.Symbol, &p.Quantity, &p.ReservedQuantity, &p.UpdatedAt)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, fmt.Errorf("no position for account %s symbol %s", accountID, symbol)
	}
	return &p, err
}

// --- DB write helpers ---

// updateBalance adds delta (positive or negative) to available_amount.
func updateBalance(ctx context.Context, tx pgx.Tx, accountID uuid.UUID, delta float64) error {
	_, err := tx.Exec(ctx, `
		UPDATE balances
		SET available_amount = available_amount + $1, updated_at = $2
		WHERE account_id = $3
	`, delta, time.Now().UTC(), accountID)
	return err
}

// upsertPosition adds delta shares to the position row, creating it if it doesn't exist.
func upsertPosition(ctx context.Context, tx pgx.Tx, accountID uuid.UUID, symbol string, delta int) error {
	_, err := tx.Exec(ctx, `
		INSERT INTO positions (id, account_id, symbol, quantity, reserved_quantity, updated_at)
		VALUES ($1, $2, $3, $4, 0, $5)
		ON CONFLICT (account_id, symbol)
		DO UPDATE SET quantity = positions.quantity + $4, updated_at = $5
	`, uuid.New(), accountID, symbol, delta, time.Now().UTC())
	return err
}

// insertTrade writes a new trade record to the ledger.
func insertTrade(ctx context.Context, tx pgx.Tx, order *models.Order, price float64) error {
	_, err := tx.Exec(ctx, `
		INSERT INTO trades (id, order_id, account_id, symbol, side, quantity, price, executed_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
	`, uuid.New(), order.ID, order.AccountID, order.Symbol, order.Side, order.Quantity, price, time.Now().UTC())
	return err
}

// markOrderFilled sets the order status to FILLED and records the filled_at timestamp.
func markOrderFilled(ctx context.Context, tx pgx.Tx, orderID uuid.UUID) error {
	_, err := tx.Exec(ctx, `
		UPDATE orders SET status = 'FILLED', filled_at = $1 WHERE id = $2
	`, time.Now().UTC(), orderID)
	return err
}
