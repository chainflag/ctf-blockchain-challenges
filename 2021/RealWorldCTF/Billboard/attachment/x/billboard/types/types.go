package types

import (
	"strings"

	sdk "github.com/cosmos/cosmos-sdk/types"
)

const DefaultDepositDenom = "ctc"

var (
	DefaultAdvertisementDeposit = sdk.NewCoin(DefaultDepositDenom, sdk.NewInt(0))
	ModuleInitialBalance        = sdk.NewCoins(sdk.NewCoin(DefaultDepositDenom, sdk.NewInt(100)))
)

type Advertisement struct {
	Creator sdk.AccAddress `json:"creator" yaml:"creator"`
	ID      string         `json:"id" yaml:"id"`
	Content string         `json:"content" yaml:"content"`
	Deposit sdk.Coin       `json:"deposit" yaml:"deposit"`
}

type Advertisements []*Advertisement

func (a Advertisements) Len() int { return len(a) }

func (a Advertisements) Less(i, j int) bool {
	if a[i].Deposit.IsLT(a[j].Deposit) {
		return false
	} else if !a[i].Deposit.IsEqual(a[j].Deposit) {
		return true
	}

	return strings.Compare(a[i].ID, a[j].ID) < 0
}

func (a Advertisements) Swap(i, j int) { a[i], a[j] = a[j], a[i] }
