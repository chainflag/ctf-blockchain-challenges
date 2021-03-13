package types

import (
	sdkerrors "github.com/cosmos/cosmos-sdk/types/errors"
)

var (
	ErrInvalidBalance = sdkerrors.Register(ModuleName, 22, "invalid balance")
)
