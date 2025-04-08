import { type Writable } from "svelte/store";
import { type Node } from "@xyflow/svelte";
import type { NodeArchitecture } from "./node-architecture.interface";
import type {
  PipelineId,
  PipelineInfoDescription,
  PipelineMetaDescription,
  NetworkPipelineDescription,
} from "$lib/types/pipeline";

export interface AvailablePipeline {
  id: PipelineId;
  meta: PipelineMetaDescription;
  info: PipelineInfoDescription;
}
export enum PipelineStatusEnum {
  Saving = "Saving...",
  Success = "Pipeline is up to date",
  NotSaved = "Pipeline is not saved",
  Failed = "Failed to Save. Try Again",
}

export interface PipelineStoreProps {
  availablePipelines: AvailablePipeline[] | undefined;
  activePipeline: NodeArchitecture | undefined;
  isSaved: boolean;
  saveStatus: PipelineStatusEnum;
}

export interface PipelineStore extends Writable<PipelineStoreProps> {
  getAvailablePipelines: () => void;
  loadPipelineById: (id: PipelineId) => void;
  clearActivePipeline: () => void;
  deletePipeline: (id: PipelineId) => Promise<boolean>;
  saveActivePipeline: (
    isNew?: boolean
  ) => Promise<{ id?: PipelineId; success: boolean }>;
  createNewPipeline: (
    name: string,
    description: string
  ) => Promise<{ id?: PipelineId; success: boolean }>;
  addNodeToActivePipeline: (node: Node) => void;
  deleteNodeFromActivePipeline: (id: string) => void;
  updatePipelineSaveStatus: () => void;
  updateSaveStatus: (isSaved: boolean, status: PipelineStatusEnum) => void;
  getPipelineNameById: (id: PipelineId) => Promise<string>;
}

export type AvailablePipelinesResponse = {
  available: AvailablePipeline[];
  success: boolean;
};

export type LoadPipelineResponse = {
  object: NetworkPipelineDescription;
  success: boolean;
};
