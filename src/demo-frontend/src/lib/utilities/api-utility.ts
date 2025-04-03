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
}