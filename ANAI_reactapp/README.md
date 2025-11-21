# AssessNex AI — Frontend (Vite + React)

This repository contains a complete frontend scaffold for AssessNex AI — a mock AI-powered exam/assignment generation platform built with React 18, Vite, TailwindCSS, Framer Motion, and Zustand.

Features
- React 18 + Vite
- TailwindCSS with custom palette
- Framer Motion animations and smooth page transitions
- Lucide icons
- React Router v6 with role-protected routes
- Zustand store for auth (mock JWT) and global state
- Axios-based mock API service (frontend-only)
- React Hot Toast for notifications
- Role system: Professor, Assistant, Student

Quick start

1. Install dependencies

```powershell
cd "assessnex-ai"
npm install
```

2. Run dev server

```powershell
npm run dev
```

3. Build for production

```powershell
npm run build
```

Deploy to GitHub Pages

This project is configured to publish to GitHub Pages at:

`https://Atharv-Chaudhari.github.io/AssessNex-AI`

Make sure the repository name is `AssessNex-AI` and the `homepage` field in `package.json` is set (it already is).

To deploy:

```powershell
npm run build
npm run deploy
```

This uses `gh-pages` to publish the `dist` folder. `vite.config.js` has `base: '/AssessNex-AI/'` which is required for GitHub Pages.

Notes
- All API calls are mocked in `src/services/api.js` so the app runs fully frontend-only.
- Authentication uses a mock JWT stored via `useAuthStore` (Zustand) and persisted to `localStorage`.
- To change the GitHub Pages URL or repo name, update `homepage` in `package.json` and `base` in `vite.config.js`.

Next steps you might want:
- Improve visual polish and accessibility.
- Hook real backend endpoints when available.
- Add unit / integration tests and CI.

Enjoy — let me know if you want further polish or I should commit and push these changes for you.
# AssessNex AI — Frontend (Vite + React)

This is a frontend-only mock of AssessNex AI built with React 18, Vite, TailwindCSS, Framer Motion, Zustand and mock API endpoints.

Run locally:

```powershell
cd "assessnex-ai"
npm install
npm run dev
```

To build and deploy to GitHub Pages (repository `Atharv-Chaudhari/AssessNex-AI`):

```powershell
npm run build
npm run deploy
```

Notes:
- `vite.config.js` is configured with `base: '/AssessNex-AI/'` and `package.json` includes `homepage` for gh-pages.
- All API endpoints are mocked in `src/services/api.js` so the app runs completely frontend-only.
# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
