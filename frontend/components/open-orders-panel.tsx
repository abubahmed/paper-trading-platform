"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { cn } from "@/lib/utils";

interface OpenOrder {
  id: string;
  symbol: string;
  side: "BUY" | "SELL";
  type: "MARKET" | "LIMIT";
  quantity: number;
  limitPrice: number | null;
  createdAt: string;
}

const MOCK_OPEN_ORDERS: OpenOrder[] = [
  { id: "1", symbol: "AAPL", side: "BUY", type: "LIMIT", quantity: 15, limitPrice: 185.0, createdAt: "2026-03-09T14:32:00Z" },
  { id: "2", symbol: "TSLA", side: "SELL", type: "LIMIT", quantity: 10, limitPrice: 180.0, createdAt: "2026-03-09T13:15:00Z" },
  { id: "3", symbol: "AMZN", side: "BUY", type: "LIMIT", quantity: 20, limitPrice: 175.0, createdAt: "2026-03-09T11:48:00Z" },
  { id: "4", symbol: "GOOGL", side: "BUY", type: "LIMIT", quantity: 25, limitPrice: 139.5, createdAt: "2026-03-08T16:20:00Z" },
  { id: "5", symbol: "JPM", side: "SELL", type: "LIMIT", quantity: 12, limitPrice: 200.0, createdAt: "2026-03-08T10:05:00Z" },
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

export function OpenOrdersPanel({ showHeader = true }: { showHeader?: boolean }) {
  return (
    <Card className="h-full gap-0 rounded-none border-0 bg-transparent shadow-none ring-0">
      {showHeader && (
        <>
          <CardHeader className="py-2.5">
            <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Open Orders
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
                  Limit
                </TableHead>
                <TableHead className="h-auto py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Time
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {MOCK_OPEN_ORDERS.map((o, i) => (
                <TableRow key={o.id} className={cn("border-0", i % 2 === 1 && "bg-muted/20")}>
                  <TableCell className="py-2">
                    <div className="text-xs font-semibold">{o.symbol}</div>
                    <div className="text-[11px] text-muted-foreground">{o.type}</div>
                  </TableCell>
                  <TableCell className="py-2 text-center">
                    <Badge variant="outline" className={cn("rounded border-0", sideColor(o.side))}>
                      {o.side}
                    </Badge>
                  </TableCell>
                  <TableCell className="py-2 text-right font-mono text-xs">
                    {o.quantity}
                  </TableCell>
                  <TableCell className="py-2 text-right font-mono text-xs text-muted-foreground">
                    {o.limitPrice ? formatCurrency(o.limitPrice) : "—"}
                  </TableCell>
                  <TableCell className="py-2 text-right text-[11px] text-muted-foreground">
                    {formatTime(o.createdAt)}
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
