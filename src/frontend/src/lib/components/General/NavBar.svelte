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
        InputSeries,
    } from "kiwi-nl";
    import ArchitectureMenuItem from "$lib/components/General/ArchitectureMenuItem.svelte";
    import {
        dummyTabs,
        type dummyData,
    } from "../../../routes/general-layout/+page.svelte";
    import { goto } from "$app/navigation";
    let editArchitectureFlyout: any;
    let editPipelineFlyout: any;
    let editModelFlyout: any;

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
        console.log(mytabs);
        console.log($dummyTabs);
    }
</script>

<nav>
    <Button 
        type={ButtonTypeEnum.secondary} 
        size={ButtonSizeEnum.large} 
        on:click={() => {goto('/select-architecture')}}
    >
        Architectures
    </Button>
    <hr />
    <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.large}>
        Pipelines
    </Button>
    <hr />
    <Button
        type={ButtonTypeEnum.secondary}
        size={ButtonSizeEnum.large}
        >Models</Button
    >
    <hr />
    <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.large}
        >User Docs</Button
    >
    <hr />
    <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.large}
        >Options</Button
    >
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
