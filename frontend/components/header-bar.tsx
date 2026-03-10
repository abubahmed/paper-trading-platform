"use client";

import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";

const MOCK_PORTFOLIO = {
  startingCash: 100000,
  cashBalance: 62450.75,
  investedAmount: 38720.5,
  portfolioValue: 103171.25,
  pnl: 3171.25,
  pnlPercent: 3.17,
};

const MOCK_COMPETITION = {
  season: "Spring 2026",
  status: "Active",
};

const MOCK_USER = {
  name: "John Doe",
  rank: 4,
};

function formatCurrency(value: number) {
  return value.toLocaleString("en-US", { style: "currency", currency: "USD" });
}

function StatItem({ label, value, className }: { label: string; value: string; className?: string }) {
  return (
    <div className="flex flex-col gap-0">
      <span className="text-[10px] uppercase tracking-wider text-muted-foreground">{label}</span>
      <span className={cn("font-mono text-xs font-semibold", className)}>{value}</span>
    </div>
  );
}

export function HeaderBar() {
  const pnlPositive = MOCK_PORTFOLIO.pnl >= 0;

  return (
    <div className="flex items-center gap-0 px-3 py-1.5">
      {/* Logo + Title */}
      <div className="flex items-center gap-2 pr-4">
        <img
          src="https://brandlogos.net/wp-content/uploads/2025/05/princeton_seal-logo_brandlogos.net_k7qwf.png"
          alt="Princeton"
          className="h-7 w-7 object-contain"
        />
        <div className="flex flex-col">
          <span className="text-xs font-bold tracking-wide text-foreground">Princeton Trading</span>
          <span className="text-[10px] text-muted-foreground">Paper Trading Competition</span>
        </div>
      </div>

      <Separator orientation="vertical" className="mx-3 !h-8" />

      {/* Portfolio stats */}
      <div className="flex items-center gap-4">
        <StatItem label="Starting Cash" value={formatCurrency(MOCK_PORTFOLIO.startingCash)} />
        <StatItem label="Cash Balance" value={formatCurrency(MOCK_PORTFOLIO.cashBalance)} />
        <StatItem label="Invested" value={formatCurrency(MOCK_PORTFOLIO.investedAmount)} />
        <StatItem label="Portfolio Value" value={formatCurrency(MOCK_PORTFOLIO.portfolioValue)} className="text-foreground" />
        <StatItem
          label="P&L"
          value={`${pnlPositive ? "+" : ""}${formatCurrency(MOCK_PORTFOLIO.pnl)} (${pnlPositive ? "+" : ""}${MOCK_PORTFOLIO.pnlPercent.toFixed(2)}%)`}
          className={pnlPositive ? "text-emerald-400" : "text-red-400"}
        />
      </div>

      <Separator orientation="vertical" className="mx-3 !h-8" />

      {/* Competition info */}
      <div className="flex items-center gap-3">
        <StatItem label="Season" value={MOCK_COMPETITION.season} />
        <Badge variant="outline" className="rounded border-0 bg-emerald-500/10 text-[10px] text-emerald-400">
          {MOCK_COMPETITION.status}
        </Badge>
      </div>

      {/* User info — pushed to right */}
      <div className="ml-auto flex items-center gap-3">
        <div className="flex flex-col items-end gap-0">
          <span className="text-xs font-semibold text-foreground">{MOCK_USER.name}</span>
          <span className="text-[10px] text-muted-foreground">Rank #{MOCK_USER.rank}</span>
        </div>
        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-muted text-[10px] font-semibold text-muted-foreground">
          {MOCK_USER.name.split(" ").map(n => n[0]).join("")}
        </div>
      </div>
    </div>
  );
}
