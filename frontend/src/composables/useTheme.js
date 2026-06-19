import { ref, watch } from "vue";

const STORAGE_KEY = "dev-landing-theme";

const mode = ref("dark");
const accent = ref("cyan");

const accents = [
  { id: "cyan", label: "Cyan" },
  { id: "violet", label: "Violet" },
  { id: "emerald", label: "Emerald" },
];

function loadStored() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    if (saved.mode === "light" || saved.mode === "dark") {
      mode.value = saved.mode;
    }
    if (accents.some((item) => item.id === saved.accent)) {
      accent.value = saved.accent;
    }
  } catch {
    /* ignore */
  }
}

function applyTheme() {
  document.documentElement.dataset.theme = mode.value;
  document.documentElement.dataset.accent = accent.value;
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({ mode: mode.value, accent: accent.value }),
  );
}

loadStored();
applyTheme();

watch([mode, accent], applyTheme);

export function useTheme() {
  function toggleMode() {
    mode.value = mode.value === "dark" ? "light" : "dark";
  }

  function setAccent(id) {
    accent.value = id;
  }

  return { mode, accent, accents, toggleMode, setAccent };
}
