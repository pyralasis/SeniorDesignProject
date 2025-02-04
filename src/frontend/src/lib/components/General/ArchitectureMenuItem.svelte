<script lang="ts">
    import { SoundUtility } from '$lib/utilities/sound.utility';

    export let title;
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="architecture-menu-item" on:mouseenter={() => SoundUtility.playClick2()}>
    <div class="architecture-menu-item-title">{title}</div>
</div>

<style>
    .architecture-menu-item {
        width: 100%;
        height: 50px;
        background-color: #000;
        border: 1px solid #fff;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;

        &:hover {
            transform: scale(1.05);
            transition: transform 0.1s ease-in-out;
        }
    }
</style>
