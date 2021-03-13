module github.com/iczc/billboard

go 1.14

require (
	github.com/cosmos/cosmos-sdk v0.39.1
	github.com/golang/mock v1.4.3 // indirect
	github.com/gorilla/mux v1.7.4
	github.com/onsi/ginkgo v1.8.0 // indirect
	github.com/onsi/gomega v1.5.0 // indirect
	github.com/spf13/afero v1.2.2 // indirect
	github.com/spf13/cobra v1.0.0
	github.com/spf13/viper v1.7.1
	github.com/stretchr/testify v1.6.1
	github.com/tendermint/go-amino v0.15.1
	github.com/tendermint/tendermint v0.33.8
	github.com/tendermint/tm-db v0.5.1
	golang.org/x/net v0.0.0-20200520182314-0ba52f642ac2 // indirect
	gopkg.in/yaml.v2 v2.3.0
)

replace github.com/tendermint/tendermint v0.33.8 => github.com/iczc/tendermint v0.0.0-20201218052552-42111f2a780d
