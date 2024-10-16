<script>
	import { createEventDispatcher, getContext } from 'svelte';
	import { createToastStore } from './ToastStore.js';
	import { fly, fade, slide } from 'svelte/transition';
	import Button from '../Button/Button.svelte';

	export let type = 'success';
	export let duration = 5000;
	export let title = '';
	export let message = '';
	export let position = 'bottom-center';

	const dispatch = createEventDispatcher();
	const toastStore = createToastStore();

	export function addToast() {
		let toast = {
			id: Math.random().toString(36),
			type,
			title,
			message
		};
		toastStore.add(toast);
		dispatch('toastAdded', toast);
		setTimeout(() => {
			toastStore.remove(toast.id);
		}, duration);
	}
</script>

<div
	class="toast-group"
	class:top-right={position === 'top-right'}
	class:top-left={position === 'top-left'}
	class:bottom-right={position === 'bottom-right'}
	class:bottom-left={position === 'bottom-left'}
	class:bottom-center={position === 'bottom-center'}
	class:top-center={position === 'top-center'}
>
	{#each $toastStore as toast}
		<div
			class="toast"
			in:slide={{ y: position.includes('top') ? -40 : 40, duration: 300 }}
			out:slide={{ y: position.includes('top') ? -40 : 40, duration: 300 }}
			class:success={toast.type === 'success'}
			class:error={toast.type === 'error'}
			class:warning={toast.type === 'warning'}
			class:info={toast.type === 'info'}
		>
			<div class="left">
				<div class="toast-icon">
					{#if toast.type === 'success'}
						<svg
							width="24"
							height="24"
							viewBox="0 0 24 24"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M12 0C5.384 0 0 5.384 0 12C0 18.616 5.384 24 12 24C18.616 24 24 18.616 24 12C24 5.384 18.616 0 12 0ZM12 22.9333C5.97067 22.9333 1.06667 18.0293 1.06667 12C1.06667 5.97067 5.97067 1.06667 12 1.06667C18.0293 1.06667 22.9333 5.97067 22.9333 12C22.9333 18.0293 18.0293 22.9333 12 22.9333ZM17.976 7.89067C18.184 8.09867 18.184 8.43733 17.976 8.64533L10.5093 16.112C10.4053 16.2133 10.2693 16.2667 10.1333 16.2667C9.99733 16.2667 9.86133 16.2133 9.75733 16.1093L6.024 12.376C5.816 12.168 5.816 11.8293 6.024 11.6213C6.232 11.4133 6.57067 11.4133 6.77867 11.6213L10.1333 14.9787L17.224 7.888C17.432 7.68 17.768 7.68 17.976 7.89067Z"
								fill="white"
							/>
						</svg>
					{/if}
					{#if toast.type === 'error'}
						<svg
							width="24"
							height="24"
							viewBox="0 0 384 384"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M113.067 270.933C117.333 275.2 121.6 277.333 128 277.333C134.4 277.333 138.667 275.2 142.933 270.933L192 221.867L241.067 270.933C245.333 275.2 251.733 277.333 256 277.333C260.267 277.333 266.667 275.2 270.933 270.933C279.467 262.4 279.467 249.6 270.933 241.067L221.867 192L270.933 142.933C279.467 134.4 279.467 121.6 270.933 113.067C262.4 104.533 249.6 104.533 241.067 113.067L192 162.133L142.933 113.067C134.4 104.533 121.6 104.533 113.067 113.067C104.533 121.6 104.533 134.4 113.067 142.933L162.133 192L113.067 241.067C104.533 249.6 104.533 262.4 113.067 270.933Z"
								fill="white"
							/>
							<path
								d="M192 384C298.667 384 384 298.667 384 192C384 85.3333 298.667 0 192 0C85.3333 0 0 85.3333 0 192C0 298.667 85.3333 384 192 384ZM192 42.6667C275.2 42.6667 341.333 108.8 341.333 192C341.333 275.2 275.2 341.333 192 341.333C108.8 341.333 42.6667 275.2 42.6667 192C42.6667 108.8 108.8 42.6667 192 42.6667Z"
								fill="white"
							/>
						</svg>
					{/if}
					{#if toast.type === 'warning'}
						<svg
							width="24"
							height="21"
							viewBox="0 0 24 21"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M12 0L0 20.8H24L12 0ZM12 3.2016L21.2296 19.2H2.7704L12 3.2016Z"
								fill="white"
							/>
							<path d="M11.2 8.80005V10.4L11.6 14.4H12.4L12.8 10.4V8.80005H11.2Z" fill="white" />
							<path
								d="M12 16.8C12.4418 16.8 12.8 16.4418 12.8 16C12.8 15.5581 12.4418 15.2 12 15.2C11.5581 15.2 11.2 15.5581 11.2 16C11.2 16.4418 11.5581 16.8 12 16.8Z"
								fill="white"
							/>
						</svg>
					{/if}
					{#if toast.type === 'info'}
						<svg
							width="25"
							height="25"
							viewBox="0 0 25 25"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M12.6666 0.666626C10.2932 0.666626 7.97312 1.37041 5.99973 2.68899C4.02634 4.00757 2.48827 5.88171 1.58002 8.07442C0.671764 10.2671 0.434124 12.6799 0.897147 15.0077C1.36017 17.3355 2.50306 19.4737 4.18129 21.1519C5.85952 22.8301 7.99771 23.973 10.3255 24.436C12.6533 24.8991 15.0661 24.6614 17.2588 23.7532C19.4515 22.8449 21.3256 21.3069 22.6442 19.3335C23.9628 17.3601 24.6666 15.04 24.6666 12.6666C24.6666 11.0908 24.3562 9.53033 23.7531 8.07442C23.1501 6.61852 22.2662 5.29565 21.1518 4.18134C20.0375 3.06704 18.7147 2.18313 17.2588 1.58007C15.8029 0.977015 14.2424 0.666626 12.6666 0.666626ZM12.6666 22.2666C10.7679 22.2666 8.91181 21.7036 7.33309 20.6487C5.75438 19.5939 4.52393 18.0946 3.79733 16.3404C3.07073 14.5862 2.88061 12.656 3.25103 10.7938C3.62145 8.93154 4.53576 7.22098 5.87834 5.8784C7.22093 4.53582 8.93148 3.62151 10.7937 3.25109C12.6559 2.88067 14.5862 3.07078 16.3403 3.79738C18.0945 4.52398 19.5938 5.75444 20.6487 7.33315C21.7035 8.91186 22.2666 10.7679 22.2666 12.6666C22.2666 15.2127 21.2551 17.6545 19.4548 19.4548C17.6544 21.2552 15.2126 22.2666 12.6666 22.2666Z"
								fill="white"
							/>
							<path
								d="M12.6666 9.06663C13.3293 9.06663 13.8666 8.52937 13.8666 7.86663C13.8666 7.20388 13.3293 6.66663 12.6666 6.66663C12.0038 6.66663 11.4666 7.20388 11.4666 7.86663C11.4666 8.52937 12.0038 9.06663 12.6666 9.06663Z"
								fill="white"
							/>
							<path
								d="M12.6666 10.2666C12.3483 10.2666 12.0431 10.393 11.818 10.6181C11.593 10.8431 11.4666 11.1483 11.4666 11.4666V17.4666C11.4666 17.7849 11.593 18.0901 11.818 18.3151C12.0431 18.5402 12.3483 18.6666 12.6666 18.6666C12.9848 18.6666 13.29 18.5402 13.5151 18.3151C13.7401 18.0901 13.8666 17.7849 13.8666 17.4666V11.4666C13.8666 11.1483 13.7401 10.8431 13.5151 10.6181C13.29 10.393 12.9848 10.2666 12.6666 10.2666Z"
								fill="white"
							/>
						</svg>
					{/if}
				</div>
			</div>
			<div class="right">
				<div class="header">
					<div class="toast-title">{toast.title}</div>
					<Button size="sm" type="empty-white" on:click={() => toastStore.remove(toast.id)}
						><svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							width="18"
							height="18"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M6 18L18 6M6 6l12 12"
							></path>
						</svg>
					</Button>
				</div>
				<div class="toast-message">{toast.message}</div>
			</div>
		</div>
	{/each}
</div>

<style>
	@import '../../../variables.css';

	.toast-group {
		position: fixed;
		display: flex;
		flex-direction: column;
		padding: 16px;
		z-index: 10000;
	}

	.top-right {
		top: 0;
		right: 16px;
	}

	.top-left {
		top: 0;
		left: 16px;
	}

	.bottom-right {
		bottom: 0;
		right: 16px;
	}

	.bottom-left {
		bottom: 0;
		left: 16px;
	}

	.bottom-center {
		bottom: 0;
		left: calc(50% - 175px);
	}

	.top-center {
		top: 0;
		left: calc(50% - 175px);
	}

	.toast {
		width: 350px;
		display: flex;
		gap: 4px;
		padding: 8px;
		margin: 4px 0;
		border-radius: 8px;
		background-color: var(--color-surface);
		box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
		transform-origin: 50% 50% 0px;
		color: white;
		box-sizing: border-box;
	}

	.right {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.left {
		display: flex;
		justify-content: center;
		align-items: center;
		box-sizing: border-box;
		padding: 0 8px;
	}

	.toast-icon {
		width: 24px;
		height: 24px;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.success {
		background-color: var(--color-green);
	}

	.error {
		background-color: var(--color-red);
	}

	.warning {
		background-color: var(--color-orange);
		color: black;
	}

	.info {
		background-color: var(--color-navy);
	}

	.toast-title {
		font-weight: 600;
	}

	.toast-message {
		font-size: 0.8rem;
	}
</style>
