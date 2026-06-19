<script setup>
const apiBase = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <header class="border-b border-slate-800">
      <div class="mx-auto flex max-w-4xl items-center justify-between px-6 py-4">
        <span class="text-lg font-semibold">Dev Landing</span>
        <span class="text-sm text-slate-400">API: {{ apiBase }}</span>
      </div>
    </header>

    <main class="mx-auto max-w-4xl px-6 py-16">
      <p class="text-sm uppercase tracking-wide text-emerald-400">Backend developer</p>
      <h1 class="mt-2 text-4xl font-bold">Landing page in progress</h1>
      <p class="mt-4 max-w-2xl text-slate-300">
        Stage 0 foundation is ready. The contact form will arrive in stage 4.
      </p>
    </main>
  </div>
</template>
