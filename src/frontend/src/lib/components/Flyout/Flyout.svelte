<script>
	import { close, flyoutStore } from '$lib/utilities/stores.js';
	import Button from '../Button/Button.svelte';

	export let id;
	export let side = 'right';
	export let header = 'Header';
	export let subheader = 'Subheader';
	export let hidesbackground = true;

	let expanded = false;
	$: {
		$flyoutStore, (expanded = $flyoutStore.get(id) || false);
	}
</script>

<div class="flyout">
	<div class="flyout-content" class:expanded class:left={side === 'left'}>
		<div class="inner">
			<div class="header">
				<div class="close-button">
					<Button type="empty" on:click={() => close(id)}
						><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
							><path
								fill="currentColor"
								d="M6.4 19L5 17.6l5.6-5.6L5 6.4L6.4 5l5.6 5.6L17.6 5L19 6.4L13.4 12l5.6 5.6l-1.4 1.4l-5.6-5.6z"
							/></svg
						></Button
					>
				</div>
				<h2>{header}</h2>
				<h3>{subheader}</h3>
			</div>
			<div class="body">
				<slot name="flyout-body" />
			</div>
			<div class="footer">
				<slot name="flyout-footer" />
			</div>
		</div>
	</div>
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->

	<div class="overlay" class:hidesbackground class:expanded on:click={() => close(id)}></div>
</div>

<style>
	.flyout-content {
		position: fixed;
		top: 0;
		right: -500px;
		height: 100vh;
		width: 500px;
		z-index: 1500;
		transition: 0.2s ease;
	}

	.flyout-content.expanded {
		display: block;
		transform: translateX(-500px);
	}

	.flyout-content.left {
		left: 0;
	}

	.overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: transparent;
		z-index: 1499;
		display: none;
	}

	.overlay.expanded {
		display: block;
	}

	.overlay.hidesbackground {
		background-color: rgba(0, 0, 0, 0.5);
	}

	.inner {
		display: flex;
		flex-direction: column;
		height: 100%;
		background-color: var(--color-surface);
		padding: var(--size-md) var(--size-lg);
		gap: var(--size-md);
		box-sizing: border-box;
	}

	.close-button {
		display: flex;
		justify-content: flex-end;
	}

	.header {
		display: flex;
		flex-direction: column;
		gap: var(--size-xs);
	}

	h2 {
		margin: 0;
		color: var(--color-text);
		font-size: 240%;
	}

	h3 {
		margin: 0;
		color: var(--color-text-lighter);
	}

	.body {
		height: 100%;
	}

	.footer {
		display: flex;
		padding: var(--size-md) 0;
	}
</style>
