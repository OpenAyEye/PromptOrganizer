import openai
import datetime
import pandas as pd
import keyfile
import os
# Set up the OpenAI API
openai.api_key = keyfile.OpenAikey

# Define the categories
categories = ["code help", "write something", "Jailbreaks", "Summarize", "Act as Character", "Manipulate Text"]

# Get the prompt from the user
prompt = input("Enter a GPT prompt: ")
promptname = input("Name the prompt: ")
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
if os.path.exists("GPT Prompts.xlsx"):
    existing_data = pd.read_excel("GPT Prompts.xlsx", sheet_name="Sheet1")

# Concatenate the new data with the existing data
if 'existing_data' in locals():
    combined_data = pd.concat([existing_data, df], ignore_index=True)
else:
    combined_data = df

# Write the combined data back to Sheet1
with pd.ExcelWriter("GPT Prompts.xlsx") as writer:
    combined_data.to_excel(writer, index=False, sheet_name="Sheet1")


