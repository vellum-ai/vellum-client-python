const packageJson = require("../package.json");

const main = async () => {
  const version = packageJson.version;
  console.log("Upgrading codegen service to version", version);
};

main();
