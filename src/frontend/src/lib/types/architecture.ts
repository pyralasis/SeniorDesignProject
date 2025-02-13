import { type LayerId, type LayerInstanceId, type TensorSize, type ParameterValue, type InputDefinition } from '$lib/types/layer';

export type InputLayerDescription = {
    id: LayerInstanceId
    size: TensorSize
};

export type NetworkLayerDescription = {
    instance_id: LayerInstanceId;
    layer_id: LayerId;
    input: LayerInstanceId | LayerInstanceId[];
    param_values: { [id: string]: ParameterValue<any> }
}


export type ArchitectureId = string;
export type ArchitectureVersion = number;

export type NetworkNodeDescription = {
    x: number;
    y: number;
    metadata: {
        title: string;
        color: string;
    }
}

export type NetworkLayoutDescription = {
    nodes: { [id: LayerInstanceId]: NetworkNodeDescription };
    edges: any[];
}


export type ArchitectureDataDescription = {
    inputs: InputDefinition[],
    layers: NetworkLayerDescription[],
    output: LayerInstanceId
}

export type ArchitectureInfoDescription = {
    version: ArchitectureVersion
}

export type ArchitectureMetaDescription = {
    name: string,
    description?: string,
    created_at: string,
    last_modified: string,
}

export type NetworkArchitectureDescription = {
    id: ArchitectureId,
    data: {
        data: ArchitectureDataDescription,
        layout: NetworkLayoutDescription,
        meta: ArchitectureMetaDescription,
    }
    info?: ArchitectureInfoDescription

};