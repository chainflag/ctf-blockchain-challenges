# You can run all of these commands from your home directory
cd $HOME
rm -rf .billboardd
rm -rf .billboardcli

# Initialize the genesis.json file that will help you to bootstrap the network
billboardd init testing --chain-id=testnet

# Create a key to hold your validator account
billboardcli keys add validator
billboardcli keys add ctfer

billboardcli config indent true
billboardcli config output json
billboardcli config trust-node true

# Add that key into the genesis.app_state.accounts array in the genesis file
# NOTE: this command lets you set the number of coins. Make sure this account has some coins
# with the genesis.app_state.staking.params.bond_denom denom, the default is staking
billboardd add-genesis-account $(billboardcli keys show validator -a) 1000000000stake
billboardd add-genesis-account $(billboardcli keys show ctfer -a) 1000ctc

# Generate the transaction that creates your validator
billboardd gentx --name validator

# Add the generated bonding transaction to the genesis file
billboardd collect-gentxs

# Now its safe to start `billboardd`
billboardd start
