from fastapi import FastAPI, HTTPException
import os
import subprocess
import json
from datetime import datetime
import sqlite3

app = FastAPI()

DATA_DIR = "/data"

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

@app.post("/run")
async def run_task(task: str):
    ensure_data_dir()
    try:
        if "count wednesdays" in task.lower():
            return {"status": "success", "message": count_wednesdays()}
        elif "sort contacts" in task.lower():
            return {"status": "success", "message": sort_contacts()}
        elif "extract email sender" in task.lower():
            return {"status": "success", "message": extract_email_sender()}
        else:
            raise HTTPException(status_code=400, detail="Task not supported")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file(path: str):
    file_path = os.path.join(DATA_DIR, path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(file_path, "r") as file:
        content = file.read()
    return {"content": content}

def count_wednesdays():
    file_path = os.path.join(DATA_DIR, "dates.txt")
    if not os.path.exists(file_path):
        return "File not found"
    
    with open(file_path, "r") as file:
        dates = file.readlines()
    
    count = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)
    output_path = os.path.join(DATA_DIR, "dates-wednesdays.txt")
    with open(output_path, "w") as file:
        file.write(str(count))
    
    return f"Counted {count} Wednesdays. Saved to dates-wednesdays.txt"

def sort_contacts():
    file_path = os.path.join(DATA_DIR, "contacts.json")
    if not os.path.exists(file_path):
        return "File not found"
    
    with open(file_path, "r") as file:
        contacts = json.load(file)
    
    contacts_sorted = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    output_path = os.path.join(DATA_DIR, "contacts-sorted.json")
    with open(output_path, "w") as file:
        json.dump(contacts_sorted, file, indent=4)
    
    return "Sorted contacts and saved to contacts-sorted.json"

def extract_email_sender():
    file_path = os.path.join(DATA_DIR, "email.txt")
    if not os.path.exists(file_path):
        return "File not found"
    
    with open(file_path, "r") as file:
        content = file.read()
    
    sender_email = content.split("From: ")[1].split("\n")[0]  # Extract email
    output_path = os.path.join(DATA_DIR, "email-sender.txt")
    with open(output_path, "w") as file:
        file.write(sender_email)
    
    return f"Extracted email: {sender_email}"

from fastapi import FastAPI

app = FastAPI()

@app.get("/")  # This will handle requests to http://127.0.0.1:8000
def read_root():
    return {"message": "FastAPI is running!"}

