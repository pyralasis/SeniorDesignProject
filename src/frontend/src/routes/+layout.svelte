<script lang="ts">
    import { page } from '$app/state';
    import NavigationHeader from '$lib/components/Navigation/NavigationHeader.svelte';
</script>

<div class="layout">
    {#if page.data.hasHeader}
        <NavigationHeader />
    {/if}
    <slot></slot>
</div>

<style lang="scss">
    .layout {
        display: flex;
        flex-direction: column;
        height: 100%;
        box-sizing: border-box;
        width: auto;
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
        background-color: #111111;
        scrollbar-color: #111 #fff;
    }
</style>
