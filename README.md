# Mood Dump Landing Page

> **Note:** This repository is proprietary and not open source. Unauthorized distribution or reproduction is prohibited.

A promotional landing page for **Mood Dump** — a personal diary application designed as a safe space to dump your raw thoughts, track your mood, and reflect on your story without filters or judgment.

## Overview

This repository contains the static frontend code for the Mood Dump landing website. The site features a highly interactive, scroll-linked canvas animation in the hero section that simulates opening a physical diary as the user scrolls down the page.

### Features
* **Scroll-Linked Hero Animation**: A smooth, 240-frame image sequence rendered on an HTML5 `<canvas>` that plays forwards and backwards as you scroll.
* **Dynamic Typewriter Effect**: A custom JavaScript text typing animation synced with the scroll progress.
* **Scroll-Triggered Reveals**: Elements elegantly fade and slide into view as you scroll down the page, handled via the Intersection Observer API.
* **Responsive Design**: Built with Tailwind CSS utility classes (via CDN) to ensure the layout looks great on all devices.
* **Loading State**: A custom loading screen with a progress bar that ensures all heavy animation frames are preloaded before the user interacts with the page, preventing jank.

## Tech Stack

The site is built with a lightweight, dependency-free stack:
* **HTML5** & **CSS3** (Custom styling and animations)
* **JavaScript (ES6+)** (Canvas rendering, asset preloading, scroll events)
* **Tailwind CSS** (via CDN for layout utilities)
* **Google Fonts**: DM Sans, Playfair Display, and Kalam
* **FontAwesome**: For UI icons

## Setup & Running Locally

Because this is a static site with no build process or backend, getting it running is extremely simple.

1. **Access the codebase:**
   Ensure you have access to the internal repository and have pulled the latest changes to your local machine.
   ```bash
   cd path/to/moodump/website
   ```

2. **Serve the files:**
   You can open `index.html` directly in your browser, but due to CORS restrictions with canvas elements or local file loading, it's highly recommended to use a local development server.

   Using Python:
   ```bash
   python3 -m http.server 8000
   ```
   Or using Node.js (if `http-server` is installed):
   ```bash
   npx http-server
   ```

3. **View the site:**
   Open your browser and navigate to `http://localhost:8000` (or the port provided by your local server).

## Project Structure

* `index.html` - The main entry point containing all HTML structure, custom CSS, and animation JavaScript.
* `assets/` - Contains all visual assets:
  * `Mood-removebg-preview.png` - The main logo.
  * `ezgif-frame-*.png` - The 240 individual image frames used for the scroll animation.

## Potential Improvements & Known Issues

* **Asset Optimization**: Currently, the site preloads 240 PNG frames which can consume significant bandwidth (~70MB). Future optimizations could involve using WebP/AVIF formats, sprite sheets, or converting the image sequence to a scroll-scrubbable video format (like an MP4 or WebM) to reduce load times and memory footprint.
* **Tailwind CDN**: For production deployment, Tailwind CSS should be compiled locally via a build process (e.g., PostCSS/Vite) rather than relying on the JIT CDN script to improve initial load performance.
