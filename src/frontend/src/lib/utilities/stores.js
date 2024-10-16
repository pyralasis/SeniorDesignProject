import { get, writable } from 'svelte/store';
import { presetClothes } from '../../presetClothingData';
import { presetOutfits } from '../../presetOutfitData';


function createWeatherStore() {
    const { subscribe, set } = writable({
        temp: 0,
        condition: '',
        isRaining: false,
    });

    let location = 'Cincinnati';
    let baseUrl = `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${location}`;
    let apikey = import.meta.env.VITE_API_KEY;
    let apiParams = {
        include: 'days'
    };

    const queryString = new URLSearchParams(apiParams).toString();

    async function updateWeather() {
        fetch(`${baseUrl}?${queryString}&key=${apikey}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                let today = data.days[0];
                console.log(today);
                let temp = Math.round(today.temp);
                let condition = today.conditions;
                let isRaining = today.preciptype?.includes('rain');
                set({ temp, condition, isRaining });
            })
            .catch((error) => console.error('Fetch error:', error));
    }

    updateWeather();

    return {
        subscribe,
        updateWeather: () => {
            updateWeather();
        },
        getTemp: () => {
            let tempValue;
            subscribe(state => tempValue = state.temp)();
            return tempValue;
        },
    }
}

export const weatherStore = createWeatherStore();

function createMousePositionStore(initValues) {
    const { subscribe, set } = writable(initValues);

    if (typeof window !== 'undefined') {
        function updatePosition(e) {
            set({ x: e.clientX, y: e.clientY });
        }

        window.addEventListener('mousemove', updatePosition);

        const cleanup = () => window.removeEventListener('mousemove', updatePosition);

        return {
            subscribe,
            cleanup,
        };
    }
    return { subscribe };
}

export const mousePosition = createMousePositionStore({ x: 0, y: 0 });




function createClothesStore() {
    const { subscribe, set, update } = writable(presetClothes);

    return {
        subscribe,

        addClothingItem: (name, filters, type, img) => {
            update((items) => {
                const id = items.length ? Math.max(...items.map(item => item.id)) + 1 : 1;
                return [...items, { id, name, img, type, filters, clean: true }];
            });
        },

        getClothingItemById: (id) => {
            let foundItem;
            update(items => {
                foundItem = items.find((item) => item.id === id);
                return items; // Ensure items remain unchanged
            });
            return foundItem;
        },

        removeClothingItemById: (id) => {
            update((items) => items.filter((item) => item.id !== id));
        },

        getClothingItemsByType: (type) => {
            let itemsOfType;
            update(items => {
                itemsOfType = items.filter((item) => item.type === type);
                return items;
            });
            return itemsOfType;
        },

        getClothingItemByFilters: (filterQuery) => {
            let itemsOfFilters;
            update(items => {
                itemsOfFilters = items.filter((item) => {
                    item.filters.cozy === filterQuery.cozy && item.filters.formal === filterQuery.formal
                        && outfit.filters.temphigh >= filterQuery.temp && outfit.filters.templow <= filterQuery.temp;
                });
                return items;
            });
            return itemsOfFilters;
        },

        isClothingItemClean: (id) => {
            let isClean = false;
            update(items => {
                const item = items.find((item) => item.id === id);
                isClean = item ? item.clean : false;
                return items;
            });
            return isClean;
        },

        cleanAllClothes: () => {
            update((items) => items.map((item) => ({ ...item, clean: true })));
        },

        cleanClothingItemById: (id) => {
            update((items) =>
                items.map((item) => (item.id === id ? { ...item, clean: true } : item))
            );
        },

        dirtyClothingItemById: (id) => {
            update((items) =>
                items.map((item) => (item.id === id ? { ...item, clean: false } : item))
            );
        },

        editClothingItemById: (id, name, filters, type, img) => {
            update((items) =>
                items.map((item) =>
                    item.id === id ? { ...item, name, filters, type, img } : item
                )
            );
        },
    };
}

export const clothesStore = createClothesStore();



function createOutfitStore() {
    const { subscribe, set, update } = writable(presetOutfits);

    return {
        subscribe,

        addOutfit: (name, topid, bottomid, filters) => {
            update((outfits) => {
                const id = outfits.length ? Math.max(...outfits.map(outfit => outfit.id)) + 1 : 1;
                return [...outfits, { id, name, topid, bottomid, filters }];
            });
        },

        getOutfitById: (id) => {
            let foundOutfit;
            update(outfits => {
                foundOutfit = outfits.find((outfit) => outfit.id === id);
                return outfits;
            });
            return foundOutfit;
        },

        getOutfitByFilters: (filterQuery) => {
            let outfitsOfFilters;
            update(outfits => {
                outfitsOfFilters = outfits.filter(outfit => outfit.filters.cozy === filterQuery.cozy && outfit.filters.formal === filterQuery.formal &&
                    outfit.filters.temphigh >= filterQuery.temp && outfit.filters.templow <= filterQuery.temp);
                return outfits;
            });
            return outfitsOfFilters;
        },

        removeOutfitById: (id) => {
            update((outfits) => outfits.filter((outfit) => outfit.id !== id));
        },

        isOutfitClean: (id) => {
            let isClean = false;
            update(outfits => {
                const outfit = outfits.find((outfit) => outfit.id === id);
                isClean =
                    outfit &&
                    clothesStore.isClothingItemClean(outfit.topid) &&
                    clothesStore.isClothingItemClean(outfit.bottomid);
                return outfits;
            });
            return isClean;
        },

        makeOutfitDirty: (id) => {
            update(outfits => {
                const outfit = outfits.find((outfit) => outfit.id === id);
                if (outfit) {
                    clothesStore.dirtyClothingItemById(outfit.topid);
                    clothesStore.dirtyClothingItemById(outfit.bottomid);
                }
                return outfits;
            });
        },

        makeOutfitClean: (id) => {
            update(outfits => {
                const outfit = outfits.find((outfit) => outfit.id === id);
                if (outfit) {
                    clothesStore.cleanClothingItemById(outfit.topid);
                    clothesStore.cleanClothingItemById(outfit.bottomid);
                }
                return outfits;
            });
        },

        editOutfitById: (id, name, topid, bottomid, filters) => {
            update((outfits) =>
                outfits.map((outfit) =>
                    outfit.id === id ? { ...outfit, name, topid, bottomid, filters } : outfit
                )
            );
        },
    };
}

export const outfitStore = createOutfitStore();



/**
 * Flyout store
 */
const flyoutStore = writable(new Map());

function open(id) {
    flyoutStore.update((map) => {
        map.set(id, true);
        return map;
    });
}

function close(id) {
    flyoutStore.update((map) => {
        map.delete(id);
        return map;
    });
}

function toggle(id) {
    flyoutStore.update((map) => {
        map.set(id, !map.get(id));
        return map;
    });
}

export { close, flyoutStore, open, toggle };

