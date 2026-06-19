<script setup>
import { useTheme } from "../composables/useTheme.js";

const { mode, accent, accents, toggleMode, setAccent } = useTheme();
</script>

<template>
  <div class="theme-switcher">
    <button
      type="button"
      class="theme-toggle"
      :aria-label="mode === 'dark' ? 'Светлая тема' : 'Тёмная тема'"
      @click="toggleMode"
    >
      <span
        v-if="mode === 'dark'"
        aria-hidden="true"
      >☀</span>
      <span
        v-else
        aria-hidden="true"
      >☾</span>
    </button>
    <div
      class="accent-picker"
      role="group"
      aria-label="Цветовой акцент"
    >
      <button
        v-for="item in accents"
        :key="item.id"
        type="button"
        class="accent-dot"
        :class="{ 'accent-dot--active': accent === item.id }"
        :data-accent-choice="item.id"
        :aria-label="item.label"
        :aria-pressed="accent === item.id"
        @click="setAccent(item.id)"
      />
    </div>
  </div>
</template>
