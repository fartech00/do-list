import streamlit as st
import sys
import pandas as pd
import json
import os
from datetime import date

# File to store tasks
task_file = "tasks.json"

# Load existing tasks
def load_tasks():
    if os.path.exists(task_file):
        with open(task_file, "r") as file:
            return json.load(file)
    return {}

# Save tasks
def save_tasks(tasks):
    with open(task_file, "w") as file:
        json.dump(tasks, file)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# App Title
st.title("🗓️ Calendar & To-Do List")

# Calendar Selection
selected_date = st.date_input("Select a date", date.today())

# Display Tasks for Selected Date
selected_date_str = str(selected_date)
if selected_date_str not in st.session_state.tasks:
    st.session_state.tasks[selected_date_str] = []

st.subheader(f"Tasks for {selected_date_str}")

tasks = st.session_state.tasks[selected_date_str]
for i, task in enumerate(tasks):
    col1, col2, col3 = st.columns([6, 2, 2])
    with col1:
        updated_task = st.text_input(f"Task {i+1}", task, key=f"task_{selected_date_str}_{i}")
    with col2:
        if st.button("Update", key=f"update_{selected_date_str}_{i}"):
            st.session_state.tasks[selected_date_str][i] = updated_task
            save_tasks(st.session_state.tasks)
    with col3:
        if st.button("Delete", key=f"delete_{selected_date_str}_{i}"):
            del st.session_state.tasks[selected_date_str][i]
            save_tasks(st.session_state.tasks)
            st.rerun()

# Add New Task
new_task = st.text_input("New Task")
if st.button("Add Task"):
    if new_task:
        st.session_state.tasks[selected_date_str].append(new_task)
        save_tasks(st.session_state.tasks)
        st.rerun()

# Save tasks before closing the app
save_tasks(st.session_state.tasks)
