<script setup>
import { ref } from "vue";
import { profile } from "../data/profile.js";

const tab = ref("work");

function setTab(value) {
  tab.value = value;
}
</script>

<template>
  <section
    id="portfolio"
    class="py-20"
  >
    <span class="section-label">Портфолио</span>
    <h2 class="section-title mt-4">
      Проекты
    </h2>
    <p class="mt-4 max-w-3xl text-muted">
      Production-решения для TRASSIR VMS и pet-проекты с открытым кодом на GitHub.
    </p>

    <div class="portfolio-tabs mt-8">
      <button
        type="button"
        class="portfolio-tab"
        :class="{ 'portfolio-tab--active': tab === 'work' }"
        @click="setTab('work')"
      >
        Рабочие · DSSL
      </button>
      <button
        type="button"
        class="portfolio-tab"
        :class="{ 'portfolio-tab--active': tab === 'pet' }"
        @click="setTab('pet')"
      >
        Pet-проекты
      </button>
    </div>

    <div
      v-if="tab === 'work'"
      class="mt-8 space-y-8"
      data-testid="portfolio-work"
    >
      <article
        v-for="project in profile.portfolio.work"
        :key="project.id"
        class="glass card-accent rounded-2xl p-6 sm:p-8"
      >
        <div class="flex flex-wrap items-start justify-between gap-3 pl-3">
          <div>
            <span class="section-label text-[0.65rem]">{{ project.name }}</span>
            <h3 class="project-block__title mt-2">
              {{ project.title }}
            </h3>
            <p class="mt-1 text-sm text-accent">
              {{ project.platform }}
            </p>
          </div>
          <span
            v-if="project.private"
            class="badge-private"
          >Закрытый проект</span>
        </div>

        <p class="mt-5 pl-3 text-sm leading-relaxed text-body">
          {{ project.summary }}
        </p>

        <p class="project-block__group pl-3">
          Архитектура
        </p>
        <ul class="mt-2 space-y-2 pl-3">
          <li
            v-for="item in project.architecture"
            :key="item"
            class="flex items-start gap-3 text-sm leading-relaxed text-muted"
          >
            <span class="dot" />
            {{ item }}
          </li>
        </ul>

        <p class="project-block__group pl-3">
          Ключевые возможности
        </p>
        <ul class="mt-2 space-y-2 pl-3">
          <li
            v-for="item in project.features"
            :key="item"
            class="flex items-start gap-3 text-sm leading-relaxed text-muted"
          >
            <span class="dot" />
            {{ item }}
          </li>
        </ul>

        <ul class="mt-6 flex flex-wrap gap-2 pl-3">
          <li
            v-for="tech in project.stack"
            :key="tech"
            class="tag"
          >
            {{ tech }}
          </li>
        </ul>
      </article>
    </div>

    <div
      v-if="tab === 'pet'"
      class="mt-8 grid gap-6 lg:grid-cols-2"
      data-testid="portfolio-pet"
    >
      <article
        v-for="project in profile.portfolio.pet"
        :key="project.id"
        class="glass card-accent group rounded-2xl p-6 transition hover:-translate-y-0.5 sm:p-7"
      >
        <component
          :is="project.url ? 'a' : 'div'"
          :href="project.url"
          :target="project.url ? '_blank' : undefined"
          :rel="project.url ? 'noopener noreferrer' : undefined"
          class="card-link block pl-3"
        >
          <p class="text-xs font-semibold uppercase tracking-wider text-accent">
            {{ project.platform }}
          </p>
          <h3
            class="project-block__title mt-1 transition"
            :class="{ 'group-hover:text-accent': project.url }"
          >
            {{ project.title }}
          </h3>
          <p class="mt-3 text-sm leading-relaxed text-body">
            {{ project.summary }}
          </p>

          <ul class="mt-4 space-y-2">
            <li
              v-for="item in project.highlights"
              :key="item"
              class="flex items-start gap-3 text-sm leading-relaxed text-muted"
            >
              <span class="dot" />
              {{ item }}
            </li>
          </ul>

          <ul class="mt-5 flex flex-wrap gap-2">
            <li
              v-for="tech in project.stack"
              :key="tech"
              class="tag"
            >
              {{ tech }}
            </li>
          </ul>

          <p
            v-if="project.url"
            class="mt-4 text-xs font-medium text-accent"
          >
            GitHub →
          </p>
        </component>
      </article>
    </div>
  </section>
</template>
