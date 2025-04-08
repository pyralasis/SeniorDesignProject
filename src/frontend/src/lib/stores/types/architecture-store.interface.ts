import { type Writable } from "svelte/store";
import type {
  NetworkArchitectureDescription,
  ArchitectureId,
  ArchitectureMetaDescription,
  ArchitectureInfoDescription,
} from "$lib/types/architecture";
import { type Node } from "@xyflow/svelte";
import type { NodeArchitecture } from "./node-architecture.interface";

export interface AvailableArchitecture {
  id: ArchitectureId;
  meta: ArchitectureMetaDescription;
  info: ArchitectureInfoDescription;
}

export enum SaveStatusEnum {
  Saving = "Saving...",
  Success = "Architecture is up to date",
  NotSaved = "Architecture is not saved",
  Failed = "Failed to Save. Try Again",
}

export interface ArchitectureStoreProps {
  availableArchitectures: AvailableArchitecture[] | undefined;
  activeArchitecture: NodeArchitecture | undefined;
  //Booleans to see if its true and an enum for 4 string values
  isSaved: boolean;
  saveStatus: SaveStatusEnum;
}

export interface ArchitectureStore extends Writable<ArchitectureStoreProps> {
  getAvailableArchitectures: () => void;
  loadArchitectureById: (id: ArchitectureId) => void;
  clearActiveArchitecture: () => void;
  deleteArchitecture: (id: ArchitectureId) => Promise<boolean>;
  saveActiveArchitecture: (
    isNew?: boolean
  ) => Promise<{ id?: ArchitectureId; success: boolean }>;
  createNewArchitecture: (
    name: string,
    description: string
  ) => Promise<{ id?: ArchitectureId; success: boolean }>;
  addNodeToActiveArchitecture: (node: Node) => void;
  deleteNodeFromActiveArchitecture: (id: string) => void;
  //My AutoSave / Save Function
  updateArchitectureSaveStatus: () => void;
  updateSaveStatus: (isSaved: boolean, status: SaveStatusEnum) => void;
}

export type AvailableArchitecturesResponse = {
  available: AvailableArchitecture[];
  success: boolean;
};

export type LoadArchitectureResponse = {
  object: NetworkArchitectureDescription;
  success: boolean;
};
