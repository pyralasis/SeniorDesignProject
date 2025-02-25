<script lang="ts">
    import Logo from '$lib/assets/logo-5.svg';
    import { writable, type Writable } from 'svelte/store';
    import Icon from '../Icon/Icon.svelte';
    import { IconNameEnum } from '../Icon/types/icon-name.enum';
    import { clickOutside } from '$lib/directives/click-outside';
    import { SoundUtility } from '$lib/utilities/sound.utility';

    let expanded: Writable<boolean> = writable(true);
    let rotationDegrees: Writable<number> = writable(0);

    const links: {
        name: string;
        href: string;
    }[] = [
        { name: 'Architectures', href: '/architectures' },
        { name: 'Pipelines', href: '/pipelines' },
        { name: 'Models', href: '/models' },
        { name: 'Training', href: '/training' },
    ];

    function toggleDrawer() {
        SoundUtility.playSwoosh();
        expanded.update((value) => !value);
        rotationDegrees.update((value) => (value + 180) % 360);
    }

    function handleClickOutside() {
        expanded.set(false);
    }
</script>

<div class="navigation-header">
    <a class="logo-container" href="/">
        <img src={Logo} alt="Check Logo" />
    </a>

    <div class="drawer-container" class:expanded={$expanded} use:clickOutside>
        <nav>
            <ul>
                {#each links as link}
                    <a href={link.href}>{link.name}</a>
                {/each}
            </ul>
        </nav>

        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <!-- <div class="icon-wrapper" on:click={toggleDrawer} style="transform: rotate({$rotationDegrees}deg);">
            <Icon name={IconNameEnum.sideways_hamburger} />
        </div> -->
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
        border-bottom: 1px solid #ffffff;
    }

    .logo-container {
        padding-left: 16px;
        z-index: 2;
        background-color: #111111;
        height: 27px;
    }

    img {
        height: 27px;
    }

    .drawer-container {
        display: flex;
        align-items: center;
        position: absolute;
        left: 0;
        height: 100%;
        background-color: #111111;
        transform: translateX(-83%);
        transition: transform 0.3s ease;
        padding-left: 75px; // Adjust based on your logo width
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

            a {
                text-decoration: none;
                cursor: pointer;
                padding: 8px 16px;
                border-radius: 4px;
                white-space: nowrap;
                color: #ffffff;
                &:hover {
                    color: #fe2e00;
                    transition: all 0.3s ease;
                    text-decoration: underline;
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
            color: #b91c1c;
        }
    }
</style>
