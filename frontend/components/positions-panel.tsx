"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { cn } from "@/lib/utils";

interface Position {
  symbol: string;
  quantity: number;
  avgCost: number;
  currentPrice: number;
  marketValue: number;
  pnl: number;
  pnlPercent: number;
}

const MOCK_POSITIONS: Position[] = [
  { symbol: "AAPL", quantity: 25, avgCost: 178.5, currentPrice: 189.84, marketValue: 4746.0, pnl: 283.5, pnlPercent: 6.35 },
  { symbol: "NVDA", quantity: 10, avgCost: 820.0, currentPrice: 881.86, marketValue: 8818.6, pnl: 618.6, pnlPercent: 7.54 },
  { symbol: "MSFT", quantity: 15, avgCost: 390.2, currentPrice: 378.91, marketValue: 5683.65, pnl: -169.35, pnlPercent: -2.89 },
  { symbol: "TSLA", quantity: 20, avgCost: 185.0, currentPrice: 175.21, marketValue: 3504.2, pnl: -195.8, pnlPercent: -5.29 },
  { symbol: "META", quantity: 8, avgCost: 470.0, currentPrice: 493.5, marketValue: 3948.0, pnl: 188.0, pnlPercent: 5.0 },
  { symbol: "GOOGL", quantity: 30, avgCost: 138.0, currentPrice: 141.8, marketValue: 4254.0, pnl: 114.0, pnlPercent: 2.75 },
];

function formatCurrency(value: number) {
  return value.toLocaleString("en-US", { style: "currency", currency: "USD" });
}

function formatPnl(value: number) {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${formatCurrency(value)}`;
}

function formatPercent(value: number) {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

function pnlColor(value: number) {
  if (value > 0) return "bg-emerald-500/10 text-emerald-400";
  if (value < 0) return "bg-red-500/10 text-red-400";
  return "bg-muted text-muted-foreground";
}

export function PositionsPanel() {
  return (
    <Card className="h-full gap-0 rounded-none border-0 bg-transparent shadow-none ring-0">
      <CardHeader className="py-2.5">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Your Positions
        </CardTitle>
      </CardHeader>
      <Separator />
      <CardContent className="flex-1 overflow-hidden p-0">
        <ScrollArea className="h-full">
          <Table>
            <TableHeader className="sticky top-0 z-10 bg-muted/30">
              <TableRow className="border-0 hover:bg-transparent">
                <TableHead className="h-auto py-1.5 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Symbol
                </TableHead>
                <TableHead className="h-auto py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Qty
                </TableHead>
                <TableHead className="h-auto py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Avg Cost
                </TableHead>
                <TableHead className="h-auto py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Price
                </TableHead>
                <TableHead className="h-auto py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Mkt Value
                </TableHead>
                <TableHead className="h-auto py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  P&L
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {MOCK_POSITIONS.map((p, i) => (
                <TableRow key={p.symbol} className={cn("border-0", i % 2 === 1 && "bg-muted/20")}>
                  <TableCell className="py-2">
                    <div className="text-xs font-semibold">{p.symbol}</div>
                  </TableCell>
                  <TableCell className="py-2 text-right font-mono text-xs">
                    {p.quantity}
                  </TableCell>
                  <TableCell className="py-2 text-right font-mono text-xs text-muted-foreground">
                    {formatCurrency(p.avgCost)}
                  </TableCell>
                  <TableCell className="py-2 text-right font-mono text-xs">
                    {formatCurrency(p.currentPrice)}
                  </TableCell>
                  <TableCell className="py-2 text-right font-mono text-xs">
                    {formatCurrency(p.marketValue)}
                  </TableCell>
                  <TableCell className="py-2 text-right">
                    <Badge variant="outline" className={cn("rounded border-0", pnlColor(p.pnl))}>
                      {formatPnl(p.pnl)} ({formatPercent(p.pnlPercent)})
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
