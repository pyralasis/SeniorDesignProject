export class Layer {
    constructor(object: Object) {
        object && Object.assign(this, object);
    }
};