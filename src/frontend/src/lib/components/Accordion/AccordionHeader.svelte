<script>
	import { getContext } from 'svelte';

	const accordionStore = getContext('accordionStore');
	let rotateDegrees = 0;

	$: rotateDegrees = $accordionStore?.isOpen ? 180 : 0;

	function handleClick() {
		accordionStore.toggle();
	}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
	class="accordion-header"
	class:accordion-header-open={$accordionStore?.isOpen}
	on:click={handleClick}
>
	<div class="accordion-title">
		<slot></slot>
	</div>
	<div class="accordion-chevron">
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

<style>
	.accordion-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--size-sm);
		cursor: pointer;
	}

	.accordion-header:hover {
		background-color: var(--color-surface-dark);
	}

	.accordion-header-open {
		box-shadow: 0px 2px 2px 0px rgba(0, 0, 0, 0.1);
	}

	.accordion-title {
		font-size: 16px;
		font-weight: 600;
	}

	.accordion-chevron {
		height: 24px;
		width: 24px;
		transition: transform 0.3s ease;
		color: #787878;
	}
</style>
