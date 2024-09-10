import streamlit as st

#______________________________________________________________________FOR PERFECTIONISTS________________________________________________________________________________________________________________________________________________________

st.title("To-Do List Manager")

# Initialize an empty list for tasks and an input session state
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []
if 'new_task_input' not in st.session_state:
    st.session_state['new_task_input'] = ''

# Function to handle task submission
def submit():
    task = st.session_state['new_task_input']
    if task and task not in st.session_state['tasks']:
        st.session_state['tasks'].append(task)
    st.session_state['new_task_input'] = ''  # Clear the input field after submission

# Text input with submission handler
st.text_input('Add a new task:', key='new_task_input', on_change=submit)

# Display the list of tasks
st.write("### Your To-Do List:")
for i, task in enumerate(st.session_state['tasks']):
    if st.checkbox(f"Task {i+1}: {task}"):
        st.session_state['tasks'].remove(task)
        st.rerun()  # Refresh the app after removing a task


#____________________________OLD STUFF WHERE BUTTONS DON'T WORK PERFECTLY (BUT EVERYTHING ELSE DOES)____________________________________________________________________________________________________________________________________________
# Initialize an empty list
#if 'tasks' not in st.session_state:
#    st.session_state['tasks'] = []
#
# Input to add a new task
#new_task = st.text_input('Add a new task:')
#if st.button('Add Task'): # Maybe needs an additional state for when someone presses Enter?
#    st.session_state['tasks'].append(new_task)

# Display the list of tasks
#st.write("### Your To-Do List:")
#for i, task in enumerate(st.session_state['tasks']):
#    if st.checkbox(f"Task {i+1}: {task}"):
#        st.session_state['tasks'].remove(task)
#        st.rerun()