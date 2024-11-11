import type { EnumOf } from "$lib/utilities";

export const TagColorEnum = {
    green: "green",
    red: "red",
    blue: "blue",
    yellow: "yellow",
    purple: "purple",
    orange: "orange",
    gray: "gray",
    white: "white",
} as const;

export type TagColor = EnumOf<typeof TagColorEnum>;