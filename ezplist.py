# EzPlist Project
# All Rights Reserved
# Megab1t @ Github

import sys
import os
import zipfile
import plistlib
import shutil

def unzip_ipa(ipa_file):
    # Change extension to .zip
    zip_file = ipa_file.replace('.ipa', '.zip')
    os.rename(ipa_file, zip_file)
    
    # Unzip the file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('.')
    
    return zip_file

def find_plist_files(directory):
    plist_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.plist'):
                plist_files.append(os.path.join(root, file))
    
    return plist_files

def view_plist_file(plist_file):
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)
        xml_output = plistlib.dumps(plist_data).decode('utf-8')
        print(xml_output)
        
        # Prompt user to save the XML output to a file
        save_choice = input("Do you want to save the XML output to a file? (y/n): ")
        if save_choice.lower() == "y":
            save_file = input("Enter the path to save the XML file: ")
            with open(save_file, 'w') as output_file:
                output_file.write(xml_output)
                print(f"XML output saved to {save_file}")

def cleanup(zip_file):
    # Delete the 'Payload' folder.
    shutil.rmtree('Payload')

    # Rename the zip file back to an IPA file
    ipa_file = zip_file.replace('.zip', '.ipa')
    os.rename(zip_file, ipa_file)

def main():
    # Check if IPA file argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <ipa_file>")
        return
    
    ipa_file = sys.argv[1]
    
    # Unzip the IPA file
    zip_file = unzip_ipa(ipa_file)
    
    # Find plist files
    plist_files = find_plist_files('.')
    
    # Display numbered list of plist files
    for i, plist_file in enumerate(plist_files):
        print(f"{i + 1}. {plist_file}")
    
    if len(plist_files) == 0:
        print("No plist files found.")
        cleanup(zip_file)
        return
    
    # Prompt user to choose a plist file to view
    choice = input("Enter the number of the plist file to view (0 to exit): ")
    if choice == "0":
        cleanup(zip_file)
        return
    
    try:
        choice = int(choice)
        if choice < 1 or choice > len(plist_files):
            print("Invalid choice.")
            cleanup(zip_file)
            return
    except ValueError:
        print("Invalid choice.")
        cleanup(zip_file)
        return
    
    # View the chosen plist file in XML format
    plist_file = plist_files[choice - 1]
    view_plist_file(plist_file)
    
    # Perform cleanup
    cleanup(zip_file)

if __name__ == "__main__":
    main()
