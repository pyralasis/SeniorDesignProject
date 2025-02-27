import { type Writable } from 'svelte/store';
import type { NetworkArchitectureDescription, ArchitectureId, ArchitectureMetaDescription, ArchitectureInfoDescription } from '$lib/types/architecture';
import { type Node } from '@xyflow/svelte';
import type { NodeArchitecture } from './node-architecture.interface';


export interface AvailableArchitecture {
    id: ArchitectureId;
    meta: ArchitectureMetaDescription;
    info: ArchitectureInfoDescription
}

export interface ArchitectureStoreProps {
    availableArchitectures: AvailableArchitecture[] | undefined;
    activeArchitecture: NodeArchitecture | undefined;
}

export interface ArchitectureStore extends Writable<ArchitectureStoreProps> {
    getAvailableArchitectures: () => void;
    loadArchitectureById: (id: ArchitectureId) => void;
    clearActiveArchitecture: () => void;
    deleteArchitecture: (id: ArchitectureId) => void;
    saveActiveArchitecture: (isNew?: boolean) => Promise<ArchitectureId | void>;
    createNewArchitecture: (name: string, description: string) => void;
    addNodeToActiveArchitecture: (node: Node) => void;
    deleteNodeFromActiveArchitecture: (id: string) => void;
}

export type AvailableArchitecturesResponse = {
    available: AvailableArchitecture[],
    success: boolean
}

export type LoadArchitectureResponse = {
    object: NetworkArchitectureDescription,
    success: boolean
}
