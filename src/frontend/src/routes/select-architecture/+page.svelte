<script>
    import ArchitectureItemCreatePanel from '$lib/components/General/ArchitectureItemCreatePanel.svelte';
    import ArchitectureMenuItem from '$lib/components/General/ArchitectureMenuItem.svelte';
</script>

<div class="main__panels">
    <ArchitectureItemCreatePanel></ArchitectureItemCreatePanel>
    {#each { length: 15 }, i}
        <ArchitectureMenuItem title="TEST"></ArchitectureMenuItem>
    {/each}
</div>

<style lang="scss">
    div {
        display: flex;
        flex-direction: column;
        justify-content: center;
        overflow-y: hidden;
    }
    .main {
        &__header {
            display: flex;
            justify-content: center;
            padding: 50px;
        }
        &__panels {
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: center;
            max-width: 1000px;
            margin: 0 auto;
            width: 100%;
            overflow-y: scroll;
            padding: 0 32px;
        }
    }
</style>
