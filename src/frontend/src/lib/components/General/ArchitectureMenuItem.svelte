<script lang="ts">
    import { text } from "@sveltejs/kit";
    import {
        ButtonSizeEnum,
        ButtonTypeEnum,
        Flyout,
        Header,
        HeaderTypeEnum,
        Popover,
        PopoverChipTrigger,
        PopoverMultiSelectContent,
        TabContent,
        TabLabel,
        Tabs,
        Button,
        Accordion,
        AccordionHeader,
        AccordionBody,
        Checkbox,
        Text,
        type PopoverItem,
        Tag,
        TagColorEnum,
        TextInput,
        PopoverSingleSelectContent,
        InputSeries,
    } from "kiwi-nl";

    export let title;
    export let description;
</script>

<Accordion>
    <AccordionHeader slot="header"
        ><Header type={HeaderTypeEnum.h4}>{title}</Header></AccordionHeader
    >
    <AccordionBody slot="body">
        <Text>{description}</Text>
        <div class="button-container">
            <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.small}
                >Edit</Button
            >
            <Button type={ButtonTypeEnum.secondary} size={ButtonSizeEnum.small}
                >Delete</Button
            >
        </div>
    </AccordionBody>
</Accordion>

<style>
    .button-container {
        display: flex;
        flex-direction: row;
    }
</style>
