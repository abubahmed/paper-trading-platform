"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { cn } from "@/lib/utils";

interface Trade {
  id: string;
  symbol: string;
  side: "BUY" | "SELL";
  quantity: number;
  price: number;
  status: "FILLED" | "CANCELED";
  executedAt: string;
}

const MOCK_TRADES: Trade[] = [
  { id: "1", symbol: "NVDA", side: "BUY", quantity: 10, price: 820.0, status: "FILLED", executedAt: "2026-03-09T14:05:00Z" },
  { id: "2", symbol: "AAPL", side: "BUY", quantity: 25, price: 178.5, status: "FILLED", executedAt: "2026-03-09T12:30:00Z" },
  { id: "3", symbol: "TSLA", side: "SELL", quantity: 5, price: 182.4, status: "FILLED", executedAt: "2026-03-09T11:15:00Z" },
  { id: "4", symbol: "META", side: "BUY", quantity: 8, price: 470.0, status: "FILLED", executedAt: "2026-03-08T15:45:00Z" },
  { id: "5", symbol: "MSFT", side: "BUY", quantity: 15, price: 390.2, status: "FILLED", executedAt: "2026-03-08T14:20:00Z" },
  { id: "6", symbol: "AMZN", side: "BUY", quantity: 10, price: 176.0, status: "CANCELED", executedAt: "2026-03-08T13:00:00Z" },
  { id: "7", symbol: "GOOGL", side: "BUY", quantity: 30, price: 138.0, status: "FILLED", executedAt: "2026-03-08T10:30:00Z" },
  { id: "8", symbol: "TSLA", side: "BUY", quantity: 20, price: 185.0, status: "FILLED", executedAt: "2026-03-07T16:10:00Z" },
  { id: "9", symbol: "WMT", side: "SELL", quantity: 15, price: 170.5, status: "FILLED", executedAt: "2026-03-07T11:45:00Z" },
  { id: "10", symbol: "V", side: "BUY", quantity: 12, price: 275.0, status: "CANCELED", executedAt: "2026-03-07T09:30:00Z" },
];

function formatCurrency(value: number) {
  return value.toLocaleString("en-US", { style: "currency", currency: "USD" });
}

function formatTime(dateStr: string) {
  return new Date(dateStr).toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
}

function sideColor(side: "BUY" | "SELL") {
  return side === "BUY" ? "bg-emerald-500/10 text-emerald-400" : "bg-red-500/10 text-red-400";
}

function statusColor(status: "FILLED" | "CANCELED") {
  return status === "FILLED" ? "bg-emerald-500/10 text-emerald-400" : "bg-muted text-muted-foreground";
}

export function TradeHistoryPanel({ showHeader = true }: { showHeader?: boolean }) {
  return (
    <Card className="h-full gap-0 rounded-none border-0 bg-transparent shadow-none ring-0">
      {showHeader && (
        <>
          <CardHeader className="py-2.5">
            <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Trade History
            </CardTitle>
          </CardHeader>
          <Separator />
        </>
      )}
      <CardContent className="flex-1 overflow-hidden p-0">
        <ScrollArea className="h-full">
          <Table>
            <TableHeader className="sticky top-0 z-10 bg-muted/30">
              <TableRow className="border-0 hover:bg-transparent">
                <TableHead className="h-auto py-1.5 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Symbol
                </TableHead>
                <TableHead className="h-auto py-1.5 text-center text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Side
                </TableHead>
                <TableHead className="h-auto py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Qty
                </TableHead>
                <TableHead className="h-auto py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Price
                </TableHead>
                <TableHead className="h-auto py-1.5 text-center text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Status
                </TableHead>
                <TableHead className="h-auto py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Time
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {MOCK_TRADES.map((t, i) => (
                <TableRow key={t.id} className={cn("border-0", i % 2 === 1 && "bg-muted/20")}>
                  <TableCell className="py-2">
                    <div className="text-xs font-semibold">{t.symbol}</div>
                  </TableCell>
                  <TableCell className="py-2 text-center">
                    <Badge variant="outline" className={cn("rounded border-0", sideColor(t.side))}>
                      {t.side}
                    </Badge>
                  </TableCell>
                  <TableCell className="py-2 text-right font-mono text-xs">
                    {t.quantity}
                  </TableCell>
                  <TableCell className="py-2 text-right font-mono text-xs">
                    {formatCurrency(t.price)}
                  </TableCell>
                  <TableCell className="py-2 text-center">
                    <Badge variant="outline" className={cn("rounded border-0", statusColor(t.status))}>
                      {t.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="py-2 text-right text-[11px] text-muted-foreground">
                    {formatTime(t.executedAt)}
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
