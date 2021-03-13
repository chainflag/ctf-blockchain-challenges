package util

import (
	"crypto/sha256"

	"github.com/bartekn/go-bip39"
	"github.com/cosmos/cosmos-sdk/crypto/keys"
	tmcrypto "github.com/tendermint/tendermint/crypto"
)

func GenerateMnemonic(inputEntropy string) (string, error) {
	hashedEntropy := sha256.Sum256([]byte(inputEntropy))
	entropySeed := hashedEntropy[:]

	return bip39.NewMnemonic(entropySeed)
}

func GetPrivKeyFromMnemonic(mnemonic string, bip39Passphrase, hdPath string) (tmcrypto.PrivKey, error) {
	derivedPriv, err := keys.SecpDeriveKey(mnemonic, bip39Passphrase, hdPath)
	if err != nil {
		return nil, err
	}

	privKey := keys.SecpPrivKeyGen(derivedPriv)
	return privKey, nil
}
