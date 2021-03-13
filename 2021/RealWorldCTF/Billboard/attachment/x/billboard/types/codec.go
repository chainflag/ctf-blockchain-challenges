package types

import (
	"github.com/cosmos/cosmos-sdk/codec"
)

// RegisterCodec registers concrete types on codec
func RegisterCodec(cdc *codec.Codec) {
	cdc.RegisterConcrete(MsgCreateAdvertisement{}, "billboard/CreateAdvertisement", nil)
	cdc.RegisterConcrete(MsgDeleteAdvertisement{}, "billboard/DeleteAdvertisement", nil)
	cdc.RegisterConcrete(MsgDeposit{}, "billboard/deposit", nil)
	cdc.RegisterConcrete(MsgWithdraw{}, "billboard/withdraw", nil)
	cdc.RegisterConcrete(MsgCaptureTheFlag{}, "billboard/CaptureTheFlag", nil)
}

// ModuleCdc defines the module codec
var ModuleCdc *codec.Codec

func init() {
	ModuleCdc = codec.New()
	RegisterCodec(ModuleCdc)
	codec.RegisterCrypto(ModuleCdc)
	ModuleCdc.Seal()
}
