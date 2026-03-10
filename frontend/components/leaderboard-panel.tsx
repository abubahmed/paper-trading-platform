"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { cn } from "@/lib/utils";

interface LeaderboardEntry {
  rank: number;
  username: string;
  totalValue: number;
  cash: number;
  positionsValue: number;
}

const MOCK_LEADERBOARD: LeaderboardEntry[] = [
  { rank: 1, username: "Sarah Chen", totalValue: 112840.5, cash: 45200.0, positionsValue: 67640.5 },
  { rank: 2, username: "James Rodriguez", totalValue: 109320.75, cash: 32100.0, positionsValue: 77220.75 },
  { rank: 3, username: "Emily Park", totalValue: 106450.0, cash: 58900.0, positionsValue: 47550.0 },
  { rank: 4, username: "Michael Thompson", totalValue: 103880.2, cash: 41500.0, positionsValue: 62380.2 },
  { rank: 5, username: "Priya Sharma", totalValue: 101200.0, cash: 72000.0, positionsValue: 29200.0 },
  { rank: 6, username: "David Kim", totalValue: 99750.3, cash: 25300.0, positionsValue: 74450.3 },
  { rank: 7, username: "Nancy Liu", totalValue: 98100.0, cash: 88100.0, positionsValue: 10000.0 },
  { rank: 8, username: "Andrew Walsh", totalValue: 96540.6, cash: 15800.0, positionsValue: 80740.6 },
  { rank: 9, username: "Robert Singh", totalValue: 94200.0, cash: 94200.0, positionsValue: 0 },
  { rank: 10, username: "Olivia Martinez", totalValue: 87650.4, cash: 12400.0, positionsValue: 75250.4 },
];

function formatCurrency(value: number) {
  return value.toLocaleString("en-US", { style: "currency", currency: "USD" });
}

function rankBadge(rank: number) {
  if (rank === 1) return "bg-yellow-500/15 text-yellow-400";
  if (rank === 2) return "bg-zinc-400/15 text-zinc-300";
  if (rank === 3) return "bg-amber-600/15 text-amber-500";
  return "bg-muted text-muted-foreground";
}

export function LeaderboardPanel() {
  return (
    <Card className="h-full gap-0 rounded-none border-0 bg-transparent shadow-none ring-0">
      <CardHeader className="py-2.5">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Leaderboard
        </CardTitle>
      </CardHeader>
      <Separator />
      <CardContent className="flex-1 overflow-hidden p-0">
        <ScrollArea className="h-full">
          <Table>
            <TableHeader className="sticky top-0 z-10 bg-muted/30">
              <TableRow className="border-0 hover:bg-transparent">
                <TableHead className="h-auto w-10 py-1.5 text-center text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  #
                </TableHead>
                <TableHead className="h-auto py-1.5 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  User
                </TableHead>
                <TableHead className="h-auto py-1.5 text-right text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Total Value
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {MOCK_LEADERBOARD.map((entry, i) => (
                <TableRow key={entry.username} className={cn("border-0", i % 2 === 1 && "bg-muted/20")}>
                  <TableCell className="py-2 text-center">
                    <Badge variant="outline" className={cn("rounded border-0 tabular-nums", rankBadge(entry.rank))}>
                      {entry.rank}
                    </Badge>
                  </TableCell>
                  <TableCell className="py-2">
                    <div className="text-xs font-semibold leading-tight">{entry.username}</div>
                  </TableCell>
                  <TableCell className="py-2 text-right font-mono text-xs">
                    {formatCurrency(entry.totalValue)}
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
