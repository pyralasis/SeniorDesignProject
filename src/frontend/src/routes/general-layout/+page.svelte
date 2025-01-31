<script module>
    export type dummyData = { tabID: number; tabTitle: string };
    let test: dummyData[] = [
        { tabID: 1, tabTitle: 'A' },
        { tabID: 2, tabTitle: 'B' },
    ];
    export let dummyTabs = writable<dummyData[]>(test);
</script>

<script lang="ts">
    import {
        ButtonSizeEnum,
        ButtonTypeEnum,
        Flyout,
        Header,
        HeaderTypeEnum,
        Popover,
        PopoverChipTrigger,
        PopoverMultiSelectContent,
        TabContent,
        TabLabel,
        Tabs,
        Button,
        Accordion,
        AccordionHeader,
        AccordionBody,
        Checkbox,
        Text,
        type PopoverItem,
        Tag,
        TagColorEnum,
        TextInput,
        PopoverSingleSelectContent,
    } from 'kiwi-nl';

    import { SvelteFlowProvider } from '@xyflow/svelte';
    import DnDProvider from '$lib/components/DnDProvider.svelte';

    import Flow from '$lib/components/NodeEditor/NodeEditor.svelte';
    import { writable, type Writable } from 'svelte/store';
    import type { Edge, Node } from '@xyflow/svelte';
    import NavBar from '$lib/components/General/NavBar.svelte';
    import { architectureStore } from '$lib/stores/ArchitectureStore';

    architectureStore.createNewArchitecture('New Architecture');

    let architectureNodes: Writable<Node[]> = writable([]);
    let architectureEdges: Writable<Edge[]> = writable([]);

    architectureStore.subscribe((store) => {
        if (!store.activeArchitecture) {
            return;
        }
        architectureNodes = store.activeArchitecture.nodes;
        architectureEdges = store.activeArchitecture.edges;
    });

    function onSave() {
        architectureStore.saveActiveArchitecture();
    }

    let closeTab = (tabID: number) => {
        let mytabs = $dummyTabs;
        let findTabByID = (element: dummyData, id: number) => {
            return element.tabID == id;
        };
        mytabs.splice(
            mytabs.findIndex((element) => findTabByID(element, tabID)),
            1,
        );
        $dummyTabs = mytabs;
    };

    function openTab(newTab: dummyData) {
        let mytabs = $dummyTabs;
        mytabs.push(newTab);
        $dummyTabs = mytabs;
    }
</script>

<div class="wrapper">
    <div class="nav-bar">
        <NavBar></NavBar>
    </div>
    <main>
        <Tabs activeTab={1}>
            <svelte:fragment slot="labels">
                {#each $dummyTabs as tab, i}
                    <TabLabel tabnum={i + 1}>{tab.tabTitle}</TabLabel>
                {/each}
            </svelte:fragment>
            <svelte:fragment slot="contents">
                {#each $dummyTabs as tab, i}
                    <TabContent tabnum={i + 1}>
                        <div class="info-bar">
                            <Header type={HeaderTypeEnum.h1}>Architecture Title</Header>
                            <br />
                            <Button type={ButtonTypeEnum.primary} size={ButtonSizeEnum.medium}>Save</Button>
                            <Button type={ButtonTypeEnum.primary} size={ButtonSizeEnum.medium} on:click={() => closeTab(tab.tabID)}
                                >Close</Button
                            >
                        </div>

                        <div class="DnD">
                            <SvelteFlowProvider>
                                <DnDProvider>
                                    <Flow {onSave} nodes={architectureNodes} edges={architectureEdges} />
                                </DnDProvider>
                            </SvelteFlowProvider>
                        </div>
                    </TabContent>
                {/each}
            </svelte:fragment>
        </Tabs>
    </main>
</div>

<style>
    .wrapper {
        margin: 0 auto;
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-columns: 12% 88%;
        /* grid-gap: 10px; */
        grid-template-rows: 100%;
    }
    main {
        background-color: white;
        padding: 1em 2em;
    }
</style>
