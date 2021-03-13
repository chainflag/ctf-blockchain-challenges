package service

import (
	"strings"

	"github.com/cosmos/cosmos-sdk/crypto/keys"
	"github.com/cosmos/cosmos-sdk/types"

	"github.com/iczc/billboard/playground/pkg/util"
)

type Account struct {
	Token string
}

func NewAccount(token string) *Account {
	return &Account{
		Token: token + strings.Repeat("0", 32),
	}
}

func (a *Account) GetAddress() (string, error) {
	mnemonic, err := util.GenerateMnemonic(a.Token)
	if err != nil {
		return "", err
	}

	var account uint32
	var index uint32
	hdPath := keys.CreateHDPath(account, index).String()

	var bip39Passphrase string
	privKey, err := util.GetPrivKeyFromMnemonic(mnemonic, bip39Passphrase, hdPath)
	if err != nil {
		return "", err
	}

	var address types.AccAddress = privKey.PubKey().Address().Bytes()

	return address.String(), nil
}
