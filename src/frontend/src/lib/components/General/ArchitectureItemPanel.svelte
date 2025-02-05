<script lang="ts">
    import { goto } from "$app/navigation";
    import type { ArchitectureId } from "$lib/types/architecture";
    import { Button, ButtonSizeEnum, ButtonTypeEnum, Header, HeaderTypeEnum } from "kiwi-nl";
    
    export let title: string;
    export let id: ArchitectureId;
</script>

<div class="panel">
    <div class="panel__header">
        <Header type={HeaderTypeEnum.h4}>{title}</Header>
    </div>

    <div class="panel__buttons">
        <Button type={ButtonTypeEnum.primary} size={ButtonSizeEnum.large} on:click={() => {goto("/edit-architecture?id=" + id)}}>
            Edit
        </Button>
        <Button type={ButtonTypeEnum.primary} size={ButtonSizeEnum.large}>
            Delete
        </Button>
    </div>
</div>

<style lang="scss">
    .panel{
        width: 20%;
        height: 20%;
        max-width: 20%;
        max-height: 20%;
        border: black solid 1px;
        border-radius: 10px;
        justify-content: center;
        box-shadow: 1px 1px 1px black;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 10px;

        &__header{
            display: flex;
            justify-content: center;
        }
        &__buttons{
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 10px;
        }
    }
</style>