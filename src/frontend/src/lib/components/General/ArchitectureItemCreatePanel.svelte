<script lang="ts">
    import { Button, ButtonSizeEnum, ButtonTypeEnum, Flyout, Header, HeaderTypeEnum } from "kiwi-nl";
    
    let createFlyout: any;
</script>

<div class="panel">
    <div class="panel__header">
        <Header type={HeaderTypeEnum.h4}>Create New Architecture</Header>
    </div>

    <div class="panel__buttons">
        <Button type={ButtonTypeEnum.primary} size={ButtonSizeEnum.large} on:click={() => createFlyout.toggle()}>
            Create
        </Button>
    </div>
</div>

<Flyout bind:this={createFlyout}>
    <div slot="flyout-body" class="flyout-body">
    </div>
    <div slot="flyout-footer" class="flyout-actions">
        <Button type={ButtonTypeEnum.secondary}>Cancel</Button><Button>Save</Button>
    </div>
</Flyout>

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