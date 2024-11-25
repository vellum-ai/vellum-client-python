import os from "os";
import path from "path";

export function makeTempDir(base?: string): string {
  const randomSuffix = Math.random().toString(36).substring(7);
  return path.join(os.tmpdir(), `${base ?? "test-directory"}-${randomSuffix}`);
}
