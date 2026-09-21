/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./partials/*.html', './pages/*.html', './make_pages.py', './assets/js/site.js'],
  theme: { extend: {
    colors: { bg:'#F4F6F1', ink:'#16191C', muted:'#4F5A52', brand:'#5A984B', 'brand-dark':'#3E7A34', deep:'#17261B', cream:'#F3F8D6', pulse:'#FFC400', line:'#D6DCD2', danger:'#C8372D' },
    fontFamily: { sans:['"Golos Text"','system-ui','sans-serif'], serif:['Vollkorn','Georgia','serif'] },
    maxWidth: { site:'1400px' },
    transitionTimingFunction: { out:'cubic-bezier(0.22, 1, 0.36, 1)' },
    zIndex: { float:'30', nav:'40', menu:'45', bar:'40', preloader:'100' }
  } },
  plugins: [],
};
