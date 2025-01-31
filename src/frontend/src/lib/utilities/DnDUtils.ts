import type { Layer } from '$lib/types/layer';
import type { NodeType } from '$lib/types/node-type.enum';
import { getContext } from 'svelte';
import type { Writable } from 'svelte/store';

export type DnDContext = {
    type: NodeType,
    layerBlueprint: Layer<any>,
};

export const useDnD = () => {
    return getContext('dnd') as Writable<DnDContext | null>;
};