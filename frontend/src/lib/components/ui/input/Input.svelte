<script lang="ts">
    import { cn } from "$lib/utils";

    export let className: string | undefined = undefined;
    export let type: "text" | "email" | "password" | "number" | "file" = "text";
    export let value: string = "";
    export let files: FileList | null = null;
</script>

{#if type === "password"}
    <input
        type="password"
        bind:value
        class={cn(
            "flex h-10 w-full rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-0 focus-visible:border-transparent transition-all disabled:cursor-not-allowed disabled:opacity-50 text-white",
            className,
        )}
        {...$$restProps}
    />
{:else if type === "email"}
    <input
        type="email"
        bind:value
        class={cn(
            "flex h-10 w-full rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-0 focus-visible:border-transparent transition-all disabled:cursor-not-allowed disabled:opacity-50 text-white",
            className,
        )}
        {...$$restProps}
    />
{:else if type === "file"}
    <input
        type="file"
        bind:files
        class={cn(
            "flex h-10 w-full rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-0 focus-visible:border-transparent transition-all disabled:cursor-not-allowed disabled:opacity-50 text-white",
            className,
        )}
        {...$$restProps}
    />
{:else}
    <input
        type="text"
        bind:value
        class={cn(
            "flex h-10 w-full rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-0 focus-visible:border-transparent transition-all disabled:cursor-not-allowed disabled:opacity-50 text-white",
            className,
        )}
        {...$$restProps}
    />
{/if}
