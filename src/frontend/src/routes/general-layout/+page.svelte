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
    let editArchitectureFlyout: any;
    let editPipelineFlyout: any;
    let editModelFlyout: any;
</script>

<div class="wrapper">
    <!-- <header>
            <Header type={HeaderTypeEnum.h1}>Velvit</Header>
    </header> -->
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
        <SvelteFlowProvider>
            <DnDProvider>
                <Flow />
            </DnDProvider>
        </SvelteFlowProvider>
    </main>
    <!-- <footer></footer> -->

    <Flyout
        bind:this={editArchitectureFlyout}
        header="Architectures"
        subheader="Select the Architecture You Wish to Edit"
    >
        <div slot="flyout-body" class="flyout-body">
            <Accordion>
                <AccordionHeader slot="header"
                    ><Text>Architecture 1</Text>
                </AccordionHeader>
                <AccordionBody slot="body">
                    <Text>Description of Architecture 1</Text>
                    <br />
                    <Text>
                        Maybe a thumbnail of the architecture? Or a custom
                        image?
                    </Text>
                    <Button
                        type={ButtonTypeEnum.secondary}
                        size={ButtonSizeEnum.small}>Edit</Button
                    >
                </AccordionBody>
            </Accordion>
            <Accordion>
                <AccordionHeader slot="header"
                    ><Text>Architecture 2</Text>
                </AccordionHeader>
                <AccordionBody slot="body">
                    <Text>Description of Architecture 2</Text>
                    <br />
                    <Text>
                        Maybe a thumbnail of the architecture? Or a custom
                        image?
                    </Text>
                    <Button
                        type={ButtonTypeEnum.secondary}
                        size={ButtonSizeEnum.small}>Edit</Button
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
        grid-template-columns: 10% 90%;
        /* grid-gap: 10px; */
        grid-template-rows: 100%;
    }
    header {
        grid-column: span 2;
        text-align: center;
        background-color: orange;
    }
    main {
        background-color: white;
        padding: 1em 2em;
    }
    nav {
        background-color: rgb(253, 217, 152);
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    footer {
        clear: both;
        text-align: center;
        grid-column: span 2;
        background-color: orange;
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
