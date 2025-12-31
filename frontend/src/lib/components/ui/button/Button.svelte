<script lang="ts">
    import { type ButtonPrimitive } from "bits-ui";
    import { cn } from "$lib/utils";

    export let variant:
        | "default"
        | "destructive"
        | "outline"
        | "secondary"
        | "ghost"
        | "link"
        | "premium" = "default";
    export let size: "default" | "sm" | "lg" | "icon" = "default";
    export let className: string | undefined = undefined;
    export let href: string | undefined = undefined;

    let classNameVal = "";
    $: classNameVal = cn(
        "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-95",
        {
            "bg-primary text-primary-foreground hover:bg-primary/90 shadow-[0_0_15px_rgba(124,58,237,0.5)]":
                variant === "default",
            "bg-destructive text-destructive-foreground hover:bg-destructive/90":
                variant === "destructive",
            "border border-input bg-background hover:bg-accent hover:text-accent-foreground":
                variant === "outline",
            "bg-secondary text-secondary-foreground hover:bg-secondary/80":
                variant === "secondary",
            "hover:bg-accent hover:text-accent-foreground": variant === "ghost",
            "text-primary underline-offset-4 hover:underline":
                variant === "link",
            "bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white shadow-lg hover:shadow-pink-500/25 border-0": 
                variant === "premium",
            "h-10 px-4 py-2": size === "default",
            "h-9 rounded-md px-3": size === "sm",
            "h-11 rounded-md px-8": size === "lg",
            "h-10 w-10": size === "icon",
        },
        className,
    );
</script>

{#if href}
    <a {href} class={classNameVal} {...$$restProps}>
        <slot />
    </a>
{:else}
    <button class={classNameVal} {...$$restProps}>
        <slot />
    </button>
{/if}
