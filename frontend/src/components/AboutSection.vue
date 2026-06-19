<script setup>
import { profile } from "../data/profile.js";
</script>

<template>
  <section
    id="about"
    class="animate-fade-up-delay py-20"
  >
    <span class="section-label">Обо мне</span>
    <h2 class="section-title mt-4">
      Backend, данные и развитие систем
    </h2>
    <p class="mt-4 max-w-3xl text-lg leading-relaxed text-muted">
      Фокус на данных, API и развитии существующих систем. Pet-проекты — практика
      FastAPI, Docker и современного Python 3.
    </p>

    <div
      id="skills"
      class="mt-12 grid gap-5 sm:grid-cols-2"
    >
      <article
        v-for="skill in profile.skills"
        :key="skill.title"
        class="glass card-accent rounded-2xl p-6 transition hover:-translate-y-0.5"
      >
        <h3 class="text-lg font-semibold text-heading">
          {{ skill.title }}
        </h3>
        <ul class="mt-4 flex flex-wrap gap-2">
          <li
            v-for="item in skill.items"
            :key="item"
            class="tag"
          >
            {{ item }}
          </li>
        </ul>
      </article>
    </div>

    <div class="mt-8 flex flex-wrap gap-6 text-sm text-muted">
      <p>
        <span class="text-subtle">Образование:</span>
        {{ profile.education.fullUniversity }}, {{ profile.education.degree }}
        ({{ profile.education.year }})
      </p>
      <p>
        <span class="text-subtle">Языки:</span>
        <span
          v-for="(lang, i) in profile.languages"
          :key="lang.name"
        >
          {{ lang.name }} — {{ lang.level }}<span v-if="i < profile.languages.length - 1">, </span>
        </span>
      </p>
    </div>
  </section>
</template>
