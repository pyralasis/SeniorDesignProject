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
    } from 'kiwi-nl';

    // function handleChange(event) {
    // 	console.log(event.detail.value);
    // }

    // function handleClick() {
    // 	toggle('flyout1');
    // }

    let exampleItems: PopoverItem[] = [
        { label: 'Item 1', value: 'item1' },
        { label: 'Item 2', value: 'item2' },
        { label: 'Item 3', value: 'item3' },
        { label: 'Item 4', value: 'item4' },
    ];

    let popoverItems: PopoverItem[] = [];
    // let toast;

    function handlePopoverItemsChanged(event: CustomEvent): void {
        popoverItems = event.detail.selectedItems;
    }

    // function makeOutfitDirty(outfitid) {
    // 	outfitStore.makeOutfitDirty(outfitid);
    // }

    // function makeOutfitClean(outfitid) {
    // 	outfitStore.makeOutfitClean(outfitid);
    // }
    function handleChange(event: CustomEvent) {
        console.log(event.detail.value);
    }
    let flyoutElement: any;
</script>

<div class="components">
    <div class="accordion">
        <Accordion>
            <AccordionHeader slot="header"><Text>This is an Accordion</Text></AccordionHeader>
            <AccordionBody slot="body"><Text>This is the body of the Accordion</Text></AccordionBody>
        </Accordion>
    </div>
    <div class="buttons">
        <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.medium} on:click={() => flyoutElement.toggle()}>I'm a Button</Button>
        <Button type={ButtonTypeEnum.primary} size={ButtonSizeEnum.medium}>I'm a Button</Button>
        <Button type={ButtonTypeEnum.tertiary} size={ButtonSizeEnum.medium}>I'm a Button</Button>
    </div>
    <Checkbox label="Checkbox" on:change={handleChange} />
    <Flyout bind:this={flyoutElement}>
        <div slot="flyout-body" class="flyout-body">
            <Tabs activeTab={1}>
                <svelte:fragment slot="labels">
                    <TabLabel tabnum={1}>Tab 1</TabLabel>
                    <TabLabel tabnum={2}>Tab 2</TabLabel>
                </svelte:fragment>
                <svelte:fragment slot="contents">
                    <TabContent tabnum={1}>
                        <img
                            class="orange"
                            src="https://plus.unsplash.com/premium_photo-1675237625695-710b9a6c3f2e?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8b3JhbmdlfGVufDB8fDB8fHww"
                            alt="orange"
                        />
                    </TabContent>
                    <TabContent tabnum={2}>
                        <div class="flyout-body">
                            <TextInput label="Input In Flyout" />
                            <Popover on:popoverItemsChanged={handlePopoverItemsChanged} items={exampleItems}>
                                <PopoverChipTrigger slot="trigger" label="Multi" />
                                <PopoverMultiSelectContent slot="content" />
                            </Popover>
                        </div>
                    </TabContent>
                </svelte:fragment>
            </Tabs>
        </div>
        <div slot="flyout-footer" class="flyout-actions">
            <Button type={ButtonTypeEnum.secondary}>Cancel</Button><Button>Save</Button>
        </div>
    </Flyout>
    <Header type={HeaderTypeEnum.h1}>This is an h1 Header</Header>
    <Header type={HeaderTypeEnum.h2}>This is an h2 Header</Header>
    <Header type={HeaderTypeEnum.h3}>This is an h3 Header</Header>
    <Header type={HeaderTypeEnum.h4}>This is an h4 Header</Header>
    <Header type={HeaderTypeEnum.subheader}>This is a Subheader</Header>

    <div class="popovers">
        <Popover on:popoverItemsChanged={handlePopoverItemsChanged} items={exampleItems}>
            <PopoverChipTrigger slot="trigger" label="Multi" />
            <PopoverMultiSelectContent slot="content" />
        </Popover>
        <Popover on:popoverItemsChanged={handlePopoverItemsChanged} items={exampleItems}>
            <PopoverChipTrigger slot="trigger" label="Single" />
            <PopoverSingleSelectContent slot="content" />
        </Popover>
    </div>
    <Tabs activeTab={1}>
        <svelte:fragment slot="labels">
            <TabLabel tabnum={1}>Tab 1</TabLabel>
            <TabLabel tabnum={2}>Tab 2</TabLabel>
        </svelte:fragment>
        <svelte:fragment slot="contents">
            <TabContent tabnum={1}><Text>Tab Content 1</Text></TabContent>
            <TabContent tabnum={2}><Text>Tab Content 2</Text></TabContent>
        </svelte:fragment>
    </Tabs>
    <div class="tags">
        <Tag color={TagColorEnum.green}>Tag</Tag>
        <Tag color={TagColorEnum.red}>Tag</Tag>
        <Tag color={TagColorEnum.blue}>Tag</Tag>
        <Tag color={TagColorEnum.gray}>Tag</Tag>
        <Tag color={TagColorEnum.orange}>Tag</Tag>
        <Tag color={TagColorEnum.purple}>Tag</Tag>
        <Tag color={TagColorEnum.yellow}>Tag</Tag>
    </div>
    <Text>This is the text component</Text>
    <TextInput label="This is an Input" on:change={handleChange} />
    <InputSeries label="This is an Input Series" on:change={handleChange} />
</div>

<style>
    .components {
        display: flex;
        flex-direction: column;
        width: auto;
        gap: 16px;
        padding: 30px;
        box-sizing: border-box;
    }

    .shrek {
        width: 100%;
    }

    .flyout-actions {
        display: flex;
        justify-content: flex-end;
        gap: 8px;
        width: 100%;
    }

    .accordion {
        width: 50%;
    }

    .tags {
        display: flex;
        gap: 8px;
    }

    .popovers {
        display: flex;
        gap: 16px;
        width: 100%;
        justify-content: center;
    }

    .buttons {
        display: flex;
        gap: 8px;
    }

    .flyout-body {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
</style>
