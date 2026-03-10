"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";


export function SubmitOrderPanel({ showHeader = true }: { showHeader?: boolean }) {
  const [side, setSide] = useState<"BUY" | "SELL">("BUY");
  const [orderType, setOrderType] = useState("MARKET");
  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState("");
  const [limitPrice, setLimitPrice] = useState("");

  return (
    <Card className="h-full gap-0 rounded-none border-0 bg-transparent shadow-none ring-0">
      {showHeader && (
        <>
          <CardHeader className="py-2.5">
            <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Submit Order
            </CardTitle>
          </CardHeader>
          <Separator />
        </>
      )}
      <CardContent className="flex-1 overflow-y-auto px-2.5 py-2">
        <div className="flex flex-col gap-2">
          {/* Buy / Sell toggle */}
          <div className="grid grid-cols-2 gap-px overflow-hidden rounded-md border border-border/50">
            <button
              type="button"
              onClick={() => setSide("BUY")}
              className={cn(
                "py-1.5 text-[11px] font-semibold uppercase tracking-wider transition-colors",
                side === "BUY"
                  ? "bg-emerald-500/20 text-emerald-400"
                  : "bg-muted/30 text-muted-foreground hover:text-foreground",
              )}
            >
              Buy
            </button>
            <button
              type="button"
              onClick={() => setSide("SELL")}
              className={cn(
                "py-1.5 text-[11px] font-semibold uppercase tracking-wider transition-colors",
                side === "SELL"
                  ? "bg-red-500/20 text-red-400"
                  : "bg-muted/30 text-muted-foreground hover:text-foreground",
              )}
            >
              Sell
            </button>
          </div>

          {/* Symbol + Order type side by side */}
          <div className="grid grid-cols-2 gap-2">
            <div className="space-y-0.5">
              <Label className="text-[10px] uppercase tracking-wider text-muted-foreground">Symbol</Label>
              <Input
                className="h-6 text-xs uppercase"
                placeholder="AAPL"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              />
            </div>
            <div className="space-y-0.5">
              <Label className="text-[10px] uppercase tracking-wider text-muted-foreground">Type</Label>
              <Select value={orderType} onValueChange={setOrderType}>
                <SelectTrigger size="sm" className="w-full">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="MARKET">Market</SelectItem>
                  <SelectItem value="LIMIT">Limit</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Quantity + Limit price side by side */}
          <div className={cn("grid gap-2", orderType === "LIMIT" ? "grid-cols-2" : "grid-cols-1")}>
            <div className="space-y-0.5">
              <Label className="text-[10px] uppercase tracking-wider text-muted-foreground">Qty</Label>
              <Input
                className="h-6 text-xs"
                type="number"
                placeholder="0"
                min={1}
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
              />
            </div>
            {orderType === "LIMIT" && (
              <div className="space-y-0.5">
                <Label className="text-[10px] uppercase tracking-wider text-muted-foreground">Limit $</Label>
                <Input
                  className="h-6 text-xs"
                  type="number"
                  placeholder="0.00"
                  min={0}
                  step={0.01}
                  value={limitPrice}
                  onChange={(e) => setLimitPrice(e.target.value)}
                />
              </div>
            )}
          </div>

          {/* Submit */}
          <Button
            size="sm"
            className={cn(
              "mt-0.5 w-full text-[11px] font-semibold uppercase tracking-wider",
              side === "BUY"
                ? "bg-emerald-600 text-white hover:bg-emerald-500"
                : "bg-red-600 text-white hover:bg-red-500",
            )}
          >
            {side === "BUY" ? "Buy" : "Sell"} {symbol || "—"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
