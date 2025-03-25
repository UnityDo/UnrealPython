import csv
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def format_translation(translation):
    # Convert line breaks to \r\n
    translation = translation.replace('\n', '\r\n')
    
    # Replace straight quotes with curly quotes while preserving string structure
    translation = translation.replace('"', '" "')
    
    # Ensure translation starts and ends with double quotes
    if not translation.startswith('"'):
        translation = '"' + translation
    if not translation.endswith('"'):
        translation = translation + '"'
    
    return translation

def update_po_with_csv(po_file_path, csv_file_path, output_file_path):
    # Verify that the files exist
    if not os.path.exists(po_file_path):
        messagebox.showerror("Error", f"The PO file '{po_file_path}' does not exist.")
        return False
    if not os.path.exists(csv_file_path):
        messagebox.showerror("Error", f"The CSV file '{csv_file_path}' does not exist.")
        return False

    # Read the CSV file and create a dictionary of translations
    translations = {}
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                key = row.get('Key', '')
                translation = row.get('Translation', '')
                if key and translation:
                    translations[key] = translation
    except Exception as e:
        messagebox.showerror("CSV Read Error", f"Error reading the CSV file: {e}")
        return False

    try:
        with open(po_file_path, 'r', encoding='utf-8') as po_file:
            lines = po_file.readlines()
    except Exception as e:
        messagebox.showerror("PO File Read Error", f"Error reading the PO file: {e}")
        return False

    # Process line by line
    output_lines = []
    current_key = None
    translations_updated = 0
    keys_found = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect the key line
        key_match = re.match(r'#\. Key:\s*(.+)', line)
        if key_match:
            current_key = key_match.group(1).strip()
            keys_found += 1
            output_lines.append(line)
            i += 1
            continue

        # Detect the start of msgstr - Match any msgstr line
        msgstr_match = re.match(r'msgstr\s+"(.*)"', line)
        if msgstr_match and current_key:
            if current_key in translations:
                # Replace with the new translation
                translation = translations[current_key]
                
                # Format the translation with special handling
                formatted_translation = format_translation(translation)
                
                output_lines.append(f'msgstr {formatted_translation}\n')
                translations_updated += 1
                i += 1  # Skip the original msgstr line
                
                # Skip any continuation lines of the original msgstr
                while i < len(lines) and lines[i].strip().startswith('"'):
                    i += 1
                continue
            else:
                # Keep the original msgstr line if no translation exists
                output_lines.append(line)
                i += 1
                continue
        
        # Keep msgid unchanged, including multiple lines
        msgid_match = re.match(r'msgid\s+".*"', line)
        if msgid_match:
            output_lines.append(line)
            i += 1
            # Copy any continuation lines
            while i < len(lines) and lines[i].strip().startswith('"'):
                output_lines.append(lines[i])
                i += 1
            continue

        # Any other line we add it without changes
        output_lines.append(line)
        i += 1

    # Write the updated content to the output file
    try:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.writelines(output_lines)
        
        # Clean the output file
        clean_po_file(output_file_path)
        
        messagebox.showinfo("Success", 
                             f"File updated successfully!\n"
                             f"Keys found: {keys_found}\n"
                             f"Translations updated: {translations_updated}")
        return True

    except Exception as e:
        messagebox.showerror("Output File Error", f"Error writing output file: {e}")
        return False

def clean_po_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as po_file:
            lines = po_file.readlines()

        cleaned_lines = []
        for line in lines:
            cleaned_line = line.replace("///", "//").replace("//", "/")
            cleaned_lines.append(cleaned_line)

        with open(file_path, 'w', encoding='utf-8') as po_file:
            po_file.writelines(cleaned_lines)

    except Exception as e:
        messagebox.showerror("Cleaning Error", f"Error cleaning the file: {e}")

class POTranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("PO File Translator")
        master.geometry("500x300")

        # PO File Selection
        self.po_label = tk.Label(master, text="Select PO File:")
        self.po_label.pack(pady=(10,0))
        
        self.po_entry = tk.Entry(master, width=50)
        self.po_entry.pack(pady=(0,5))
        
        self.po_button = tk.Button(master, text="Browse PO File", command=self.select_po_file)
        self.po_button.pack(pady=(0,10))

        # CSV File Selection
        self.csv_label = tk.Label(master, text="Select CSV File:")
        self.csv_label.pack(pady=(10,0))
        
        self.csv_entry = tk.Entry(master, width=50)
        self.csv_entry.pack(pady=(0,5))
        
        self.csv_button = tk.Button(master, text="Browse CSV File", command=self.select_csv_file)
        self.csv_button.pack(pady=(0,10))

        # Output File Selection
        self.output_label = tk.Label(master, text="Select Output File:")
        self.output_label.pack(pady=(10,0))
        
        self.output_entry = tk.Entry(master, width=50)
        self.output_entry.pack(pady=(0,5))
        
        self.output_button = tk.Button(master, text="Browse Output File", command=self.select_output_file)
        self.output_button.pack(pady=(0,10))

        # Translate Button
        self.translate_button = tk.Button(master, text="Update PO File", command=self.translate_po_file)
        self.translate_button.pack(pady=10)

    def select_po_file(self):
        filename = filedialog.askopenfilename(
            title="Select PO File", 
            filetypes=[("PO Files", "*.po"), ("All Files", "*.*")]
        )
        if filename:
            self.po_entry.delete(0, tk.END)
            self.po_entry.insert(0, filename)

    def select_csv_file(self):
        filename = filedialog.askopenfilename(
            title="Select CSV File", 
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            self.csv_entry.delete(0, tk.END)
            self.csv_entry.insert(0, filename)

    def select_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save Updated PO File", 
            defaultextension=".po",
            filetypes=[("PO Files", "*.po"), ("All Files", "*.*")]
        )
        if filename:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)

    def translate_po_file(self):
        po_file = self.po_entry.get()
        csv_file = self.csv_entry.get()
        output_file = self.output_entry.get()

        # Validate inputs
        if not po_file:
            messagebox.showerror("Error", "Please select a PO file")
            return
        if not csv_file:
            messagebox.showerror("Error", "Please select a CSV file")
            return
        if not output_file:
            messagebox.showerror("Error", "Please select an output file")
            return

        # Perform translation
        update_po_with_csv(po_file, csv_file, output_file)

def main():
    root = tk.Tk()
    app = POTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
