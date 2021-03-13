package service

import (
	"errors"
	"strings"

	"github.com/iczc/billboard/playground/pkg/util"
)

type Verifier struct {
	TxHash  string
	Account *Account
}

func NewFlagVerifier(txHash string, account *Account) *Verifier {
	return &Verifier{
		TxHash:  strings.ToUpper(txHash),
		Account: account,
	}
}

func (v *Verifier) ValidateTx(lcd string) error {
	result, err := util.QueryTx(lcd, v.TxHash)
	if err != nil {
		return err
	}

	if result.Code != 0 {
		return errors.New("failed tx")
	}

	ctfMsg := result.Tx.Value.Msg[0]
	if ctfMsg.Type != "billboard/CaptureTheFlag" {
		return errors.New("invalid tx type")
	}

	teamAddress, err := v.Account.GetAddress()
	if err != nil {
		return err
	}

	if ctfMsg.Value.Winner != teamAddress {
		return errors.New("invalid winner")
	}

	return nil
}
