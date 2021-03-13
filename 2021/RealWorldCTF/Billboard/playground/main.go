package main

import (
	"fmt"
	"os"

	_ "github.com/joho/godotenv/autoload"
	"github.com/spf13/cobra"

	"github.com/iczc/billboard/playground/cmd/server"
)

func main() {
	rootCmd := cobra.Command{
		Use: "billboard-playground",
	}

	rootCmd.AddCommand(
		server.Cmd,
	)

	if err := rootCmd.Execute(); err != nil {
		fmt.Printf("Failed executing CLI command: %s, exiting...\n", err)
		os.Exit(1)
	}
}
