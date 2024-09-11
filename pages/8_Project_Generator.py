import streamlit as st
import json
import os
import random

# Function to load the project ideas from a JSON file
def load_project_ideas():
    file_path = 'project_ideas.json'
    #file_path = os.path.join(os.path.dirname(__file__), 'project_ideas.json')
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to get a random project based on difficulty
def get_random_project(project_ideas, difficulty='Beginner'):
    if difficulty not in project_ideas:
        return "Whoa, you just broke the difficulty level! Choose 'Beginner', 'Intermediate', or 'HARDCORE'."
    return random.choice(project_ideas[difficulty])

# Streamlit app content directly
st.title("🤖 Random Coding Project Generator 🚀")

# Load the project ideas from JSON
project_ideas = load_project_ideas()

# Difficulty level selection with emojis
difficulty_options = {
    'Beginner 🐣 (Simple enough to do in your sleep)': 'Beginner',
    'Intermediate 🚀 (You might need coffee for this)': 'Intermediate',
    'HARDCORE 💀 (Prepare for sleepless nights)': 'HARDCORE'
}

difficulty_display = list(difficulty_options.keys())
selected_display = st.selectbox("Choose your difficulty level:", difficulty_display)
difficulty = difficulty_options[selected_display]

# Button to generate a random project
if st.button("Surprise me with a project! 🎲"):
    project = get_random_project(project_ideas, difficulty)
    st.write(f"**Your project idea is:** {project}")
    st.write("Good luck, you got this! 💪")
