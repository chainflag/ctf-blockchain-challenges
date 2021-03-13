package types

// GenesisState - all billboard state that must be provided at genesis
type GenesisState struct {
	Advertisements []*Advertisement `json:"advertisement" yaml:"advertisement"`
}

// NewGenesisState creates a new GenesisState object
func NewGenesisState(advertisements []*Advertisement) GenesisState {
	return GenesisState{
		Advertisements: advertisements,
	}
}

// DefaultGenesisState - default GenesisState used by Cosmos Hub
func DefaultGenesisState() GenesisState {
	return GenesisState{
		Advertisements: nil,
	}
}
