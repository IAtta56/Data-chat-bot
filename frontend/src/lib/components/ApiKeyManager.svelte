<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";

    let apiKey: string | null = null;
    let copied = false;

    async function fetchKey() {
        const token = localStorage.getItem("token");
        const res = await fetch("http://localhost:8000/auth/api-key", {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
            const data = await res.json();
            apiKey = data.api_key;
        }
    }

    async function generateKey() {
        const token = localStorage.getItem("token");
        const res = await fetch("http://localhost:8000/auth/api-key", {
            method: "POST",
            headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
            const data = await res.json();
            apiKey = data.api_key;
        }
    }

    import { onMount } from "svelte";
    onMount(fetchKey);

    function copyKey() {
        if (apiKey) {
            navigator.clipboard.writeText(apiKey);
            copied = true;
            setTimeout(() => (copied = false), 2000);
        }
    }
</script>

<div class="p-6 bg-white dark:bg-slate-900 rounded-lg shadow border mb-8">
    <h2 class="text-xl font-semibold mb-4">API Access</h2>
    <p class="text-sm text-slate-500 mb-4">
        Use this key to access the DataChat API programmatically. Include it in
        the header <code>X-API-Key</code>.
    </p>

    {#if apiKey}
        <div class="flex gap-2 items-center">
            <Input readonly value={apiKey} class="font-mono" />
            <Button variant="outline" on:click={copyKey}>
                {copied ? "Copied" : "Copy"}
            </Button>
            <Button variant="destructive" on:click={generateKey}
                >Regenerate</Button
            >
        </div>
    {:else}
        <Button on:click={generateKey}>Generate API Key</Button>
    {/if}
</div>
