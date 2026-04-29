import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from functions import *
import os

class PhonebookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Phonebook Manager")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f0f0")
        
        # Load contacts
        self.phonebook = load_contacts()
        self.filtered_contacts = self.phonebook
        self.selected_category = "All"
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), background="#f0f0f0")
        style.configure('TButton', font=('Helvetica', 10))
        
        self.create_widgets()
        self.refresh_display()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header = ttk.Label(main_frame, text="📞 PHONEBOOK MANAGER", style='Header.TLabel')
        header.pack(pady=(0, 20))
        
        # Top control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, padx=0, pady=(0, 15))
        
        # Category filter
        cat_frame = ttk.Frame(control_frame)
        cat_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(cat_frame, text="Category:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.category_var = tk.StringVar(value="All")
        self.category_combo = ttk.Combobox(cat_frame, textvariable=self.category_var, 
                                           width=15, state='readonly')
        self.category_combo.pack(side=tk.LEFT)
        self.category_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_by_category())
        
        # Search frame
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_display())
        
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=0, pady=(0, 15))
        
        ttk.Button(button_frame, text="➕ Add Contact", command=self.add_contact_window).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="✎ Edit", command=self.edit_contact).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="🗑️ Delete", command=self.delete_contact).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="📁 Manage Categories", command=self.manage_categories).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="⬆️ Sort", command=self.sort_window).pack(side=tk.LEFT, padx=3)
        
        # Contacts list frame
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 15))
        
        # Create treeview
        columns = ('Name', 'Number', 'Category')
        self.tree = ttk.Treeview(list_frame, columns=columns, height=15, show='headings')
        
        # Define column headings and widths
        self.tree.column('Name', width=250, anchor=tk.W)
        self.tree.column('Number', width=200, anchor=tk.CENTER)
        self.tree.column('Category', width=150, anchor=tk.CENTER)
        
        self.tree.heading('Name', text='Name')
        self.tree.heading('Number', text='Phone Number')
        self.tree.heading('Category', text='Category')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, padx=0, pady=(0, 0))
        
        self.status_label = ttk.Label(status_frame, text="", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, side=tk.LEFT)
    
    def refresh_display(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter contacts and keep track of which ones are displayed
        search_term = self.search_var.get().lower()
        filtered = self.phonebook
        
        if search_term:
            filtered = [c for c in filtered if search_term in c['name'].lower()]
        
        if self.selected_category != "All":
            filtered = [c for c in filtered if c.get('category', 'General') == self.selected_category]
        
        # Store filtered contacts for reference
        self.filtered_contacts = filtered
        
        # Add to treeview
        for i, contact in enumerate(filtered):
            category = contact.get('category', 'General')
            # Store index in the tree item tags for easy retrieval
            self.tree.insert('', tk.END, values=(contact['name'], contact['number'], category), tags=(str(i),))
        
        # Update status
        total = len(self.phonebook)
        shown = len(filtered)
        self.status_label.config(text=f"Showing {shown} of {total} contacts")
        
        # Update category combo
        categories = ["All"] + get_all_categories(self.phonebook)
        self.category_combo['values'] = categories
    
    def filter_by_category(self):
        self.selected_category = self.category_var.get()
        self.refresh_display()
    
    def clear_search(self):
        self.search_var.set("")
        self.refresh_display()
    
    def add_contact_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Contact")
        window.geometry("400x250")
        window.transient(self.root)
        window.grab_set()
        
        # Name
        ttk.Label(window, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(window, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        name_entry.focus()
        
        # Number
        ttk.Label(window, text="Phone Number:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        number_var = tk.StringVar()
        number_entry = ttk.Entry(window, textvariable=number_var, width=30)
        number_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Category
        ttk.Label(window, text="Category:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        category_var = tk.StringVar(value="General")
        category_combo = ttk.Combobox(window, textvariable=category_var, width=27)
        category_combo['values'] = get_all_categories(self.phonebook) + ["New Category..."]
        category_combo.grid(row=2, column=1, padx=10, pady=10)
        
        def save_contact():
            name = name_var.get().strip()
            number = number_var.get().strip()
            category = category_var.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            if not number:
                messagebox.showerror("Error", "Phone number cannot be empty")
                return
            
            if not number.isdigit():
                messagebox.showerror("Error", "Phone number must contain only digits")
                return
            
            if category == "New Category...":
                category = simpledialog.askstring("New Category", "Enter category name:")
                if not category:
                    return
            
            self.phonebook.append({
                "name": name,
                "number": int(number),
                "category": category
            })
            save_contacts(self.phonebook)
            messagebox.showinfo("Success", "Contact added successfully!")
            self.refresh_display()
            window.destroy()
        
        ttk.Button(window, text="Save", command=save_contact).grid(row=3, column=0, columnspan=2, pady=20)
    
    def edit_contact(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to edit")
            return
        
        item = selection[0]
        tags = self.tree.item(item)['tags']
        
        if not tags:
            messagebox.showerror("Error", "Could not identify contact")
            return
        
        contact_index = int(tags[0])
        contact = self.filtered_contacts[contact_index]
        
        window = tk.Toplevel(self.root)
        window.title("Edit Contact")
        window.geometry("400x250")
        window.transient(self.root)
        window.grab_set()
        
        # Name
        ttk.Label(window, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        name_var = tk.StringVar(value=contact['name'])
        name_entry = ttk.Entry(window, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Number
        ttk.Label(window, text="Phone Number:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        number_var = tk.StringVar(value=str(contact['number']))
        number_entry = ttk.Entry(window, textvariable=number_var, width=30)
        number_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Category
        ttk.Label(window, text="Category:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        category_var = tk.StringVar(value=contact.get('category', 'General'))
        category_combo = ttk.Combobox(window, textvariable=category_var, width=27)
        category_combo['values'] = get_all_categories(self.phonebook)
        category_combo.grid(row=2, column=1, padx=10, pady=10)
        
        def save_changes():
            name = name_var.get().strip()
            number_str = number_var.get().strip()
            category = category_var.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            if not number_str or not number_str.isdigit():
                messagebox.showerror("Error", "Phone number must contain only digits")
                return
            
            contact['name'] = name
            contact['number'] = int(number_str)
            contact['category'] = category
            save_contacts(self.phonebook)
            messagebox.showinfo("Success", "Contact updated successfully!")
            self.refresh_display()
            window.destroy()
        
        ttk.Button(window, text="Save", command=save_changes).grid(row=3, column=0, columnspan=2, pady=20)
    
    def delete_contact(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to delete")
            return
        
        item = selection[0]
        tags = self.tree.item(item)['tags']
        
        if not tags:
            messagebox.showerror("Error", "Could not identify contact")
            return
        
        contact_index = int(tags[0])
        contact = self.filtered_contacts[contact_index]
        
        if messagebox.askyesno("Confirm", f"Delete '{contact['name']}'?"):
            self.phonebook.remove(contact)
            save_contacts(self.phonebook)
            messagebox.showinfo("Success", "Contact deleted!")
            self.refresh_display()
    
    def manage_categories(self):
        window = tk.Toplevel(self.root)
        window.title("Manage Categories")
        window.geometry("450x400")
        window.transient(self.root)
        window.grab_set()
        
        # Header
        ttk.Label(window, text="Categories:", font=('Helvetica', 12, 'bold')).pack(padx=10, pady=10)
        
        # Create frame with scrollbar for categories
        list_frame = ttk.Frame(window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        categories = get_all_categories(self.phonebook)
        for cat in categories:
            count = sum(1 for c in self.phonebook if c.get('category', 'General') == cat)
            cat_frame = ttk.Frame(scrollable_frame)
            cat_frame.pack(fill=tk.X, pady=5, padx=5)
            
            label = ttk.Label(cat_frame, text=f"  {cat}: {count} contacts")
            label.pack(side=tk.LEFT, anchor=tk.W)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add new category section
        add_frame = ttk.Frame(window)
        add_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)
        
        ttk.Label(add_frame, text="Add New Category:", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        input_frame = ttk.Frame(add_frame)
        input_frame.pack(fill=tk.X)
        
        new_cat_var = tk.StringVar()
        new_cat_entry = ttk.Entry(input_frame, textvariable=new_cat_var, width=30)
        new_cat_entry.pack(side=tk.LEFT, padx=(0, 5))
        new_cat_entry.focus()
        
        def add_new_category():
            new_cat = new_cat_var.get().strip()
            if not new_cat:
                messagebox.showerror("Error", "Category name cannot be empty")
                return
            
            categories = get_all_categories(self.phonebook)
            if new_cat in categories:
                messagebox.showerror("Error", f"Category '{new_cat}' already exists")
                return
            
            # Create a contact with the new category to save it
            messagebox.showinfo("Success", f"Category '{new_cat}' created! It will be available when adding contacts.")
            self.category_combo['values'] = ["All"] + get_all_categories(self.phonebook) + [new_cat]
            new_cat_entry.delete(0, tk.END)
        
        ttk.Button(input_frame, text="Add", command=add_new_category).pack(side=tk.LEFT)
    
    def sort_window(self):
        window = tk.Toplevel(self.root)
        window.title("Sort Contacts")
        window.geometry("300x200")
        window.transient(self.root)
        window.grab_set()
        
        ttk.Label(window, text="Sort by:", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        def sort_by(key, reverse=False):
            self.phonebook.sort(key=lambda c: c[key].lower() if isinstance(c[key], str) else c[key], reverse=reverse)
            save_contacts(self.phonebook)
            self.refresh_display()
            window.destroy()
            messagebox.showinfo("Success", "Contacts sorted!")
        
        ttk.Button(window, text="Name (A-Z)", 
                  command=lambda: sort_by('name', False)).pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(window, text="Name (Z-A)", 
                  command=lambda: sort_by('name', True)).pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(window, text="Phone Number", 
                  command=lambda: sort_by('number', False)).pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(window, text="Category", 
                  command=lambda: sort_by('category', False)).pack(fill=tk.X, padx=10, pady=5)

def main():
    root = tk.Tk()
    app = PhonebookGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
