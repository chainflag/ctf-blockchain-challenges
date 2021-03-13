package server

import (
	"strconv"

	"github.com/gin-gonic/gin"
)

func setupRouter() *gin.Engine {
	r := gin.Default()

	v1 := r.Group("/api/v1")
	v1.GET("/flag", getFlagByTxHash)

	return r
}

func run() {
	if isDebug == false {
		gin.SetMode(gin.ReleaseMode)
	}

	r := setupRouter()
	r.Run(":" + strconv.Itoa(port))
}
