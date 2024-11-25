export function isDefined<TValue>(value: TValue | undefined): value is TValue {
  return value !== undefined;
}

export function assertUnreachable(_: never): never {
  throw new Error("Didn't expect to get here");
}
