/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,jsx,tsx}"],
  theme: {
    extend: {
      height: {
        138: "42rem",
      },
      colors: {
        "btn-blue": "#0167d6",
      },
    },
  },
  plugins: [],
};
