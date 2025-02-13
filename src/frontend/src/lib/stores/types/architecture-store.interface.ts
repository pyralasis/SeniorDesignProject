import { type Writable } from 'svelte/store';
import { type NetworkArchitectureDescription, type ArchitectureId, type NetworkLayerDescription, type ArchitectureVersion } from '$lib/types/architecture';
import { type Node, type Edge } from '@xyflow/svelte';
import type { InputDefinition, Layer } from '$lib/types/layer';

export interface NodeArchitecture {
    id?: string;
    meta: {
        name: string;
        description?: string;
        last_modified?: string;
        created_at?: string;
        version?: number;
    }
    nodes: Writable<Node[]>;
    edges: Writable<Edge[]>;
    loading: boolean;
}

export interface AvailableArchitecture {
    id: ArchitectureId;
    meta: {
        name: string;
        description?: string;
        lastModified?: string;
        createdAt?: string;
    },
    info: {
        version: ArchitectureVersion;
    }
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
    saveActiveArchitecture: (isNew?: boolean) => void;
    createNewArchitecture: (name: string) => void;
    addNodeToActiveArchitecture: (node: Node) => void;
    deleteNodeFromActiveArchitecture: (id: string) => void;
}

export type AvailableArchitecturesResponse = {
    available: {
        id: ArchitectureId;
        meta: {
            name: string;
            description?: string;
            last_modified?: string;
            created_at?: string;
        }
        info: {
            version: ArchitectureVersion;
        }
    }[],
    success: boolean
}

export type LoadArchitectureResponse = {
    object: NetworkArchitectureDescription,
    success: boolean
}
