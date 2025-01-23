import { type Layer, type LayerId } from '$lib/types/layer';
import { BACKEND_API_BASE_URL } from './api.constants';

export const BackendApiRequestsEnum = {
    getAvailableLayers: `${BACKEND_API_BASE_URL}/layer/available`,
    postLayerOutputSize: `${BACKEND_API_BASE_URL}/layer/output_size`,
    getAvailableArchitechture: `${BACKEND_API_BASE_URL}/architecture/available`,
    postDeleteArchitecture: `${BACKEND_API_BASE_URL}/architecture/delete`,
    getLoadArchitecture: `${BACKEND_API_BASE_URL}/architecture/load`,
    postSaveArchitecture: `${BACKEND_API_BASE_URL}/architecture/save`,
} as const;

export class BackendApi {

    static parseLayers(data: any): Layer<any>[] {
        let layers: Layer<any>[] = [];
        data.map((l: any) => {
            layers.push(l as Layer<any>);
        })
        console.log(layers);
        return layers;
    }

    static async getAvailableLayers(): Promise<Layer<any>[]> {
        const response = await fetch(BackendApiRequestsEnum.getAvailableLayers);
        const data = await response.json();
        return this.parseLayers(data);
    }
}

