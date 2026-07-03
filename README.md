# Wan2GP Skin Manager

Wan2GP Skin Manager is an independent, zero-dependency plugin for Wan2GP that lets you dynamically select and apply themes from the official Gradio Themes Gallery.

## Features

- **Live Theme Fetching**: Retrieves all available themes directly from the Hugging Face Spaces API.
- **Interactive Grid View**: Displays themes in a searchable data grid with details including Author, Name, and Popularity (Likes).
- **Search & Filter**: Instantly filter the theme list by author or theme name.
- **Safe Injection**: Safely monkey-patches Gradio's layout initialization to inject the selected theme without needing any modifications to the core Wan2GP codebase.

## Installation

1. Copy the `wan2gp-skin-manager` directory into your Wan2GP `plugins` folder.
2. Ensure the plugin is enabled in Wan2GP.
3. Restart Wan2GP.

## Usage

1. Open the Wan2GP web interface and navigate to the **Skin Manager** tab.
2. Click **Fetch / Refresh Themes** to load the latest themes from the gallery.
3. Use the search box to find a specific theme, or browse the grid.
4. Click on a row in the grid to select a theme.
5. Click **Apply Selected Theme**.
6. Restart Wan2GP for the theme changes to take effect!

## Requirements
- Wan2GP

## Author
David Brum
