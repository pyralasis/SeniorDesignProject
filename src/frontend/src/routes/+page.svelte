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
        PopoverSingleSelectContent,
    } from '$lib/components';
    import TextInput from '$lib/components/TextInput/TextInput.svelte';

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
            <AccordionHeader slot="header"><span>This is an Accordion</span></AccordionHeader>
            <AccordionBody slot="body"
                ><span>This is the body of the Accordion</span>
                <div class="accordion-img">
                    <img class="shrek" src="https://i.pinimg.com/736x/a9/ef/a9/a9efa9e0d9a868bf182a920938c0c094.jpg" alt="shrek" />
                </div>
            </AccordionBody>
        </Accordion>
    </div>
    <div class="buttons">
        <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.medium} on:click={() => flyoutElement.toggle()}>I'm a Button</Button>
        <Button type={ButtonTypeEnum.primary} size={ButtonSizeEnum.medium} on:click={() => flyoutElement.toggle()}>I'm a Button</Button>
    </div>
    <Checkbox label="Checkbox" on:change={handleChange} />
    <Flyout bind:this={flyoutElement}>
        <div slot="flyout-body">
            <img class="shrek" src="https://i.pinimg.com/736x/82/f2/e5/82f2e56c0bb7958a3806cb134f999bde.jpg" alt="shrek" />Shrek says hi
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
    <!-- <Tabs activeTab="1">
        <svelte:fragment slot="labels">
            <TabLabel tabnum="1">Display Elements</TabLabel>
            <TabLabel tabnum="2">Interactable Elements</TabLabel>
            <TabLabel tabnum="3">Store Example</TabLabel>
        </svelte:fragment>
        <svelte:fragment slot="contents">
            <TabContent tabnum="1">
                <StandardContentLayout>
                    <Header>This is an H1 Header</Header>
                    <Header type="h2">This is an H2 Header</Header>
                    <Header type="subheader">This is a Subheader</Header>
                    <Text
                        >This is a text element. There isnt much to it yet, but this applies default color, font weight, and font styles.
                    </Text>
                    <div class="tags">
                        <Tag color="green">Green Tag</Tag>
                        <Tag color="red">Red Tag</Tag>
                        <Tag color="navy">Navy Tag</Tag>
                        <Tag color="gray">Gray Tag</Tag>
                        <Tag color="orange">Orange Tag</Tag>
                        <Tag size="sm">Small Tag</Tag>
                        <Tag size="lg">Large Tag</Tag>
                    </div>
                </StandardContentLayout>
            </TabContent>
            <TabContent tabnum="2">
                <StandardContentLayout>
                    <TextInput label="This is an Input" required on:change={handleChange} />
                    <div class="buttons">
                        <Button on:click={handleClick}>This is a Default Button</Button>
                        <Button type="inverse" on:click={toast?.addToast()}>This is an Inverse Button</Button>
                        <Button type="empty">This is an Empty Button</Button>
                    </div>
                    <Text>Click the Default Button to see a flyout</Text>
                    <Text>Click the Inverse Button to see a Toast</Text>
                    <div class="checkboxes">
                        <Checkbox label="Checkbox" required on:change={handleChange} />
                    </div>
                    <div class="accordion">
                        <Accordion>
                            <AccordionHeader slot="header"><Text type="light">This is an Accordion</Text></AccordionHeader>
                            <AccordionBody slot="body"
                                ><Text>This is the body of the Accordion</Text>
                                <div class="accordion-img">
                                    <img
                                        class="shrek"
                                        src="https://i.pinimg.com/736x/a9/ef/a9/a9efa9e0d9a868bf182a920938c0c094.jpg"
                                        alt="shrek"
                                    />
                                </div></AccordionBody
                            >
                        </Accordion>
                    </div>
                    <Popover on:popoverItemsChanged={handlePopoverItemsChanged}>
                        <PopoverChipTrigger slot="trigger" />
                        <PopoverMultiSelectContent slot="content" items={exampleItems} />
                    </Popover>
                    <div>
                        <Text>Selected Items:</Text>
                        {#each popoverItems as item}
                            <Tag>{item.label}</Tag>
                        {/each}
                    </div>
                    <Toast
                        title="This is a toast"
                        message="Use this to show temporary info, like a task was completed, or failed."
                        bind:this={toast}
                    />
                </StandardContentLayout>
            </TabContent>
            <TabContent tabnum="3">
                <div class="outfit-example">
                    {#each $outfitStore as outfit}
                        <Header type="h2">{outfit.name}</Header>

                        <div class="img-wrapper">
                            <img class="outfit-top" src={clothesStore.getClothingItemById(outfit.topid).img} alt="top" />
                            <img class="outfit-bottom" src={clothesStore.getClothingItemById(outfit.bottomid).img} alt="bottom" />
                        </div>
                        <div class="outfit-footer">
                            <Button on:click={makeOutfitClean(outfit.id)}>Make Outfit Clean</Button>
                            {#if clothesStore.isClothingItemClean(outfit.topid) || clothesStore.isClothingItemClean(outfit.bottomid)}
                                <Tag color="green">Clean</Tag>
                            {:else}
                                <Tag color="red">Dirty</Tag>
                            {/if}
                            <Button on:click={makeOutfitDirty(outfit.id)}>Make Outfit Dirty</Button>
                        </div>
                    {/each}
                </div>
            </TabContent>
        </svelte:fragment>
    </Tabs>

    <Flyout id="flyout1" header="This is a Flyout">
        <div slot="flyout-body">
            <img class="shrek" src="https://i.pinimg.com/736x/82/f2/e5/82f2e56c0bb7958a3806cb134f999bde.jpg" alt="shrek" />Shrek says hi
        </div>
        <div slot="flyout-footer" class="flyout-actions">
            <Button type="inverse">Cancel</Button><Button>Save</Button>
        </div>
    </Flyout> -->
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

    .accordion-img {
        width: 80%;
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
</style>
