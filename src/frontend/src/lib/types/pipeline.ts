import { type ParameterValue } from "./parameter";
import { type NetworkLayoutDescription } from "./layout";
import type { MetaData } from "./metadata";
import type { TransformConfig } from "./transform";
import type { SourceConfig } from "./source";

export type InstanceId = number;
export type PipelineId = number;

export type PipelineElement = SourceConfig | TransformConfig;

export type PipelineConfig = {
    elements: PipelineElement[];
    value_output: InstanceId;
    label_output: InstanceId;
}

export type PipelineVersion = number;

export type PipelineInfoDescription = {
    version: PipelineVersion
}

export type PipelineMetaDescription = MetaData & {}

export type NetworkPipelineDescription = {
    id: PipelineId,
    content: {
        data: PipelineConfig,
        meta: PipelineMetaDescription,
        layout: NetworkLayoutDescription,
    },
    info?: PipelineInfoDescription
};