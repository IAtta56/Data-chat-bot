<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { BarChart3 } from "lucide-svelte";
    import { goto } from "$app/navigation";

    let name = "";
    let email = "";
    let password = "";
    let isLoading = false;
    let error = "";

    async function handleRegister() {
        isLoading = true;
        error = "";
        try {
            const res = await fetch("http://127.0.0.1:8000/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                }),
            });

            if (!res.ok) {
                const data = await res.json();
                // Handle both string and array error formats from FastAPI
                let errorMsg = "Registration failed";
                if (typeof data.detail === "string") {
                    errorMsg = data.detail;
                } else if (Array.isArray(data.detail)) {
                    errorMsg = data.detail
                        .map(
                            (e: any) => e.msg || e.message || JSON.stringify(e),
                        )
                        .join(", ");
                } else if (data.detail) {
                    errorMsg = JSON.stringify(data.detail);
                }
                throw new Error(errorMsg);
            }

            // Auto login after register
            const formData = new FormData();
            formData.append("username", email);
            formData.append("password", password);

            const loginRes = await fetch("http://127.0.0.1:8000/auth/token", {
                method: "POST",
                body: formData,
            });

            if (loginRes.ok) {
                const data = await loginRes.json();
                localStorage.setItem("token", data.access_token);
                goto("/dashboard");
            } else {
                goto("/login");
            }
        } catch (err: any) {
            console.error("Registration failed:", err);
            error = err.message;
        } finally {
            isLoading = false;
        }
    }
</script>

<div
    class="flex flex-col min-h-screen bg-cosmos-950 px-4 items-center justify-center relative overflow-hidden"
>
    <!-- Background Blobs -->
    <div class="fixed inset-0 z-0 pointer-events-none">
        <div
            class="absolute top-0 -left-4 w-96 h-96 bg-purple-500/20 rounded-full blur-[100px] animate-pulse-slow"
        ></div>
        <div
            class="absolute bottom-0 right-0 w-80 h-80 bg-blue-500/10 rounded-full blur-[100px] animate-float"
        ></div>
    </div>

    <!-- Decoration -->
    <div class="absolute top-8 left-8 flex items-center space-x-2 z-10">
        <BarChart3 class="h-6 w-6 text-white" />
        <span class="text-xl font-bold tracking-tight text-white font-heading"
            >DataChat SaaS</span
        >
    </div>

    <div
        class="w-full max-w-md space-y-8 glass-panel p-8 rounded-2xl relative z-10"
    >
        <div class="text-center">
            <h2
                class="mt-2 text-3xl font-bold tracking-tight text-white font-heading"
            >
                Create an account
            </h2>
            <p class="mt-2 text-sm text-slate-400">
                Already have an account? <a
                    href="/login"
                    class="font-medium text-primary hover:text-primary/80 transition-colors"
                    >Sign in</a
                >
            </p>
        </div>
        <form class="mt-8 space-y-6" on:submit|preventDefault={handleRegister}>
            <div class="space-y-4">
                <div class="space-y-2">
                    <Label for="name" class="text-slate-300">Full Name</Label>
                    <Input
                        id="name"
                        name="name"
                        type="text"
                        autocomplete="name"
                        required
                        placeholder="John Doe"
                        bind:value={name}
                    />
                </div>
                <div class="space-y-2">
                    <Label for="email-address" class="text-slate-300"
                        >Email address</Label
                    >
                    <Input
                        id="email-address"
                        name="email"
                        type="email"
                        autocomplete="email"
                        required
                        placeholder="you@example.com"
                        bind:value={email}
                    />
                </div>
                <div class="space-y-2">
                    <Label for="password" class="text-slate-300">Password</Label
                    >
                    <Input
                        id="password"
                        name="password"
                        type="password"
                        autocomplete="new-password"
                        required
                        placeholder="••••••••"
                        bind:value={password}
                    />
                </div>
            </div>

            {#if error}
                <div
                    class="p-3 rounded-md bg-red-500/10 border border-red-500/20 text-red-400 text-sm"
                >
                    {error}
                </div>
            {/if}

            <div>
                <Button
                    class="w-full"
                    type="submit"
                    variant="premium"
                    disabled={isLoading}
                >
                    {#if isLoading}
                        Creating account...
                    {:else}
                        Create account
                    {/if}
                </Button>
            </div>
        </form>
    </div>
</div>
