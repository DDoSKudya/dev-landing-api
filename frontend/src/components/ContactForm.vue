<script setup>
import { reactive, ref } from "vue";
import { submitContact } from "../api/client.js";
import { profile } from "../data/profile.js";
import { mapValidationErrors } from "../utils/validationErrors.js";

const contactLinks = [
  {
    label: "Email",
    value: profile.contacts.email,
    href: `mailto:${profile.contacts.email}`,
    icon: "@",
    external: false,
  },
  {
    label: "Телефон",
    value: profile.contacts.phoneDisplay,
    href: `tel:${profile.contacts.phone}`,
    icon: "☎",
    external: false,
  },
  {
    label: "Telegram",
    value: profile.contacts.telegram,
    href: profile.contacts.telegramUrl,
    icon: "TG",
    external: true,
  },
  {
    label: "GitHub",
    value: "DDoSKudya",
    href: profile.contacts.github,
    icon: "GH",
    external: true,
  },
  {
    label: "Сетка",
    value: "set.ki",
    href: profile.contacts.setka,
    icon: "S",
    external: true,
  },
];

const form = reactive({
  name: "",
  phone: "",
  email: "",
  comment: "",
});

const loading = ref(false);
const success = ref("");
const error = ref("");
const fieldErrors = ref({});

function resetMessages() {
  success.value = "";
  error.value = "";
  fieldErrors.value = {};
}

async function onSubmit() {
  resetMessages();
  loading.value = true;

  try {
    const result = await submitContact({ ...form });
    success.value = result.message || "Сообщение отправлено.";
    form.name = "";
    form.phone = "";
    form.email = "";
    form.comment = "";
  } catch (err) {
    if (err.status === 422) {
      error.value = err.body?.message || "Проверьте поля формы.";
      fieldErrors.value = mapValidationErrors(err.body?.details);
    } else if (err.status === 429) {
      const retry = err.retryAfter ? ` Повторите через ${err.retryAfter} сек.` : "";
      error.value = (err.body?.message || "Слишком много запросов.") + retry;
    } else if (err.status === 502) {
      error.value =
        "Заявка сохранена, но письмо не отправилось. Я свяжусь с вами по указанному email.";
    } else {
      error.value = err.body?.message || "Не удалось отправить форму. Попробуйте позже.";
    }
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <section
    id="contact"
    class="py-20"
  >
    <div class="grid gap-12 lg:grid-cols-5">
      <div class="lg:col-span-2">
        <span class="section-label">Контакты</span>
        <h2 class="section-title mt-4">
          Свяжитесь со мной
        </h2>
        <p class="mt-4 leading-relaxed text-muted">
          Открыт к предложениям о полной занятости. Формат — удалённо или гибрид.
          Предпочитаемый способ связи — email.
        </p>

        <ul class="mt-8 space-y-3">
          <li
            v-for="link in contactLinks"
            :key="link.label"
          >
            <a
              :href="link.href"
              :target="link.external ? '_blank' : undefined"
              :rel="link.external ? 'noopener noreferrer' : undefined"
              class="contact-link"
            >
              <span class="contact-link__icon">{{ link.icon }}</span>
              <span>
                <span class="contact-link__label">{{ link.label }}</span>
                <span class="contact-link__value">{{ link.value }}</span>
              </span>
            </a>
          </li>
        </ul>
      </div>

      <form
        class="glass card-accent rounded-2xl p-6 sm:p-8 lg:col-span-3"
        @submit.prevent="onSubmit"
      >
        <p class="mb-6 pl-3 text-sm text-muted">
          Или оставьте заявку через форму — отвечу в ближайшее время.
        </p>

        <div class="grid gap-5 pl-3 sm:grid-cols-2">
          <div class="sm:col-span-2">
            <label
              class="mb-2 block text-sm font-medium text-body"
              for="name"
            >Имя</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              minlength="2"
              placeholder="Ваше имя"
              class="input-field"
            >
            <p
              v-if="fieldErrors.name"
              class="mt-1.5 text-sm alert-error inline-block px-2 py-1"
            >
              {{ fieldErrors.name }}
            </p>
          </div>

          <div>
            <label
              class="mb-2 block text-sm font-medium text-body"
              for="phone"
            >Телефон</label>
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              required
              placeholder="+79991234567"
              class="input-field"
            >
            <p
              v-if="fieldErrors.phone"
              class="mt-1.5 text-sm alert-error inline-block px-2 py-1"
            >
              {{ fieldErrors.phone }}
            </p>
          </div>

          <div>
            <label
              class="mb-2 block text-sm font-medium text-body"
              for="email"
            >Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              placeholder="you@example.com"
              class="input-field"
            >
            <p
              v-if="fieldErrors.email"
              class="mt-1.5 text-sm alert-error inline-block px-2 py-1"
            >
              {{ fieldErrors.email }}
            </p>
          </div>

          <div class="sm:col-span-2">
            <label
              class="mb-2 block text-sm font-medium text-body"
              for="comment"
            >
              Комментарий
            </label>
            <textarea
              id="comment"
              v-model="form.comment"
              required
              minlength="10"
              rows="4"
              placeholder="Расскажите о вакансии или проекте..."
              class="input-field resize-none"
            />
            <p
              v-if="fieldErrors.comment"
              class="mt-1.5 text-sm alert-error inline-block px-2 py-1"
            >
              {{ fieldErrors.comment }}
            </p>
          </div>
        </div>

        <div
          v-if="success"
          class="alert-success mt-5 px-4 py-3 text-sm"
        >
          {{ success }}
        </div>
        <div
          v-if="error"
          class="alert-error mt-5 px-4 py-3 text-sm"
        >
          {{ error }}
        </div>

        <button
          type="submit"
          class="btn-primary mt-6 w-full sm:ml-3 sm:w-auto"
          :disabled="loading"
        >
          <span
            v-if="loading"
            class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-current/30 border-t-current"
          />
          {{ loading ? "Отправка…" : "Отправить сообщение" }}
        </button>
      </form>
    </div>
  </section>
</template>

<style scoped>
.contact-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-radius: 0.85rem;
  border: 1px solid var(--border);
  background: var(--glass-hover);
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: var(--body);
  transition: transform 0.15s ease, border-color 0.2s, background 0.2s, color 0.2s;
  -webkit-tap-highlight-color: transparent;
}

.contact-link:hover {
  border-color: var(--accent-ring);
  color: var(--heading);
}

.contact-link:active {
  transform: scale(0.98);
  background: var(--label-bg);
  border-color: var(--accent);
}

.contact-link__icon {
  display: flex;
  height: 2.25rem;
  width: 2.25rem;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  border-radius: 0.65rem;
  background: var(--label-bg);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--accent-text);
}

.contact-link__label {
  display: block;
  font-size: 0.7rem;
  color: var(--subtle);
}

.contact-link__value {
  display: block;
  font-weight: 500;
  color: var(--heading);
}
</style>
