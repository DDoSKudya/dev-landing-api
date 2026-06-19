import { describe, expect, it } from "vitest";
import { mapValidationErrors } from "./validationErrors.js";

describe("mapValidationErrors", () => {
  it("maps pydantic loc tail to field message", () => {
    const details = [
      { loc: ["body", "email"], msg: "value is not a valid email" },
      { loc: ["body", "name"], msg: "String should have at least 2 characters" },
    ];

    expect(mapValidationErrors(details)).toEqual({
      email: "value is not a valid email",
      name: "String should have at least 2 characters",
    });
  });

  it("returns empty object for missing details", () => {
    expect(mapValidationErrors(null)).toEqual({});
    expect(mapValidationErrors([])).toEqual({});
  });

  it("skips items without field in loc", () => {
    const details = [{ loc: [], msg: "root error" }];
    expect(mapValidationErrors(details)).toEqual({});
  });
});
