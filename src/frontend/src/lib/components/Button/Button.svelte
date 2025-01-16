<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { ButtonTypeEnum, type ButtonType, ButtonSizeEnum, type ButtonSize } from './types';

    // -----------------------
    // External Properties
    // -----------------------
    export let href: string = '';
    export let target: string = '';
    export let type: ButtonType = ButtonTypeEnum.primary;
    export let size: ButtonSize = ButtonSizeEnum.medium;

    // -----------------------
    // Internal Properties
    // -----------------------
    let button: HTMLElement;
    let dispatch = createEventDispatcher();

    // -----------------------
    // Internal Methods
    // -----------------------
    const onClick = (event: MouseEvent) => {
        if (!href) {
            event.preventDefault();
        }
        dispatch('click', event);
        const ripple: HTMLElement = document.createElement('div');
        ripple.classList.add('ripple');
        ripple.style.backgroundColor = 'var(--color-interactable-primary)';
        button.appendChild(ripple);

        const rect = button.getBoundingClientRect();

        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;

        setTimeout(() => {
            ripple.remove();
        }, 1000);
    };
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<a
    class="button"
    class:button--primary={type === ButtonTypeEnum.primary}
    class:button--secondary={type === ButtonTypeEnum.secondary}
    class:button--tertiary={type === ButtonTypeEnum.tertiary}
    class:button--small={size === ButtonSizeEnum.small}
    class:button--medium={size === ButtonSizeEnum.medium}
    class:button--large={size === ButtonSizeEnum.large}
    {href}
    {target}
    on:click={onClick}
    bind:this={button}
>
    <span
        class="button__label"
        class:button__label--primary={type === ButtonTypeEnum.primary}
        class:button__label--secondary={type === ButtonTypeEnum.secondary}
        class:button__label--tertiary={type === ButtonTypeEnum.tertiary}
        class:button__label--small={size === ButtonSizeEnum.small}
        class:button__label--medium={size === ButtonSizeEnum.medium}
        class:button__label--large={size === ButtonSizeEnum.large}
    >
        <slot />
    </span>
</a>

<style lang="scss">
    @import '../../../variables.css';
    .button {
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
        padding: var(--size-xs) var(--size-sm);
        border-radius: var(--border-radius-sm);
        background-color: var(--color-interactable-priamry);
        cursor: pointer;
        width: fit-content;
        user-select: none;
        transition: all 0.3s ease;
        text-decoration: none;
        outline: 2px solid transparent;

        &:hover {
            background-color: var(--color-interactable-primary-hover);
        }

        &--primary {
            background-color: var(--color-interactable-primary);
        }

        &--secondary {
            background-color: transparent;

            &:hover {
                background-color: var(--color-interactable-secondary-hover);
            }
        }

        &--tertiary {
            background-color: transparent;
            border: 2px solid var(--color-primary);

            &:hover {
                background-color: var(--color-interactable-secondary-hover);
            }
        }

        &--small {
            padding: var(--size-xs) var(--size-xs);
        }

        &--medium {
            padding: var(--size-xs) var(--size-sm);
        }

        &--large {
            padding: var(--size-sm) var(--size-md);
        }

        &__label {
            z-index: 2;
            display: flex;
            align-items: center;

            &--primary {
                color: var(--color-interactable-primary-text);
            }

            &--secondary {
                color: var(--color-interactable-secondary-text);
            }

            &--tertiary {
                color: var(--color-interactable-secondary-text);
            }

            &--small {
                height: 18px;
                font-size: 14px;
            }

            &--medium {
                height: 24px;
                font-size: 16px;
            }

            &--large {
                height: 32px;
                font-size: 18px;
            }
        }
    }

    :global(.ripple) {
        position: absolute;
        border-radius: 50%;
        width: 100px;
        height: 100px;
        transform: translate(-50%, -50%) scale(0);
        animation: ripple 1s forwards;
        pointer-events: none;
        z-index: 1;
    }

    @keyframes ripple {
        from {
            opacity: 1;
            transform: translate(-50%, -50%) scale(0);
        }
        to {
            opacity: 0;
            transform: translate(-50%, -50%) scale(4);
        }
    }
</style>
