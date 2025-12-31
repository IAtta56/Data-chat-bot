<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import {
    ArrowRight,
    BarChart3,
    MessageSquare,
    ShieldCheck,
    Sparkles,
    Zap,
    Brain,
    TrendingUp,
    FileSearch,
    Wand2,
    Download,
    Users,
    Globe,
    Cpu,
    LineChart,
    PieChart,
    Database,
    Lock,
    Rocket,
    Star,
    ChevronRight,
    Play,
    CheckCircle,
    Github,
    Heart,
  } from "lucide-svelte";
  import { onMount } from "svelte";

  let mounted = false;
  let activeFeature = 0;
  let statsVisible = false;

  const stats = [
    { value: "10M+", label: "Data Points Analyzed", icon: Database },
    { value: "500K+", label: "Visualizations Created", icon: PieChart },
    { value: "99.9%", label: "Uptime Guaranteed", icon: Zap },
    { value: "50+", label: "AI Models Supported", icon: Brain },
  ];

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms analyze your data patterns, anomalies, and correlations in seconds.",
      color: "from-purple-500 to-indigo-500",
      bgColor: "bg-purple-500/20",
      borderColor: "border-purple-500/30"
    },
    {
      icon: LineChart,
      title: "Smart Visualizations",
      description: "Automatically generate beautiful, interactive charts and graphs tailored to your data type.",
      color: "from-blue-500 to-cyan-500",
      bgColor: "bg-blue-500/20",
      borderColor: "border-blue-500/30"
    },
    {
      icon: TrendingUp,
      title: "Trend Prediction",
      description: "Forecast future trends using predictive analytics and time-series analysis.",
      color: "from-green-500 to-emerald-500",
      bgColor: "bg-green-500/20",
      borderColor: "border-green-500/30"
    },
    {
      icon: Wand2,
      title: "Auto Data Cleaning",
      description: "Automatically detect and fix missing values, outliers, and formatting issues.",
      color: "from-orange-500 to-amber-500",
      bgColor: "bg-orange-500/20",
      borderColor: "border-orange-500/30"
    },
    {
      icon: FileSearch,
      title: "Natural Language Queries",
      description: "Ask questions in plain English and get instant insights without writing code.",
      color: "from-pink-500 to-rose-500",
      bgColor: "bg-pink-500/20",
      borderColor: "border-pink-500/30"
    },
    {
      icon: Download,
      title: "Export & Share",
      description: "Export reports as PDF, CSV, or share interactive dashboards with your team.",
      color: "from-teal-500 to-cyan-500",
      bgColor: "bg-teal-500/20",
      borderColor: "border-teal-500/30"
    },
    {
      icon: Globe,
      title: "Multi-Provider AI",
      description: "Connect to Groq, OpenAI, Anthropic, Google AI, or use local Ollama models.",
      color: "from-violet-500 to-purple-500",
      bgColor: "bg-violet-500/20",
      borderColor: "border-violet-500/30"
    },
    {
      icon: Lock,
      title: "Enterprise Security",
      description: "Bank-level encryption, SOC2 compliance, and complete data privacy.",
      color: "from-red-500 to-orange-500",
      bgColor: "bg-red-500/20",
      borderColor: "border-red-500/30"
    },
  ];

  const useCases = [
    { title: "Sales Analytics", desc: "Track revenue, forecast sales, identify top performers" },
    { title: "Customer Insights", desc: "Analyze behavior, segment users, predict churn" },
    { title: "Financial Analysis", desc: "Budget tracking, expense analysis, ROI calculation" },
    { title: "Marketing Metrics", desc: "Campaign performance, conversion rates, attribution" },
    { title: "Operations Data", desc: "Process optimization, resource allocation, efficiency" },
    { title: "Research Data", desc: "Statistical analysis, hypothesis testing, data mining" },
  ];

  onMount(() => {
    mounted = true;
    
    // Animate stats on scroll
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          statsVisible = true;
        }
      });
    }, { threshold: 0.5 });

    const statsSection = document.getElementById('stats-section');
    if (statsSection) observer.observe(statsSection);

    // Rotate features
    const interval = setInterval(() => {
      activeFeature = (activeFeature + 1) % features.length;
    }, 3000);

    return () => {
      clearInterval(interval);
      observer.disconnect();
    };
  });
</script>

<svelte:head>
  <title>DataChat AI - Transform Your Data Into Insights</title>
</svelte:head>

<div class="flex flex-col min-h-screen bg-slate-950 overflow-x-hidden selection:bg-purple-500/30 selection:text-white">
  <!-- Animated Background -->
  <div class="fixed inset-0 z-0 pointer-events-none overflow-hidden">
    <!-- Gradient orbs -->
    <div class="absolute top-0 -left-40 w-[600px] h-[600px] bg-purple-600/20 rounded-full blur-[150px] animate-pulse"></div>
    <div class="absolute top-1/3 -right-40 w-[500px] h-[500px] bg-blue-600/15 rounded-full blur-[150px] animate-pulse" style="animation-delay: 1s;"></div>
    <div class="absolute bottom-0 left-1/3 w-[700px] h-[700px] bg-indigo-600/10 rounded-full blur-[180px] animate-pulse" style="animation-delay: 2s;"></div>
    <div class="absolute top-2/3 right-1/4 w-[400px] h-[400px] bg-pink-600/10 rounded-full blur-[120px] animate-pulse" style="animation-delay: 0.5s;"></div>
    
    <!-- Grid pattern -->
    <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4wMikiIGQ9Ik0wIDBoNjB2NjBIMHoiLz48cGF0aCBkPSJNNjAgMEgwdjYwaDYwVjB6TTU5IDFIMXY1OGg1OFYxeiIgZmlsbD0icmdiYSgyNTUsMjU1LDI1NSwwLjAzKSIvPjwvZz48L3N2Zz4=')] opacity-40"></div>
  </div>

  <!-- Navigation -->
  <nav class="relative z-50 flex items-center justify-between px-6 py-5 max-w-7xl mx-auto w-full">
    <a href="/" class="flex items-center space-x-3 group">
      <div class="relative">
        <div class="absolute inset-0 bg-gradient-to-r from-purple-500 to-indigo-600 rounded-xl blur opacity-75 group-hover:opacity-100 transition duration-500 group-hover:scale-110"></div>
        <div class="relative bg-slate-900 p-2.5 rounded-xl border border-white/10 group-hover:border-purple-500/50 transition-all">
          <Sparkles class="h-6 w-6 text-purple-400" />
        </div>
      </div>
      <div>
        <span class="text-xl font-bold text-white">DataChat</span>
        <span class="text-xs text-purple-400 block -mt-1">AI Analytics</span>
      </div>
    </a>

    <div class="hidden md:flex items-center space-x-8">
      <a href="#features" class="text-slate-400 hover:text-white transition-colors text-sm font-medium hover:scale-105 transform">Features</a>
      <a href="#use-cases" class="text-slate-400 hover:text-white transition-colors text-sm font-medium hover:scale-105 transform">Use Cases</a>
      <a href="#stats" class="text-slate-400 hover:text-white transition-colors text-sm font-medium hover:scale-105 transform">Stats</a>

      <div class="flex items-center space-x-3 pl-6 border-l border-white/10">
        <Button variant="ghost" href="/login" class="text-white hover:bg-white/10 hover:scale-105 transition-all">
          Log in
        </Button>
        <Button href="/register" class="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white border-0 shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 hover:scale-105 transition-all">
          Get Started Free
          <ArrowRight class="h-4 w-4 ml-2" />
        </Button>
      </div>
    </div>
  </nav>

  <main class="flex-1 relative z-10">
    <!-- Hero Section -->
    <section class="py-16 px-6 text-center max-w-6xl mx-auto mt-8">
      <!-- Badge -->
      <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-purple-500/10 to-indigo-500/10 border border-purple-500/20 text-purple-300 text-sm font-medium mb-8 hover:border-purple-500/40 transition-all cursor-default animate-bounce" style="animation-duration: 2s;">
        <Rocket class="h-4 w-4" />
        <span>Version 2.0 is here!</span>
        <span class="bg-purple-500/20 px-2 py-0.5 rounded-full text-xs">New</span>
      </div>

      <!-- Main Headline -->
      <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight text-white leading-[1.1] mb-6">
        Transform Your Data Into
        <span class="block mt-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-indigo-400 animate-pulse" style="animation-duration: 3s;">
          Actionable Insights
        </span>
      </h1>

      <p class="text-lg md:text-xl text-slate-400 max-w-3xl mx-auto leading-relaxed mb-10">
        Upload your datasets and ask questions in natural language. Our AI analyzes patterns, 
        creates visualizations, predicts trends, and generates reports — all in seconds.
      </p>

      <!-- CTA Buttons -->
      <div class="flex flex-col sm:flex-row justify-center gap-4 mb-16">
        <Button href="/register" class="h-14 px-8 text-lg bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white border-0 shadow-xl shadow-purple-500/30 hover:shadow-purple-500/50 hover:scale-105 transition-all group">
          Start Analyzing Free
          <ArrowRight class="h-5 w-5 ml-2 group-hover:translate-x-1 transition-transform" />
        </Button>
        <Button variant="outline" href="#demo" class="h-14 px-8 text-lg border-white/20 text-white hover:bg-white/5 hover:border-purple-500/50 group">
          <Play class="h-5 w-5 mr-2 group-hover:scale-110 transition-transform" />
          Watch Demo
        </Button>
      </div>

      <!-- Feature Pills -->
      <div class="flex flex-wrap justify-center gap-3 mb-16">
        {#each ["No Credit Card", "Free Forever Plan", "5 Min Setup", "Multi-Provider AI"] as pill}
          <div class="flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-slate-300 text-sm">
            <CheckCircle class="h-4 w-4 text-green-400" />
            {pill}
          </div>
        {/each}
      </div>

      <!-- Dashboard Preview -->
      <div class="relative group max-w-5xl mx-auto">
        <!-- Glow effect -->
        <div class="absolute -inset-4 bg-gradient-to-r from-purple-600/20 via-pink-600/20 to-indigo-600/20 rounded-2xl blur-xl opacity-50 group-hover:opacity-75 transition duration-500"></div>
        
        <div class="relative rounded-2xl border border-white/10 bg-slate-900/80 shadow-2xl backdrop-blur-sm overflow-hidden ring-1 ring-white/10 transform transition-all duration-500 hover:scale-[1.02] hover:border-purple-500/30">
          <!-- Window header -->
          <div class="h-12 border-b border-white/10 bg-slate-900/80 flex items-center px-4 gap-4">
            <div class="flex gap-2">
              <div class="w-3 h-3 rounded-full bg-red-500 hover:bg-red-400 transition-colors cursor-pointer"></div>
              <div class="w-3 h-3 rounded-full bg-yellow-500 hover:bg-yellow-400 transition-colors cursor-pointer"></div>
              <div class="w-3 h-3 rounded-full bg-green-500 hover:bg-green-400 transition-colors cursor-pointer"></div>
            </div>
            <div class="flex-1 h-7 bg-slate-800 rounded-lg flex items-center px-3 text-xs text-slate-500 font-mono">
              <Lock class="h-3 w-3 mr-2 text-green-400" />
              datachat.ai/dashboard
            </div>
          </div>

          <!-- Mock Dashboard -->
          <div class="p-6 bg-gradient-to-br from-slate-900 via-slate-900 to-purple-900/20">
            <div class="grid grid-cols-12 gap-4">
              <!-- Sidebar mockup -->
              <div class="col-span-3 space-y-3">
                <div class="h-10 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-lg flex items-center justify-center text-white text-sm font-medium">
                  + New Analysis
                </div>
                <div class="h-8 bg-slate-800/50 rounded-lg"></div>
                <div class="h-8 bg-purple-500/20 border border-purple-500/30 rounded-lg"></div>
                <div class="h-8 bg-slate-800/50 rounded-lg"></div>
              </div>
              
              <!-- Main content mockup -->
              <div class="col-span-9 space-y-4">
                <!-- Chat message -->
                <div class="flex gap-3">
                  <div class="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center">
                    <Sparkles class="h-4 w-4 text-white" />
                  </div>
                  <div class="flex-1 bg-slate-800/50 rounded-lg p-4 text-left">
                    <p class="text-sm text-slate-300">Analyzing your sales data... Found 3 key insights:</p>
                    <ul class="mt-2 space-y-1 text-sm text-slate-400">
                      <li class="flex items-center gap-2"><TrendingUp class="h-3 w-3 text-green-400" /> Revenue up 24% this quarter</li>
                      <li class="flex items-center gap-2"><Star class="h-3 w-3 text-yellow-400" /> Top product: Premium Plan ($45K)</li>
                      <li class="flex items-center gap-2"><Users class="h-3 w-3 text-blue-400" /> Customer retention: 94%</li>
                    </ul>
                  </div>
                </div>
                
                <!-- Chart placeholder -->
                <div class="h-40 bg-gradient-to-br from-slate-800/50 to-purple-900/20 rounded-lg border border-white/5 flex items-center justify-center">
                  <div class="flex items-end gap-2 h-24">
                    {#each [40, 65, 45, 80, 55, 90, 70, 85] as height}
                      <div class="w-6 bg-gradient-to-t from-purple-600 to-indigo-400 rounded-t transition-all hover:from-purple-500 hover:to-indigo-300" style="height: {height}%;"></div>
                    {/each}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section id="stats" class="py-20 relative">
      <div id="stats-section" class="max-w-6xl mx-auto px-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          {#each stats as stat, i}
            <div class="relative group">
              <div class="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-indigo-600/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div class="relative p-6 rounded-2xl bg-slate-900/50 border border-white/10 hover:border-purple-500/30 transition-all text-center group-hover:scale-105 transform duration-300">
                <svelte:component this={stat.icon} class="h-8 w-8 mx-auto mb-3 text-purple-400" />
                <div class="text-3xl md:text-4xl font-bold text-white mb-1 {statsVisible ? 'animate-pulse' : ''}" style="animation-duration: 0.5s;">
                  {stat.value}
                </div>
                <div class="text-sm text-slate-400">{stat.label}</div>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-24 relative">
      <div class="max-w-6xl mx-auto px-6">
        <div class="text-center mb-16">
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-sm font-medium mb-4">
            <Cpu class="h-4 w-4" />
            Powerful Features
          </div>
          <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
            Everything You Need to 
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">Analyze Data</span>
          </h2>
          <p class="text-lg text-slate-400 max-w-2xl mx-auto">
            From simple queries to complex analytics, DataChat has you covered with AI-powered tools.
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {#each features as feature, i}
            <div 
              class="group relative p-6 rounded-2xl bg-slate-900/50 border border-white/10 hover:border-purple-500/30 transition-all duration-300 hover:scale-105 cursor-default {activeFeature === i ? 'ring-2 ring-purple-500/50' : ''}"
            >
              <!-- Hover glow -->
              <div class="absolute inset-0 bg-gradient-to-r {feature.color} opacity-0 group-hover:opacity-10 rounded-2xl transition-opacity"></div>
              
              <div class="relative">
                <div class="h-12 w-12 {feature.bgColor} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform ring-1 {feature.borderColor}">
                  <svelte:component this={feature.icon} class="h-6 w-6 text-white" />
                </div>
                <h3 class="text-lg font-bold text-white mb-2">{feature.title}</h3>
                <p class="text-sm text-slate-400 leading-relaxed">{feature.description}</p>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </section>

    <!-- Use Cases Section -->
    <section id="use-cases" class="py-24 relative">
      <div class="max-w-6xl mx-auto px-6">
        <div class="text-center mb-16">
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-sm font-medium mb-4">
            <BarChart3 class="h-4 w-4" />
            Use Cases
          </div>
          <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
            Built For Every
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Industry</span>
          </h2>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {#each useCases as useCase, i}
            <div class="group p-6 rounded-2xl bg-gradient-to-br from-slate-900/80 to-slate-800/50 border border-white/10 hover:border-indigo-500/30 transition-all duration-300 hover:scale-105 hover:-translate-y-1">
              <div class="flex items-start gap-4">
                <div class="h-10 w-10 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white font-bold shrink-0">
                  {i + 1}
                </div>
                <div>
                  <h3 class="text-lg font-bold text-white mb-1">{useCase.title}</h3>
                  <p class="text-sm text-slate-400">{useCase.desc}</p>
                </div>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-24 relative">
      <div class="max-w-4xl mx-auto px-6">
        <div class="relative rounded-3xl overflow-hidden">
          <!-- Background gradient -->
          <div class="absolute inset-0 bg-gradient-to-r from-purple-600 via-indigo-600 to-purple-600 animate-pulse" style="animation-duration: 4s;"></div>
          <div class="absolute inset-0 bg-gradient-to-b from-transparent via-black/20 to-black/40"></div>
          
          <!-- Content -->
          <div class="relative p-12 md:p-16 text-center">
            <Sparkles class="h-12 w-12 mx-auto mb-6 text-white/80" />
            <h2 class="text-3xl md:text-4xl font-bold text-white mb-4">
              Ready to Transform Your Data?
            </h2>
            <p class="text-lg text-white/80 mb-8 max-w-xl mx-auto">
              Join thousands of analysts and businesses using DataChat to unlock insights faster than ever.
            </p>
            <Button href="/register" class="h-14 px-10 text-lg bg-white text-purple-600 hover:bg-white/90 shadow-xl hover:scale-105 transition-all group font-bold">
              Get Started Free
              <ChevronRight class="h-5 w-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </Button>
          </div>
        </div>
      </div>
    </section>

    <!-- Trusted By Section -->
    <section class="py-16 border-t border-white/5">
      <div class="max-w-6xl mx-auto px-6 text-center">
        <p class="text-slate-500 text-sm mb-8">Trusted by data teams worldwide</p>
        <div class="flex flex-wrap justify-center items-center gap-8 md:gap-12 opacity-50">
          {#each ["TechCorp", "DataFlow", "AnalyticsPro", "InsightAI", "MetricsHub"] as company}
            <div class="text-xl md:text-2xl font-bold text-slate-600">{company}</div>
          {/each}
        </div>
      </div>
    </section>
  </main>
</div>

<style>
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
  }
  
  :global(.animate-float) {
    animation: float 6s ease-in-out infinite;
  }
</style>
