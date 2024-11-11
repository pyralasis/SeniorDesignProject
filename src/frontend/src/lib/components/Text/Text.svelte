<script lang="ts">
    import { type TextColor, TextColorEnum, type TextSize, TextSizeEnum } from './types';
    // -----------------------
    // External Properties
    // -----------------------
    export let color: TextColor = TextColorEnum.primary;
    export let size: TextSize = TextSizeEnum.medium;
</script>

<span
    class="text"
    class:text--primary={color === TextColorEnum.primary}
    class:text--secondary={color === TextColorEnum.secondary}
    class:text--light={color == TextColorEnum.light}
    class:text--white={color == TextColorEnum.white}
    class:text--small={size === TextSizeEnum.small}
    class:text--medium={size === TextSizeEnum.medium}
    class:text--large={size === TextSizeEnum.large}
    class:text--xl={size === TextSizeEnum.xl}
>
    <slot></slot>
</span>

<style lang="scss">
    @import '../../../variables.css';
    .text {
        &--primary {
            color: var(--color-text-primary);
        }

        &--secondary {
            color: var(--color-text-secondary);
        }

        &--light {
            color: var(--color-text-light);
        }

        &--white {
            color: white;
        }

        &--small {
            font-size: 12px;
        }

        &--medium {
            font-size: 14px;
        }

        &--large {
            font-size: 16px;
        }

        &--xl {
            font-size: 18px;
        }
    }
</style>
