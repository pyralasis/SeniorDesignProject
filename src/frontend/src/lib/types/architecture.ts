import { type LayerId, type LayerInstanceId, type TensorSize, type ParameterValue } from '$lib/types/layer';

export type InputLayerDescription = {
    id: LayerInstanceId
    size: TensorSize
};

export type NetworkLayerDescription = {
    id: LayerInstanceId;
    layer_id: LayerId;
    input: LayerInstanceId | LayerInstanceId[];
    param_values: { [id: string]: ParameterValue<any> }
}

export type ArchitectureId = string;

export type LayoutId = string;

export type NetworkNodeDescription = {
    x: number;
    y: number;
    metadata: {
        title: string;
        color: string;
    }
}

export type NetworkLayoutDescription = {
    id: LayoutId;
    nodes: NetworkNodeDescription[];
    edges: any[];
}

export type NetworkArchitectureDescription = {
    id: ArchitectureId;
    name: string;
    version: number;
    inputs: InputLayerDescription[];
    layers: NetworkLayerDescription[];
    layout: NetworkLayoutDescription;
};