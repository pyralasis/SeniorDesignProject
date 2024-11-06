<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    export let label;
    export let checked = false;

    let checkbox: HTMLElement;

    const dispatch = createEventDispatcher();
    function handleClick(event: MouseEvent) {
        checked = !checked;
        dispatch('change', { value: checked });

        const ripple = document.createElement('div');
        ripple.classList.add('checkbox-ripple');
        if (checked) {
            ripple.style.backgroundColor = 'var(--color-green)';
        } else {
            ripple.style.backgroundColor = 'var(--color-edge-darker)';
        }
        checkbox.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 1000);
    }

    $: checked;
</script>

<div class="checkbox">
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="checkbox__inner" class:checkbox__inner--checked={checked} bind:this={checkbox} on:click={handleClick}>
        {#if checked}
            <svg width="8" height="7" viewBox="0 0 8 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M2.46971 5.65706L0.812892 3.72545C0.626679 3.50835 0.325873 3.50835 0.13966 3.72545C-0.0465533 3.94254 -0.0465533 4.29324 0.13966 4.51034L2.13548 6.83718C2.3217 7.05427 2.6225 7.05427 2.80871 6.83718L7.86034 0.947714C8.04655 0.730616 8.04655 0.37992 7.86034 0.162823C7.67413 -0.0542743 7.37332 -0.0542743 7.18711 0.162823L2.46971 5.65706Z"
                    fill="white"
                />
            </svg>
        {/if}
    </div>
    {#if label}
        <div class="checkbox__label">
            {label}
        </div>
    {/if}
</div>

<style lang="scss">
    .checkbox {
        display: flex;
        align-items: center;
        gap: 8px;
        width: fit-content;

        &__inner {
            width: 13px;
            height: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            border: 2px solid var(--color-edge);
            border-radius: 4px;
            cursor: pointer;

            &--checked {
                background-color: var(--color-green);
            }
        }

        &__label {
            font-weight: 500;
            color: var(--color-text);
        }

        &__check-mark {
            width: 5px;
            height: 5px;
            background-color: white;
            border-radius: 50%;
        }
    }

    :global(.checkbox-ripple) {
        position: absolute;
        border-radius: 50%;
        width: 60%;
        height: 60%;
        animation: ripple 0.5s forwards;
        pointer-events: none;
        z-index: 1;
        top: 50%;
        left: 50%;
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
