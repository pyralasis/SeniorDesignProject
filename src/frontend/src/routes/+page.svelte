<script>
	import Accordion from '$lib/components/Accordion/Accordion.svelte';
	import AccordionBody from '$lib/components/Accordion/AccordionBody.svelte';
	import AccordionHeader from '$lib/components/Accordion/AccordionHeader.svelte';
	import Button from '$lib/components/Button/Button.svelte';
	import Checkbox from '$lib/components/Checkbox/Checkbox.svelte';
	import Flyout from '$lib/components/Flyout/Flyout.svelte';
	import Header from '$lib/components/Header/Header.svelte';
	import Popover from '$lib/components/Popover/Popover.svelte';
	import Tag from '$lib/components/Tag/Tag.svelte';
	import Text from '$lib/components/Text/Text.svelte';
	import TextInput from '$lib/components/TextInput/TextInput.svelte';
	import PopoverMultiSelectContent from '$lib/components/Popover/CustomPopoverTrigger/PopoverMultiSelectContent.svelte';
	import { clothesStore, outfitStore, toggle } from '$lib/utilities/stores.js';
	import PopoverChipTrigger from '../../lib/components/Popover/CustomPopoverContent/PopoverChipTrigger.svelte';
	import Tabs from '$lib/components/Tabs/Tabs.svelte';
	import TabContent from '$lib/components/Tabs/TabContent.svelte';
	import TabLabel from '$lib/components/Tabs/TabLabel.svelte';
	import StandardContentLayout from '$lib/components/StandardContentLayout/StandardContentLayout.svelte';
	import Toast from '$lib/components/Toast/Toast.svelte';

	function handleChange(event) {
		console.log(event.detail.value);
	}

	function handleClick() {
		toggle('flyout1');
	}

	let exampleItems = [
		{ label: 'Item 1', value: 'item1' },
		{ label: 'Item 2', value: 'item2' },
		{ label: 'Item 3', value: 'item3' },
		{ label: 'Item 4', value: 'item4' }
	];

	let popoverItems = [];
	let toast;

	function handlePopoverItemsChanged(event) {
		popoverItems = event.detail.selectedItems;
	}

	function makeOutfitDirty(outfitid) {
		outfitStore.makeOutfitDirty(outfitid);
	}

	function makeOutfitClean(outfitid) {
		outfitStore.makeOutfitClean(outfitid);
	}
</script>

<div class="components">
	<Tabs activeTab="1">
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
						>This is a text element. There isnt much to it yet, but this applies default color, font
						weight, and font styles.
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
							<AccordionHeader slot="header"
								><Text type="light">This is an Accordion</Text></AccordionHeader
							>
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
							<img
								class="outfit-top"
								src={clothesStore.getClothingItemById(outfit.topid).img}
								alt="top"
							/>
							<img
								class="outfit-bottom"
								src={clothesStore.getClothingItemById(outfit.bottomid).img}
								alt="bottom"
							/>
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
			<img
				class="shrek"
				src="https://i.pinimg.com/736x/82/f2/e5/82f2e56c0bb7958a3806cb134f999bde.jpg"
				alt="shrek"
			/>Shrek says hi
		</div>
		<div slot="flyout-footer" class="flyout-actions">
			<Button type="inverse">Cancel</Button><Button>Save</Button>
		</div>
	</Flyout>
</div>

<style>
	.components {
		display: flex;
		flex-direction: column;
		width: 100%;
		gap: 16px;
	}

	.flyout-actions {
		display: flex;
		justify-content: flex-end;
		gap: 8px;
		width: 100%;
	}

	.shrek {
		width: 100%;
	}

	.buttons,
	.tags {
		display: flex;
		gap: 8px;
		align-items: center;
	}

	.accordion {
		width: 50%;
	}

	.accordion-img {
		width: 80%;
	}

	.outfit-example {
		display: flex;
		flex-direction: column;
		gap: 16px;
		align-items: center;
		justify-content: center;
		width: fit-content;
		border-radius: 8px;
		box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.1);
		padding: 16px;
	}

	.outfit-footer {
		display: flex;
		gap: 8px;
		align-items: center;
	}

	.img-wrapper {
		display: flex;
		gap: 8px;
	}

	.img-wrapper img {
		width: 100px;
		border-radius: 8px;
		border: 3px solid var(--color-edge);
		padding: 16px;
	}
</style>
