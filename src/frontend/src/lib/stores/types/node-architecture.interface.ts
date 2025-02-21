import type { ArchitectureId } from "$lib/types/architecture";
import type { PipelineId } from "$lib/types/pipeline";
import type { Edge, Node } from "@xyflow/svelte";
import type { Writable } from "svelte/store";

export interface NodeArchitecture {
    id?: ArchitectureId | PipelineId;
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