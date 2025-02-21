import type { LayerInstanceId } from "./layer";
import type { InstanceId } from "./pipeline";

export type NetworkNodeDescription = {
    x: number;
    y: number;
    metadata: {
        title: string;
        color: string;
    }
}

export type NetworkLayoutDescription = {
    nodes: { [id: LayerInstanceId | InstanceId]: NetworkNodeDescription };
    edges: any[];
}