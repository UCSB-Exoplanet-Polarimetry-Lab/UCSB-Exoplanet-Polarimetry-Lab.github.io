# News and Travel Management Guide

The news and travel section is now data-driven and much easier to maintain! Here's how to manage it:

## 📁 File Structure

- **`_data/news.yml`** - Contains all news items and categories
- **`index.html`** - The homepage template (don't edit this directly)
- **`scripts/manage_news.py`** - Helper script for easy management

## 🚀 Quick Start

### Option 1: Use the Python Script (Recommended)

```bash
# Make the script executable
chmod +x scripts/manage_news.py

# Run the management script
python scripts/manage_news.py
```

The script provides an interactive menu to:
- Add new news items
- Edit existing items
- Remove items
- View all items
- Add new categories

### Option 2: Edit the YAML File Directly

Edit `_data/news.yml` directly. The structure is:

```yaml
items:
  - date: "2024-08-24"
    title: "Postdoc Position Available"
    description: "I'm hiring a new postdoc to work with me on the Roman Coronagraph Instrument..."
    category: "opportunity"
    link: "https://recruit.ap.ucsb.edu/JPF02686"
    featured: true

categories:
  - name: "opportunity"
    display_name: "Opportunities"
    icon: "fa-briefcase"
    color: "#28a745"
```

## 📝 News Item Fields

### Required Fields:
- **`date`** - Date in YYYY-MM-DD format
- **`title`** - Short, descriptive title
- **`description`** - Full description of the news item
- **`category`** - Must match a category name from the categories list

### Optional Fields:
- **`link`** - URL for more information
- **`featured`** - Boolean (true/false) to highlight important items

## 🏷️ Categories

### Current Categories:
- **Opportunities** - Job openings, student positions, etc.
- **Conferences & Travel** - Conference presentations, travel plans
- **Publications** - New papers, research updates
- **Updates** - General website or group updates

### Adding New Categories:
1. Use the Python script: `python scripts/manage_news.py` → Option 5
2. Or edit `_data/news.yml` directly
3. Each category needs: `name`, `display_name`, `icon`, `color`

## 🎨 Visual Features

### Featured Items:
- **Blue border** and gradient background
- **Displayed prominently** at the top of the news section
- **Limited to 3** most recent featured items

### Category Styling:
- **Color-coded** by category type
- **Icons** for visual identification
- **Hover effects** for better UX

### Responsive Design:
- **Mobile-friendly** layout
- **Adaptive spacing** for different screen sizes
- **Touch-friendly** interactions

## 🔄 Common Tasks

### Adding a New News Item

```bash
python scripts/manage_news.py
# Choose option 1: Add news item
# Fill in the prompts
```

### Making an Item Featured

```bash
python scripts/manage_news.py
# Choose option 2: Edit news item
# Select the item and set featured to 'y'
```

### Removing Old Items

```bash
python scripts/manage_news.py
# Choose option 3: Remove news item
# Select the item to remove
```

### Viewing All Items

```bash
python scripts/manage_news.py
# Choose option 4: View all news items
# See all items sorted by date
```

## 📱 How It Appears on the Website

### Featured Section:
- **Top 3 featured items** displayed prominently
- **Large cards** with blue styling
- **"Learn More" buttons** for items with links

### Recent Updates Section:
- **All items** (up to 10 most recent)
- **Smaller cards** with category indicators
- **Chronological order** (newest first)

## 💡 Tips

1. **Keep titles concise** - 5-10 words work best
2. **Use descriptive descriptions** - 1-2 sentences
3. **Set important items as featured** - They'll appear prominently
4. **Add links when relevant** - Makes items more actionable
5. **Use appropriate categories** - Helps visitors find relevant information
6. **Update regularly** - Keep the section fresh and current

## 🔧 Troubleshooting

### YAML Syntax Errors:
- Use a YAML validator (like [yamllint.com](https://www.yamllint.com/))
- Check indentation (use spaces, not tabs)
- Ensure quotes are properly closed

### Script Issues:
- Make sure Python 3 is installed
- Install PyYAML: `pip install pyyaml`
- Check file permissions on the script

### Display Issues:
- Verify category names match exactly
- Check that dates are in YYYY-MM-DD format
- Ensure all required fields are present

## 🆘 Need Help?

If you encounter issues:
1. Check the browser console for errors
2. Verify the YAML syntax
3. Test the local Jekyll build: `bundle exec jekyll serve`
4. Check that all category names match

## 🎯 Best Practices

1. **Regular updates** - Add news items as they happen
2. **Consistent formatting** - Use similar title and description styles
3. **Relevant links** - Include links to papers, registration forms, etc.
4. **Appropriate categorization** - Helps visitors find what they're looking for
5. **Featured highlights** - Use featured status for important announcements
