<script lang="ts">
    import { onMount } from "svelte";
    import {
        MessageSquare,
        Plus,
        Upload,
        Settings,
        ChevronLeft,
        ChevronRight,
        Send,
        FileText,
        Trash2,
        LogOut,
        Sparkles,
        X,
        Zap,
        Brain,
        FileSpreadsheet,
        Github,
        Moon,
        Sun,
        Download,
        RefreshCw,
        Check,
        AlertCircle,
        BarChart3,
        TrendingUp,
        PieChart,
        Activity,
    } from "lucide-svelte";

    // State
    let sidebarOpen = true;
    let files: any[] = [];
    let sessions: any[] = [];
    let currentSession: any = null;
    let messages: any[] = [];
    let messageInput = "";
    let isLoading = false;
    let uploadFiles: FileList | null = null;
    let showUploadModal = false;
    let activeTab: 'chat' | 'insights' | 'dashboards' = 'chat';
    let dashboardData: any = null;
    let insightsData: any = null;
    let buildingDashboard = false;
    let buildingInsights = false;
    let darkMode = true;

    const API_BASE = "http://localhost:8000";

    function getToken() {
        return localStorage.getItem("token");
    }

    async function loadFiles() {
        const token = getToken();
        const res = await fetch(`${API_BASE}/files/`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
            files = await res.json();
        }
    }

    async function loadSessions() {
        const token = getToken();
        const res = await fetch(`${API_BASE}/chat/sessions`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
            sessions = await res.json();
        }
    }

    async function handleUpload() {
        if (!uploadFiles || uploadFiles.length === 0) return;
        
        const token = getToken();
        if (!token) {
            window.location.href = "/login";
            return;
        }

        isLoading = true;
        try {
            // Upload all selected files
            for (let i = 0; i < uploadFiles.length; i++) {
                const formData = new FormData();
                formData.append("file", uploadFiles[i]);

                const res = await fetch(`${API_BASE}/files/`, {
                    method: "POST",
                    headers: { Authorization: `Bearer ${token}` },
                    body: formData,
                });

                if (!res.ok) {
                    const errData = await res.json().catch(() => ({}));
                    alert(`Upload failed for ${uploadFiles[i].name}: ` + (errData.detail || res.statusText));
                }
            }
            
            await loadFiles();
            showUploadModal = false;
            uploadFiles = null;
            
            // Start chat with the first uploaded file if available
            if (files.length > 0) {
                await startNewChat(files[files.length - 1].id);
            }
        } catch (err: any) {
            alert("Upload failed: " + err.message);
        } finally {
            isLoading = false;
        }
    }

    async function startNewChat(fileId: number) {
        const token = getToken();
        const res = await fetch(`${API_BASE}/chat/sessions?file_id=${fileId}`, {
            method: "POST",
            headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
            const session = await res.json();
            await loadSessions();
            await selectSession(session);
        }
    }

    async function selectSession(session: any) {
        currentSession = session;
        messages = [];
        
        const token = getToken();
        const res = await fetch(`${API_BASE}/chat/history/${session.id}`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
            messages = await res.json();
            // Scroll to bottom
            setTimeout(() => {
                const container = document.querySelector('.messages-container');
                if (container) container.scrollTop = container.scrollHeight;
            }, 100);
        }
    }

    async function sendMessage() {
        if (!messageInput.trim() || !currentSession || isLoading) return;
        
        const userMessage = messageInput;
        messageInput = "";
        messages = [...messages, { role: "user", content: userMessage }];
        
        isLoading = true;
        const token = getToken();
        
        try {
            const res = await fetch(`${API_BASE}/chat/message/${currentSession.id}`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: userMessage,
                    file_id: currentSession.file_id,
                }),
            });
            
            if (res.ok) {
                const data = await res.json();
                messages = [...messages, { role: "assistant", content: data.response }];
            } else {
                const err = await res.json().catch(() => ({}));
                messages = [...messages, { role: "assistant", content: `⚠️ ${err.detail || "Error processing request"}` }];
            }
        } catch (err) {
            messages = [...messages, { role: "assistant", content: "⚠️ Connection error. Please try again." }];
        } finally {
            isLoading = false;
            setTimeout(() => {
                const container = document.querySelector('.messages-container');
                if (container) container.scrollTop = container.scrollHeight;
            }, 100);
        }
    }

    async function deleteFile(fileId: number, e: Event) {
        e.stopPropagation();
        const token = getToken();
        await fetch(`${API_BASE}/files/${fileId}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${token}` },
        });
        await loadFiles();
    }

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    }

    function exportChat() {
        if (!messages.length) return;
        const content = messages.map(m => `${m.role.toUpperCase()}: ${m.content}`).join('\n\n');
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat-${currentSession?.title || 'export'}.txt`;
        a.click();
    }

    async function buildInsights() {
        if (files.length === 0) {
            alert("Please upload a file first");
            return;
        }
        buildingInsights = true;
        activeTab = 'insights';
        const token = getToken();
        
        try {
            console.log("Building insights...");
            const res = await fetch(`${API_BASE}/chat/build-dashboard`, {
                method: "POST",
                headers: { Authorization: `Bearer ${token}` },
            });
            
            console.log("Response status:", res.status);
            if (res.ok) {
                insightsData = await res.json();
                console.log("Insights data:", insightsData);
            } else {
                const err = await res.json().catch(() => ({}));
                console.error("Error:", err);
                alert(err.detail || "Failed to build insights");
            }
        } catch (err) {
            console.error("Exception:", err);
            alert("Error building insights: " + err.message);
        } finally {
            buildingInsights = false;
        }
    }

    async function buildDashboard() {
        if (files.length === 0) {
            alert("Please upload a file first");
            return;
        }
        buildingDashboard = true;
        activeTab = 'dashboards';
        const token = getToken();
        
        try {
            console.log("Building dashboard...");
            const res = await fetch(`${API_BASE}/chat/build-dashboard`, {
                method: "POST",
                headers: { Authorization: `Bearer ${token}` },
            });
            
            console.log("Response status:", res.status);
            if (res.ok) {
                dashboardData = await res.json();
                console.log("Dashboard data:", dashboardData);
            } else {
                const err = await res.json().catch(() => ({}));
                console.error("Error:", err);
                alert(err.detail || "Failed to build dashboard");
            }
        } catch (err) {
            alert("Error building dashboard");
        } finally {
            buildingDashboard = false;
        }
    }

    function logout() {
        localStorage.removeItem("token");
        window.location.href = "/login";
    }

    onMount(() => {
        const token = getToken();
        if (!token) {
            window.location.href = "/login";
            return;
        }
        loadFiles();
        loadSessions();
    });
</script>

<div class="flex flex-col h-screen bg-gradient-to-br from-slate-950 via-purple-950/20 to-slate-950 text-white overflow-hidden relative">
    <!-- Animated Background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="absolute top-0 left-1/4 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-fuchsia-500/10 rounded-full blur-3xl animate-pulse-slower"></div>
    </div>
    
    <div class="flex flex-1 overflow-hidden relative z-10">
        <!-- Sidebar -->
        <div 
            class="flex flex-col bg-slate-900/40 backdrop-blur-2xl border-r border-white/10 transition-all duration-500 ease-out {sidebarOpen ? 'w-72' : 'w-0'} relative shadow-2xl"
        >
            {#if sidebarOpen}
                <div class="flex flex-col h-full animate-fadeIn">
                    <!-- Logo -->
                    <div class="p-5 border-b border-white/10 bg-gradient-to-b from-white/5 to-transparent">
                        <div class="flex items-center gap-3">
                            <div class="relative group">
                                <div class="absolute inset-0 bg-gradient-to-r from-violet-600 via-fuchsia-600 to-pink-600 rounded-2xl blur-xl opacity-60 group-hover:opacity-100 transition-opacity duration-500 animate-pulse-slow"></div>
                                <div class="relative p-3 bg-gradient-to-br from-violet-600 via-fuchsia-600 to-pink-600 rounded-2xl shadow-2xl group-hover:scale-110 transition-transform duration-300">
                                    <Sparkles class="h-6 w-6 text-white animate-spin-slow" />
                                </div>
                            </div>
                            <div>
                                <span class="font-black text-2xl bg-gradient-to-r from-white via-violet-200 to-fuchsia-200 bg-clip-text text-transparent">DataChat</span>
                                <p class="text-[9px] text-violet-400 uppercase tracking-widest font-bold">✨ AI Analytics</p>
                            </div>
                        </div>
                    </div>

                    <!-- New Chat Button -->
                    <div class="p-4">
                        <button
                            on:click={() => showUploadModal = true}
                            class="w-full flex items-center justify-center gap-2 px-4 py-3.5 rounded-2xl bg-gradient-to-r from-violet-600 via-fuchsia-600 to-pink-600 hover:from-violet-500 hover:via-fuchsia-500 hover:to-pink-500 transition-all duration-300 text-sm font-bold shadow-2xl shadow-violet-500/30 hover:shadow-violet-500/50 hover:scale-[1.03] active:scale-[0.97] border border-white/10"
                        >
                            <Plus class="h-5 w-5 animate-pulse" />
                            <span>New Analysis</span>
                        </button>
                    </div>

                    <!-- Chat History -->
                    <div class="flex-1 overflow-y-auto px-3 scrollbar-thin">
                        <div class="text-[10px] text-gray-500 px-3 py-2 uppercase tracking-widest font-medium">Recent Chats</div>
                        {#each sessions as session, i}
                            <button
                                on:click={() => selectSession(session)}
                                class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-white/10 transition-all duration-200 text-sm text-left mb-1 group {currentSession?.id === session.id ? 'bg-gradient-to-r from-violet-600/30 to-fuchsia-600/30 border border-violet-400/50 shadow-lg shadow-violet-500/20' : 'hover:shadow-md'}"
                                style="animation-delay: {i * 50}ms"
                            >
                                <div class="p-1.5 rounded-lg bg-gradient-to-br {currentSession?.id === session.id ? 'from-violet-500 to-fuchsia-500 shadow-lg' : 'from-gray-700 to-gray-600 group-hover:from-violet-600 group-hover:to-fuchsia-600'} transition-all duration-300">
                                    <MessageSquare class="h-3.5 w-3.5" />
                                </div>
                                <span class="truncate text-gray-300 group-hover:text-white transition-colors font-medium">{session.title || 'Untitled Chat'}</span>
                            </button>
                        {/each}
                        {#if sessions.length === 0}
                            <div class="text-center py-8 px-4">
                                <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-gray-800/50 flex items-center justify-center">
                                    <MessageSquare class="h-5 w-5 text-gray-600" />
                                </div>
                                <p class="text-gray-500 text-xs">No chats yet</p>
                            </div>
                        {/if}
                    </div>

                    <!-- Files Section -->
                    <div class="border-t border-white/5 px-3 py-3">
                        <div class="text-[10px] text-gray-500 px-3 py-2 uppercase tracking-widest font-medium flex items-center justify-between">
                            <span>Your Files</span>
                            <span class="text-violet-400">{files.length}</span>
                        </div>
                        <div class="max-h-28 overflow-y-auto scrollbar-thin">
                            {#each files as file}
                                <button 
                                    on:click={() => startNewChat(file.id)}
                                    class="w-full flex items-center justify-between px-3 py-2 rounded-lg hover:bg-white/5 group transition-all cursor-pointer text-left"
                                >
                                    <div class="flex items-center gap-2 min-w-0">
                                        <FileSpreadsheet class="h-4 w-4 text-emerald-400 flex-shrink-0" />
                                        <span class="text-sm text-gray-400 truncate group-hover:text-white transition-colors">{file.filename}</span>
                                    </div>
                                    <span
                                        role="button"
                                        tabindex="0"
                                        on:click={(e) => deleteFile(file.id, e)}
                                        on:keydown={(e) => e.key === 'Enter' && deleteFile(file.id, e)}
                                        class="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-red-500/20 rounded-lg transition-all"
                                    >
                                        <Trash2 class="h-3 w-3 text-red-400" />
                                    </span>
                                </button>
                            {/each}
                        </div>
                    </div>

                    <!-- Bottom Actions -->
                    <div class="border-t border-white/5 p-3 space-y-1">
                        <button
                            on:click={logout}
                            class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-red-500/10 transition-all text-sm text-gray-400 hover:text-red-400 group"
                        >
                            <div class="p-1.5 rounded-lg bg-gray-800 group-hover:bg-red-500/20 transition-all">
                                <LogOut class="h-3.5 w-3.5" />
                            </div>
                            <span>Logout</span>
                        </button>
                    </div>
                </div>
            {/if}
        </div>

        <!-- Sidebar Toggle -->
        <button
            on:click={() => sidebarOpen = !sidebarOpen}
            class="absolute left-0 top-1/2 -translate-y-1/2 z-50 p-2 bg-slate-800/80 backdrop-blur border border-white/10 rounded-r-xl hover:bg-slate-700/80 transition-all duration-300 {sidebarOpen ? 'translate-x-72' : 'translate-x-0'}"
        >
            {#if sidebarOpen}
                <ChevronLeft class="h-4 w-4" />
            {:else}
                <ChevronRight class="h-4 w-4" />
            {/if}
        </button>

        <!-- Main Content -->
        <div class="flex-1 flex flex-col min-w-0">
            {#if currentSession}
                <!-- Tab Navigation -->
                <div class="border-b border-white/10 px-6 py-4 bg-gradient-to-b from-slate-900/50 to-transparent backdrop-blur-xl flex items-center gap-3 shadow-lg">
                    <button
                        on:click={() => activeTab = 'chat'}
                        class="px-5 py-2.5 rounded-xl transition-all duration-300 flex items-center gap-2 text-sm font-bold {activeTab === 'chat' ? 'bg-gradient-to-r from-violet-600 to-fuchsia-600 shadow-2xl shadow-violet-500/40 scale-105 border border-white/20' : 'hover:bg-white/10 text-gray-400 hover:text-white hover:scale-105'}"
                    >
                        <MessageSquare class="h-4 w-4" />
                        Chat
                    </button>
                    <button
                        on:click={buildingInsights ? null : buildInsights}
                        disabled={buildingInsights || files.length === 0}
                        class="px-5 py-2.5 rounded-xl transition-all duration-300 flex items-center gap-2 text-sm font-bold {activeTab === 'insights' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 shadow-2xl shadow-emerald-500/40 scale-105 border border-white/20' : 'hover:bg-white/10 text-gray-400 hover:text-white hover:scale-105'} disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                        {#if buildingInsights}
                            <RefreshCw class="h-4 w-4 animate-spin" />
                        {:else}
                            <Brain class="h-4 w-4" />
                        {/if}
                        Insights
                    </button>
                    <button
                        on:click={buildingDashboard ? null : buildDashboard}
                        disabled={buildingDashboard || files.length === 0}
                        class="px-5 py-2.5 rounded-xl transition-all duration-300 flex items-center gap-2 text-sm font-bold {activeTab === 'dashboards' ? 'bg-gradient-to-r from-blue-600 to-cyan-600 shadow-2xl shadow-blue-500/40 scale-105 border border-white/20' : 'hover:bg-white/10 text-gray-400 hover:text-white hover:scale-105'} disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                        {#if buildingDashboard}
                            <RefreshCw class="h-4 w-4 animate-spin" />
                        {:else}
                            <BarChart3 class="h-4 w-4" />
                        {/if}
                        Dashboards
                    </button>
                    <div class="flex-1"></div>
                    <button
                        on:click={exportChat}
                        class="p-2 rounded-lg hover:bg-white/5 transition-colors text-gray-400 hover:text-white"
                        title="Export Chat"
                    >
                        <Download class="h-4 w-4" />
                    </button>
                </div>
            {/if}

            {#if activeTab === 'insights' && insightsData}
                <!-- Insights View -->
                <div class="flex-1 overflow-y-auto bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
                    <div class="p-6 max-w-7xl mx-auto">
                        <div class="mb-8">
                            <h1 class="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">AI Insights</h1>
                            <p class="text-gray-400 mt-1">Smart analysis and recommendations from your data</p>
                        </div>

                        {#if insightsData.insights && insightsData.insights.length > 0}
                            <div class="space-y-4">
                                {#each insightsData.insights as insight, i}
                                    <div class="p-5 rounded-2xl bg-gradient-to-r from-emerald-500/10 to-teal-500/10 border border-emerald-500/20 animate-slideUp" style="animation-delay: {i * 0.1}s">
                                        <div class="flex items-start gap-3">
                                            <div class="p-2 rounded-lg bg-emerald-500/20">
                                                <FileSpreadsheet class="h-4 w-4 text-emerald-400" />
                                            </div>
                                            <div class="flex-1">
                                                <h4 class="font-medium text-emerald-300 mb-2">{insight.file}</h4>
                                                <p class="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">{insight.text}</p>
                                            </div>
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    </div>
                </div>
            {:else if activeTab === 'dashboards' && dashboardData}
                <!-- Dashboards View -->
                <div class="flex-1 overflow-y-auto bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
                    <div class="p-6 max-w-7xl mx-auto">
                        <div class="mb-8">
                            <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Analytics Dashboard</h1>
                            <p class="text-gray-400 mt-1">Comprehensive data visualization and metrics</p>
                        </div>

                        {#if dashboardData}
                            <!-- KPIs -->
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                                {#each dashboardData.kpis.slice(0, 8) as kpi, i}
                                    <div class="p-6 rounded-2xl bg-gradient-to-br from-slate-800/70 via-violet-900/20 to-slate-900/70 border border-white/10 hover:border-violet-400/50 transition-all duration-500 hover:scale-110 hover:shadow-2xl hover:shadow-violet-500/30 group backdrop-blur-sm" style="animation: slideUp 0.4s ease-out {i * 0.05}s backwards">
                                        <div class="text-xs text-violet-300/70 mb-3 uppercase tracking-widest font-bold">{kpi.title}</div>
                                        <div class="text-3xl font-black bg-gradient-to-r from-violet-300 via-fuchsia-300 to-pink-300 bg-clip-text text-transparent group-hover:scale-110 transition-transform duration-300">
                                            {kpi.format === 'decimal' ? kpi.value.toFixed(2) : kpi.value.toLocaleString()}
                                        </div>
                                        <div class="mt-2 h-1 w-full bg-gradient-to-r from-violet-500/30 to-fuchsia-500/30 rounded-full overflow-hidden">
                                            <div class="h-full bg-gradient-to-r from-violet-500 to-fuchsia-500 w-3/4 rounded-full group-hover:w-full transition-all duration-1000"></div>
                                        </div>
                                    </div>
                                {/each}
                            </div>

                            <!-- Charts -->
                            <div class="grid md:grid-cols-2 gap-6 mb-8">
                                {#each dashboardData.charts as chart, i}
                                    <div class="p-6 rounded-2xl bg-gradient-to-br from-slate-800/70 via-slate-900/50 to-slate-950/70 border border-white/10 hover:border-violet-400/40 transition-all duration-500 hover:scale-[1.02] hover:shadow-2xl hover:shadow-violet-500/20 backdrop-blur-sm group" style="animation: slideUp 0.4s ease-out {0.4 + i * 0.1}s backwards">
                                        <h3 class="text-lg font-bold mb-4 flex items-center gap-2 text-violet-100">
                                            {#if chart.type === 'bar'}
                                                <BarChart3 class="h-5 w-5 text-violet-400 group-hover:scale-110 transition-transform" />
                                            {:else if chart.type === 'pie'}
                                                <PieChart class="h-5 w-5 text-fuchsia-400 group-hover:scale-110 transition-transform" />
                                            {:else if chart.type === 'line'}
                                                <TrendingUp class="h-5 w-5 text-emerald-400 group-hover:scale-110 transition-transform" />
                                            {/if}
                                            {chart.title}
                                        </h3>
                                        
                                        {#if chart.image}
                                            <div class="bg-white rounded-xl p-4 shadow-inner overflow-hidden">
                                                <img 
                                                    src={chart.image} 
                                                    alt={chart.title}
                                                    class="w-full h-auto rounded-lg transition-transform duration-300 group-hover:scale-105"
                                                />
                                            </div>
                                        {:else}
                                            <div class="bg-slate-900/50 rounded-xl p-4 h-64 flex items-center justify-center">
                                                <div class="text-center text-gray-500 text-sm">
                                                    <Activity class="h-12 w-12 mx-auto mb-2 text-gray-600 animate-pulse" />
                                                    <p>Chart visualization not available</p>
                                                </div>
                                            </div>
                                        {/if}
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    </div>
                </div>
            {:else if activeTab === 'chat' && currentSession}

                <!-- Messages -->
                <div class="flex-1 overflow-y-auto messages-container">
                    <div class="max-w-4xl mx-auto px-4 py-6 space-y-6">
                        {#each messages as message, i}
                            <div 
                                class="flex gap-4 animate-slideUp {message.role === 'user' ? 'flex-row-reverse' : ''}"
                                style="animation-delay: {i * 50}ms"
                            >
                                <div class="flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center shadow-lg {message.role === 'user' ? 'bg-gradient-to-r from-violet-600 to-fuchsia-600' : 'bg-gradient-to-r from-emerald-500 to-teal-500'}">
                                    {#if message.role === 'user'}
                                        <span class="text-xs font-bold">You</span>
                                    {:else}
                                        <Sparkles class="h-4 w-4" />
                                    {/if}
                                </div>
                                <div class="flex-1 {message.role === 'user' ? 'text-right' : ''}">
                                    <div class="inline-block px-5 py-4 rounded-2xl {message.role === 'user' ? 'bg-gradient-to-br from-violet-600 via-fuchsia-600 to-pink-600 text-white rounded-tr-sm shadow-2xl shadow-violet-500/30 border border-violet-400/30' : 'bg-slate-800/90 text-gray-100 rounded-tl-sm border border-white/10 shadow-xl'} max-w-[85%] backdrop-blur-md hover:scale-[1.01] transition-transform duration-200">
                                        <div class="text-sm leading-relaxed text-left space-y-2">
                                            {#each message.content.split(/!\[([^\]]*)\]\(([^)]+)\)/g) as part, i}
                                                {#if i % 3 === 0}
                                                    {#if part.trim()}
                                                        <p class="whitespace-pre-wrap">{part}</p>
                                                    {/if}
                                                {:else if i % 3 === 2}
                                                    <img src={part} alt={message.content.split(/!\[([^\]]*)\]\(([^)]+)\)/g)[i-1]} class="rounded-xl max-w-full h-auto border border-white/10 shadow-lg my-2" />
                                                {/if}
                                            {/each}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {/each}
                        
                        {#if isLoading}
                            <div class="flex gap-4 animate-slideUp">
                                <div class="flex-shrink-0 w-9 h-9 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 flex items-center justify-center shadow-lg">
                                    <Sparkles class="h-4 w-4 animate-spin" />
                                </div>
                                <div class="bg-slate-800/80 px-5 py-4 rounded-2xl rounded-tl-sm border border-white/5 backdrop-blur-sm">
                                    <div class="flex gap-1.5">
                                        <div class="w-2 h-2 bg-violet-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
                                        <div class="w-2 h-2 bg-fuchsia-400 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
                                        <div class="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
                                    </div>
                                </div>
                            </div>
                        {/if}
                    </div>
                </div>

                <!-- Input -->
                <div class="border-t border-white/5 p-4 bg-slate-900/30 backdrop-blur-sm">
                    <div class="max-w-4xl mx-auto">
                        <div class="flex items-end gap-3 bg-slate-800/50 rounded-2xl px-4 py-3 border border-white/10 focus-within:border-violet-500/50 focus-within:shadow-lg focus-within:shadow-violet-500/10 transition-all duration-300">
                            <textarea
                                bind:value={messageInput}
                                on:keydown={handleKeydown}
                                placeholder="Ask anything about your data..."
                                rows="1"
                                class="flex-1 bg-transparent resize-none text-sm focus:outline-none placeholder-gray-500 max-h-32"
                            ></textarea>
                            <button
                                on:click={sendMessage}
                                disabled={!messageInput.trim() || isLoading}
                                class="p-2.5 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-500 hover:to-fuchsia-500 disabled:opacity-40 disabled:cursor-not-allowed rounded-xl transition-all duration-300 shadow-lg shadow-violet-500/20 hover:shadow-violet-500/40 hover:scale-105 active:scale-95"
                            >
                                <Send class="h-4 w-4" />
                            </button>
                        </div>
                    </div>
                </div>
            {:else}
                <!-- Welcome Screen -->
                <div class="flex-1 flex items-center justify-center p-6 overflow-y-auto">
                    <div class="text-center max-w-2xl animate-fadeIn">
                        <div class="relative inline-block mb-8">
                            <div class="absolute inset-0 bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-3xl blur-2xl opacity-30 animate-pulse"></div>
                            <div class="relative p-6 bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-3xl">
                                <Sparkles class="h-16 w-16 text-white" />
                            </div>
                        </div>
                        <h1 class="text-4xl font-bold mb-4 bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent">Welcome to DataChat</h1>
                        <p class="text-gray-400 mb-10 text-lg leading-relaxed">Upload your data files and unlock powerful AI-driven insights. Analyze spreadsheets, query documents, and visualize trends with natural language.</p>
                        
                        <div class="flex flex-col sm:flex-row gap-4 justify-center mb-12">
                            <button
                                on:click={() => showUploadModal = true}
                                class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-500 hover:to-fuchsia-500 rounded-xl font-medium transition-all duration-300 shadow-xl shadow-violet-500/25 hover:shadow-violet-500/40 hover:scale-105 active:scale-95"
                            >
                                <Upload class="h-5 w-5" />
                                Upload & Analyze
                            </button>
                        </div>

                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div class="p-5 bg-slate-800/50 rounded-2xl border border-white/5 hover:border-violet-500/30 transition-all duration-300 hover:scale-105 group">
                                <div class="w-10 h-10 mb-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 flex items-center justify-center shadow-lg">
                                    <FileSpreadsheet class="h-5 w-5" />
                                </div>
                                <h3 class="font-medium text-sm mb-1 group-hover:text-emerald-400 transition-colors">CSV & Excel</h3>
                                <p class="text-xs text-gray-500">Analyze data</p>
                            </div>
                            <div class="p-5 bg-slate-800/50 rounded-2xl border border-white/5 hover:border-violet-500/30 transition-all duration-300 hover:scale-105 group">
                                <div class="w-10 h-10 mb-3 rounded-xl bg-gradient-to-r from-violet-500 to-purple-500 flex items-center justify-center shadow-lg">
                                    <FileText class="h-5 w-5" />
                                </div>
                                <h3 class="font-medium text-sm mb-1 group-hover:text-violet-400 transition-colors">PDF & Docs</h3>
                                <p class="text-xs text-gray-500">Query content</p>
                            </div>
                            <div class="p-5 bg-slate-800/50 rounded-2xl border border-white/5 hover:border-violet-500/30 transition-all duration-300 hover:scale-105 group">
                                <div class="w-10 h-10 mb-3 rounded-xl bg-gradient-to-r from-fuchsia-500 to-pink-500 flex items-center justify-center shadow-lg">
                                    <Brain class="h-5 w-5" />
                                </div>
                                <h3 class="font-medium text-sm mb-1 group-hover:text-fuchsia-400 transition-colors">AI Insights</h3>
                                <p class="text-xs text-gray-500">Smart analysis</p>
                            </div>
                            <div class="p-5 bg-slate-800/50 rounded-2xl border border-white/5 hover:border-violet-500/30 transition-all duration-300 hover:scale-105 group">
                                <div class="w-10 h-10 mb-3 rounded-xl bg-gradient-to-r from-orange-500 to-red-500 flex items-center justify-center shadow-lg">
                                    <Zap class="h-5 w-5" />
                                </div>
                                <h3 class="font-medium text-sm mb-1 group-hover:text-orange-400 transition-colors">Visualize</h3>
                                <p class="text-xs text-gray-500">Charts & plots</p>
                            </div>
                        </div>
                    </div>
                </div>
            {/if}
        </div>
    </div>

    <!-- Footer -->
    <footer class="border-t border-white/5 bg-slate-900/50 backdrop-blur-sm px-6 py-3">
        <div class="flex items-center justify-between max-w-7xl mx-auto">
            <div class="flex items-center gap-2 text-xs text-gray-500">
                <span>Built with</span>
                <span class="text-red-400 animate-pulse">❤️</span>
                <span>by</span>
                <span class="font-medium bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">Atta Ur Rehman</span>
            </div>
            <a
                href="https://github.com/Iatta56"
                target="_blank"
                rel="noopener noreferrer"
                class="flex items-center gap-2 text-xs text-gray-500 hover:text-white transition-colors group bg-white/5 px-3 py-1.5 rounded-full border border-white/10 hover:border-violet-500/50"
            >
                <Github class="h-4 w-4 group-hover:scale-110 transition-transform" />
                <span>@Iatta56</span>
            </a>
        </div>
    </footer>
</div>

<!-- Upload Modal -->
{#if showUploadModal}
    <div class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fadeIn">
        <div class="bg-slate-900 rounded-3xl border border-white/10 w-full max-w-md p-6 relative shadow-2xl animate-slideUp">
            <button
                on:click={() => { showUploadModal = false; uploadFiles = null; }}
                class="absolute top-4 right-4 p-2 hover:bg-white/10 rounded-xl transition-colors"
            >
                <X class="h-5 w-5" />
            </button>
            
            <div class="text-center mb-6">
                <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-600 flex items-center justify-center shadow-lg shadow-violet-500/30">
                    <Upload class="h-6 w-6" />
                </div>
                <h2 class="text-xl font-bold">Upload File</h2>
                <p class="text-gray-400 text-sm mt-1">CSV, Excel, PDF, or text files</p>
            </div>
            
            <label class="block border-2 border-dashed border-white/10 rounded-2xl p-8 text-center hover:border-violet-500/50 transition-all cursor-pointer relative group hover:bg-violet-500/5">
                <Upload class="h-10 w-10 text-gray-500 mx-auto mb-4 group-hover:text-violet-400 group-hover:scale-110 transition-all" />
                <p class="text-sm text-gray-400 mb-2">Drag & drop or click to browse</p>
                <p class="text-xs text-gray-600">Max file size: 50MB • Multiple files supported</p>
                <input
                    type="file"
                    accept=".csv,.xlsx,.xls,.pdf,.txt,.epub"
                    bind:files={uploadFiles}
                    multiple
                    class="absolute inset-0 opacity-0 cursor-pointer"
                />
                {#if uploadFiles && uploadFiles.length > 0}
                    <div class="mt-4 space-y-2">
                        {#each Array.from(uploadFiles) as file}
                            <div class="bg-violet-500/20 text-violet-300 px-4 py-2 rounded-xl inline-flex items-center gap-2">
                                <FileText class="h-4 w-4" />
                                <span class="text-sm font-medium">{file.name}</span>
                            </div>
                        {/each}
                    </div>
                {/if}
            </label>
            
            <div class="flex gap-3 mt-6">
                <button
                    on:click={() => { showUploadModal = false; uploadFiles = null; }}
                    class="flex-1 px-4 py-3 border border-white/10 rounded-xl hover:bg-white/5 transition-all font-medium"
                >
                    Cancel
                </button>
                <button
                    on:click={handleUpload}
                    disabled={!uploadFiles || uploadFiles.length === 0 || isLoading}
                    class="flex-1 px-4 py-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-500 hover:to-fuchsia-500 disabled:opacity-40 disabled:cursor-not-allowed rounded-xl transition-all font-medium shadow-lg shadow-violet-500/20"
                >
                    {isLoading ? 'Uploading...' : uploadFiles && uploadFiles.length > 1 ? `Upload ${uploadFiles.length} Files` : 'Start Chat'}
                </button>
            </div>
        </div>
    </div>
{/if}


<style>
    textarea {
        field-sizing: content;
    }
    
    .scrollbar-thin::-webkit-scrollbar {
        width: 4px;
    }
    
    .scrollbar-thin::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .scrollbar-thin::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
    }
    
    .scrollbar-thin::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(20px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse-slow {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.05); }
    }
    
    @keyframes pulse-slower {
        0%, 100% { opacity: 0.2; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(1.08); }
    }
    
    @keyframes spin-slow {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .animate-fadeIn {
        animation: fadeIn 0.3s ease-out forwards;
    }
    
    .animate-slideUp {
        animation: slideUp 0.4s ease-out forwards;
    }
    
    .animate-pulse-slow {
        animation: pulse-slow 4s ease-in-out infinite;
    }
    
    .animate-pulse-slower {
        animation: pulse-slower 6s ease-in-out infinite;
    }
    
    .animate-spin-slow {
        animation: spin-slow 3s linear infinite;
    }
</style>
