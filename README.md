# Millar-Blanchaer Research Group - Academic Website

This is the source code for my academic website, built with Jekyll and hosted on GitHub Pages.

## Local Development

### Prerequisites
- Ruby (version 2.6 or higher)
- RubyGems
- Bundler

### Setup
1. Clone this repository
2. Install dependencies:
   ```bash
   bundle install
   ```
3. Start the local development server:
   ```bash
   bundle exec jekyll serve
   ```
4. Open your browser and go to `http://localhost:4000`

## Deployment

This site is configured for GitHub Pages deployment. Simply push changes to the main branch and GitHub Pages will automatically build and deploy the site.

### GitHub Pages Setup
1. Go to your repository settings on GitHub
2. Navigate to "Pages" in the sidebar
3. Select "Deploy from a branch"
4. Choose the main branch and `/ (root)` folder
5. Click "Save"

## Site Structure

- `_layouts/` - Jekyll layout templates
- `_includes/` - Reusable HTML components
- `_posts/` - Blog posts (future feature)
- `_data/` - Data files for dynamic content
- `assets/` - CSS, JavaScript, and other static assets
- `images/` - Image files
- `videos/` - Video files

## Features

- **Dynamic Navigation**: Automatically highlights the current page
- **Responsive Design**: Works on all device sizes
- **SEO Optimized**: Built-in meta tags and structured data
- **Fast Loading**: Optimized assets and minimal dependencies

## Customization

### Adding New Pages
1. Create a new HTML file in the root directory
2. Add Jekyll front matter at the top:
   ```yaml
   ---
   layout: default
   title: Your Page Title
   ---
   ```
3. Add your content below the front matter

### Updating Navigation
Edit `_includes/navigation.html` to add or modify navigation links.

### Site Configuration
Edit `_config.yml` to change site-wide settings like title, description, and social links.

## License

This site uses the Massively theme by HTML5 UP, which is free for personal and commercial use under the CCA 3.0 license.
