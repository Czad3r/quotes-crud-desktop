import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from db import Database
import re

db = Database('store.db')

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Quotes Manager')
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), 450))
        self.create_widgets()
        self.selected_item = 0
        self.populate_list()

    def create_widgets(self):
        self.textFieldWidth=90
        self.create_Quote()
        self.create_Author()
        self.create_Source()
        self.create_Date()
        self.create_QuotesList()
        self.create_Scrollbar()
        self.quotes_list.bind('<<TreeviewSelect>>', self.select_item)
        self.create_Buttons()

    def create_Quote(self):
        self.quote_text = tk.StringVar()
        self.quote_label = tk.Label(self.master, text='Quote', font=('bold', 14), padx=20, pady=20)
        self.quote_label.grid(row=0, column=0, sticky=tk.W)
        self.quote_entry = tk.Entry(self.master, textvariable=self.quote_text,width=self.textFieldWidth)
        self.quote_entry.grid(row=0, column=1)
        
    def create_Author(self):
        self.author_text = tk.StringVar()
        self.author_label = tk.Label(self.master, text='Author', font=('bold', 14))
        self.author_label.grid(row=0, column=2, sticky=tk.W)
        self.author_entry = tk.Entry(self.master, textvariable=self.author_text,width=self.textFieldWidth)
        self.author_entry.grid(row=0, column=3)
        
    def create_Source(self):
        self.source_text = tk.StringVar()
        self.source_label = tk.Label(self.master, text='Source', font=('bold', 14), padx=20)
        self.source_label.grid(row=1, column=0, sticky=tk.W)
        self.source_entry = tk.Entry(self.master, textvariable=self.source_text,width=self.textFieldWidth)
        self.source_entry.grid(row=1, column=1)
    
    def create_Date(self):
        self.date_text = tk.StringVar()
        self.date_label = tk.Label(self.master, text='Date(yyyy-mm-dd)', font=('bold', 14))
        self.date_label.grid(row=1, column=2, sticky=tk.W)
        self.date_entry = tk.Entry(self.master, textvariable=self.date_text,width=self.textFieldWidth)
        self.date_entry.grid(row=1, column=3)
        
    def create_QuotesList(self):
        self.quotes_list = ttk.Treeview(self.master)
        self.quotes_list["columns"]=("Quote","Author","Source","Date")
        self.quotes_list.column("#0", width=40, minwidth=40)
        self.quotes_list.column("Quote", width=850, minwidth=650)
        self.quotes_list.column("Author", width=150, minwidth=150)
        self.quotes_list.column("Source", width=150, minwidth=150)
        self.quotes_list.column("Date", width=150, minwidth=150)
        self.quotes_list.heading("#0",text="ID",anchor=tk.W)
        self.quotes_list.heading("Quote", text="Quote",anchor=tk.W)
        self.quotes_list.heading("Author", text="Author",anchor=tk.W)
        self.quotes_list.heading("Source", text="Source",anchor=tk.W)
        self.quotes_list.heading("Date", text="Date",anchor=tk.W)
        self.quotes_list.grid(row=3, column=0,columnspan=4,rowspan=3, pady=20, padx=20)
        
    def create_Scrollbar(self):
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=4,rowspan=6,sticky='w')
        self.quotes_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.quotes_list.yview)

    def create_Buttons(self):
        self.add_btn = tk.Button(self.master, text="Add quote", width=12, command=self.add_item)
        self.add_btn.grid(row=2, column=0, pady=20)

        self.remove_btn = tk.Button(self.master, text="Remove quote", width=12, command=self.remove_item)
        self.remove_btn.grid(row=2, column=1)

        self.update_btn = tk.Button(self.master, text="Update quote", width=12, command=self.update_item)
        self.update_btn.grid(row=2, column=2)

        self.exit_btn = tk.Button(self.master, text="Clear Inputs", width=12, command=self.clear_text)
        self.exit_btn.grid(row=2, column=3)
    
    def populate_list(self):
        self.quotes_list.delete(*self.quotes_list.get_children())
        for row in db.fetch():
            self.quotes_list.insert("", "end", row[0], text=row[0], values=(row[1],row[2],row[3],row[4]))

    @staticmethod
    def __chceck_date(date):
        flag = re.findall("^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$", date)
        return False if flag else True

    @staticmethod
    def __chceck_author(author):
        flag = re.findall("^[^1-9-+/*@%^{}['\]]+?$$",author)
        return False if flag else True

    def __chceck_inputs(self):

        if self.quote_text.get() == '' or self.source_text.get() == '':
            messagebox.showerror(
                "Required Fields", "Please include all fields")
            return False

        if Application.__chceck_date(self.date_text.get()):
            messagebox.showerror(
                "Required Fields", "Invalid date format (yyyy-mm-dd)")
            return False

        if Application.__chceck_author(self.author_text.get()):
            messagebox.showerror(
                "Required Fields", "Please enter correct author's name")
            return False

        return True

    def add_item(self):

        if self.__chceck_inputs():
            db.insert(self.quote_text.get(), self.author_text.get(),self.source_text.get(), self.date_text.get())
            self.clear_text()
            self.populate_list()

    def select_item(self, event):
        try:
            id=self.quotes_list.focus()
            self.selected_item = (id,)+self.quotes_list.item(id,option='values')

            self.quote_entry.delete(0, tk.END)
            self.quote_entry.insert(tk.END, self.selected_item[1])
            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(tk.END, self.selected_item[2])
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(tk.END, self.selected_item[3])
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(tk.END, self.selected_item[4])
        except IndexError:
            pass

    def remove_item(self):
        db.remove(self.selected_item[0])
        self.clear_text()
        self.populate_list()

    def update_item(self):

        if self.__chceck_inputs():
            db.update(self.selected_item[0], self.quote_text.get(), self.author_text.get(), self.source_text.get(), self.date_text.get())
            self.populate_list()

    def clear_text(self):
        self.quote_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.source_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
