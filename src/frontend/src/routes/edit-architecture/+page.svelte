<script lang="ts">
    import DnDProvider from '$lib/components/DnDProvider.svelte';
    import NodeEditor from '$lib/components/NodeEditor/NodeEditor.svelte';
    import NavBar from '$lib/components/General/NavBar.svelte';
    import { SvelteFlowProvider } from '@xyflow/svelte';
    import { Header } from 'kiwi-nl';

    //Need to set the loaded architecture and apply it to the flow.
    //Should this be done by passing the architecture id to this page
    //then set the loaded architecture, or should the select architecture
    //page set it?
</script>

<div class="wrapper">
    <div class="nav-bar">
        <NavBar></NavBar>
    </div>
    <main class="main">
        <div class="main__header">
            <Header>Editing Architecture: TITLE</Header>
        </div>

        <SvelteFlowProvider>
            <DnDProvider>
                <NodeEditor />
            </DnDProvider>
        </SvelteFlowProvider>
    </main>
</div>

<style lang="scss">
    .wrapper {
        margin: 0 auto;
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-columns: 12% 88%;
        /* grid-gap: 10px; */
        grid-template-rows: 100%;
    }
    .main {
        background-color: white;
        padding: 1em 2em;
        display: flex;
        flex-direction: column;
        justify-content: center;
        max-height: 100vh;
        overflow-y: scroll;
        &__header {
            display: flex;
            justify-content: center;
            padding: 50px;
        }
    }
</style>
