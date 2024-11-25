const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

// Read package.json from project root
const packageJsonPath = path.join(__dirname, "../package.json");
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));
const version = packageJson.version;

if (typeof version !== "string") {
  throw new Error("Package version is not a string");
}

if (version.match(/^\d+\.\d+\.\d+$/)) {
  const newVersion = `${version}-post1`;
  console.log(`Bumping version to ${newVersion}`);
  execSync(`npm version ${newVersion}`, { stdio: "inherit" });
} else if (version.match(/^\d+\.\d+\.\d+-post\d+$/)) {
  const [major, minor, patch, post] = version.split(".");
  const postNumber = Number(post);
  if (isNaN(postNumber)) {
    throw new Error(`Invalid post version format: ${post}`);
  }

  const newVersion = `${major}.${minor}.${patch}-post${postNumber + 1}`;
  console.log(`Bumping version to ${newVersion}`);
  execSync(`npm version ${newVersion}`, { stdio: "inherit" });
} else {
  throw new Error(`Invalid version format: ${version}`);
}
