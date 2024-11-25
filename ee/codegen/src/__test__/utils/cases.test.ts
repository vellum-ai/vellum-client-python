import { toKebabCase, toPascalCase, toSnakeCase } from "src/utils/casing";

describe("Casing utility functions", () => {
  describe("toKebabCase", () => {
    const testCases = [
      { input: "hello world", expected: "hello-world" },
      { input: "HelloWorld", expected: "hello-world" },
      { input: "hello_world", expected: "hello-world" },
      { input: "Hello World_Example-123", expected: "hello-world-example-123" },
    ];

    it.each(testCases)(
      "should convert '$input' to '$expected'",
      ({ input, expected }) => {
        expect(toKebabCase(input)).toBe(expected);
      }
    );
  });

  describe("toPascalCase", () => {
    const testCases = [
      { input: "hello-world", expected: "HelloWorld" },
      { input: "hello_world", expected: "HelloWorld" },
      { input: "hello world", expected: "HelloWorld" },
      { input: "hello-world_example 123", expected: "HelloWorldExample123" },
    ];

    it.each(testCases)(
      "should convert '$input' to '$expected'",
      ({ input, expected }) => {
        expect(toPascalCase(input)).toBe(expected);
      }
    );
  });

  describe("toSnakeCase", () => {
    const testCases = [
      { input: "hello-world", expected: "hello_world" },
      { input: "HelloWorld", expected: "hello_world" },
      { input: "hello world", expected: "hello_world" },
      { input: "Hello-World_Example 123", expected: "hello_world_example_123" },
    ];

    it.each(testCases)(
      "should convert '$input' to '$expected'",
      ({ input, expected }) => {
        expect(toSnakeCase(input)).toBe(expected);
      }
    );
  });
});
