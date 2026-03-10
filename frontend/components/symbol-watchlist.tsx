"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { cn } from "@/lib/utils";

interface WatchlistSymbol {
  ticker: string;
  name: string;
  price: number;
  changePercent: number;
}

const MOCK_SYMBOLS: WatchlistSymbol[] = [
  { ticker: "AAPL", name: "Apple Inc.", price: 189.84, changePercent: 1.23 },
  { ticker: "MSFT", name: "Microsoft Corp.", price: 378.91, changePercent: 0.67 },
  { ticker: "NVDA", name: "NVIDIA Corp.", price: 881.86, changePercent: 3.41 },
  { ticker: "GOOGL", name: "Alphabet Inc.", price: 141.8, changePercent: -0.52 },
  { ticker: "AMZN", name: "Amazon.com Inc.", price: 178.25, changePercent: -1.14 },
  { ticker: "META", name: "Meta Platforms", price: 493.5, changePercent: 2.08 },
  { ticker: "TSLA", name: "Tesla Inc.", price: 175.21, changePercent: -2.63 },
  { ticker: "JPM", name: "JPMorgan Chase", price: 196.2, changePercent: 0.34 },
  { ticker: "V", name: "Visa Inc.", price: 279.08, changePercent: 0.11 },
  { ticker: "WMT", name: "Walmart Inc.", price: 168.72, changePercent: -0.28 },
  { ticker: "JNJ", name: "Johnson & Johnson", price: 156.4, changePercent: 0.89 },
  { ticker: "PG", name: "Procter & Gamble", price: 162.35, changePercent: -0.15 },
];

function formatPrice(price: number) {
  return price.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
  });
}

function formatChange(changePercent: number) {
  const sign = changePercent >= 0 ? "+" : "";
  return `${sign}${changePercent.toFixed(2)}%`;
}

function changeColor(changePercent: number) {
  if (changePercent > 0) return "bg-emerald-500/10 text-emerald-400";
  if (changePercent < 0) return "bg-red-500/10 text-red-400";
  return "bg-muted text-muted-foreground";
}

export function SymbolWatchlist() {
  return (
    <Card className="h-full gap-0 rounded-none border-0 bg-transparent shadow-none ring-0">
      <CardHeader className="py-2.5">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Watchlist
        </CardTitle>
      </CardHeader>
      <Separator />
      <CardContent className="flex-1 overflow-hidden p-0">
        <ScrollArea className="h-full">
          <Table className="table-fixed">
            <TableHeader className="sticky top-0 z-10 bg-muted/30">
              <TableRow className="border-0 hover:bg-transparent">
                <TableHead className="h-auto py-1.5 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Symbol
                </TableHead>
                <TableHead className="h-auto w-20 py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Price
                </TableHead>
                <TableHead className="h-auto w-20 py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Change
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {MOCK_SYMBOLS.map((s, i) => (
                <TableRow key={s.ticker} className={cn("border-0 cursor-pointer", i % 2 === 1 && "bg-muted/20")}>
                  <TableCell className="py-2">
                    <div className="text-xs font-semibold leading-tight">{s.ticker}</div>
                    <div className="truncate text-[11px] leading-tight text-muted-foreground">{s.name}</div>
                  </TableCell>
                  <TableCell className="py-2 text-right font-mono text-xs">{formatPrice(s.price)}</TableCell>
                  <TableCell className="py-2 text-right">
                    <Badge variant="outline" className={cn("rounded border-0", changeColor(s.changePercent))}>
                      {formatChange(s.changePercent)}
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
