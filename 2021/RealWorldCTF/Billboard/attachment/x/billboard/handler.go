package billboard

import (
	"fmt"

	sdk "github.com/cosmos/cosmos-sdk/types"
	sdkerrors "github.com/cosmos/cosmos-sdk/types/errors"

	"github.com/iczc/billboard/x/billboard/keeper"
	"github.com/iczc/billboard/x/billboard/types"
	"github.com/iczc/billboard/x/supply"
)

// NewHandler ...
func NewHandler(k keeper.Keeper) sdk.Handler {
	return func(ctx sdk.Context, msg sdk.Msg) (*sdk.Result, error) {
		ctx = ctx.WithEventManager(sdk.NewEventManager())
		switch msg := msg.(type) {
		case types.MsgCreateAdvertisement:
			return handleMsgCreateAdvertisement(ctx, k, msg)
		case types.MsgDeleteAdvertisement:
			return handleMsgDeleteAdvertisement(ctx, k, msg)
		case types.MsgDeposit:
			return handleMsgDeposit(ctx, k, msg)
		case types.MsgWithdraw:
			return handleMsgWithdraw(ctx, k, msg)
		case types.MsgCaptureTheFlag:
			return handleMsgCaptureTheFlag(ctx, k, msg)
		default:
			errMsg := fmt.Sprintf("unrecognized %s message type: %T", types.ModuleName, msg)
			return nil, sdkerrors.Wrap(sdkerrors.ErrUnknownRequest, errMsg)
		}
	}
}

func handleMsgCreateAdvertisement(ctx sdk.Context, k keeper.Keeper, msg types.MsgCreateAdvertisement) (*sdk.Result, error) {
	if k.AdvertisementExists(ctx, msg.ID) {
		return nil, sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, msg.ID)
	}

	maccPerms := map[string][]string{
		msg.ID: {supply.Minter, supply.Burner},
	}
	k.GetSupplyKeeper().SetModuleAddressAndPermissions(maccPerms)

	if err := k.GetSupplyKeeper().MintCoins(ctx, msg.ID, types.ModuleInitialBalance); err != nil {
		return nil, err
	}

	var advertisement = &types.Advertisement{
		Creator: msg.Creator,
		ID:      msg.ID,
		Content: msg.Content,
		Deposit: types.DefaultAdvertisementDeposit,
	}
	k.SetAdvertisement(ctx, advertisement)

	return &sdk.Result{Events: ctx.EventManager().Events()}, nil
}

func handleMsgDeleteAdvertisement(ctx sdk.Context, k keeper.Keeper, msg types.MsgDeleteAdvertisement) (*sdk.Result, error) {
	if !k.AdvertisementExists(ctx, msg.ID) {
		return nil, sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, msg.ID)
	}

	advertisement, err := k.GetAdvertisement(ctx, msg.ID)
	if err != nil {
		return nil, err
	}

	if !msg.Creator.Equals(advertisement.Creator) {
		return nil, sdkerrors.Wrap(sdkerrors.ErrUnauthorized, "Incorrect Owner")
	}

	if !advertisement.Deposit.IsZero() {
		return nil, sdkerrors.Wrap(types.ErrInvalidBalance, "Deposit must be zero")
	}

	k.DeleteAdvertisement(ctx, msg.ID)
	macc := k.GetSupplyKeeper().GetModuleAccount(ctx, msg.ID)
	if macc == nil {
		return nil, sdkerrors.ErrUnknownAddress
	}
	if err := k.GetSupplyKeeper().BurnCoins(ctx, msg.ID, macc.GetCoins()); err != nil {
		return nil, err
	}

	return &sdk.Result{}, nil
}

func handleMsgDeposit(ctx sdk.Context, k keeper.Keeper, msg types.MsgDeposit) (*sdk.Result, error) {
	if !k.AdvertisementExists(ctx, msg.ID) {
		return nil, sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, msg.ID)
	}

	if err := k.Deposit(ctx, msg.ID, msg.Depositor, msg.Amount); err != nil {
		return nil, err
	}

	return &sdk.Result{}, nil
}

func handleMsgWithdraw(ctx sdk.Context, k keeper.Keeper, msg types.MsgWithdraw) (*sdk.Result, error) {
	if !k.AdvertisementExists(ctx, msg.ID) {
		return nil, sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, msg.ID)
	}

	if err := k.Withdraw(ctx, msg.ID, msg.Depositor, msg.Amount); err != nil {
		return nil, err
	}

	return &sdk.Result{}, nil
}

func handleMsgCaptureTheFlag(ctx sdk.Context, k keeper.Keeper, msg types.MsgCaptureTheFlag) (*sdk.Result, error) {
	if !k.AdvertisementExists(ctx, msg.ID) {
		return nil, sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, msg.ID)
	}

	advertisement, err := k.GetAdvertisement(ctx, msg.ID)
	if err != nil {
		return nil, err
	}

	if !msg.Winner.Equals(advertisement.Creator) {
		return nil, sdkerrors.Wrap(sdkerrors.ErrUnauthorized, "Incorrect Owner")
	}

	macc := k.GetSupplyKeeper().GetModuleAccount(ctx, msg.ID)
	if macc == nil {
		return nil, sdkerrors.ErrUnknownAddress
	}

	if !macc.GetCoins().AmountOf(types.DefaultDepositDenom).Equal(sdk.ZeroInt()) {
		return nil, sdkerrors.Wrap(types.ErrInvalidBalance, fmt.Sprintf("module account balance: %s", macc.GetCoins().AmountOf(types.DefaultDepositDenom)))
	}

	return &sdk.Result{}, nil
}
