import { access, readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const required = [
  "public/index.html",
  "public/picture-dictionary/index.html",
  "public/picture-dictionary/privacy/index.html",
  "public/picture-dictionary/support/index.html",
  "public/privacy/index.html",
  "public/support/index.html",
  "public/assets/site.css"
];

for (const file of required) {
  await access(resolve(root, file));
}

const privacy = await readFile(resolve(root, "public/picture-dictionary/privacy/index.html"), "utf8");
const forbiddenPublicNotes = [
  "This draft is for planning",
  "This is not legal advice",
  "Review Before Publishing",
  "Operator placeholder:",
  "Public URL placeholder:"
];

for (const phrase of forbiddenPublicNotes) {
  if (privacy.includes(phrase)) {
    throw new Error(`Privacy page contains internal note: ${phrase}`);
  }
}

console.log("Static site checks passed");
