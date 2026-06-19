import { describe, expect, it, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import ContactForm from "./ContactForm.vue";
import * as client from "../api/client.js";

describe("ContactForm", () => {
  it("shows success message after submit", async () => {
    vi.spyOn(client, "submitContact").mockResolvedValue({
      message: "Сообщение отправлено.",
    });

    const wrapper = mount(ContactForm);
    await wrapper.find("#name").setValue("Ivan Petrov");
    await wrapper.find("#phone").setValue("+79991234567");
    await wrapper.find("#email").setValue("ivan@example.com");
    await wrapper.find("#comment").setValue("Long enough comment.");
    await wrapper.find("form").trigger("submit.prevent");
    await flushPromises();
    expect(wrapper.text()).toContain("Сообщение отправлено.");
  });

  it("maps 422 validation errors to fields", async () => {
    vi.spyOn(client, "submitContact").mockRejectedValue({
      status: 422,
      body: {
        message: "Request validation failed",
        details: [{ loc: ["body", "email"], msg: "invalid email" }],
      },
    });

    const wrapper = mount(ContactForm);
    await wrapper.find("#name").setValue("Ivan Petrov");
    await wrapper.find("#phone").setValue("+79991234567");
    await wrapper.find("#email").setValue("bad");
    await wrapper.find("#comment").setValue("Long enough comment.");
    await wrapper.find("form").trigger("submit.prevent");
    await flushPromises();
    expect(wrapper.text()).toContain("invalid email");
  });

  it("shows rate limit message with retry hint", async () => {
    vi.spyOn(client, "submitContact").mockRejectedValue({
      status: 429,
      body: { message: "Too many requests." },
      retryAfter: "15",
    });

    const wrapper = mount(ContactForm);
    await wrapper.find("#name").setValue("Ivan Petrov");
    await wrapper.find("#phone").setValue("+79991234567");
    await wrapper.find("#email").setValue("ivan@example.com");
    await wrapper.find("#comment").setValue("Long enough comment.");
    await wrapper.find("form").trigger("submit.prevent");
    await flushPromises();
    expect(wrapper.text()).toContain("15");
  });
});
