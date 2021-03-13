package server

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"

	"github.com/iczc/billboard/playground/internal/service"
)

type Resp struct {
	Err  string `json:"err"`
	Msg  string `json:"msg"`
	Data string `json:"data"`
}

func resp(context *gin.Context, err, msg, data string) {
	resp := Resp{
		Err:  err,
		Msg:  msg,
		Data: data,
	}

	context.JSON(http.StatusOK, resp)
}

func getFlagByTxHash(context *gin.Context) {
	token := context.Query("token")
	txHash := context.Query("tx")
	if token == "" || txHash == "" {
		context.AbortWithStatus(http.StatusBadRequest)
		return
	}

	if len(txHash) != 64 || len(token) != 32 {
		context.AbortWithStatus(http.StatusBadRequest)
		return
	}

	account := service.NewAccount(token)
	verifier := service.NewFlagVerifier(txHash, account)
	err := verifier.ValidateTx(os.Getenv("LCD"))
	if err != nil {
		resp(context, err.Error(), "", "")
		return
	}

	resp(context, "", "", os.Getenv("FLAG"))
}
