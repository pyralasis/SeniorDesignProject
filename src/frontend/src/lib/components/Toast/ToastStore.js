import { writable } from 'svelte/store';

export function createToastStore() {
  const { subscribe, set, update } = writable([]);

  return {
    subscribe,
    add: (toast) => update((toasts) => [...toasts, toast]),
    remove: (id) => update((toasts) => toasts.filter((toast) => toast.id !== id)),
  };
}