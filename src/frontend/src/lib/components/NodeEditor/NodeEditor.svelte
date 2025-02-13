<script module>
</script>

<script lang="ts">
    import { SaveUtility } from '$lib/utilities/save.utility';
    import { writable, type Writable } from 'svelte/store';
    import { type Node, SvelteFlow, Controls, Background, MiniMap, useSvelteFlow, type NodeTypes, type Edge } from '@xyflow/svelte';
    import { useDnD } from '$lib/utilities/DnDUtils';
    import { onMount } from 'svelte';
    import LayerNode from '../Node/LayerNode.svelte';
    import Sidebar from '$lib/components/Sidebar/Sidebar.svelte';
    import '@xyflow/svelte/dist/style.css';
    import { type Parameter, type ParameterValue } from '$lib/types/layer';
    import NodeEditorActions from './NodeEditorActions.svelte';
    import { setContext } from 'svelte';
    import { SoundUtility } from '$lib/utilities/sound.utility';

    export let nodes: Writable<Node[]>;
    export let edges: Writable<Edge[]>;
    export let onDeleteNode: (nodeId: string) => void;
    export let onCreateNode: (node: Node) => void;
    export let onSave: () => void;

    const { screenToFlowPosition } = useSvelteFlow();
    const dndContext = useDnD();
    let selectedNodeTitle: Writable<string> | undefined;
    let sidebarExpanded: Writable<boolean> = writable(true);

    const xColor = writable<string>('#FFFFFF');
    setContext('xColor', xColor);
    setContext('sidebarExpanded', sidebarExpanded);
    


    const saveStatus = writable('Page Up to Date');
    const isSaving = writable(false)
    async function saveNodes() {
        try {
            isSaving.set(true);
            saveStatus.set('Saving...');
            
            await SaveUtility.saveFlow($nodes, $edges);
            
            saveStatus.set('All Changes Saved');
            setTimeout(() => {
                saveStatus.set('Page Up to Date');
            }, 2000);

        } catch (error) {
            console.error('Save failed:', error);
            saveStatus.set('Failed to Save');
        } finally {
            isSaving.set(false);
        }
    }


    const inputStyle = {
        backgroundColor: '#000000',
        color: '#ffffff',
        border: '1px solid #ffffff',
        label: {
            color: '#ffffff',
        },
        hover: {
            backgroundColor: '#000000',
            color: '#ffffff',
            border: '1px solid #ffffff',
        },
        focus: {
            backgroundColor: '#000000',
            color: '#ffffff',
            border: '1px solid #ffffff',
        },
    };

    function getParameterDefaultValue(parameter: Parameter<any>): { parameter: Parameter<any>; value: ParameterValue<any> } {
        return {
            parameter,
            value: {
                type: parameter.type,
                value: parameter.default,
            },
        };
    }

    const onDragOver = (event: DragEvent) => {
        event.preventDefault();

        if (event.dataTransfer) {
            event.dataTransfer.dropEffect = 'move';
        }
    };

    const onDrop = (event: DragEvent) => {
        event.preventDefault();
        SoundUtility.playDrop(0.02);

        if (!$dndContext?.type) {
            return;
        }

        const position = screenToFlowPosition({
            x: event.clientX,
            y: event.clientY,
        });

        const newNode = {
            id: `${Math.floor(Math.random() * 1000000)}`,
            type: $dndContext?.type,
            data: {
                color: writable<string>($xColor),
                title: writable<string>('Untitled Node'),
                layer_id: writable<string>($dndContext.layerBlueprint.name),
                parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                    $dndContext.layerBlueprint.parameters.map(getParameterDefaultValue),
                ),
                expanded: writable<boolean>(false),
            },
            dragHandle: '.node__header',
            position: { x: position.x, y: position.y },
        } satisfies Node;

        onCreateNode(newNode);
    };

    const nodeTypes: NodeTypes = {
        layer: LayerNode,
    };

    function onDelete() {
        onDeleteNode(selectedNode?.id ?? '');
    }

    function onClearNodes() {
        nodes.update((nodes) => (nodes = []));
    }
    onMount(() => {
        const savedData = SaveUtility.loadFlow();
        if (savedData) {
            nodes.set(savedData.nodes.map(node => ({
                ...node,
                data: {
                    ...node.data,
                    title: writable(node.data.title),
                    color: writable(node.data.color),
                    layer_id: writable(node.data.layer_id),
                    parameters: writable(node.data.parameters),
                    expanded: writable(node.data.expanded),
                }
            })));
            edges.set(savedData.edges);
        }

        // Add Ctrl+S handler
        const handleKeyDown = (event: KeyboardEvent) => {
            if ((event.ctrlKey || event.metaKey) && event.key === 's') {
                event.preventDefault();
                saveNodes();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    });



    $: selectedNode = $nodes.find((node) => node.selected);
    $: selectedNodeTitle = selectedNode?.data.title as Writable<string> | undefined;
    $: selectedNodeColor = selectedNode?.data.color as Writable<string> | undefined;
</script>

<div class="node-editor">
    <NodeEditorActions {selectedNodeTitle} {selectedNodeColor} {onDelete} {onClearNodes} />
    <div class="node-editor__content">
        <div class="node-editor__sidebar">
            <Sidebar expanded={$sidebarExpanded} />
        </div>
        
        <div class="node-editor__flow">
            <div class="save-status">
                <span>{$saveStatus}</span>
            </div>
            <SvelteFlow {nodes} {edges} {nodeTypes} on:dragover={onDragOver} on:drop={onDrop}>
                <Background bgColor="#000000" patternColor="#FFFFFF" />
            </SvelteFlow>  
            
        </div>
    </div>
</div>

<style lang="scss">
    .node-editor {
        display: flex;
        flex-direction: column;
        overflow: hidden;
        background-color: #000000;
        height: 100%;

        &__content {
            display: flex;
            flex-direction: row;
            height: calc(100% + 30px);
        }

        &__flow {
            width: 100%;
            height: 100%;
        }

        &__sidebar {
            width: fit-content;
        }
        .save-status {
            position: absolute;
            top: 10px;
            right: 20px;
            background-color: #222;
            color: white;
            padding: 10px;
            border-radius: 5px;
            z-index: 1000;
            font-size: 14px;
            font-weight: 500;
    }
}
</style>
