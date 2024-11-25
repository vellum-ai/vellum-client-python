export function toKebabCase(str: string): string {
  return str
    .replace(/([a-z])([A-Z])/g, "$1-$2") // Insert hyphen between lower and upper case
    .replace(/[\s_]+/g, "-") // Replace spaces and underscores with hyphens
    .replace(/[^a-zA-Z0-9]+/g, "-") // Replace consecutive non-alphanumeric characters with a single hyphen
    .replace(/^-+|-+$/g, "") // Remove leading and trailing hyphens
    .toLowerCase(); // Convert to lowercase
}

export function toPascalCase(str: string): string {
  return str
    .split(/[-_\s]+/)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join("");
}

export function toSnakeCase(str: string): string {
  return str
    .replace(/([a-z])([A-Z])/g, "$1_$2") // Insert underscore between lower and upper case
    .replace(/[\s-]+/g, "_") // Replace spaces and hyphens with underscores
    .replace(/[^a-zA-Z0-9]+/g, "_") // Replace consecutive non-alphanumeric characters with a single underscore
    .replace(/^-+|-+$/g, "") // Remove leading and trailing underscores
    .toLowerCase(); // Convert to lowercase
}
