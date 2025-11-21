// Re-export the real App component implemented in App.jsx to avoid
// having JSX inside a .js file which can confuse esbuild loaders.
import App from './App.jsx'
export default App
