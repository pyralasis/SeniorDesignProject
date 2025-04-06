import type { LayerId, LayerInstanceId, TensorSize } from '$lib/types/layer';
import type { Info } from './info';
import type { NetworkLayoutDescription } from './layout';
import type { MetaData } from './metadata';
import type { ParameterValue } from './parameter';

export type InputLayerDescription = {
    instance_id: LayerInstanceId
    size: TensorSize
};

export type NetworkLayerDescription = {
    instance_id: LayerInstanceId;
    layer_id: LayerId;
    input: LayerInstanceId | LayerInstanceId[];
    param_values: [string, ParameterValue<any>][];
}

export type ArchitectureId = string;

export type ArchitectureDataDescription = {
    inputs: InputLayerDescription[],
    layers: NetworkLayerDescription[],
    output: LayerInstanceId
}

export type ArchitectureInfoDescription = Info & {}

export type ArchitectureMetaDescription = MetaData & {}

export type NetworkArchitectureDescription = {
    id: ArchitectureId,
    content: {
        data: ArchitectureDataDescription,
        layout: NetworkLayoutDescription,
        meta: ArchitectureMetaDescription,
    }
    info?: ArchitectureInfoDescription

};