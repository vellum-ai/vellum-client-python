import { describe, it, expect } from "vitest";

import { assertUnreachable, isDefined, isNilOrEmpty } from "src/utils/typing";

describe("isDefined", () => {
  it.each([
    { input: 0, expected: true },
    { input: false, expected: true },
    { input: "", expected: true },
    { input: [], expected: true },
    { input: {}, expected: true },
    { input: undefined, expected: false },
  ])("should return $expected for $input", ({ input, expected }) => {
    expect(isDefined(input)).toBe(expected);
  });
});

type TestCase = "case1" | "case2";

describe("assertUnreachable", () => {
  it.each([
    { input: "case1" as TestCase, expected: "Handled case1" },
    { input: "case2" as TestCase, expected: "Handled case2" },
  ])("should handle valid cases ($input)", ({ input, expected }) => {
    const handleCase = (value: TestCase) => {
      switch (value) {
        case "case1":
          return "Handled case1";
        case "case2":
          return "Handled case2";
        default:
          throw new Error("Unexpected case");
      }
    };

    expect(handleCase(input)).toBe(expected);
  });

  it("should throw an error for an unreachable case", () => {
    type TestCase = "case1" | "case2";
    expect(() => {
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
      handleCase("unexpected" as TestCase);
    }).toThrowError("Didn't expect to get here");
  });
});

describe("isNilOrEmpty", () => {
  it.each([
    { input: null, expected: true },
    { input: undefined, expected: true },
    { input: [], expected: true },
    { input: {}, expected: true },
    { input: [1, 2, 3], expected: false },
  ])("should return $expected for $input", ({ input, expected }) => {
    expect(isNilOrEmpty(input)).toBe(expected);
  });
});
