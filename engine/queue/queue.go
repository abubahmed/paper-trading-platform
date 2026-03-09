package queue

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/redis/go-redis/v9"
)

const orderQueue = "order_queue"

var client *redis.Client

func Connect() error {
	url := os.Getenv("REDIS_URL")
	if url == "" {
		return fmt.Errorf("REDIS_URL is not set")
	}

	opts, err := redis.ParseURL(url)
	if err != nil {
		return fmt.Errorf("invalid REDIS_URL: %w", err)
	}

	client = redis.NewClient(opts)

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := client.Ping(ctx).Err(); err != nil {
		return fmt.Errorf("failed to ping redis: %w", err)
	}

	return nil
}

func Close() {
	if client != nil {
		client.Close()
	}
}

// Consume blocks waiting for the next message on the queue.
// It returns the raw message string, which is either an order UUID or "PRICE_UPDATE".
func Consume(ctx context.Context) (string, error) {
	result, err := client.BRPop(ctx, 0, orderQueue).Result()
	if err != nil {
		return "", err
	}
	// BRPop returns [key, value]
	return result[1], nil
}
