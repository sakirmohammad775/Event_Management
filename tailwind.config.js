/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", //Template at the Project Level
    "./**/templates/**/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
