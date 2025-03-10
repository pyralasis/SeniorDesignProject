import type { LayerBlueprint } from '$lib/types/layer';
import type { NodeType } from '$lib/types/node-type.enum';
import type { SourceBlueprint } from '$lib/types/source';
import type { TransformBlueprint } from '$lib/types/transform';
import { getContext } from 'svelte';
import type { Writable } from 'svelte/store';

type BasicBlueprint<T> = {
    id: string,
    name: string,
    parameters: T[],
}
export type NodeBlueprint = LayerBlueprint<any> | SourceBlueprint<any> | TransformBlueprint<any> | BasicBlueprint<any>;

export type DnDContext = {
    type: NodeType,
    nodeBlueprint: NodeBlueprint,
};

export const useDnD = () => {
    return getContext('dnd') as Writable<DnDContext | null>;
};