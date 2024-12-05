import { describe, it, expect } from "vitest";

import { assertUnreachable, isDefined, isNilOrEmpty } from "src/utils/typing";

describe("isDefined", () => {
  it("should return true for defined values", () => {
    expect(isDefined(0)).toBe(true);
    expect(isDefined(false)).toBe(true);
    expect(isDefined("")).toBe(true);
    expect(isDefined([])).toBe(true);
    expect(isDefined({})).toBe(true);
  });

  it("should return false for undefined", () => {
    expect(isDefined(undefined)).toBe(false);
  });
});

describe("assertUnreachable", () => {
  it("should throw an error when called", () => {
    expect(() => assertUnreachable("unexpected" as never)).toThrowError(
      "Didn't expect to get here"
    );
  });

  it("should handle an exhaustive case match", () => {
    type TestCase = "case1" | "case2";

    const handleCase = (value: TestCase) => {
      switch (value) {
        case "case1":
          return "Handled case1";
        case "case2":
          return "Handled case2";
        default:
          return assertUnreachable(value);
      }
    };

    expect(handleCase("case1")).toBe("Handled case1");
    expect(handleCase("case2")).toBe("Handled case2");
    expect(() => handleCase("unexpected" as TestCase)).toThrowError(
      "Didn't expect to get here"
    );
  });
});

describe("isNilOrEmpty", () => {
  it("should return true for null, undefined, or empty values", () => {
    expect(isNilOrEmpty(null)).toBe(true);
    expect(isNilOrEmpty(undefined)).toBe(true);
    expect(isNilOrEmpty([])).toBe(true);
    expect(isNilOrEmpty({})).toBe(true);
  });

  it("should return false for non-empty arrays", () => {
    expect(isNilOrEmpty([1, 2, 3])).toBe(false);
  });

  it("should return false for non-empty objects", () => {
    expect(isNilOrEmpty({ key: "value" })).toBe(false);
  });

  it("should return true for empty arrays or objects", () => {
    expect(isNilOrEmpty([])).toBe(true);
    expect(isNilOrEmpty({})).toBe(true);
  });
});
