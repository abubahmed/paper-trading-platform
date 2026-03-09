package models

import (
	"time"

	"github.com/google/uuid"
)

type OrderSide string

const (
	OrderSideBuy  OrderSide = "BUY"
	OrderSideSell OrderSide = "SELL"
)

type OrderType string

const (
	OrderTypeMarket OrderType = "MARKET"
	OrderTypeLimit  OrderType = "LIMIT"
)

type OrderStatus string

const (
	OrderStatusOpen     OrderStatus = "OPEN"
	OrderStatusFilled   OrderStatus = "FILLED"
	OrderStatusCanceled OrderStatus = "CANCELED"
)

type User struct {
	ID         uuid.UUID
	ClerkID    string
	FirstName  string
	LastName   string
	Email      string
	Username   string
	NetID      string
	ClassYear  int
	Active     bool
	LastSeenAt *time.Time
	CreatedAt  time.Time
}

type Competition struct {
	ID          uuid.UUID
	Name        string
	Description string
	StartTime   time.Time
	EndTime     time.Time
	InitialCash float64
	IsActive    bool
	CreatedAt   time.Time
}

type Account struct {
	ID            uuid.UUID
	UserID        uuid.UUID
	CompetitionID uuid.UUID
	CreatedAt     time.Time
}

type Balance struct {
	ID              uuid.UUID
	AccountID       uuid.UUID
	AvailableAmount float64
	ReservedAmount  float64
	UpdatedAt       time.Time
}

type Position struct {
	ID               uuid.UUID
	AccountID        uuid.UUID
	Symbol           string
	Quantity         int
	ReservedQuantity int
	UpdatedAt        time.Time
}

type Order struct {
	ID            uuid.UUID
	AccountID     uuid.UUID
	CompetitionID uuid.UUID
	Symbol        string
	Side          OrderSide
	Type          OrderType
	Quantity      int
	Status        OrderStatus
	LimitPrice    *float64
	FilledAt      *time.Time
	CanceledAt    *time.Time
	CreatedAt     time.Time
}

type Trade struct {
	ID         uuid.UUID
	OrderID    uuid.UUID
	AccountID  uuid.UUID
	Symbol     string
	Side       OrderSide
	Quantity   int
	Price      float64
	ExecutedAt time.Time
}

type Price struct {
	Symbol    string
	Price     float64
	UpdatedAt time.Time
}

type PriceBar struct {
	ID        int64
	Symbol    string
	Timestamp time.Time
	Timeframe string
	Open      float64
	High      float64
	Low       float64
	Close     float64
	Volume    int64
}
