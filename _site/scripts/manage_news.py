#!/usr/bin/env python3
"""
Script to easily manage news and travel items in the Jekyll data file.
Usage: python scripts/manage_news.py
"""

import yaml
import os
import sys
from datetime import datetime

def load_news_data():
    """Load the current news data from YAML file."""
    data_file = "_data/news.yml"
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return yaml.safe_load(f)
    else:
        return {"items": [], "categories": []}

def save_news_data(data):
    """Save the news data back to YAML file."""
    data_file = "_data/news.yml"
    with open(data_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)

def add_news_item(data):
    """Add a new news item."""
    print("\n=== Adding new news item ===")
    
    item = {}
    
    # Get date
    while True:
        date_input = input("Date (YYYY-MM-DD, or 'today'): ").strip()
        if date_input.lower() == 'today':
            item['date'] = datetime.now().strftime("%Y-%m-%d")
            break
        elif len(date_input) == 10 and date_input.count('-') == 2:
            item['date'] = date_input
            break
        else:
            print("Please enter a valid date in YYYY-MM-DD format or 'today'")
    
    item['title'] = input("Title: ").strip()
    item['description'] = input("Description: ").strip()
    
    # Show available categories
    print("\nAvailable categories:")
    for i, cat in enumerate(data['categories']):
        print(f"{i+1}. {cat['display_name']} ({cat['name']})")
    
    while True:
        try:
            cat_choice = int(input(f"\nSelect category (1-{len(data['categories'])}): ")) - 1
            if 0 <= cat_choice < len(data['categories']):
                item['category'] = data['categories'][cat_choice]['name']
                break
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")
    
    # Optional fields
    link = input("Link URL (optional): ").strip()
    if link:
        item['link'] = link
    
    featured = input("Featured item? (y/n, default: n): ").strip().lower()
    item['featured'] = featured in ['y', 'yes', 'true']
    
    data['items'].append(item)
    print(f"\n✅ Added news item: {item['title']}")

def edit_news_item(data):
    """Edit an existing news item."""
    if not data['items']:
        print("No news items found.")
        return
    
    print(f"\n=== Current news items ===")
    for i, item in enumerate(data['items']):
        print(f"{i+1}. {item['date']} - {item['title']}")
    
    try:
        choice = int(input(f"\nSelect item to edit (1-{len(data['items'])}): ")) - 1
        if 0 <= choice < len(data['items']):
            item = data['items'][choice]
            print(f"\n=== Editing: {item['title']} ===")
            
            # Allow editing each field
            new_date = input(f"Date ({item['date']}): ").strip()
            if new_date:
                item['date'] = new_date
                
            new_title = input(f"Title ({item['title']}): ").strip()
            if new_title:
                item['title'] = new_title
                
            new_description = input(f"Description ({item['description'][:50]}...): ").strip()
            if new_description:
                item['description'] = new_description
                
            new_link = input(f"Link ({item.get('link', '')}): ").strip()
            if new_link:
                item['link'] = new_link
            elif 'link' in item and not new_link:
                del item['link']
            
            new_featured = input(f"Featured ({item.get('featured', False)}): ").strip().lower()
            if new_featured in ['y', 'yes', 'true']:
                item['featured'] = True
            elif new_featured in ['n', 'no', 'false']:
                item['featured'] = False
            
            print(f"\n✅ Updated: {item['title']}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

def remove_news_item(data):
    """Remove a news item."""
    if not data['items']:
        print("No news items found.")
        return
    
    print(f"\n=== Current news items ===")
    for i, item in enumerate(data['items']):
        print(f"{i+1}. {item['date']} - {item['title']}")
    
    try:
        choice = int(input(f"\nSelect item to remove (1-{len(data['items'])}): ")) - 1
        if 0 <= choice < len(data['items']):
            item = data['items'].pop(choice)
            print(f"\n✅ Removed: {item['title']}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

def view_news_items(data):
    """View all news items."""
    if not data['items']:
        print("No news items found.")
        return
    
    print(f"\n=== All News Items ({len(data['items'])} total) ===")
    
    # Sort by date (newest first)
    sorted_items = sorted(data['items'], key=lambda x: x['date'], reverse=True)
    
    for i, item in enumerate(sorted_items):
        featured_mark = " ⭐" if item.get('featured', False) else ""
        category = next((cat['display_name'] for cat in data['categories'] if cat['name'] == item['category']), item['category'])
        print(f"\n{i+1}. {item['date']} - {item['title']}{featured_mark}")
        print(f"   Category: {category}")
        print(f"   Description: {item['description'][:100]}...")
        if item.get('link'):
            print(f"   Link: {item['link']}")

def add_category(data):
    """Add a new category."""
    print("\n=== Adding new category ===")
    
    category = {}
    category['name'] = input("Category name (lowercase, no spaces): ").strip()
    category['display_name'] = input("Display name: ").strip()
    category['icon'] = input("FontAwesome icon (e.g., fa-briefcase): ").strip()
    category['color'] = input("Color (hex code, e.g., #28a745): ").strip()
    
    data['categories'].append(category)
    print(f"\n✅ Added category: {category['display_name']}")

def main():
    """Main function to run the news management script."""
    print("=== News and Travel Management ===")
    print("This script helps you manage news items in the Jekyll data file.")
    
    data = load_news_data()
    
    while True:
        print("\n=== Menu ===")
        print("1. Add news item")
        print("2. Edit news item")
        print("3. Remove news item")
        print("4. View all news items")
        print("5. Add category")
        print("6. View current data")
        print("7. Save and exit")
        print("0. Exit without saving")
        
        try:
            choice = int(input("\nSelect option (0-7): "))
            
            if choice == 1:
                add_news_item(data)
            elif choice == 2:
                edit_news_item(data)
            elif choice == 3:
                remove_news_item(data)
            elif choice == 4:
                view_news_items(data)
            elif choice == 5:
                add_category(data)
            elif choice == 6:
                print("\n=== Current Data ===")
                print(yaml.dump(data, default_flow_style=False, sort_keys=False))
            elif choice == 7:
                save_news_data(data)
                print("\n✅ Data saved successfully!")
                break
            elif choice == 0:
                print("\nExiting without saving changes.")
                break
            else:
                print("Invalid choice. Please select 0-7.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break

if __name__ == "__main__":
    main()
