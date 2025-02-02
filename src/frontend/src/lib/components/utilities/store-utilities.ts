import type { Writable } from "svelte/store"
import { getContext, setContext } from "svelte"

export const getParentStore = <T>(): Writable<T> => {
    return getContext("private_store");
}

export const setParentStoreContext = <T>(store: Writable<T>): void => {
    setContext("private_store", store);
}