package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"

	"princeton-trading/engine/db"
	"princeton-trading/engine/executor"
	"princeton-trading/engine/queue"
)

func main() {
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer cancel()

	if err := db.Connect(ctx); err != nil {
		log.Fatalf("db: %v", err)
	}
	defer db.Close()

	if err := queue.Connect(); err != nil {
		log.Fatalf("queue: %v", err)
	}
	defer queue.Close()

	log.Println("trading engine started")

	for {
		msg, err := queue.Consume(ctx)
		if err != nil {
			if ctx.Err() != nil {
				log.Println("shutting down")
				return
			}
			log.Printf("queue error: %v", err)
			continue
		}

		executor.Dispatch(ctx, msg)
	}
}
