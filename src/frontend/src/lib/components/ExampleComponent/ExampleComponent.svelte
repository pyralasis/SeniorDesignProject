<script>
	import { mousePosition } from '$lib/utilities/stores.js';

	let divy;
	let divyCursorPos = { x: 0, y: 0 };
	let divyPos = { top: 100, left: 350 };
	let draggingDivy = false;

	$: if (draggingDivy) {
		divyPos.top = $mousePosition.y - divyCursorPos.y;
		divyPos.left = $mousePosition.x - divyCursorPos.x;
	}

	function handleMouseDown(event) {
		draggingDivy = true;
		divyCursorPos.x = event.offsetX;
		divyCursorPos.y = event.offsetY;
	}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
	class="divy"
	class:dragging={draggingDivy}
	bind:this={divy}
	on:mousedown={handleMouseDown}
	on:mouseup={() => (draggingDivy = false)}
	style={`top: ${divyPos.top}px; left:${divyPos.left}px`}
>
	<slot />
</div>

<style>
	@import '../../../variables.css';
	.divy {
		position: absolute;
		background-color: var(--color-navy);
		cursor: grab;
		border-radius: var(--border-radius-md);
		display: flex;
		flex-direction: column;
		width: fit-content;
		height: fit-content;
		padding: var(--size-lg);
	}

	.divy:hover {
		background-color: var(--color-red);
	}
	.dragging:hover {
		background-color: var(--color-green);
		cursor: grabbing;
	}
</style>
