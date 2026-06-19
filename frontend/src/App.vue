<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import AboutSection from "./components/AboutSection.vue";
import ContactForm from "./components/ContactForm.vue";
import ExperienceSection from "./components/ExperienceSection.vue";
import HeroSection from "./components/HeroSection.vue";
import PortfolioSection from "./components/PortfolioSection.vue";
import ThemeSwitcher from "./components/ThemeSwitcher.vue";
import { profile } from "./data/profile.js";

const scrolled = ref(false);

function onScroll() {
  scrolled.value = window.scrollY > 24;
}

onMounted(() => window.addEventListener("scroll", onScroll, { passive: true }));
onUnmounted(() => window.removeEventListener("scroll", onScroll));
</script>

<template>
  <div class="page-shell">
    <div
      class="page-bg"
      aria-hidden="true"
    >
      <div class="page-bg__mesh page-bg__mesh--1" />
      <div class="page-bg__mesh page-bg__mesh--2" />
      <div class="page-bg__mesh page-bg__mesh--3" />
      <div class="page-bg__grid" />
    </div>

    <div class="page-content">
      <header
        class="site-header fixed inset-x-0 top-0 z-50"
        :class="scrolled ? 'glass site-header--scrolled' : ''"
      >
        <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-4">
          <a
            href="#"
            class="header-brand flex min-w-0 items-center gap-2.5 font-semibold tracking-tight text-heading"
          >
            <span class="logo-badge">{{ profile.initials }}</span>
            <span class="truncate">{{ profile.shortName }}</span>
          </a>

          <nav class="hidden items-center gap-7 text-sm lg:flex">
            <a
              href="#about"
              class="nav-link"
            >Обо мне</a>
            <a
              href="#portfolio"
              class="nav-link"
            >Портфолио</a>
            <a
              href="#experience"
              class="nav-link"
            >Опыт</a>
            <a
              href="#contact"
              class="nav-link"
            >Контакты</a>
          </nav>

          <div class="flex items-center gap-3">
            <ThemeSwitcher />
            <a
              href="#contact"
              class="btn-primary hidden text-sm sm:inline-flex"
            >Связаться</a>
          </div>
        </div>
      </header>

      <main class="mx-auto max-w-6xl px-6 pt-28 pb-20">
        <HeroSection />
        <AboutSection />
        <PortfolioSection />
        <ExperienceSection />
        <ContactForm />
      </main>

      <footer
        class="border-t py-10 text-center text-sm text-subtle"
        style="border-color: var(--border)"
      >
        <p class="text-muted">
          © {{ new Date().getFullYear() }} {{ profile.fullName }}
        </p>
        <p class="mt-2 flex flex-wrap items-center justify-center gap-x-4 gap-y-1">
          <a
            :href="profile.contacts.github"
            target="_blank"
            rel="noopener noreferrer"
            class="nav-link"
          >
            GitHub
          </a>
          <a
            :href="profile.contacts.telegramUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="nav-link"
          >
            Telegram
          </a>
          <a
            :href="`mailto:${profile.contacts.email}`"
            class="nav-link"
          >
            {{ profile.contacts.email }}
          </a>
        </p>
      </footer>
    </div>
  </div>
</template>
