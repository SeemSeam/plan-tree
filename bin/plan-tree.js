#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const PACKAGE_VERSION = "0.2.0";
const REPO_URL = "https://github.com/SeemSeam/plan-tree.git";
const SKILL_NAME = "plan-tree";

const CORE_FILES = ["SKILL.md", "VERSION", "README.md", "README.zh-CN.md"];
const CORE_DIRS = ["references", "assets"];

const PROVIDER_TARGETS = {
  claude: () => path.join(os.homedir(), ".claude", "skills", SKILL_NAME),
  opencode: () => path.join(os.homedir(), ".config", "opencode", "skill", SKILL_NAME),
  codex: () => path.join(process.env.CODEX_HOME || path.join(os.homedir(), ".codex"), "skills", SKILL_NAME)
};

function main(argv) {
  const [command, ...rest] = argv;
  if (command === "version") {
    console.log(PACKAGE_VERSION);
    return 0;
  }
  if (command === "install") {
    return install(parseInstallArgs(rest));
  }
  usage();
  return 2;
}

function usage() {
  console.log("Use `plan-tree install --provider claude|opencode|codex`.");
}

function parseInstallArgs(args) {
  const options = {
    provider: "claude",
    target: null,
    source: null,
    version: PACKAGE_VERSION,
    force: false,
    dryRun: false
  };

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === "--provider") options.provider = requireValue(args, ++i, arg);
    else if (arg === "--target") options.target = requireValue(args, ++i, arg);
    else if (arg === "--source") options.source = requireValue(args, ++i, arg);
    else if (arg === "--version") options.version = requireValue(args, ++i, arg);
    else if (arg === "--force") options.force = true;
    else if (arg === "--dry-run") options.dryRun = true;
    else if (arg === "--help" || arg === "-h") {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  const allowed = [...Object.keys(PROVIDER_TARGETS), "all"];
  if (!allowed.includes(options.provider)) {
    throw new Error(`--provider must be one of: ${allowed.join(", ")}`);
  }
  if (options.target && options.provider === "all") {
    throw new Error("--target cannot be combined with --provider all");
  }
  return options;
}

function requireValue(args, index, flag) {
  const value = args[index];
  if (!value || value.startsWith("--")) {
    throw new Error(`${flag} requires a value`);
  }
  return value;
}

function install(options) {
  const providers = options.provider === "all" ? Object.keys(PROVIDER_TARGETS) : [options.provider];
  const source = options.source ? path.resolve(options.source) : cloneSource(options.version);

  validateSource(source);
  for (const provider of providers) {
    const target = path.resolve(expandHome(options.target || PROVIDER_TARGETS[provider]()));
    installToProvider(source, target, provider, options.force, options.dryRun);
  }
  return 0;
}

function cloneSource(version) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "plan-tree-"));
  const target = path.join(tmp, "source");
  const result = spawnSync("git", ["clone", "--depth=1", "--branch", `v${version}`, REPO_URL, target], {
    stdio: "inherit"
  });
  if (result.status !== 0) {
    throw new Error("Failed to clone plan-tree. Install git or use --source /path/to/plan-tree.");
  }
  return target;
}

function validateSource(source) {
  const missing = [];
  for (const item of CORE_FILES) {
    if (!fs.existsSync(path.join(source, item))) missing.push(item);
  }
  for (const item of CORE_DIRS) {
    if (!fs.existsSync(path.join(source, item))) missing.push(item);
  }
  if (missing.length > 0) {
    throw new Error(`${source} is not a valid plan-tree source; missing: ${missing.join(", ")}`);
  }
}

function installToProvider(source, target, provider, force, dryRun) {
  const planned = [...CORE_FILES, ...CORE_DIRS];
  if (provider === "codex" && fs.existsSync(path.join(source, "agents"))) {
    planned.push("agents");
  }

  console.log(`Installing plan-tree for ${provider} -> ${target}`);
  if (dryRun) {
    for (const item of planned) console.log(`  would copy ${item}`);
    return;
  }

  if (fs.existsSync(target)) {
    if (!force) throw new Error(`${target} already exists. Use --force to replace it.`);
    fs.rmSync(target, { recursive: true, force: true });
  }
  fs.mkdirSync(target, { recursive: true });

  for (const item of planned) {
    copyPath(path.join(source, item), path.join(target, item));
  }

  console.log(`Installed plan-tree ${readVersion(target)}`);
}

function copyPath(source, target) {
  const stat = fs.statSync(source);
  if (stat.isDirectory()) {
    fs.cpSync(source, target, { recursive: true });
  } else {
    fs.copyFileSync(source, target);
  }
}

function readVersion(target) {
  const versionPath = path.join(target, "VERSION");
  if (fs.existsSync(versionPath)) {
    return `v${fs.readFileSync(versionPath, "utf8").trim()}`;
  }
  return "unknown version";
}

function expandHome(value) {
  if (value === "~") return os.homedir();
  if (value.startsWith("~/")) return path.join(os.homedir(), value.slice(2));
  return value;
}

try {
  process.exitCode = main(process.argv.slice(2));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
