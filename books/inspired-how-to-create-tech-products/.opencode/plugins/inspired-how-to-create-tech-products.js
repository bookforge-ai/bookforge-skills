import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const pluginRoot = join(__dirname, "../..");
const skillsDir = join(pluginRoot, "skills");

export const Plugin = async ({ client, directory }) => ({
  config: async (config) => {
    config.skills = config.skills || {};
    config.skills.paths = config.skills.paths || [];
    if (!config.skills.paths.includes(skillsDir)) {
      config.skills.paths.push(skillsDir);
    }
  },
  "experimental.chat.system.transform": async (_input, output) => {
    try {
      const bootstrap = readFileSync(
        join(skillsDir, "product-discovery-risk-assessment", "SKILL.md"), "utf-8"
      );
      return output + "\n\n---\n# Hub Skill (product-discovery-risk-assessment)\n\n" + bootstrap;
    } catch {
      return output;
    }
  },
});
