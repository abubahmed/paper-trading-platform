"use client";

import { useEffect, useRef } from "react";
import { createChart, ColorType, CandlestickData, Time, CandlestickSeries } from "lightweight-charts";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

function generateMockCandles(): CandlestickData<Time>[] {
  const candles: CandlestickData<Time>[] = [];
  let date = new Date("2025-06-01");
  let price = 185;

  for (let i = 0; i < 120; i++) {
    // Skip weekends
    if (date.getDay() === 0) date.setDate(date.getDate() + 1);
    if (date.getDay() === 6) date.setDate(date.getDate() + 2);

    const open = price + (Math.random() - 0.48) * 3;
    const close = open + (Math.random() - 0.48) * 4;
    const high = Math.max(open, close) + Math.random() * 2;
    const low = Math.min(open, close) - Math.random() * 2;

    candles.push({
      time: date.toISOString().split("T")[0] as Time,
      open: +open.toFixed(2),
      high: +high.toFixed(2),
      low: +low.toFixed(2),
      close: +close.toFixed(2),
    });

    price = close;
    date.setDate(date.getDate() + 1);
  }

  return candles;
}

const MOCK_CANDLES = generateMockCandles();

export function PriceChartPanel() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const chart = createChart(container, {
      layout: {
        background: { type: ColorType.Solid, color: "transparent" },
        textColor: "#9ca3af",
        fontSize: 11,
      },
      grid: {
        vertLines: { color: "rgba(255, 255, 255, 0.04)" },
        horzLines: { color: "rgba(255, 255, 255, 0.04)" },
      },
      crosshair: {
        vertLine: { color: "rgba(255, 255, 255, 0.15)", labelBackgroundColor: "#374151" },
        horzLine: { color: "rgba(255, 255, 255, 0.15)", labelBackgroundColor: "#374151" },
      },
      rightPriceScale: {
        borderColor: "rgba(255, 255, 255, 0.1)",
      },
      timeScale: {
        borderColor: "rgba(255, 255, 255, 0.1)",
        timeVisible: false,
      },
      handleScroll: true,
      handleScale: true,
    });

    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: "#10b981",
      downColor: "#ef4444",
      borderUpColor: "#10b981",
      borderDownColor: "#ef4444",
      wickUpColor: "#10b981",
      wickDownColor: "#ef4444",
    });

    candleSeries.setData(MOCK_CANDLES);
    chart.timeScale().fitContent();

    const resizeObserver = new ResizeObserver(() => {
      chart.applyOptions({
        width: container.clientWidth,
        height: container.clientHeight,
      });
    });
    resizeObserver.observe(container);

    return () => {
      resizeObserver.disconnect();
      chart.remove();
    };
  }, []);

  return (
    <Card className="h-full gap-0 rounded-none border-0 bg-transparent shadow-none ring-0">
      <CardHeader className="py-2.5">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          AAPL — Apple Inc.
        </CardTitle>
      </CardHeader>
      <Separator />
      <CardContent className="flex-1 overflow-hidden p-0">
        <div ref={containerRef} className="h-full w-full" />
      </CardContent>
    </Card>
  );
}
