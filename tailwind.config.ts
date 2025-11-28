import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./**/*.py",
  ],
  theme: {
    extend: {},
  },
};

export default config;
