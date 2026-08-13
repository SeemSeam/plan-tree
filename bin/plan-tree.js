#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");
const { TextDecoder } = require("util");

const PACKAGE_VERSION = "0.4.0";
const REPO_URL = "https://github.com/SeemSeam/plan-tree.git";
const README_URL = "https://github.com/SeemSeam/plan-tree#readme";
const SKILL_NAME = "plan-tree";

const CORE_FILES = ["SKILL.md", "VERSION", "README.md", "README.zh-CN.md"];
const CORE_DIRS = ["references", "assets", "prompts"];

const PROVIDER_TARGETS = {
  claude: () => path.join(os.homedir(), ".claude", "skills", SKILL_NAME),
  opencode: () => path.join(os.homedir(), ".config", "opencode", "skill", SKILL_NAME),
  codex: () => path.join(process.env.CODEX_HOME || path.join(os.homedir(), ".codex"), "skills", SKILL_NAME)
};
const PROVIDER_INSTRUCTION_TARGETS = {
  claude: () => path.join(os.homedir(), ".claude", "CLAUDE.md"),
  opencode: () => path.join(os.homedir(), ".config", "opencode", "AGENTS.md"),
  codex: () => path.join(process.env.CODEX_HOME || path.join(os.homedir(), ".codex"), "AGENTS.md")
};
const INSTRUCTION_START = "<!-- plan-tree:instructions:start -->";
const INSTRUCTION_END = "<!-- plan-tree:instructions:end -->";
const UTF8_DECODER = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true });

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
  console.log("Use `plan-tree install claude|opencode|codex|all`.");
  console.log("Installs persistent provider instructions by default; use --no-instructions to skip them.");
  console.log(`README: ${README_URL}`);
}

function parseInstallArgs(args) {
  const options = {
    provider: null,
    target: null,
    source: null,
    version: PACKAGE_VERSION,
    force: false,
    dryRun: false,
    noInstructions: false
  };
  let providerArg = null;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === "--provider") {
      const providerValue = requireValue(args, ++i, arg);
      if (providerArg && providerArg !== providerValue) {
        throw new Error("provider specified twice with different values");
      }
      providerArg = providerValue;
    } else if (arg === "--target") options.target = requireValue(args, ++i, arg);
    else if (arg === "--source") options.source = requireValue(args, ++i, arg);
    else if (arg === "--version") options.version = requireValue(args, ++i, arg);
    else if (arg === "--force") options.force = true;
    else if (arg === "--dry-run") options.dryRun = true;
    else if (arg === "--no-instructions") options.noInstructions = true;
    else if (arg === "--help" || arg === "-h") {
      usage();
      process.exit(0);
    } else if (arg.startsWith("-")) {
      throw new Error(`Unknown argument: ${arg}`);
    } else if (providerArg) {
      throw new Error(`Unexpected argument: ${arg}`);
    } else {
      providerArg = arg;
    }
  }

  options.provider = providerArg || "claude";

  const allowed = [...Object.keys(PROVIDER_TARGETS), "all"];
  if (!allowed.includes(options.provider)) {
    throw new Error(`provider must be one of: ${allowed.join(", ")}`);
  }
  if (options.target && options.provider === "all") {
    throw new Error("--target cannot be combined with provider all");
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
  if (!options.dryRun) {
    for (const provider of providers) {
      const target = path.resolve(expandHome(options.target || PROVIDER_TARGETS[provider]()));
      preflightSkillTarget(target, options.force);
      if (!options.noInstructions) {
        preflightInstructionTarget(path.resolve(PROVIDER_INSTRUCTION_TARGETS[provider]()));
      }
    }
  }
  for (const provider of providers) {
    const target = path.resolve(expandHome(options.target || PROVIDER_TARGETS[provider]()));
    installToProvider(source, target, provider, options.force, options.dryRun);
    if (!options.noInstructions) {
      installProviderInstructions(
        source,
        path.resolve(PROVIDER_INSTRUCTION_TARGETS[provider]()),
        provider,
        options.dryRun
      );
    }
  }
  if (!options.dryRun) {
    console.log(`Read the README: ${README_URL}`);
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
    const candidate = path.join(source, item);
    if (!fs.existsSync(candidate) || !fs.statSync(candidate).isFile()) missing.push(item);
  }
  for (const item of CORE_DIRS) {
    const candidate = path.join(source, item);
    if (!fs.existsSync(candidate) || !fs.statSync(candidate).isDirectory()) missing.push(item);
  }
  for (const provider of Object.keys(PROVIDER_TARGETS)) {
    const prompt = path.join("prompts", `${provider}.md`);
    if (!fs.existsSync(path.join(source, prompt))) missing.push(prompt);
  }
  if (missing.length > 0) {
    throw new Error(`${source} is not a valid plan-tree source; missing: ${missing.join(", ")}`);
  }
  const emptyPrompts = Object.keys(PROVIDER_TARGETS)
    .map((provider) => path.join("prompts", `${provider}.md`))
    .filter((prompt) => !readUtf8(path.join(source, prompt)).trim());
  if (emptyPrompts.length > 0) {
    throw new Error(
      `${source} is not a valid plan-tree source; empty provider prompts: ${emptyPrompts.join(", ")}`
    );
  }
}

function preflightSkillTarget(target, force) {
  if (fs.existsSync(target) && !force) {
    throw new Error(`${target} already exists. Use --force to replace it.`);
  }
}

function preflightInstructionTarget(target) {
  const resolved = resolveInstructionTarget(target);
  if (fs.existsSync(resolved) && !fs.statSync(resolved).isFile()) {
    throw new Error(`${target} is not a regular provider instruction file.`);
  }
  if (fs.existsSync(resolved)) {
    managedBlockSpan(readUtf8(resolved, target), target);
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

function installProviderInstructions(source, target, provider, dryRun) {
  const promptPath = path.join(source, "prompts", `${provider}.md`);
  const prompt = readUtf8(promptPath).trim();
  if (!prompt) throw new Error(`Provider prompt is empty: prompts/${provider}.md`);

  const resolved = resolveInstructionTarget(target);
  const exists = fs.existsSync(resolved);
  const action = exists ? "update" : "create";
  console.log(`Persistent instructions for ${provider} -> ${target}`);
  if (dryRun) {
    console.log(`  would ${action} managed Plan Tree block`);
    return;
  }

  const existing = exists ? readUtf8(resolved, target) : "";
  const updated = mergeManagedInstructions(existing, prompt, target);
  if (updated === existing) {
    console.log("Persistent instructions already current");
    return;
  }

  atomicWriteText(resolved, updated);
  console.log(`${action[0].toUpperCase() + action.slice(1)}d persistent instructions`);
}

function resolveInstructionTarget(target) {
  if (!fs.existsSync(target)) {
    try {
      if (fs.lstatSync(target).isSymbolicLink()) {
        throw new Error(`${target} is a dangling symbolic link; repair it before installing.`);
      }
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    return target;
  }
  return fs.lstatSync(target).isSymbolicLink() ? fs.realpathSync(target) : target;
}

function readUtf8(target, display = target) {
  try {
    return UTF8_DECODER.decode(fs.readFileSync(target));
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(`${display} is not valid UTF-8; convert it before installing.`);
    }
    throw error;
  }
}

function managedBlockSpan(content, target) {
  const starts = content.split(INSTRUCTION_START).length - 1;
  const ends = content.split(INSTRUCTION_END).length - 1;
  if (starts === 0 && ends === 0) return null;
  if (starts !== 1 || ends !== 1) {
    throw new Error(
      `${target} has ambiguous Plan Tree instruction markers; repair them manually before installing.`
    );
  }

  const start = content.indexOf(INSTRUCTION_START);
  const endStart = content.indexOf(INSTRUCTION_END);
  if (endStart < start) {
    throw new Error(
      `${target} has reversed Plan Tree instruction markers; repair them manually before installing.`
    );
  }
  return [start, endStart + INSTRUCTION_END.length];
}

function mergeManagedInstructions(existing, prompt, target) {
  const newline = existing.includes("\r\n") ? "\r\n" : "\n";
  const normalizedPrompt = prompt.split(/\r?\n/).join(newline);
  const block = [INSTRUCTION_START, normalizedPrompt, INSTRUCTION_END].join(newline);
  const span = managedBlockSpan(existing, target);
  if (span) {
    return existing.slice(0, span[0]) + block + existing.slice(span[1]);
  }
  if (!existing) return block + newline;

  let separator;
  if (existing.endsWith(newline + newline)) separator = "";
  else if (existing.endsWith(newline)) separator = newline;
  else separator = newline + newline;
  return existing + separator + block + newline;
}

function atomicWriteText(target, content) {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  const existed = fs.existsSync(target);
  const mode = existed ? fs.statSync(target).mode : undefined;
  const temporary = path.join(
    path.dirname(target),
    `.${path.basename(target)}.plan-tree-${process.pid}-${Date.now()}.tmp`
  );
  try {
    fs.writeFileSync(temporary, content, { encoding: "utf8", mode });
    if (mode !== undefined) fs.chmodSync(temporary, mode);
    try {
      fs.renameSync(temporary, target);
    } catch (error) {
      if (!["EEXIST", "EPERM"].includes(error.code)) throw error;
      fs.copyFileSync(temporary, target);
      fs.unlinkSync(temporary);
    }
  } finally {
    if (fs.existsSync(temporary)) fs.unlinkSync(temporary);
  }
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
