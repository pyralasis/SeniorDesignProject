<script lang="ts">
    import { ButtonSizeEnum, ButtonTypeEnum, Button } from 'kiwi-nl';

    import { goto } from '$app/navigation';
</script>

<nav>
    <Button
        type={ButtonTypeEnum.secondary}
        size={ButtonSizeEnum.large}
        on:click={() => {
            goto('/select-architecture');
        }}
    >
        Architectures
    </Button>
    <hr />
    <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.large}>Pipelines</Button>
    <hr />
    <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.large}>Models</Button>
    <hr />
    <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.large}>User Docs</Button>
    <hr />
    <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.large}>Options</Button>
</nav>

<style>
    nav {
        /* background-color: rgb(253, 217, 152); */
        background-color: white;
        border-right: solid black 1px;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 0.5em;
        /* grid-row: span 2; */
        height: 100%;
    }

    hr {
        display: block;
        position: relative;
        padding: 0;
        margin: 8px auto;
        height: 0;
        width: 100%;
        max-height: 0;
        font-size: 1px;
        line-height: 0;
        clear: both;
        border: none;
        border-top: 1px solid #aaaaaa;
    }
</style>
