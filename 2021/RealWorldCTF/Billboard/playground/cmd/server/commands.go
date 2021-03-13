package server

import (
	"github.com/spf13/cobra"
)

var port int
var isDebug bool

// Cmd run http server
var Cmd = &cobra.Command{
	Use:   "server",
	Short: "Run server",
	Run: func(cmd *cobra.Command, args []string) {
		run()
	},
}

func init() {
	Cmd.Flags().IntVar(&port, "port", 8080, "listen port")
	Cmd.Flags().BoolVar(&isDebug, "debug", false, "debug mode")
}
