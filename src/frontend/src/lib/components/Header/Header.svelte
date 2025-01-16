<script lang="ts">
    import { type HeaderType, type HeaderColor, HeaderColorEnum, HeaderTypeEnum } from './types';
    // -----------------------
    // External Properties
    // -----------------------
    export let type: HeaderType = HeaderTypeEnum.h1;
    export let color: HeaderColor = HeaderColorEnum.default;
</script>

<span
    class="header"
    class:header--h1={type === HeaderTypeEnum.h1}
    class:header--h2={type === HeaderTypeEnum.h2}
    class:header--h3={type === HeaderTypeEnum.h3}
    class:header--h4={type === HeaderTypeEnum.h4}
    class:header--subheader={type === HeaderTypeEnum.subheader}
    class:header--secondary={color === HeaderColorEnum.secondary}
>
    <slot></slot>
</span>

<style lang="scss">
    @import '../../../variables.css';
    .header {
        margin: 0;
        color: var(--color-text-primary);
        font-weight: bold;

        &--h1 {
            font-size: 240%;
        }

        &--h2 {
            font-size: 200%;
        }

        &--h3 {
            font-size: 160%;
        }

        &--h4 {
            font-size: 140%;
        }

        &--subheader {
            font-size: 100%;
            color: var(--color-text-secondary);
        }

        &--secondary {
            color: var(--color-text-secondary);
        }
    }
</style>
