<script lang="ts">
    import { goto } from "$app/navigation";
    import { Button, ButtonSizeEnum, ButtonTypeEnum, Flyout, Header, HeaderTypeEnum, TextInput } from "kiwi-nl";
    
    let createFlyout: any;
    let architectureTitle: string;
    
    //needs to validate any fields and display some kind of marker for invalid fields
    function createArchitecture(){
        if(architectureTitle.length > 0){
            goto('/edit-architecture');
        }
    }
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
    
    <div style="position: absolute;">
        <Flyout bind:this={createFlyout} header="New Architecture" subheader="">
            <div slot="flyout-body" class="flyout-body">
                <TextInput label="Title" bind:value={architectureTitle}></TextInput>
            </div>
            <div slot="flyout-footer" class="flyout-actions">
                <Button type={ButtonTypeEnum.secondary}>Cancel</Button>
                <Button on:click={createArchitecture}>Save</Button>
            </div>
        </Flyout>
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
            max-width: 100%;
        }
        &__buttons{
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 10px;
        }
    }
</style>