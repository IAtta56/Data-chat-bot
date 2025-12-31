<script>
    import "../app.css";
    import { Github, Heart, Code2 } from "lucide-svelte";
    import { page } from "$app/stores";
    
    // Check if on dashboard - dashboard has its own layout
    $: isDashboard = $page.url.pathname.startsWith('/dashboard');
</script>

{#if isDashboard}
    <!-- Dashboard has its own full layout, just render the slot -->
    <slot />
{:else}
    <div class="flex flex-col min-h-screen bg-gradient-to-br from-slate-950 via-purple-950/20 to-slate-950">
        <div class="flex-1">
            <slot />
        </div>

        <!-- Modern Footer - Always Visible -->
        <footer class="relative py-8 border-t border-purple-500/20 bg-gradient-to-r from-slate-950 via-purple-950/30 to-slate-950 z-50">
            <!-- Glow effect -->
            <div class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-purple-500/50 to-transparent"></div>
            
            <div class="max-w-7xl mx-auto px-6 flex flex-col items-center gap-4">
                <!-- Main credit -->
                <div class="flex items-center gap-3 text-slate-300">
                    <Code2 class="h-5 w-5 text-purple-400 animate-pulse" />
                    <span class="text-sm">Built with</span>
                    <Heart class="h-4 w-4 text-pink-500 animate-pulse" />
                    <span class="text-sm">by</span>
                    <span class="text-lg font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-indigo-400 text-transparent bg-clip-text">
                        Atta Ur Rehman
                    </span>
                </div>
                
                <!-- GitHub link -->
                <a
                    href="https://github.com/Iatta56"
                    target="_blank"
                    rel="noreferrer"
                    class="group flex items-center gap-2 text-slate-400 hover:text-white transition-all duration-300 text-sm bg-white/5 hover:bg-purple-500/20 px-5 py-2.5 rounded-full border border-white/10 hover:border-purple-500/50 hover:shadow-lg hover:shadow-purple-500/20"
                >
                    <Github class="h-4 w-4 group-hover:rotate-12 transition-transform duration-300" />
                    <span>@Iatta56</span>
                    <span class="text-purple-400">on GitHub</span>
                </a>
                
                <!-- Copyright -->
                <p class="text-slate-600 text-xs mt-2">
                    © 2024 DataChat SaaS. All rights reserved.
                </p>
            </div>
        </footer>
    </div>
{/if}
