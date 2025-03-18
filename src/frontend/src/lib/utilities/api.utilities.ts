import { type LayerBlueprint, type LayerId, type TensorSize } from '$lib/types/layer';
import type { ParameterValue } from '$lib/types/parameter';
import type { SourceBlueprint, SourceId } from '$lib/types/source';
import type { TransformBlueprint, TransformId } from '$lib/types/transform';
import { BACKEND_API_BASE_URL } from './api.constants';

export const BackendApiRequestsEnum = {
    getAvailableLayers: `${BACKEND_API_BASE_URL}/layer/available`,
    getLayerById: `${BACKEND_API_BASE_URL}/layer/get`,
    postLayerOutputSize: `${BACKEND_API_BASE_URL}/layer/output_size`,
    getAvailableArchitechture: `${BACKEND_API_BASE_URL}/architecture/available`,
    postDeleteArchitecture: `${BACKEND_API_BASE_URL}/architecture/delete`,
    getLoadArchitecture: `${BACKEND_API_BASE_URL}/architecture/load`,
    postSaveArchitecture: `${BACKEND_API_BASE_URL}/architecture/save`,
} as const;

export class BackendApi {
    static async getAvailableLayers(): Promise<LayerBlueprint<any>[]> {
        return fetch(BackendApiRequestsEnum.getAvailableLayers, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                let layers: LayerBlueprint<any>[] = [];
                data.map((l: any) => {
                    layers.push({
                        id: l.id,
                        name: l.name,
                        inputs: l.inputs,
                        parameters: l.parameters,
                    } as LayerBlueprint<any>);
                })
                return layers;
            });
    }

    static async getLayerById(id: LayerId): Promise<LayerBlueprint<any>> {
        return fetch(`${BackendApiRequestsEnum.getLayerById}?id=${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                const layer = data.layer;
                return {
                    id: layer.id,
                    name: layer.name,
                    inputs: layer.inputs,
                    parameters: layer.parameters
                } as LayerBlueprint<any>
            });
    }


    static async getAvailableSources(): Promise<SourceBlueprint<any>[]> {
        return fetch(`${BACKEND_API_BASE_URL}/pipeline/available_sources`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                let sources: SourceBlueprint<any>[] = [];
                data.map((s: any) => {
                    sources.push({
                        id: s.id,
                        name: s.name,
                        parameters: s.parameters
                    } as SourceBlueprint<any>);
                })
                return sources;
            });
    }

    static getSourceById(id: SourceId): Promise<SourceBlueprint<any>> {
        return fetch(`${BACKEND_API_BASE_URL}/pipeline/get_source?id=${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                return {
                    id: data[0].id,
                    name: data[0].name,
                    parameters: data[0].parameters
                } as SourceBlueprint<any>
            });
    }

    static async getAvailableTransforms(): Promise<TransformBlueprint<any>[]> {
        return fetch(`${BACKEND_API_BASE_URL}/pipeline/available_transforms`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                let transform: TransformBlueprint<any>[] = [];
                data.map((s: any) => {
                    transform.push({
                        id: s.id,
                        name: s.name,
                        parameters: s.parameters,
                        type: s.type
                    } as TransformBlueprint<any>);
                })
                return transform;
            });
    }

    static getTransformById(id: TransformId): Promise<TransformBlueprint<any>> {
        return fetch(`${BACKEND_API_BASE_URL}/pipeline/get_transform?id=${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                return {
                    id: data[0].id,
                    name: data[0].name,
                    parameters: data[0].parameters,
                    type: data[0].type
                } as TransformBlueprint<any>
            });
    }

    static getLayerOutputSize(layer_id: LayerId, inputSize: TensorSize, parameters: Record<string, ParameterValue<any>>): Promise<TensorSize> {
        return fetch(BackendApiRequestsEnum.postLayerOutputSize, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                layer_id,
                input_size: inputSize,
                parameters
            })
        })
            .then(response => response.json())
            .then(data => {
                return data.output_size;
            });
    }
}
