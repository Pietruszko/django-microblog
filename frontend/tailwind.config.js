import oxide from '@tailwindcss/oxide'

export default oxide({
  content: [
    "./src/**/*.{html,js,vue}",
    "./assets/**/*.css"
  ],
  theme: {
    extend: {
      colors: {
        green: 'hsla(160, 100%, 37%, 1)',
      },
    },
  },
})