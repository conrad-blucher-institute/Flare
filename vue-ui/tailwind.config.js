/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'navy-blue': '#02172f',
        'primary-bg': '#f4f4f4',
        'secondary-bg': '#ffffff',
        'dark-text': '#0f4f66',
        'light-text': '#f4f4f4',
        'accent-bg': '#f8f8f8',
        'blue-secondary': '#5c779d',
      },
      backgroundImage: {
        'banner-gradient': 'linear-gradient(to bottom, #000000, #06335f, #1899a7)',
       'banner-gradient-2': 'linear-gradient(to right, #000000, rgb(7, 40, 75), rgb(6, 120, 133))',
        'section-gradient': 'linear-gradient(to bottom right, #1899a7, #0f4c5c)',
      },
      fontFamily: {
        main: ['Open Sans', 'sans-serif'], // Main text
        heading: ['Playfair Display', 'serif'], // Headings
      },
    },
  },
  plugins: [],
};

