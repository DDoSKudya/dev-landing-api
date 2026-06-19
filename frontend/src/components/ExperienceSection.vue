<script setup>
import { profile } from "../data/profile.js";
</script>

<template>
  <section
    id="experience"
    class="py-20"
  >
    <span class="section-label">Опыт работы</span>
    <h2 class="section-title mt-4">
      {{ profile.experienceYears }} в разработке
    </h2>
    <p class="mt-4 max-w-3xl text-muted">
      DSSL: видеонаблюдение, видеоаналитика, production и legacy.
    </p>

    <div class="timeline mt-12 space-y-8">
      <article
        v-for="job in profile.experience"
        :key="`${job.role}-${job.period}`"
        class="glass card-accent rounded-2xl p-6 sm:p-8"
      >
        <div class="flex flex-wrap items-start justify-between gap-4 pl-3">
          <div>
            <h3 class="text-xl font-semibold text-heading">
              {{ job.role }}
            </h3>
            <p class="mt-1 text-accent">
              <a
                v-if="job.url"
                :href="job.url"
                target="_blank"
                rel="noopener noreferrer"
                class="transition hover:opacity-80"
              >
                {{ job.company }}
              </a>
              <span v-else>{{ job.company }}</span>
              <span
                v-if="job.location"
                class="text-subtle"
              > · {{ job.location }}</span>
            </p>
          </div>
          <div class="text-right text-sm text-muted">
            <p>{{ job.period }}</p>
            <p class="mt-0.5 text-subtle">
              {{ job.duration }}
            </p>
          </div>
        </div>
        <ul class="mt-6 space-y-2 pl-3">
          <li
            v-for="item in job.bullets"
            :key="item"
            class="flex items-start gap-3 text-sm leading-relaxed text-muted"
          >
            <span class="dot" />
            {{ item }}
          </li>
        </ul>
      </article>
    </div>
  </section>
</template>
