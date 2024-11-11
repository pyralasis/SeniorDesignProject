<script lang="ts">
    import { TagColorEnum, TagSizeEnum, type TagColor, type TagSize } from './types';
    // -----------------------
    // External Properties
    // -----------------------
    export let color: TagColor = TagColorEnum.gray;
    export let size: TagSize = TagSizeEnum.medium;
</script>

<div
    class="tag"
    class:tag--green={color === TagColorEnum.green}
    class:tag--red={color === TagColorEnum.red}
    class:tag--orange={color === TagColorEnum.orange}
    class:tag--gray={color === TagColorEnum.gray}
    class:tag--purple={color === TagColorEnum.purple}
    class:tag--white={color === TagColorEnum.white}
    class:tag--yellow={color === TagColorEnum.yellow}
    class:tag--blue={color === TagColorEnum.blue}
    class:tag--small={size === TagSizeEnum.small}
    class:tag--medium={size === TagSizeEnum.medium}
    class:tag--large={size === TagSizeEnum.large}
>
    <slot></slot>
</div>

<style lang="scss">
    @import '../../../variables.css';
    .tag {
        display: flex;
        align-items: center;
        justify-content: center;
        width: fit-content;
        height: fit-content;
        border-radius: var(--border-radius-lg);
        font-size: 12px;
        font-weight: 600;
        border: 2px solid transparent;
        user-select: none;

        &--green {
            color: var(--color-tag-green);
            border-color: var(--color-tag-green);
        }

        &--red {
            color: var(--color-tag-red);
            border-color: var(--color-tag-red);
        }

        &--orange {
            color: var(--color-tag-orange);
            border-color: var(--color-tag-orange);
        }

        &--gray {
            color: var(--color-tag-gray);
            border-color: var(--color-tag-gray);
        }

        &--purple {
            color: var(--color-tag-purple);
            border-color: var(--color-tag-purple);
        }

        &--white {
            color: var(--color-white);
            border-color: var(--color-white);
        }

        &--yellow {
            color: var(--color-tag-yellow);
            border-color: var(--color-tag-yellow);
        }

        &--blue {
            color: var(--color-tag-blue);
            border-color: var(--color-tag-blue);
        }

        &--small {
            font-size: 8px;
            border-width: 2px;
            padding: var(--size-xxs) var(--size-sm);
        }

        &--medium {
            font-size: 12px;
            padding: var(--size-xxs) var(--size-sm);
        }

        &--large {
            font-size: 16px;
            padding: var(--size-xs) var(--size-md);
        }
    }
</style>
