import { type Writable } from 'svelte/store';
import { type Node, } from '@xyflow/svelte';
import type { NodeArchitecture } from './node-architecture.interface';
import type { PipelineId, PipelineInfoDescription, PipelineMetaDescription, NetworkPipelineDescription } from '$lib/types/pipeline';

export interface AvailablePipeline {
    id: PipelineId;
    meta: PipelineMetaDescription
    info: PipelineInfoDescription
}


export interface PipelineStoreProps {
    availablePipelines: AvailablePipeline[] | undefined;
    activePipeline: NodeArchitecture | undefined;
}

export interface PipelineStore extends Writable<PipelineStoreProps> {
    getAvailablePipelines: () => void;
    loadPipelineById: (id: PipelineId) => void;
    clearActivePipeline: () => void;
    deletePipeline: (id: PipelineId) => void;
    saveActivePipeline: (isNew?: boolean) => Promise<PipelineId | void>;
    createNewPipeline: (name: string, description: string) => void;
    addNodeToActivePipeline: (node: Node) => void;
    deleteNodeFromActivePipeline: (id: string) => void;
}

export type AvailablePipelinesResponse = {
    available: AvailablePipeline[],
    success: boolean
}

export type LoadPipelineResponse = {
    object: NetworkPipelineDescription,
    success: boolean
}
