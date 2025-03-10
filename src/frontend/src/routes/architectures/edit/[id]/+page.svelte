<script lang="ts">
    import { SvelteFlowProvider, type Connection, type Edge, type Node } from '@xyflow/svelte';
    import DnDProvider from '$lib/components/DnDProvider.svelte';
    import NodeEditor from '$lib/components/NodeEditor/NodeEditor.svelte';
    import { writable, type Writable, get } from 'svelte/store';
    import { architectureStore } from '$lib/stores/ArchitectureStore';
    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { onDestroy, onMount } from 'svelte';
    import { page } from '$app/state';
    import { Button, TextInput } from 'kiwi-nl';
    import { StylingUtility } from '$lib/utilities/styling.utility';
    import Icon from '$lib/components/Icon/Icon.svelte';
    import { IconNameEnum } from '$lib/components/Icon/types/icon-name.enum';
    import { BackendApi } from '$lib/utilities/api.utilities';
    import type { DnDContext } from '$lib/utilities/DnDUtils';
    import type { LayerBlueprint, LayerInput, TensorSize } from '$lib/types/layer';
    import { NodeTypeEnum } from '$lib/types/node-type.enum';
    import { SaveStatusEnum } from '$lib/stores/types/architecture-store.interface';
    import type { Parameter, ParameterValue } from '$lib/types/parameter';
    import { HandleStatusEnum, type HandleStatus } from '$lib/components/Node/handle-status.enum';

    let nodes: Writable<Node[]>;
    let edges: Writable<Edge[]>;
    let availableLayers: Writable<DnDContext[]> = writable([]);

    $: id = page.params.id;
    let isEditingTitle: Writable<boolean> = writable(false);
    const inputNodeBluePrints: Writable<DnDContext[]> = writable([
        {
            type: NodeTypeEnum.Input,
            nodeBlueprint: {
                id: 'input',
                name: 'Input Node',
                parameters: [
                    {
                        parameter: { id: 'tensor_size', name: 'Tensor Size', type: 'size2d' },
                        value: { type: 'size2d', val: [0, 0] },
                    },
                ],
            },
        },
    ] as DnDContext[]);
    const outputNodeBluePrints: Writable<DnDContext[]> = writable([
        { type: NodeTypeEnum.Output, nodeBlueprint: { id: 'output', name: 'Output Node', parameters: [] } },
    ] as DnDContext[]);

    architectureStore.subscribe((store) => {
        if (!store.activeArchitecture) {
            return;
        }
        nodes = store?.activeArchitecture?.nodes;
        edges = store?.activeArchitecture?.edges;
    });

    function onSave() {
        saveStatus.set('Saving...');
        architectureStore
            .saveActiveArchitecture()
            .then(() => {
                setTimeout(() => {
                    saveStatus.set('Architecture is up to Date');
                    isArchitectureSaved.set(true);
                }, 500);
            })
            .catch((w) => {
                saveStatus.set('Failed to Save. Save Again');
                console.error(w);
            });
    }

    function handleKeydown(event: KeyboardEvent) {
        if ((event.ctrlKey || event.metaKey) && (event.key === 's' || event.key === 'S')) {
            event.preventDefault();
            architectureStore.updateArchitectureSaveStatus();
        }
    }
    function onChange() {
        if ($architectureStore.saveStatus === SaveStatusEnum.NotSaved) {
            return;
        }
        architectureStore.updateSaveStatus(false, SaveStatusEnum.NotSaved);
    }
    onMount(() => {
        window.addEventListener('keydown', handleKeydown);

        return () => {
            window.removeEventListener('keydown', handleKeydown);
        };
    });

    onDestroy(() => {
        architectureStore.clearActiveArchitecture();
    });

    onMount(async () => {
        availableLayers.set(
            (await BackendApi.getAvailableLayers()).map(
                (layer: LayerBlueprint<any>) => ({ type: NodeTypeEnum.Layer, nodeBlueprint: layer }) as DnDContext,
            ),
        );
        await architectureStore.loadArchitectureById(id);
    });

    function onTitleChange(event: CustomEvent) {
        if (!$architectureStore.activeArchitecture) {
            return;
        }
        $architectureStore.activeArchitecture.meta.name = event.detail.value;
    }

    function deconstructParameters(parameters: { parameter: Parameter<any>; value: ParameterValue<any> }[]): Record<string, any> {
        const result: Record<string, any> = {};
        if (!parameters) {
            return result;
        }
        parameters.forEach((parameter) => {
            result[parameter.parameter.id] = parameter.value.val;
        });
        return result;
    }

    function constructIdChain(currentNodeId: string, idChain: string[]): string[] {
        const currentEdge = $edges.find((edge) => edge.source === currentNodeId);
        if (!currentEdge) {
            return idChain;
        }
        const targetNodeId = currentEdge?.target;
        idChain.push(targetNodeId);
        return constructIdChain(targetNodeId, idChain);
    }

    function constructNodeChain(): Node[] {
        const inputNode = $nodes.find((node) => node.type === NodeTypeEnum.Input);
        // Reset the status of all nodes
        $nodes.forEach((node) => {
            if (node.data?.leftStatus) {
                (node.data.leftStatus as Writable<HandleStatus>).set(HandleStatusEnum.default);
            }
            if (node.data?.rightStatus) {
                (node.data.rightStatus as Writable<HandleStatus>).set(HandleStatusEnum.default);
            }
        });
        if (!inputNode) {
            return [];
        }
        const nodeIdChain: string[] = constructIdChain(inputNode.id, [inputNode.id]);
        const nodeChain: Node[] = nodeIdChain.map((nodeId) => $nodes.find((node) => node.id === nodeId) as Node);
        return nodeChain;
    }

    function validateNodes(nodeChain: Node[]): void {
        let currentNode: Node = nodeChain[0];
        let previousNode: Node;

        for (let i = 1; i < nodeChain.length; i++) {
            previousNode = currentNode;
            currentNode = nodeChain[i];
            if (currentNode.id === '69') {
                return;
            }
            let previousNodeOutputSize: TensorSize = get(previousNode.data?.outputSize as Writable<TensorSize>);
            let currentNodeMaxDimension: number = get(currentNode.data?.inputs as Writable<LayerInput[]>)[0]?.max_dimensions as number;
            let currentNodeMinDimension: number = get(currentNode.data?.inputs as Writable<LayerInput[]>)[0]?.min_dimensions as number;
            console.log(previousNodeOutputSize, currentNodeMinDimension, currentNodeMaxDimension);
            if (
                (previousNodeOutputSize.length >= currentNodeMinDimension || currentNodeMinDimension === null) &&
                (previousNodeOutputSize.length <= currentNodeMaxDimension || currentNodeMaxDimension === null)
            ) {
                (previousNode.data?.rightStatus as Writable<HandleStatus>).set(HandleStatusEnum.success);
                (currentNode.data?.leftStatus as Writable<HandleStatus>).set(HandleStatusEnum.success);
            } else {
                (previousNode.data?.rightStatus as Writable<HandleStatus>).set(HandleStatusEnum.error);
                (currentNode.data?.leftStatus as Writable<HandleStatus>).set(HandleStatusEnum.error);
            }
        }
    }

    async function onConnect(connection: Connection) {
        const sourceNode = $nodes.find((node) => node.id === connection.source);
        const targetNode = $nodes.find((node) => node.id === connection.target);
        if (!sourceNode || !targetNode) {
            return;
        }
        const targetNodeOutputSize: TensorSize = await BackendApi.getLayerOutputSize(
            targetNode.data.layer_id as string,
            get(sourceNode.data.outputSize as Writable<TensorSize>),
            deconstructParameters(get(targetNode.data.parameters as Writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>)),
        );

        if (targetNode.id != '69') {
            (targetNode.data.outputSize as Writable<TensorSize>).set(targetNodeOutputSize);
        }

        let nodeChain: Node[] = constructNodeChain();
        validateNodes(nodeChain);
    }

    function onNodeOrEdgeDelete() {
        let nodeChain: Node[] = constructNodeChain();
        validateNodes(nodeChain);
        console.log(nodeChain);
    }
</script>

<div class="edit-architectures-page">
    <div class="edit-architectures-page__header">
        <div class="edit-architectures-page__header-left">
            {#if $isEditingTitle}
                <TextInput
                    label="Architecture Name"
                    on:change={onTitleChange}
                    value={$architectureStore.activeArchitecture?.meta.name}
                    style={StylingUtility.textInput}
                ></TextInput>
                <Button style={StylingUtility.defaultButton} on:click={() => isEditingTitle.set(false)}
                    ><Icon name={IconNameEnum.checkmark} /></Button
                >
            {:else}
                <h1>{$architectureStore.activeArchitecture?.meta.name}</h1>
                <Button style={StylingUtility.defaultButton} on:click={() => isEditingTitle.set(true)}
                    ><Icon name={IconNameEnum.pencil} /></Button
                >
            {/if}
        </div>
        <div class="save-status">
            <span>{$architectureStore.saveStatus}</span>
        </div>
    </div>
    <SvelteFlowProvider>
        <DnDProvider>
            {#if $architectureStore.activeArchitecture?.loading}
                <div class="spinner-container">
                    <Spinner />
                </div>
            {:else if !$architectureStore.activeArchitecture?.loading && nodes && edges}
                <NodeEditor
                    onSave={() => architectureStore.updateArchitectureSaveStatus()}
                    {onChange}
                    onCreateNode={architectureStore.addNodeToActiveArchitecture}
                    onDeleteNode={architectureStore.deleteNodeFromActiveArchitecture}
                    {onConnect}
                    {onNodeOrEdgeDelete}
                    {nodes}
                    {edges}
                    nodeblueprints={[...$inputNodeBluePrints, ...$outputNodeBluePrints, ...$availableLayers]}
                />
            {:else}
                <div class="spinner-container">
                    <Spinner />
                </div>
            {/if}
        </DnDProvider>
    </SvelteFlowProvider>
</div>

<style lang="scss">
    .edit-architectures-page {
        width: 100%;
        height: 100%;

        &__header {
            padding: 16px;
            display: flex;
            align-items: end;
            justify-content: space-between;
            height: 54px;
        }

        &__header-left {
            display: flex;
            align-items: end;
            gap: 8px;
        }

        h1 {
            margin: 0;
            color: #ffffff;
        }
    }
    .save-status {
        display: flex;
        align-items: center;
        color: white;
        font-size: 14px;
        font-weight: bold;
        margin-left: auto;
        margin-right: 0;
    }
    .save-status span {
        margin-right: 10px;
    }
    .spinner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
</style>
