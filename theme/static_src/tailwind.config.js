/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [

    '../../templates/**/*.html',
    '../../core/templates/**/*.html',
    '../../theme/templates/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Montserrat', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
