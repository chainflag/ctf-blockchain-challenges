package cli

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/cosmos/cosmos-sdk/client"
	"github.com/cosmos/cosmos-sdk/client/context"
	"github.com/cosmos/cosmos-sdk/client/flags"
	"github.com/cosmos/cosmos-sdk/codec"

	"github.com/iczc/billboard/x/billboard/types"
)

// GetQueryCmd returns the cli query commands for this module
func GetQueryCmd(queryRoute string, cdc *codec.Codec) *cobra.Command {
	// Group billboard queries under a subcommand
	billboardQueryCmd := &cobra.Command{
		Use:                        types.ModuleName,
		Short:                      fmt.Sprintf("Querying commands for the %s module", types.ModuleName),
		DisableFlagParsing:         true,
		SuggestionsMinimumDistance: 2,
		RunE:                       client.ValidateCmd,
	}

	billboardQueryCmd.AddCommand(
		flags.GetCommands(
			GetCmdListAdvertisement(queryRoute, cdc),
			GetCmdGetAdvertisement(queryRoute, cdc),
		)...,
	)

	return billboardQueryCmd
}

func GetCmdListAdvertisement(queryRoute string, cdc *codec.Codec) *cobra.Command {
	return &cobra.Command{
		Use:   "list-advertisement",
		Short: "list all advertisement",
		RunE: func(cmd *cobra.Command, args []string) error {
			cliCtx := context.NewCLIContext().WithCodec(cdc)
			res, _, err := cliCtx.QueryWithData(fmt.Sprintf("custom/%s/"+types.QueryListAdvertisement, queryRoute), nil)
			if err != nil {
				fmt.Printf("could not list Advertisement\n%s\n", err.Error())
				return nil
			}
			var out []types.Advertisement
			cdc.MustUnmarshalJSON(res, &out)
			return cliCtx.PrintOutput(out)
		},
	}
}

func GetCmdGetAdvertisement(queryRoute string, cdc *codec.Codec) *cobra.Command {
	return &cobra.Command{
		Use:   "get-advertisement [key]",
		Short: "Query a advertisement by key",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			cliCtx := context.NewCLIContext().WithCodec(cdc)
			key := args[0]

			res, _, err := cliCtx.QueryWithData(fmt.Sprintf("custom/%s/%s/%s", queryRoute, types.QueryGetAdvertisement, key), nil)
			if err != nil {
				fmt.Printf("could not resolve advertisement %s \n%s\n", key, err.Error())

				return nil
			}

			var out types.Advertisement
			cdc.MustUnmarshalJSON(res, &out)
			return cliCtx.PrintOutput(out)
		},
	}
}
