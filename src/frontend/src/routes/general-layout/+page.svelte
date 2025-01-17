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

    import { SvelteFlowProvider } from "@xyflow/svelte";
    import DnDProvider from "$lib/components/DnDProvider.svelte";

    import Flow from "$lib/components/Flow/Flow.svelte";
    import ArchitectureMenuItem from "$lib/components/General/ArchitectureMenuItem.svelte";
    let editArchitectureFlyout: any;
    let editPipelineFlyout: any;
    let editModelFlyout: any;
</script>

<div class="wrapper">
    <nav>
        <Button
            type={ButtonTypeEnum.secondary}
            size={ButtonSizeEnum.large}
            on:click={() => editArchitectureFlyout.toggle()}
            >Edit Architecture</Button
        >
        <hr />
        <Button
            type={ButtonTypeEnum.secondary}
            size={ButtonSizeEnum.large}
            on:click={() => editPipelineFlyout.toggle()}>Edit Pipeline</Button
        >
        <hr />
        <Button
            type={ButtonTypeEnum.secondary}
            size={ButtonSizeEnum.large}
            on:click={() => editModelFlyout.toggle()}>Edit Model</Button
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
    <main>
        <div class="info-bar">
            <Header type={HeaderTypeEnum.h1}>Architecture Title</Header>
            <br />
            <Button type={ButtonTypeEnum.primary} size={ButtonSizeEnum.medium}
                >Save</Button
            >
        </div>
        <div class="DnD">
            <SvelteFlowProvider>
                <DnDProvider>
                    <Flow />
                </DnDProvider>
            </SvelteFlowProvider>
        </div>
    </main>

    <Flyout
        bind:this={editArchitectureFlyout}
        header="Architectures"
        subheader="Select the Architecture You Wish to Edit"
    >
        <div slot="flyout-body" class="flyout-body">
            <ArchitectureMenuItem
                title="Architecture 1"
                description="Architecture Description"
            ></ArchitectureMenuItem>
            <ArchitectureMenuItem
                title="Architecture 2"
                description="Architecture Description"
            ></ArchitectureMenuItem>
            <Accordion>
                <AccordionHeader slot="header"
                    ><Header type={HeaderTypeEnum.h4}
                        >Create New Architecture</Header
                    >
                </AccordionHeader>
                <AccordionBody slot="body">
                    <Text>Title</Text>
                    <TextInput></TextInput>
                    <Text>Description</Text>
                    <TextInput></TextInput>
                    <Button
                        type={ButtonTypeEnum.secondary}
                        size={ButtonSizeEnum.small}>Create</Button
                    >
                </AccordionBody>
            </Accordion>
        </div>
    </Flyout>

    <Flyout
        bind:this={editPipelineFlyout}
        header="Pipelines"
        subheader="Select the Pipeline You Wish to Edit"
    >
        <div slot="flyout-body" class="flyout-body">
            <Accordion>
                <AccordionHeader slot="header"
                    ><Text>Pipeline 1</Text>
                </AccordionHeader>
                <AccordionBody slot="body">
                    <Text>Description of Pipeline 1</Text>
                    <br />
                    <Text>
                        Maybe a thumbnail of the Pipeline? Or a custom image?
                    </Text>
                    <Button
                        type={ButtonTypeEnum.secondary}
                        size={ButtonSizeEnum.small}>Edit</Button
                    >
                </AccordionBody>
            </Accordion>
            <Accordion>
                <AccordionHeader slot="header"
                    ><Text>Pipeline 2</Text>
                </AccordionHeader>
                <AccordionBody slot="body">
                    <Text>Description of Pipeline 2</Text>
                    <br />
                    <Text>
                        Maybe a thumbnail of the Pipeline? Or a custom image?
                    </Text>
                    <Button
                        type={ButtonTypeEnum.secondary}
                        size={ButtonSizeEnum.small}>Edit</Button
                    >
                </AccordionBody>
            </Accordion>
        </div>
    </Flyout>
</div>

<style>
    .wrapper {
        margin: 0 auto;
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-columns: 12% 88%;
        /* grid-gap: 10px; */
        grid-template-rows: 100%;
    }
    main {
        background-color: white;
        padding: 1em 2em;
    }
    nav {
        /* background-color: rgb(253, 217, 152); */
        background-color: white;
        border-right: solid black 1px;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 0.5em;
        /* grid-row: span 2; */
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
