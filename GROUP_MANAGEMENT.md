# Group Page Management Guide

The group page is now data-driven and much easier to maintain! Here's how to manage it:

## 📁 File Structure

- **`_data/group_members.yml`** - Contains all group member data
- **`group.html`** - The page template (don't edit this directly)
- **`scripts/update_group_member.py`** - Helper script for easy management
- **`images/people/`** - Directory for member photos

## 🚀 Quick Start

### Option 1: Use the Python Script (Recommended)

```bash
# Make the script executable
chmod +x scripts/update_group_member.py

# Run the management script
python scripts/update_group_member.py
```

The script provides an interactive menu to:
- Add new members
- Edit existing members
- Remove members
- Move members between current/alumni sections
- View current data

### Option 2: Edit the YAML File Directly

Edit `_data/group_members.yml` directly. The structure is:

```yaml
current:
  - name: "Member Name"
    role: "Graduate Student"
    image: "member_photo.jpg"  # or leave empty for placeholder
    description: "Research description..."
    email: "member@ucsb.edu"
    website: "https://member-website.com"  # optional
    github: "github-username"  # optional
    ads: "https://ui.adsabs.harvard.edu/search/..."  # optional
    orcid: "https://orcid.org/0000-0000-0000-0000"  # optional

alumni:
  - name: "Alumni Name"
    role: "Former Graduate Student"
    image: "alumni_photo.jpg"
    description: "What they worked on..."
    current_position: "Current job/institution"
    email: "alumni@email.com"
    website: ""
    github: ""
    ads: ""
    orcid: ""
```

## 📸 Adding Member Photos

1. Save photos in `images/people/` directory
2. Use consistent naming: `firstname_lastname.jpg`
3. Recommended size: 300x300 pixels (will be cropped to circle)
4. Supported formats: JPG, PNG

## 🔄 Common Tasks

### Adding a New Current Member

```bash
python scripts/update_group_member.py
# Choose option 1: Add current member
# Fill in the prompts
```

### Moving a Member to Alumni

```bash
python scripts/update_group_member.py
# Choose option 7: Move member between sections
# Choose option 1: Current → Alumni
# Select the member and provide their current position
```

### Updating Member Information

```bash
python scripts/update_group_member.py
# Choose option 3: Edit current member (or 4 for alumni)
# Select the member and update fields
```

## 🎨 Customization

### Changing the Layout

The layout is defined in `group.html`. Key CSS classes:
- `.member-card` - Individual member cards
- `.member-image` - Photo container
- `.member-info` - Text information
- `.alumni` - Alumni-specific styling

### Adding New Fields

1. Add the field to `_data/group_members.yml`
2. Update the template in `group.html` to display it
3. Update the Python script if using it

## 📱 Responsive Design

The page automatically adapts to different screen sizes:
- Desktop: Grid layout with multiple columns
- Mobile: Single column layout
- Images scale appropriately

## 🔧 Troubleshooting

### Missing Images
- Check that image files exist in `images/people/`
- Verify filename matches the YAML entry
- Placeholder icons will show if no image is specified

### YAML Syntax Errors
- Use a YAML validator (like [yamllint.com](https://www.yamllint.com/))
- Check indentation (use spaces, not tabs)
- Ensure quotes are properly closed

### Script Issues
- Make sure Python 3 is installed
- Install PyYAML: `pip install pyyaml`
- Check file permissions on the script

## 💡 Tips

1. **Keep descriptions concise** - 2-3 sentences work best
2. **Use consistent naming** for images
3. **Update regularly** - especially when people join/leave
4. **Backup the YAML file** before major changes
5. **Test locally** before pushing to GitHub

## 🆘 Need Help?

If you encounter issues:
1. Check the browser console for errors
2. Verify the YAML syntax
3. Test the local Jekyll build: `bundle exec jekyll serve`
4. Check that all image paths are correct
