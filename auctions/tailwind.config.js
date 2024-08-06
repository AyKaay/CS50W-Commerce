/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'media',
  content: [    
  './node_modules/flowbite/**/*.js',
  './templates/**/*.html',
  './templates/auctions/**/*.html',
  ],
  theme: {
    extend: {
      },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

// build tailwind from CSS cmd
// npx tailwindcss -i ./static/auctions/styles.css -o ./static/auctions/tw-layout.css --watch