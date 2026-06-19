import { describe, expect, it } from "vitest";
import { mount } from "@vue/test-utils";
import PortfolioSection from "./PortfolioSection.vue";

describe("PortfolioSection", () => {
  it("shows work projects by default", () => {
    const wrapper = mount(PortfolioSection);
    expect(wrapper.find('[data-testid="portfolio-work"]').exists()).toBe(true);
    expect(wrapper.find('[data-testid="portfolio-pet"]').exists()).toBe(false);
    expect(wrapper.text()).toContain("Face Match Passage Analysis");
  });

  it("switches to pet projects tab", async () => {
    const wrapper = mount(PortfolioSection);
    const tabs = wrapper.findAll(".portfolio-tab");
    await tabs[1].trigger("click");
    expect(wrapper.find('[data-testid="portfolio-pet"]').exists()).toBe(true);
    expect(wrapper.find('[data-testid="portfolio-work"]').exists()).toBe(false);
    expect(wrapper.text()).toContain("Spend Ledger");
  });
});
