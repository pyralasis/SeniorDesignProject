<script>
    import ArchitectureItemCreatePanel from "$lib/components/General/ArchitectureItemCreatePanel.svelte";
    import ArchitectureItemPanel from "$lib/components/General/ArchitectureItemPanel.svelte";
    import NavBar from "$lib/components/General/NavBar.svelte";
    import { architectureStore } from "$lib/stores/ArchitectureStore";
    import { Header } from "kiwi-nl";
    import { onMount } from "svelte";

    onMount(async () => {
        await architectureStore.getAvailableArchitectures();
	});
</script>

<div class="wrapper">
    <div class="nav-bar">
        <NavBar></NavBar>
    </div>
    <main class="main">
        <div class="main__header">
            <Header>Select Architecture</Header>
        </div>
        <div class="main__panels">
            <ArchitectureItemCreatePanel></ArchitectureItemCreatePanel>
            {#each $architectureStore.architectureIds as id}
            <ArchitectureItemPanel title="{id}" id={id}></ArchitectureItemPanel>
            {/each} 
        </div>
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
        &__header{
            display: flex;
            justify-content: center;
            padding: 50px;
        }
        &__panels{
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            max-height: 90%;
        }
        
    }
</style>
