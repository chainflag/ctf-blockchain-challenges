package keeper

import (
	"github.com/iczc/billboard/x/billboard/types"
)

// Cache caches data
type Cache struct {
	advertisementMap map[string]*types.Advertisement
}

// NewCache returns instance of Cache
func NewCache() *Cache {
	return &Cache{advertisementMap: make(map[string]*types.Advertisement)}
}

// Reset clears cache
func (c *Cache) Reset() {
	c.advertisementMap = make(map[string]*types.Advertisement)
}

func (c *Cache) GetAdvertisement(key string) (*types.Advertisement, bool) {
	advertisement, ok := c.advertisementMap[key]
	return advertisement, ok
}

func (c *Cache) GetAllAdvertisements() []*types.Advertisement {
	Advertisements := make([]*types.Advertisement, 0, len(c.advertisementMap))
	for _, v := range c.advertisementMap {
		Advertisements = append(Advertisements, v)
	}
	return Advertisements
}

func (c *Cache) SetAdvertisement(advertisement *types.Advertisement) {
	c.advertisementMap[advertisement.ID] = advertisement
}

func (c *Cache) DelAdvertisement(key string) {
	delete(c.advertisementMap, key)
}

func (c *Cache) PrepareAdvertisements(advertisements []*types.Advertisement) {
	for _, v := range advertisements {
		c.SetAdvertisement(v)
	}
}
