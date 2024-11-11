import type { EnumOf } from "$lib/utilities";

export const TextColorEnum ={
    primary: "primary",
    secondary: "secondary",
    light: "light",
    white: "white",
} as const;

export type TextColor = EnumOf<typeof TextColorEnum>;