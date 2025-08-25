#!/usr/bin/env python3
"""
Script to easily add or update group members in the Jekyll data file.
Usage: python scripts/update_group_member.py
"""

import yaml
import os
import sys
from datetime import datetime

def load_group_data():
    """Load the current group data from YAML file."""
    data_file = "_data/group_members.yml"
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return yaml.safe_load(f)
    else:
        return {"current": [], "alumni": []}

def save_group_data(data):
    """Save the group data back to YAML file."""
    data_file = "_data/group_members.yml"
    with open(data_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)

def add_member(data, section):
    """Add a new member to the specified section."""
    print(f"\n=== Adding new {section} member ===")
    
    member = {}
    member['name'] = input("Name: ").strip()
    member['role'] = input("Role: ").strip()
    member['image'] = input("Image filename (leave empty for placeholder): ").strip()
    member['description'] = input("Description: ").strip()
    member['email'] = input("Email: ").strip()
    member['website'] = input("Website URL (leave empty if none): ").strip()
    member['github'] = input("GitHub username (leave empty if none): ").strip()
    member['ads'] = input("NASA ADS URL (leave empty if none): ").strip()
    member['orcid'] = input("ORCID URL (leave empty if none): ").strip()
    
    if section == "alumni":
        member['current_position'] = input("Current position: ").strip()
    
    data[section].append(member)
    print(f"\n✅ Added {member['name']} to {section} section!")

def edit_member(data, section):
    """Edit an existing member."""
    if not data[section]:
        print(f"No {section} members found.")
        return
    
    print(f"\n=== Current {section} members ===")
    for i, member in enumerate(data[section]):
        print(f"{i+1}. {member['name']} - {member['role']}")
    
    try:
        choice = int(input(f"\nSelect member to edit (1-{len(data[section])}): ")) - 1
        if 0 <= choice < len(data[section]):
            member = data[section][choice]
            print(f"\n=== Editing {member['name']} ===")
            
            # Allow editing each field
            new_name = input(f"Name ({member['name']}): ").strip()
            if new_name:
                member['name'] = new_name
                
            new_role = input(f"Role ({member['role']}): ").strip()
            if new_role:
                member['role'] = new_role
                
            new_image = input(f"Image ({member['image']}): ").strip()
            if new_image:
                member['image'] = new_image
                
            new_description = input(f"Description ({member['description'][:50]}...): ").strip()
            if new_description:
                member['description'] = new_description
                
            new_email = input(f"Email ({member['email']}): ").strip()
            if new_email:
                member['email'] = new_email
                
            new_website = input(f"Website ({member['website']}): ").strip()
            if new_website:
                member['website'] = new_website
                
            new_github = input(f"GitHub ({member['github']}): ").strip()
            if new_github:
                member['github'] = new_github
                
            new_ads = input(f"NASA ADS URL ({member.get('ads', '')}): ").strip()
            if new_ads:
                member['ads'] = new_ads
                
            new_orcid = input(f"ORCID URL ({member.get('orcid', '')}): ").strip()
            if new_orcid:
                member['orcid'] = new_orcid
                
            if section == "alumni":
                new_position = input(f"Current position ({member.get('current_position', '')}): ").strip()
                if new_position:
                    member['current_position'] = new_position
            
            print(f"\n✅ Updated {member['name']}!")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

def remove_member(data, section):
    """Remove a member from the specified section."""
    if not data[section]:
        print(f"No {section} members found.")
        return
    
    print(f"\n=== Current {section} members ===")
    for i, member in enumerate(data[section]):
        print(f"{i+1}. {member['name']} - {member['role']}")
    
    try:
        choice = int(input(f"\nSelect member to remove (1-{len(data[section])}): ")) - 1
        if 0 <= choice < len(data[section]):
            member = data[section].pop(choice)
            print(f"\n✅ Removed {member['name']} from {section} section!")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

def move_member(data):
    """Move a member between current and alumni sections."""
    print("\n=== Move member between sections ===")
    print("1. Current → Alumni")
    print("2. Alumni → Current")
    
    try:
        choice = int(input("Select option (1-2): "))
        if choice == 1:
            if not data['current']:
                print("No current members found.")
                return
            print("\n=== Current members ===")
            for i, member in enumerate(data['current']):
                print(f"{i+1}. {member['name']} - {member['role']}")
            
            member_choice = int(input(f"\nSelect member to move (1-{len(data['current'])}): ")) - 1
            if 0 <= member_choice < len(data['current']):
                member = data['current'].pop(member_choice)
                member['role'] = f"Former {member['role']}"
                member['current_position'] = input("Current position: ").strip()
                data['alumni'].append(member)
                print(f"\n✅ Moved {member['name']} to alumni!")
        elif choice == 2:
            if not data['alumni']:
                print("No alumni members found.")
                return
            print("\n=== Alumni members ===")
            for i, member in enumerate(data['alumni']):
                print(f"{i+1}. {member['name']} - {member['role']}")
            
            member_choice = int(input(f"\nSelect member to move (1-{len(data['alumni'])}): ")) - 1
            if 0 <= member_choice < len(data['alumni']):
                member = data['alumni'].pop(member_choice)
                member['role'] = input("New role: ").strip()
                if 'current_position' in member:
                    del member['current_position']
                data['current'].append(member)
                print(f"\n✅ Moved {member['name']} to current members!")
    except ValueError:
        print("Invalid input.")

def main():
    """Main function to run the group member management script."""
    print("=== UCSB Group Member Management ===")
    print("This script helps you manage group members in the Jekyll data file.")
    
    data = load_group_data()
    
    while True:
        print("\n=== Menu ===")
        print("1. Add current member")
        print("2. Add alumni member")
        print("3. Edit current member")
        print("4. Edit alumni member")
        print("5. Remove current member")
        print("6. Remove alumni member")
        print("7. Move member between sections")
        print("8. View current data")
        print("9. Save and exit")
        print("0. Exit without saving")
        
        try:
            choice = int(input("\nSelect option (0-9): "))
            
            if choice == 1:
                add_member(data, "current")
            elif choice == 2:
                add_member(data, "alumni")
            elif choice == 3:
                edit_member(data, "current")
            elif choice == 4:
                edit_member(data, "alumni")
            elif choice == 5:
                remove_member(data, "current")
            elif choice == 6:
                remove_member(data, "alumni")
            elif choice == 7:
                move_member(data)
            elif choice == 8:
                print("\n=== Current Data ===")
                print(yaml.dump(data, default_flow_style=False, sort_keys=False))
            elif choice == 9:
                save_group_data(data)
                print("\n✅ Data saved successfully!")
                break
            elif choice == 0:
                print("\nExiting without saving changes.")
                break
            else:
                print("Invalid choice. Please select 0-9.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break

if __name__ == "__main__":
    main()
