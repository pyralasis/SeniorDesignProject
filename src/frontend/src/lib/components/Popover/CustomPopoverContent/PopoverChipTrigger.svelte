<script>
	import { getContext } from 'svelte';
	import PopoverTrigger from '../PopoverTrigger.svelte';
	import Text from '../../Text/Text.svelte';
	const popoverStore = getContext('popoverStore');

	export let label = 'Chip';

	let rotateDegrees = 0;
	$: rotateDegrees = $popoverStore?.isOpen ? 0 : 180;
</script>

<PopoverTrigger>
	<div slot="custom-trigger" class="popover-chip-trigger">
		<div class="popover-chip-trigger-label">
			{#if $popoverStore.selectedItems.length > 0}
				<Text type="light">
					{$popoverStore.selectedItems[0].label}
				</Text>
				{#if $popoverStore.selectedItems.length > 1}
					<Text type="light" size="small">
						+{$popoverStore.selectedItems.length - 1}
					</Text>
				{/if}
			{:else}
				<Text type="light">{label}</Text>
			{/if}
		</div>
		<div class="popover-chevron">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
				style="transform: rotate({rotateDegrees}deg); transition: transform 0.3s ease;"
			>
				<polyline points="6 9 12 15 18 9"></polyline>
			</svg>
		</div>
	</div>
</PopoverTrigger>

<style>
	.popover-chip-trigger {
		display: flex;
		width: 120px;
		padding: 6px 10px;
		justify-content: space-between;
		align-items: center;
		border-radius: 8px;
		border: 1px solid #adadad;
	}

	.popover-chip-trigger:hover {
		background-color: var(--color-surface-dark);
	}

	.popover-chip-trigger-label {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.popover-chevron {
		height: 24px;
		width: 24px;
		transition: transform 0.3s ease;
		color: #787878;
	}
</style>
