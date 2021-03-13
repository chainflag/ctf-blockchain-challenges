package keeper

import (
	"fmt"
	"sort"

	"github.com/tendermint/tendermint/libs/log"

	"github.com/cosmos/cosmos-sdk/codec"
	sdk "github.com/cosmos/cosmos-sdk/types"
	sdkerrors "github.com/cosmos/cosmos-sdk/types/errors"
	"github.com/iczc/billboard/x/billboard/types"
)

// Keeper of the billboard store
type Keeper struct {
	supplyKeeper types.SupplyKeeper
	storeKey     sdk.StoreKey
	cdc          *codec.Codec
	cache        *Cache
	// paramspace types.ParamSubspace
}

// NewKeeper creates a billboard keeper
func NewKeeper(supplyKeeper types.SupplyKeeper, cdc *codec.Codec, key sdk.StoreKey) Keeper {
	keeper := Keeper{
		supplyKeeper: supplyKeeper,
		storeKey:     key,
		cdc:          cdc,
		cache:        NewCache(),
		// paramspace: paramspace.WithKeyTable(types.ParamKeyTable()),
	}
	return keeper
}

// Logger returns a module-specific logger.
func (k Keeper) Logger(ctx sdk.Context) log.Logger {
	return ctx.Logger().With("module", fmt.Sprintf("x/%s", types.ModuleName))
}

// GetSupplyKeeper returns supply Keeper
func (k Keeper) GetSupplyKeeper() types.SupplyKeeper {
	return k.supplyKeeper
}

// GetAdvertisement returns the advertisement information
func (k Keeper) GetAdvertisement(ctx sdk.Context, key string) (*types.Advertisement, error) {
	var advertisement *types.Advertisement

	advertisement, ok := k.cache.GetAdvertisement(key)
	if ok {
		return advertisement, nil
	}

	store := ctx.KVStore(k.storeKey)
	byteKey := []byte(types.AdvertisementPrefix + key)
	err := k.cdc.UnmarshalBinaryLengthPrefixed(store.Get(byteKey), &advertisement)
	if err != nil {
		return advertisement, err
	}

	k.cache.SetAdvertisement(advertisement)
	return advertisement, nil
}

// GetAdvertisements returns all advertisements
func (k Keeper) GetAdvertisements(ctx sdk.Context) []*types.Advertisement {
	cacheAdvertisements := k.cache.GetAllAdvertisements()
	if len(cacheAdvertisements) > 0 {
		return cacheAdvertisements
	}

	advertisements := k.GetAdvertisementsFromStore(ctx)
	k.cache.PrepareAdvertisements(advertisements)

	return advertisements
}

// GetAdvertisements returns all advertisements from store without cache
func (k Keeper) GetAdvertisementsFromStore(ctx sdk.Context) []*types.Advertisement {
	var advertisements []*types.Advertisement
	store := ctx.KVStore(k.storeKey)
	iterator := sdk.KVStorePrefixIterator(store, []byte(types.AdvertisementPrefix))
	for ; iterator.Valid(); iterator.Next() {
		var advertisement *types.Advertisement
		k.cdc.MustUnmarshalBinaryLengthPrefixed(store.Get(iterator.Key()), &advertisement)
		advertisements = append(advertisements, advertisement)
	}

	return advertisements
}

// SetAdvertisement sets a advertisement
func (k Keeper) SetAdvertisement(ctx sdk.Context, advertisement *types.Advertisement) {
	store := ctx.KVStore(k.storeKey)
	key := []byte(types.AdvertisementPrefix + advertisement.ID)
	value := k.cdc.MustMarshalBinaryLengthPrefixed(advertisement)
	store.Set(key, value)
	k.cache.SetAdvertisement(advertisement)
}

// DeleteAdvertisement deletes a advertisement
func (k Keeper) DeleteAdvertisement(ctx sdk.Context, key string) {
	store := ctx.KVStore(k.storeKey)
	store.Delete([]byte(types.AdvertisementPrefix + key))
	k.cache.DelAdvertisement(key)
}

func (k Keeper) Deposit(ctx sdk.Context, key string, from sdk.AccAddress, amount sdk.Coin) error {
	advertisement, err := k.GetAdvertisement(ctx, key)
	if err != nil {
		return err
	}

	if !advertisement.Creator.Equals(from) {
		return sdkerrors.Wrap(sdkerrors.ErrUnauthorized, "Incorrect Owner")
	}

	if amount.Denom != types.DefaultDepositDenom {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidCoins, fmt.Sprintf("failed to deposit because deposits only support %s token", types.DefaultDepositDenom))
	}

	depositCoins := sdk.NewCoins(amount)

	if err := k.GetSupplyKeeper().SendCoinsFromAccountToModule(ctx, from, key, depositCoins); err != nil {
		return sdkerrors.Wrap(sdkerrors.ErrInsufficientFunds, fmt.Sprintf("failed to deposit because insufficient deposit coins(need %s)", depositCoins.String()))
	}

	advertisement.Deposit = advertisement.Deposit.Add(amount)

	k.SetAdvertisement(ctx, advertisement)
	return nil
}

func (k Keeper) Withdraw(ctx sdk.Context, key string, to sdk.AccAddress, amount sdk.Coin) error {
	advertisement, err := k.GetAdvertisement(ctx, key)
	if err != nil {
		return err
	}

	if !advertisement.Creator.Equals(to) {
		return sdkerrors.Wrap(sdkerrors.ErrUnauthorized, "Incorrect Owner")
	}

	if amount.Denom != types.DefaultDepositDenom {
		return sdkerrors.Wrap(sdkerrors.ErrInvalidCoins, fmt.Sprintf("failed to withdraw because deposits only support %s token", types.DefaultDepositDenom))
	}

	if advertisement.Deposit.IsLT(amount) {
		return sdkerrors.Wrap(sdkerrors.ErrInsufficientFunds, fmt.Sprintf("failed to withdraw because deposits:%s is less than withdraw:%s", advertisement.Deposit.String(), amount.String()))
	}

	withdrawCoins := sdk.NewCoins(amount)
	if err := k.GetSupplyKeeper().SendCoinsFromModuleToAccount(ctx, key, to, withdrawCoins); err != nil {
		return err
	}

	advertisement.Deposit = advertisement.Deposit.Sub(amount)
	k.SetAdvertisement(ctx, advertisement)
	return nil
}

//
// Functions used by querier
//

func listAdvertisement(ctx sdk.Context, k Keeper) ([]byte, error) {
	advertisements := k.GetAdvertisements(ctx)
	var advertisementList types.Advertisements
	advertisementList = append(advertisementList, advertisements...)
	sort.Sort(advertisementList)

	res := codec.MustMarshalJSONIndent(k.cdc, advertisementList)
	return res, nil
}

func getAdvertisement(ctx sdk.Context, path []string, k Keeper) (res []byte, sdkError error) {
	key := path[0]
	advertisement, err := k.GetAdvertisement(ctx, key)
	if err != nil {
		return nil, err
	}

	res, err = codec.MarshalJSONIndent(k.cdc, advertisement)
	if err != nil {
		return nil, sdkerrors.Wrap(sdkerrors.ErrJSONMarshal, err.Error())
	}

	return res, nil
}

// Check if the key exists in the store
func (k Keeper) AdvertisementExists(ctx sdk.Context, key string) bool {
	store := ctx.KVStore(k.storeKey)
	return store.Has([]byte(types.AdvertisementPrefix + key))
}
