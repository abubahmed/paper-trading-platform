import type { ApiClient } from "@/hooks/use-api-client";

// ─── Auth ─────────────────────────────────────────────────────────────────────

export const getMe = (client: ApiClient) =>
  client.get("/auth/me");

// ─── Orders ───────────────────────────────────────────────────────────────────

export const createOrder = (
  client: ApiClient,
  order: any
) => client.post("/orders/create", order);

export const cancelOrder = (client: ApiClient, orderId: string) =>
  client.post("/orders/cancel", { order_id: orderId });

export const listOrders = (client: ApiClient) =>
  client.get("/orders/list");

export const listOpenOrders = (client: ApiClient) =>
  client.get("/orders/open");

export const getOrder = (client: ApiClient, orderId: string) =>
  client.get("/orders/get", { params: { order_id: orderId } });

// ─── Portfolio ────────────────────────────────────────────────────────────────

export const getBalance = (client: ApiClient) =>
  client.get("/portfolio/balance");

export const getPositions = (client: ApiClient) =>
  client.get("/portfolio/positions");

export const getPortfolioValue = (client: ApiClient) =>
  client.get("/portfolio/value");

export const getPortfolioSummary = (client: ApiClient) =>
  client.get("/portfolio/summary");

// ─── Prices ───────────────────────────────────────────────────────────────────

export const getPrices = (client: ApiClient) =>
  client.get("/prices/");

// ─── Leaderboard ─────────────────────────────────────────────────────────────

export const getLeaderboard = (client: ApiClient) =>
  client.get("/leaderboard/");
