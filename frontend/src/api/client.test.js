import { describe, expect, it, vi, beforeEach } from "vitest";
import { submitContact } from "./client.js";

describe("submitContact", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("returns body on success (happy path)", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ message: "Thank you!" }),
      }),
    );

    const result = await submitContact({ name: "Ivan" });
    expect(result.message).toBe("Thank you!");
  });

  it("throws validation error class with body on 422", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 422,
        headers: { get: () => null },
        json: async () => ({
          error: "validation_error",
          message: "Request validation failed",
          details: [],
        }),
      }),
    );

    await expect(submitContact({})).rejects.toMatchObject({
      status: 422,
      body: { error: "validation_error" },
    });
  });

  it("throws rate limit error with retryAfter on 429", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 429,
        headers: { get: (name) => (name === "Retry-After" ? "30" : null) },
        json: async () => ({
          error: "rate_limit_exceeded",
          message: "Too many requests.",
        }),
      }),
    );

    await expect(submitContact({})).rejects.toMatchObject({
      status: 429,
      retryAfter: "30",
    });
  });

  it("throws email delivery error on 502", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 502,
        headers: { get: () => null },
        json: async () => ({
          error: "email_delivery_failed",
          message: "Email failed",
        }),
      }),
    );

    await expect(submitContact({})).rejects.toMatchObject({
      status: 502,
      body: { error: "email_delivery_failed" },
    });
  });

  it("handles non-json error response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        headers: { get: () => null },
        json: async () => {
          throw new Error("invalid json");
        },
      }),
    );

    await expect(submitContact({})).rejects.toMatchObject({
      status: 500,
      message: "Request failed",
    });
  });
});
