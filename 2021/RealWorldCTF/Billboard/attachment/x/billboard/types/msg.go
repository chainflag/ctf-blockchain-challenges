package types

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"

	sdk "github.com/cosmos/cosmos-sdk/types"
	sdkerrors "github.com/cosmos/cosmos-sdk/types/errors"
)

const (
	MaxContentLength = 64
)

var _ sdk.Msg = &MsgCreateAdvertisement{}

type MsgCreateAdvertisement struct {
	ID      string         `json:"id" yaml:"id"`
	Content string         `json:"content" yaml:"content"`
	Creator sdk.AccAddress `json:"creator" yaml:"creator"`
}

func NewMsgCreateAdvertisement(id string, content string, creator sdk.AccAddress) MsgCreateAdvertisement {
	return MsgCreateAdvertisement{
		ID:      id,
		Content: content,
		Creator: creator,
	}
}

func (msg MsgCreateAdvertisement) Route() string {
	return RouterKey
}

func (msg MsgCreateAdvertisement) Type() string {
	return "CreateAdvertisement"
}

func (msg MsgCreateAdvertisement) GetSigners() []sdk.AccAddress {
	return []sdk.AccAddress{msg.Creator}
}

func (msg MsgCreateAdvertisement) GetSignBytes() []byte {
	bz := ModuleCdc.MustMarshalJSON(msg)
	return sdk.MustSortJSON(bz)
}

func (msg MsgCreateAdvertisement) ValidateBasic() error {
	if msg.Creator.Empty() {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidAddress, "creator can't be empty")
	}

	if msg.ID == "" {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, "ID can't be empty")
	}
	expectedID := sha256.Sum256([]byte(msg.Creator.String()))
	if msg.ID != hex.EncodeToString(expectedID[:]) {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, fmt.Sprintf("invalid ID, expected: %x", expectedID))
	}

	if msg.Content == "" || len(msg.Content) > MaxContentLength {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, "invalid content")
	}

	return nil
}

var _ sdk.Msg = &MsgDeleteAdvertisement{}

type MsgDeleteAdvertisement struct {
	ID      string         `json:"id" yaml:"id"`
	Creator sdk.AccAddress `json:"creator" yaml:"creator"`
}

func NewMsgDeleteAdvertisement(id string, creator sdk.AccAddress) MsgDeleteAdvertisement {
	return MsgDeleteAdvertisement{
		ID:      id,
		Creator: creator,
	}
}

func (msg MsgDeleteAdvertisement) Route() string {
	return RouterKey
}

func (msg MsgDeleteAdvertisement) Type() string {
	return "DeleteAdvertisement"
}

func (msg MsgDeleteAdvertisement) GetSigners() []sdk.AccAddress {
	return []sdk.AccAddress{msg.Creator}
}

func (msg MsgDeleteAdvertisement) GetSignBytes() []byte {
	bz := ModuleCdc.MustMarshalJSON(msg)
	return sdk.MustSortJSON(bz)
}

func (msg MsgDeleteAdvertisement) ValidateBasic() error {
	if msg.Creator.Empty() {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidAddress, "creator can't be empty")
	}
	if msg.ID == "" {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, "ID can't be empty")
	}

	return nil
}

var _ sdk.Msg = &MsgDeposit{}

type MsgDeposit struct {
	ID        string         `json:"id" yaml:"id"`
	Amount    sdk.Coin       `json:"amount" yaml:"amount"`
	Depositor sdk.AccAddress `json:"depositor" yaml:"depositor"`
}

func NewMsgDeposit(id string, amount sdk.Coin, depositor sdk.AccAddress) MsgDeposit {
	return MsgDeposit{
		ID:        id,
		Amount:    amount,
		Depositor: depositor,
	}
}

func (msg MsgDeposit) Route() string {
	return RouterKey
}

func (msg MsgDeposit) Type() string {
	return "deposit"
}

func (msg MsgDeposit) GetSigners() []sdk.AccAddress {
	return []sdk.AccAddress{msg.Depositor}
}

func (msg MsgDeposit) GetSignBytes() []byte {
	bz := ModuleCdc.MustMarshalJSON(msg)
	return sdk.MustSortJSON(bz)
}

func (msg MsgDeposit) ValidateBasic() error {
	if msg.Depositor.Empty() {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidAddress, "depositor can't be empty")
	}
	if msg.ID == "" {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, "ID can't be empty")
	}
	if msg.Amount.IsZero() || !msg.Amount.IsValid() {
		return sdkerrors.ErrInvalidCoins
	}

	return nil
}

var _ sdk.Msg = &MsgWithdraw{}

type MsgWithdraw struct {
	ID        string         `json:"id" yaml:"id"`
	Amount    sdk.Coin       `json:"amount" yaml:"amount"`
	Depositor sdk.AccAddress `json:"depositor" yaml:"depositor"`
}

func NewMsgWithdraw(id string, amount sdk.Coin, depositor sdk.AccAddress) MsgWithdraw {
	return MsgWithdraw{
		ID:        id,
		Amount:    amount,
		Depositor: depositor,
	}
}

func (msg MsgWithdraw) Route() string {
	return RouterKey
}

func (msg MsgWithdraw) Type() string {
	return "withdraw"
}

func (msg MsgWithdraw) GetSigners() []sdk.AccAddress {
	return []sdk.AccAddress{msg.Depositor}
}

func (msg MsgWithdraw) GetSignBytes() []byte {
	bz := ModuleCdc.MustMarshalJSON(msg)
	return sdk.MustSortJSON(bz)
}

func (msg MsgWithdraw) ValidateBasic() error {
	if msg.Depositor.Empty() {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidAddress, "depositor can't be empty")
	}
	if msg.ID == "" {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, "ID can't be empty")
	}
	if msg.Amount.IsZero() || !msg.Amount.IsValid() {
		return sdkerrors.ErrInvalidCoins
	}

	return nil
}

var _ sdk.Msg = &MsgCaptureTheFlag{}

type MsgCaptureTheFlag struct {
	ID     string         `json:"id" yaml:"id"`
	Winner sdk.AccAddress `json:"winner" yaml:"winner"`
}

func NewMsgCaptureTheFlag(id string, winner sdk.AccAddress) MsgCaptureTheFlag {
	return MsgCaptureTheFlag{
		ID:     id,
		Winner: winner,
	}
}

func (msg MsgCaptureTheFlag) Route() string {
	return RouterKey
}

func (msg MsgCaptureTheFlag) Type() string {
	return "CaptureTheFlag"
}

func (msg MsgCaptureTheFlag) GetSigners() []sdk.AccAddress {
	return []sdk.AccAddress{msg.Winner}
}

func (msg MsgCaptureTheFlag) GetSignBytes() []byte {
	bz := ModuleCdc.MustMarshalJSON(msg)
	return sdk.MustSortJSON(bz)
}

func (msg MsgCaptureTheFlag) ValidateBasic() error {
	if msg.Winner.Empty() {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidAddress, "creator can't be empty")
	}
	if msg.ID == "" {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidRequest, "ID can't be empty")
	}

	return nil
}
