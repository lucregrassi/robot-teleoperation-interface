import streamlit as st
import socket
import pandas as pd

# Load sentences from the "sentences.txt" file
file_path = "tempo_della_salute.txt"

# Create a UDP socket to communicate with the robot
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Function to load the predefined sentences from a text file
def load_sentences(path_file):
    try:
        with open(path_file, 'r', encoding='utf-8') as file:
            sentences = file.read().splitlines()  # Load each line as a sentence
        return sentences
    except Exception as e:
        st.error(f"Error loading sentences: {e}")
        return []


# Function to save the sentences to a text file
def save_sentences(sentences, path_file):
    try:
        with open(path_file, 'w', encoding='utf-8') as file:
            for sent in sentences:
                file.write(f"{sent}\n")  # Save each sentence on a new line
    except Exception as e:
        st.error(f"Error saving sentences: {e}")


# Function to send a command (sentence or action) to the robot
def send_command(command, robot_ip):
    try:
        sock.sendto(command.encode(), (robot_ip, 54321))  # Use the dynamic IP address
    except Exception as e:
        st.error(f"Error sending the command to {robot_ip}: {e}")


# Initialize session state for sentences if not already set
if 'sentences' not in st.session_state:
    st.session_state.sentences = load_sentences(file_path)

# Initialize session state for text inputs (new and modified sentences)
if 'new_sentence' not in st.session_state:
    st.session_state['new_sentence'] = ""

if 'modified_sentence' not in st.session_state:
    st.session_state['modified_sentence'] = ""

# Initialize session state for robot IP if not already set
if 'robot_ip' not in st.session_state:
    st.session_state['robot_ip'] = ""  # Set a default value


# Function to refresh and reload sentences in session state
def refresh_sentences():
    st.session_state.sentences = load_sentences(file_path)


# Streamlit user interface (UI)
st.title("Robot Teleoperation")

# --- Section to set the robot's IP address ---
st.subheader("Set robot IP address")
st.session_state.robot_ip = st.text_input("Enter the robot's IP address", value=st.session_state.robot_ip)

# --- Section to control the robot's movement ---
st.subheader("Movement control")
# Set up buttons in a single row to control movement
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col1:
    if st.button("⬅️"):
        send_command('ROTATE_LEFT', st.session_state.robot_ip)

with col2:
    if st.button("⬆️"):
        send_command('MOVE_FORWARD', st.session_state.robot_ip)

with col3:
    if st.button("⏺️"):
        send_command('STOP', st.session_state.robot_ip)

with col4:
    if st.button("⬇️"):
        send_command('MOVE_BACKWARD', st.session_state.robot_ip)

with col5:
    if st.button("➡️"):
        send_command('ROTATE_RIGHT', st.session_state.robot_ip)

# --- Section to control robot's volume ---
st.subheader("Volume Control")
volume_col1, volume_col2 = st.columns([1, 1])

with volume_col1:
    if st.button("🔊 Volume up"):
        send_command("VOLUME_UP", st.session_state.robot_ip)

with volume_col2:
    if st.button("🔉 Volume down"):
        send_command("VOLUME_DOWN", st.session_state.robot_ip)

# --- Section to send a sentence ---
st.subheader("Make the robot talk")

# Use a form to allow sending a sentence by pressing "Enter"
with st.form(key="sentence_form"):
    input_value = st.text_input("Write a sentence or enter the number of a predefined sentence from the table.")
    submit_sentence = st.form_submit_button(label="Send")  # Hidden button used to submit on pressing Enter

# Check if the input is a valid number
if submit_sentence:
    try:
        sentence_number = int(input_value)
        # If it's a valid number, select the corresponding sentence
        if 0 <= sentence_number < len(st.session_state.sentences):
            sentence = st.session_state.sentences[sentence_number]
            st.write(f"Selected sentence: {sentence}")
        else:
            st.error(f"Invalid number. Enter a number between 0 and {len(st.session_state.sentences) - 1}, or write a manual sentence.")
            sentence = None
    except ValueError:
        # If it's not a number, treat it as a manual sentence
        sentence = input_value if input_value else None

    # If a sentence exists (either predefined or manual), send it
    if sentence:
        send_command(sentence, st.session_state.robot_ip)

# Display the table of predefined sentences and their corresponding numbers
st.subheader("Predefined Sentences List")
df = pd.DataFrame({"Number": list(range(len(st.session_state.sentences))), "Sentence": st.session_state.sentences})
st.dataframe(df)

# --- Section to add a new sentence ---
st.subheader("Add a New Sentence")
st.session_state.new_sentence = st.text_input("Enter a new sentence", value=st.session_state.new_sentence)

if st.button("Add"):
    if st.session_state.new_sentence:
        st.session_state.sentences.append(st.session_state.new_sentence)
        save_sentences(st.session_state.sentences, file_path)
        st.success("Sentence added successfully!")
        # Clear the input field and refresh the page
        st.session_state['new_sentence'] = ""
        st.rerun()

# --- Section to modify an existing sentence ---
st.subheader("Modify a Sentence")
sentence_to_modify = st.number_input("Enter the number of the sentence to modify", min_value=0,
                                     max_value=len(st.session_state.sentences) - 1, step=1)
st.session_state.modified_sentence = st.text_input("Modify the selected sentence",
                                                   value=st.session_state.sentences[sentence_to_modify])

if st.button("Save"):
    st.session_state.sentences[sentence_to_modify] = st.session_state.modified_sentence
    save_sentences(st.session_state.sentences, file_path)
    st.success("Sentence modified successfully!")
    # Clear the input field and refresh the page
    st.session_state['modified_sentence'] = ""
    st.rerun()

# --- Section to delete an existing sentence ---
st.subheader("Delete a Sentence")
sentence_to_delete = st.number_input("Enter the number of the sentence to delete", min_value=0,
                                     max_value=len(st.session_state.sentences) - 1, step=1)
if st.button("Delete"):
    if 0 <= sentence_to_delete < len(st.session_state.sentences):
        st.session_state.sentences.pop(sentence_to_delete)
        save_sentences(st.session_state.sentences, file_path)
        st.success("Sentence deleted successfully!")
        st.rerun()

# --- Section to control robot's animations ---
st.subheader("Perform action")

# Create a dropdown menu for action selection
actions = ["Greet", "Handshake", "Hug"]
selected_action = st.selectbox("Choose an action", actions)

if st.button("Send"):
    if selected_action == "Hug":
        send_command("HUG", st.session_state.robot_ip)
        st.success("Hug command sent!")
    elif selected_action == "Greet":
        send_command("GREET", st.session_state.robot_ip)
        st.success("Greet command sent!")
    elif selected_action == "Handshake":
        send_command("HANDSHAKE", st.session_state.robot_ip)
        st.success("Handshake command sent!")