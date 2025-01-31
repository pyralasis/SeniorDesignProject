import { type Writable } from 'svelte/store';
import { type NetworkArchitectureDescription, type ArchitectureId } from '$lib/types/architecture';
import { type Node, type Edge } from '@xyflow/svelte';

export interface NodeArchitecture {
    id: string;
    fileName: string;
    name: string;
    nodes: Writable<Node[]>;
    edges: Writable<Edge[]>;
}

export interface ArchitectureStoreProps {
    architectureIds: ArchitectureId[];
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
