<script lang="ts">
    import Logo from '$lib/assets/logo.svg';
    import { writable, type Writable } from 'svelte/store';
    import Icon from '../Icon/Icon.svelte';
    import { IconNameEnum } from '../Icon/types/icon-name.enum';
    import { clickOutside } from '$lib/directives/click-outside';

    let expanded: Writable<boolean> = writable(false);

    function toggleDrawer() {
        expanded.update((value) => !value);
    }

    function handleClickOutside() {
        expanded.set(false);
    }
</script>

<div class="navigation-header">
    <a class="logo-container" href="/">
        <img src={Logo} alt="Check Logo" />
    </a>

    <div class="drawer-container" class:expanded={$expanded} use:clickOutside on:click_outside={handleClickOutside}>
        <nav>
            <ul>
                <li>Link 1</li>
                <li>Link 2</li>
                <li>Link 3</li>
            </ul>
        </nav>

        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div class="icon-wrapper" on:click={toggleDrawer}>
            <Icon name={$expanded ? IconNameEnum.plus : IconNameEnum.plus} />
        </div>
    </div>
</div>

<style lang="scss">
    .navigation-header {
        display: flex;
        align-items: center;
        height: 54px;
        color: #ffffff;
        position: relative;
        overflow: hidden;
    }

    .logo-container {
        padding-left: 16px;
        z-index: 2;
    }

    .drawer-container {
        display: flex;
        align-items: center;
        position: absolute;
        left: 0;
        height: 100%;
        background-color: #1a1a1a;
        transform: translateX(-100%);
        transition: transform 0.3s ease;
        padding-left: 175px; // Adjust based on your logo width
        padding-right: 16px;

        &.expanded {
            transform: translateX(0);
        }

        nav {
            height: 100%;

            ul {
                display: flex;
                list-style: none;
                padding: 0;
                margin: 0;
                height: 100%;
                align-items: center;
                gap: 24px;
            }

            li {
                cursor: pointer;
                padding: 8px 16px;
                border-radius: 4px;
                white-space: nowrap;

                &:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
            }
        }
    }

    .icon-wrapper {
        cursor: pointer;
        padding: 8px;
        border-radius: 4px;
        transition: background-color 0.2s ease;
        margin-left: 16px;

        &:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
    }
</style>
