<script lang="ts">
    import { createFlyoutStore } from './FlyoutStore';
    import Button from '../Button/Button.svelte';
    import { ButtonTypeEnum } from '../Button/types';
    import { type CustomFlyoutStore, type FlyoutSide, FlyoutSideEnum } from './types';

    // -----------------------
    // External Properties
    // -----------------------
    export let side: FlyoutSide = FlyoutSideEnum.right;
    export let header: string = 'Header';
    export let subheader: string = 'Subheader';
    export let hidebackground: boolean = true;

    // -----------------------
    // External Methods
    // -----------------------
    export function toggle() {
        private_store.toggle();
    }

    export function close() {
        private_store.close();
    }

    export function open() {
        private_store.expand();
    }

    // -----------------------
    // Internal Properties
    // -----------------------
    let private_store: CustomFlyoutStore = createFlyoutStore(false, hidebackground);
</script>

<div class="flyout">
    <div class="flyout__content" class:flyout__content--expanded={$private_store.open} class:left={side === 'left'}>
        <div class="flyout__inner">
            <div class="flyout__header">
                <div class="flyout__close-button">
                    <Button type={ButtonTypeEnum.secondary} on:click={() => private_store.close()}
                        ><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
                            ><path
                                fill="currentColor"
                                d="M6.4 19L5 17.6l5.6-5.6L5 6.4L6.4 5l5.6 5.6L17.6 5L19 6.4L13.4 12l5.6 5.6l-1.4 1.4l-5.6-5.6z"
                            /></svg
                        ></Button
                    >
                </div>
                <h2 class="flyout__main-header">{header}</h2>
                <h3 class="flyout__sub-header">{subheader}</h3>
            </div>
            <div class="flyout__body">
                <slot name="flyout-body" />
            </div>
            <div class="flyout__footer">
                <slot name="flyout-footer" />
            </div>
        </div>
    </div>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->

    <div
        class="flyout__overlay"
        class:flyout__overlay--expanded={$private_store.open}
        class:flyout__overlay--hidesbackground={$private_store.hideBackground}
        on:click={() => private_store.close()}
    ></div>
</div>

<style lang="scss">
    .flyout {
        &__content {
            position: fixed;
            top: 0;
            right: -500px;
            height: 100vh;
            width: 500px;
            z-index: 1500;
            transition: 0.2s ease;

            &--expanded {
                display: block;
                transform: translateX(-500px);
            }

            &--left {
                left: 0;
            }

            &--right {
                right: 0;
            }
        }

        &__overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: transparent;
            z-index: 1499;
            display: none;

            &--expanded {
                display: block;
            }

            &--hidesbackground {
                background-color: rgba(0, 0, 0, 0.5);
            }
        }

        &__inner {
            display: flex;
            flex-direction: column;
            height: 100%;
            background-color: var(--color-surface);
            padding: var(--size-md) var(--size-lg);
            gap: var(--size-md);
            box-sizing: border-box;
        }

        &__close-button {
            display: flex;
            justify-content: flex-end;
        }

        &__header {
            display: flex;
            flex-direction: column;
            gap: var(--size-xs);
        }

        &__main-header {
            margin: 0;
            color: var(--color-text);
            font-size: 240%;
        }

        &__sub-header {
            margin: 0;
            color: var(--color-text-lighter);
        }

        &__body {
            height: 100%;
        }

        &__footer {
            display: flex;
            padding: var(--size-md) 0;
        }
    }
</style>
