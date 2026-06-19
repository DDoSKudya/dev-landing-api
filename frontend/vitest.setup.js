import { beforeEach } from "vitest";

beforeEach(() => {
  localStorage.clear();
  document.documentElement.dataset.theme = "dark";
  document.documentElement.dataset.accent = "cyan";
});
