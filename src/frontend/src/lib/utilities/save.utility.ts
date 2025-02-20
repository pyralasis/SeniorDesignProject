import type { Node, Edge } from '@xyflow/svelte';
import { get, type Readable } from 'svelte/store';

export interface SaveData {
    nodes: Node[];
    edges: Edge[];
    timestamp: string;
}

interface NodeData {
    title: string | Readable<string>;
    color: string | Readable<string>;
    layer_id: string | Readable<string>;
    parameters: any | Readable<any>;
    expanded: boolean | Readable<boolean>;
}

export class SaveUtility {
    private static readonly STORAGE_KEY = 'flow-editor-save';

    private static getStoreValue<T>(value: T | Readable<T>): T {
        if (value && typeof value === 'object' && 'subscribe' in value) {
            return get(value as Readable<T>);
        }
        return value as T;
    }

    static async saveFlow(nodes: Node[], edges: Edge[]): Promise<void> {
        try {
            const saveData: SaveData = {
                nodes: nodes.map(node => ({
                    ...node,
                    data: {
                        ...node.data,
                        title: this.getStoreValue(node.data.title),
                        color: this.getStoreValue(node.data.color),
                        layer_id: this.getStoreValue(node.data.layer_id),
                        parameters: this.getStoreValue(node.data.parameters),
                        expanded: this.getStoreValue(node.data.expanded),
                    }
                })),
                edges,
                timestamp: new Date().toISOString()
            };

           
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(saveData));

            // Also save to backend if needed
            await fetch('/api/nodes/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(saveData)
            });

        } catch (error) {
            console.error('Failed to save flow:', error);
            throw error;
        }
    }

    static loadFlow(): SaveData | null {
        try {
            const savedData = localStorage.getItem(this.STORAGE_KEY);
            if (!savedData) return null;
            return JSON.parse(savedData);
        } catch (error) {
            console.error('Failed to load flow:', error);
            return null;
        }
    }
}