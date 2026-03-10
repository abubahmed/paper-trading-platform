# Princeton Trading — Design Document

Princeton Trading is a paper trading platform built exclusively for Princeton University students. Students compete in seasonal trading competitions, managing simulated portfolios using real market data — without financial risk. Each competition runs for a fixed period, with the highest portfolio value winning a cash prize. The platform is designed to make finance and quantitative trading accessible and fun — whether you're a beginner curious about markets or a CS student eager to test your first trading algorithm.

---

## Architecture

```
Next.js Frontend
      ↓ HTTP
FastAPI Backend
      ↓ SQL              ↓ Redis
  Supabase DB        Queue Service
                          ↓
                   Go Trading Engine
                          ↓ SQL
                      Supabase DB
```

### Layers

**Next.js Frontend** — renders prices, portfolios, open orders, leaderboard, and the bot IDE. Sends buy/sell requests to the API. Refreshes state via polling.

**FastAPI Backend** — authenticates users, validates requests, records order intentions in the DB with `OPEN` status, pushes order IDs to the queue, and exposes read endpoints.

**Redis Queue** — serialized stream of work between the API and trading engine. Messages are consumed in order.

**Go Trading Engine** — long-running process that consumes messages from the queue, loads order and price data, deterministically evaluates and executes eligible trades, and updates balances, positions, and order status.

**PostgreSQL (Supabase)** — system of record. Stores all users, orders, trades, balances, positions, and price history.

**Price Ingestion Job** — scheduled Python process that fetches prices from Alpaca every 3 minutes, writes to the DB, and publishes a `PRICE_UPDATE` event to the queue.

---

## User Flow

1. Student submits an order via the frontend
2. Frontend sends `POST /orders/create` to the API
3. API authenticates the user and validates the request
4. API saves the order to the DB with status `OPEN`
5. API pushes `ORDER:{order_id}` to the Redis queue
6. Go engine consumes the message, loads the order and latest price
7. Engine evaluates execution conditions
8. If eligible, engine executes the trade — updates balance, position, order status, and inserts a trade record
9. Frontend polls the API and re-renders the updated portfolio

---

## Order Types

| Type         | Behavior                                              |
| ------------ | ----------------------------------------------------- |
| Market       | Executes immediately at the current cached price      |
| Limit (Buy)  | Executes when price drops to or below the limit price |
| Limit (Sell) | Executes when price rises to or above the limit price |

**Not supported in v1:** stop-loss orders, short selling.

### Limit Order Evaluation

- On placement: engine checks if condition is already met, executes immediately if so
- On every `PRICE_UPDATE`: engine re-evaluates all `OPEN` limit orders against new prices

### Queue Message Format

```
ORDER:{uuid}       → new order placed
PRICE_UPDATE       → new prices available, re-evaluate open limit orders
```

---

## Competition Rules

- Winner determined by **highest total portfolio value** at competition end
- All open orders are **automatically cancelled** when the competition ends
- **One active competition** at a time
- Students are enrolled in a competition via an `Account` record

---

## Authentication

- Students sign in via **Clerk** using Princeton SSO
- Access restricted to Princeton emails
- Account is automatically created on first login

---

## Database Schema

### Users

`id, clerk_id, first_name, last_name, email, username, netid, class_year, active, last_seen_at, created_at`

### Competition

`id, name, description, start_time, end_time, initial_cash, is_active, created_at`

### Account _(user × competition join)_

`id, user_id, competition_id, created_at`

### Order

`id, account_id, competition_id, symbol, side, type, quantity, status, limit_price, filled_at, canceled_at, created_at`

### Trade

`id, order_id, account_id, symbol, side, quantity, price, executed_at`

### Balance

`id, account_id, available_amount, reserved_amount, updated_at`

### Position

`id, account_id, symbol, quantity, reserved_quantity, updated_at`

### Price

`symbol, price, updated_at`

### PriceBar

`id, symbol, timestamp, timeframe, open, high, low, close, volume`

---

## API Routes

### Backend (FastAPI)

| Method | Route            | Description                          |
| ------ | ---------------- | ------------------------------------ |
| GET    | `/competition`   | Active competition metadata          |
| POST   | `/orders/create` | Create and enqueue a new order       |
| POST   | `/orders/cancel` | Cancel an open order                 |
| GET    | `/orders/list`   | All orders for the current user      |
| GET    | `/orders/open`   | Open orders for the current user     |
| GET    | `/orders/get`    | Single order detail                  |
| GET    | `/portfolio`     | Cash, positions, and portfolio value |
| GET    | `/prices`        | Latest cached prices                 |
| GET    | `/charts`        | Latest price bar data                |
| GET    | `/leaderboard`   | Competition leaderboard              |

---

## Price Data

**Provider:** Alpaca Market Data API  
**Endpoint:** `https://data.alpaca.markets/v2`  
**Auth:** `APCA-API-KEY-ID` and `APCA-API-SECRET-KEY` headers  
**Plan:** Free tier — 200 req/min, historical data since 2016, real-time IEX feed  
**Schedule:** Fetch every 3 minutes  
**Key endpoint:** `GET /v2/stocks/snapshots?symbols=AAPL,MSFT,...` — fetches all symbols in one call  
**Symbols:** Top 100 S&P 500 companies, hardcoded list

---

## Algorithm / Bot Trading

Students can write Python trading bots that run automatically inside the platform — no setup, no API keys, no deployment.

### Student Experience

1. Navigate to the Bot section of the platform
2. See a pre-filled code editor (Monaco — same engine as VS Code)
3. Write strategy inside a single function:

```python
def on_price_update(prices, portfolio):
    # prices — latest prices for all symbols
    # portfolio — current cash and positions
    if portfolio["cash"] > prices["AAPL"]:
        buy("AAPL", 1)
```

4. Hit save — the platform handles everything else

### Execution Model

- Platform calls the student's saved function **once per price update** (every 3 minutes)
- Fresh prices and portfolio are passed in on every call
- Students never manage scheduling, deployment, or API keys

### Data Available to Bots

- Latest prices for all symbols
- Full price bar history via `PriceBar` table
- Current portfolio — cash, positions, trade history
- No separate state system needed — price and trade history covers all strategy needs

### Not Supported in v1

- Short selling
- High frequency strategies
- External library imports

---

## Admin Panel

- Create and manage competitions (name, start/end time, initial cash, tracked symbols)
- Ban or reset student accounts
- View all orders, trades, and portfolios

---

## Notifications

- In-app notification when a limit order is filled

---

## Tech Stack

| Layer          | Tools                                                                                 |
| -------------- | ------------------------------------------------------------------------------------- |
| Frontend       | Next.js, Tailwind, shadcn/ui, TanStack Query, Recharts, Monaco Editor, Clerk, Zustand |
| Backend        | FastAPI, SQLAlchemy, Alembic, Redis, Pydantic                                         |
| Trading Engine | Go, pgx, go-redis                                                                     |
| Database       | PostgreSQL via Supabase                                                               |
| Deployment     | Vercel (frontend), Railway (backend + engine + Redis), Supabase (DB)                  |
| Bot Execution  | AWS Lambda (free tier)                                                                |

---

## Project Structure

```
princeton-trading/
├── package.json          # root dev scripts
├── frontend/             # Next.js app
│   ├── app/
│   ├── components/
│   └── lib/
├── backend/              # FastAPI app
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── ingestion/        # price ingestion job + scheduler
│   ├── core/             # db, config, queue
│   └── main.py
├── engine/               # Go trading engine
│   ├── main.go
│   ├── executor/
│   ├── queue/
│   └── models/
└── docs/
```

---

## Deployment

| Service                  | Platform   | Cost           |
| ------------------------ | ---------- | -------------- |
| Frontend                 | Vercel     | Free           |
| FastAPI + Engine + Redis | Railway    | ~$20/month     |
| Database                 | Supabase   | Free tier      |
| Bot execution            | AWS Lambda | Free tier      |
| **Total**                |            | **~$20/month** |
