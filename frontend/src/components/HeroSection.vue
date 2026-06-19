<script setup>
import { profile } from "../data/profile.js";
</script>

<template>
  <section class="animate-fade-up py-16 sm:py-24">
    <div class="grid items-center gap-12 lg:grid-cols-[1.1fr_0.9fr]">
      <div>
        <span class="section-label">{{ profile.title }}</span>

        <h1 class="mt-6 text-4xl font-bold leading-[1.08] tracking-tight text-heading sm:text-6xl">
          {{ profile.shortName }}
        </h1>

        <p class="mt-4 text-lg text-body">
          {{ profile.location }} · {{ profile.workFormat }} · {{ profile.experienceYears }}
        </p>

        <p class="mt-6 max-w-xl text-lg leading-relaxed text-muted">
          {{ profile.tagline }}
        </p>

        <div class="mt-10 flex flex-wrap gap-4">
          <a
            href="#contact"
            class="btn-primary"
          >Написать мне</a>
          <a
            href="#portfolio"
            class="btn-secondary"
          >Смотреть проекты</a>
        </div>
      </div>

      <div class="hero-float glass card-accent rounded-2xl p-6 sm:p-8">
        <p class="hero-terminal">
          <span class="hero-terminal__prompt">$</span> curl /api/health<br>
          <span class="text-accent">{ "status": "ok", "db": "connected" }</span><br><br>
          <span class="hero-terminal__prompt">$</span> python -m backend.events<br>
          <span class="text-muted">→ EventManager → FMPA → SQLite</span><br><br>
          <span class="hero-terminal__prompt">$</span> deploy --stack docker<br>
          <span class="text-muted">→ nginx · fastapi · vue · mailhog</span>
        </p>
      </div>
    </div>

    <div class="mt-16 grid gap-4 sm:grid-cols-3">
      <div
        v-for="item in profile.highlights"
        :key="item.title"
        class="glass card-accent rounded-2xl p-5"
      >
        <p class="text-2xl font-bold gradient-text">
          {{ item.title }}
        </p>
        <p class="mt-1 text-sm text-muted">
          {{ item.subtitle }}
        </p>
      </div>
    </div>
  </section>
</template>
