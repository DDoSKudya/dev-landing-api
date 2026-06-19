import { describe, expect, it } from "vitest";
import { mount } from "@vue/test-utils";
import ThemeSwitcher from "./ThemeSwitcher.vue";

describe("ThemeSwitcher", () => {
  it("toggles theme mode on button click", async () => {
    const wrapper = mount(ThemeSwitcher);
    const html = document.documentElement;
    const initial = html.dataset.theme;

    await wrapper.find(".theme-toggle").trigger("click");
    expect(html.dataset.theme).not.toBe(initial);

    await wrapper.find(".theme-toggle").trigger("click");
    expect(html.dataset.theme).toBe(initial);
  });

  it("sets accent on dot click", async () => {
    const wrapper = mount(ThemeSwitcher);
    const violet = wrapper.find('[data-accent-choice="violet"]');
    await violet.trigger("click");
    expect(document.documentElement.dataset.accent).toBe("violet");
  });
});
