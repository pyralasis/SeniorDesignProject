export interface ModelObjectDesc {
    id: number;
    info: any;
    meta: any;
}

export class ApiUtility {
    static async inferNumber(matrix: number[][]): Promise<number | undefined> {
        try {
            return fetch('http://localhost:8888/api/demo/infer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: matrix }),
            })
                .then((response) => response.json())
                .then((data) => {
                    return data.prediction as number;
                });
        } catch (error) {
            console.error('Error:', error);
            return undefined;
        }
    }

    static async get_models(): Promise<ModelObjectDesc[]> {
        try {
            return fetch('http://localhost:8888/api/demo/available_models', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    return data as ModelObjectDesc[];
                });
        } catch (error) {
            console.error('Error:', error);
            return [];
        }
    }

    static async load_model(id: number): Promise<any> {
        try {
            return fetch(`http://localhost:8888/api/demo/load_model`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: id }),
            })
                .then(() => { })
        } catch (error) {
            console.error('Error:', error);
            return undefined;
        }
    }
}