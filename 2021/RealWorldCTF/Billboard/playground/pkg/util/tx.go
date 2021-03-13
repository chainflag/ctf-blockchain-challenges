package util

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
)

type Result struct {
	Height    string       `json:"height"`
	TxHash    string       `json:"txhash"`
	CodeSpace string       `json:"codespace"`
	Code      int64        `json:"code"`
	RawLog    string       `json:"raw_log"`
	GasWanted string       `json:"gas_wanted"`
	GasUsed   string       `json:"gas_used"`
	Tx        *Transaction `json:"tx"`
	Timestamp string       `json:"timestamp"`
	Error     string       `json:"error"`
}

type Transaction struct {
	Type  string `json:"type"`
	Value struct {
		Msg []struct {
			Type  string `json:"type"`
			Value struct {
				Winner string `json:"winner"`
				ID     string `json:"id"`
			} `json:"value"`
		} `json:"msg"`
	} `json:"value"`
}

func QueryTx(lcd, txHash string) (*Result, error) {
	resp, err := http.Get(fmt.Sprintf("%s/txs/%s", lcd, txHash))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	if resp.StatusCode != http.StatusOK {
		errResp := &Result{}
		if err := json.Unmarshal(body, errResp); err != nil {
			return nil, err
		}
		return nil, errors.New(errResp.Error)
	}

	txResp := &Result{}
	if err = json.Unmarshal(body, txResp); err != nil {
		return nil, err
	}

	return txResp, nil
}
