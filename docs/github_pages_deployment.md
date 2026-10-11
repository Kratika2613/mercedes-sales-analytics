# GitHub Pages Deployment Guide

This project includes a fully configured continuous deployment pipeline to host the React dashboard via GitHub Pages as a static, recruiter-accessible demo.

## Pre-requisites
1. A GitHub repository hosted under your account.
2. The project pushed to the `main` branch.

## Deployment Workflow
The deployment relies on GitHub Actions. The configuration file is located at `.github/workflows/deploy.yml`.

### How It Works:
1. **Trigger**: Any push to the `main` branch or manual trigger via Workflow Dispatch.
2. **Environment Setup**: Checks out the code and sets up Node.js v20.
3. **Data Pre-processing**: Copies the locally generated `mercedes_sales_demo.json` into the `dashboard/public/` folder so it gets bundled as static data.
4. **Build**: Runs `npm run build` using Vite. The base URL is configured in `vite.config.js` to match the repository name (`/mercedes-sales-analytics/`).
5. **Publishing**: Uses the official `actions/upload-pages-artifact` and `actions/deploy-pages` to deploy the `dashboard/dist` folder to GitHub Pages.

## Manual Setup Steps (If First Time)
1. Go to your GitHub repository in the web browser.
2. Navigate to **Settings** -> **Pages**.
3. Under **Build and deployment**, ensure the **Source** is set to **GitHub Actions**.
4. Trigger the action manually from the **Actions** tab if it did not run automatically.
5. After the workflow completes, the dashboard will be live at `https://<your-username>.github.io/mercedes-sales-analytics/`.

## Local Testing
To test the production build locally before pushing:
```bash
cd dashboard
npm run build
npx serve dist
```
Note that since the `base` in Vite is set to the repository subpath, some static assets might look broken on localhost root (`/`) but will work correctly in GitHub Pages.
