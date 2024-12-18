const packageJson = require("../package.json");
const { createAppAuth } = require("@octokit/auth-app");
const path = require("path");
const os = require("os");
const { execSync } = require("child_process");

export const getGithubToken = async () => {
  const appId = process.env.VELLUM_AUTOMATION_APP_ID;
  const privateKey = process.env.VELLUM_AUTOMATION_PRIVATE_KEY;
  const installationId = process.env.VELLUM_AUTOMATION_INSTALLATION_ID;

  if (!appId || !privateKey || !installationId) {
    throw new Error(
      "VELLUM_AUTOMATION_APP_ID, VELLUM_AUTOMATION_PRIVATE_KEY, and VELLUM_AUTOMATION_INSTALLATION_ID must be set"
    );
  }

  const auth = createAppAuth({
    appId,
    privateKey,
    installationId,
  });

  const { token } = await auth({ type: "installation" });
  return token;
};

const main = async () => {
  const version = packageJson.version;
  console.log("Upgrading codegen service to version", version);

  const githubToken = await getGithubToken();
  const targetDir = path.join(os.tmpdir(), `codegen-service-${id}`);

  const repoUrl = `https://x-access-token:${githubToken}@github.com/vellum-ai/codegen-service.git`;
  execSync(`git clone ${repoUrl} ${targetDir}`, { stdio: "inherit" });

  process.chdir(targetDir);
  const branchName = `vellum-automation/${version}`;
  execSync(`git checkout -b ${branchName}`, { stdio: "inherit" });
  execSync(`npm run gar-login`, { stdio: "inherit" });
  execSync(`npm install @vellum-ai/vellum-codegen@${version} --save-exact`, {
    stdio: "inherit",
  });
  execSync('git config user.name "vellum-automation[bot]"', {
    stdio: "inherit",
  });
  execSync(
    'git config user.email "vellum-automation[bot]@users.noreply.github.com"',
    { stdio: "inherit" }
  );
  execSync(`git add --all`, { stdio: "inherit" });
  execSync(`git commit -m "Upgrade codegen service to ${version}"`, {
    stdio: "inherit",
  });
  execSync(`git push origin ${branchName}`, { stdio: "inherit" });
  console.log("Successfully pushed branch", branchName);
};

main();
