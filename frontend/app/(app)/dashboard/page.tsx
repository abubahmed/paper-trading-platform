"use client";

import { LeaderboardPanel } from "@/components/leaderboard-panel";
import { OpenOrdersPanel } from "@/components/open-orders-panel";
import { PositionsPanel } from "@/components/positions-panel";
import { SubmitOrderPanel } from "@/components/submit-order-panel";
import { SymbolWatchlist } from "@/components/symbol-watchlist";
import { TradeHistoryPanel } from "@/components/trade-history-panel";
import { HeaderBar } from "@/components/header-bar";
import { PriceChartPanel } from "@/components/price-chart-panel";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";

function PanelPlaceholder({ title }: { title: string }) {
  return (
    <Card className="h-full rounded-none border-0 bg-transparent shadow-none ring-0">
      <CardHeader>
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{title}</CardTitle>
      </CardHeader>
      <CardContent />
    </Card>
  );
}

export default function DashboardPage() {
  return (
    <div className="flex h-screen w-screen flex-col bg-background">
      {/* Header */}
      <HeaderBar />
      <Separator />

      {/* Main area */}
      <ResizablePanelGroup direction="horizontal" className="flex-1">
        {/* Left half — stacked: orders tabs + watchlist */}
        <ResizablePanel defaultSize={50} minSize={25}>
          <ResizablePanelGroup direction="vertical">
            <ResizablePanel defaultSize={50}>
              <Tabs defaultValue="open" className="h-full">
                <div className="flex gap-4 border-b border-border/50 px-3">
                  <TabsList variant="line" className="h-auto gap-4 bg-transparent p-0">
                    <TabsTrigger value="open" className="rounded-none px-0 py-2.5 text-xs font-semibold uppercase tracking-wider data-[state=active]:text-foreground data-[state=active]:shadow-none">
                      Open Orders
                    </TabsTrigger>
                    <TabsTrigger value="history" className="rounded-none px-0 py-2.5 text-xs font-semibold uppercase tracking-wider data-[state=active]:text-foreground data-[state=active]:shadow-none">
                      Trade History
                    </TabsTrigger>
                    <TabsTrigger value="submit" className="rounded-none px-0 py-2.5 text-xs font-semibold uppercase tracking-wider data-[state=active]:text-foreground data-[state=active]:shadow-none">
                      Submit Order
                    </TabsTrigger>
                  </TabsList>
                </div>
                <TabsContent value="open" className="h-[calc(100%-40px)] overflow-hidden">
                  <OpenOrdersPanel showHeader={false} />
                </TabsContent>
                <TabsContent value="history" className="h-[calc(100%-40px)] overflow-hidden">
                  <TradeHistoryPanel showHeader={false} />
                </TabsContent>
                <TabsContent value="submit" className="h-[calc(100%-40px)] overflow-hidden">
                  <SubmitOrderPanel showHeader={false} />
                </TabsContent>
              </Tabs>
            </ResizablePanel>
            <ResizableHandle />
            <ResizablePanel defaultSize={50}>
              <SymbolWatchlist />
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
        <ResizableHandle />

        {/* Right half — price chart */}
        <ResizablePanel defaultSize={50}>
          <PriceChartPanel />
        </ResizablePanel>
      </ResizablePanelGroup>
      <Separator />

      {/* Bottom row */}
      <ResizablePanelGroup direction="horizontal" className="!h-48 shrink-0">
        <ResizablePanel defaultSize={33} minSize={15}>
          <LeaderboardPanel />
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel defaultSize={67}>
          <PositionsPanel />
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
}
