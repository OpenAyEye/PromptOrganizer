import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import openai
import datetime
import pandas as pd
import keyfile
import os
import pyperclip
import time
# Set up the OpenAI API
openai.api_key = keyfile.OpenAikey

# Define the categories
categories = ["code help", "write something", "Jailbreaks", "Summarize", "Act as Character", "Manipulate Text"]

def load_data():
    if os.path.exists("GPTPrompts.xlsx"):
        df = pd.read_excel("GPTPrompts.xlsx", sheet_name="Sheet1")
        return df
    else:
        return pd.DataFrame(columns=["Name", "Date:Time", "Category", "Prompt"])

def organize_data(column):
    global data_df
    data_df = data_df.sort_values(by=column)
    update_treeview()

def update_treeview():
    for i in tree.get_children():
        tree.delete(i)

    for index, row in data_df.iterrows():
        tree.insert("", "end", values=(row["Name"], row["Date:Time"], row["Category"], row["Prompt"]))

def submit_prompt():
    global data_df
    prompt = prompt_entry.get()
    promptname = name_entry.get()
    prompt_text = f"hey the following is a prompt for gpt, would it be best categorized as {categories} please respond only with the quoted category, your responses will be parsed via python and it's much easier if you respond only with one of these {categories} Here is the prompt to categorize: {prompt}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content":
                "You are a helpful assistant."},
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.5,
        max_tokens=2600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=["\nUser:"],
    )

    # Get the category
    category = response["choices"][0]["message"]["content"]

    # Get the current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Save the data to a Pandas DataFrame
    data = {
        "Name": [promptname],
        "Date:Time": [date_time],
        "Category": [category],
        "Prompt": [prompt]

    }
    df = pd.DataFrame(data)

    # Save the data to an Excel file
    # Read the existing data from the Excel file
    existing_data = None
    if os.path.exists("GPTPrompts.xlsx"):
        existing_data = pd.read_excel("GPTPrompts.xlsx", sheet_name="Sheet1")

    # Concatenate the new data with the existing data
    if 'existing_data' in locals():
        combined_data = pd.concat([existing_data, df], ignore_index=True)
    else:
        combined_data = df

    # Write the combined data back to Sheet1
    with pd.ExcelWriter("GPTPrompts.xlsx") as writer:
        combined_data.to_excel(writer, index=False, sheet_name="Sheet1")

    messagebox.showinfo("Success", "Prompt saved successfully.")
    time.sleep(2)
    data_df = load_data()

    update_treeview()


def copy_to_clipboard(text):
    pyperclip.copy(text)

def copy_prompt_to_clipboard():
    item = tree.selection()[0]
    values = tree.item(item, "values")
    prompt = values[3]
    pyperclip.copy(prompt)




app = tk.Tk()
app.title("GPT Prompt Organizer")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add Treeview
data_df = load_data()

tree = ttk.Treeview(frame, columns=("Name", "Date:Time", "Category", "Prompt"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Date:Time", text="Date:Time")
tree.heading("Category", text="Category")
tree.heading("Prompt", text="Prompt")
tree.column("Name", width=150, anchor=tk.CENTER)
tree.column("Date:Time", width=150, anchor=tk.CENTER)
tree.column("Category", width=150, anchor=tk.CENTER)
tree.column("Prompt", width=300, anchor=tk.CENTER)
tree.grid(row=0, column=0, columnspan=3)

organize_by_name_button = ttk.Button(frame, text="Organize by Name", command=lambda: organize_data("Name"))
organize_by_name_button.grid(row=1, column=0, pady=10)

organize_by_date_button = ttk.Button(frame, text="Organize by Date", command=lambda: organize_data("Date:Time"))
organize_by_date_button.grid(row=1, column=1, pady=10)

organize_by_category_button = ttk.Button(frame, text="Organize by Category", command=lambda: organize_data("Category"))
organize_by_category_button.grid(row=1, column=2, pady=10)
copy_button = ttk.Button(frame, text="Copy to Clipboard", command=copy_prompt_to_clipboard)
copy_button.grid(row=2, column=2, pady=10)
update_treeview()

# Add entry fields and submit button
name_label = ttk.Label(frame, text="Prompt Name:")
name_label.grid(column=0, row=2, sticky=tk.W)
name_entry = ttk.Entry(frame, width=50)
name_entry.grid(column=1, row=2)

prompt_label = ttk.Label(frame, text="Prompt:")
prompt_label.grid(column=0, row=3, sticky=tk.W)
prompt_entry = ttk.Entry(frame, width=50)
prompt_entry.grid(column=1, row=3)

submit_button = ttk.Button(frame, text="Submit Prompt", command=submit_prompt)
submit_button.grid(column=1, row=4, pady=10)

app.mainloop()