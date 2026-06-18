# Teleoperation Interface for Robots

This project provides a simple web-based interface for controlling a robot. It is built using [Streamlit](https://streamlit.io/) and enables users to send movement commands, adjust volume, and make the robot speak predefined or custom sentences. The application communicates with the robot over a UDP connection.

**Note:** To use this interface on the Pepper robot, the `PepperTeleoperation` application must be installed and running on the robot. You can find it here: [PepperTeleoperation](https://github.com/lucregrassi/PepperTeleoperation).

## Features

- **Custom IP Address**: Set the robot's IP address dynamically.
- **Movement Control**: Control Pepper's movements (rotate left, move forward, stop, move backward, rotate right).
- **Volume Control**: Adjust the volume (increase or decrease).
- **Speech Control**: Make Pepper speak predefined or custom sentences.
- **Sentence Management**: 
  - Add, modify, and delete predefined sentences.
  - Sentences are stored in a `sentences.txt` file and persist between sessions.

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- [PepperTeleoperation](https://github.com/lucregrassi/PepperTeleoperation) application installed and running on the Pepper robot or a socket server on any other robot.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/lucregrassi/robot-teleoperation-interface
   cd robot-teleoperation-interface
   ```
   
2. Install the required dependencies:
   
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have a sentences.txt file in the same directory. If it doesn’t exist, create one manually with the sentences you’d like the robot to speak, each on a new line.

## Usage 
1. Run the streamlit application

    ```bash
     streamlit run main.py
     ```
2.	Open your browser and navigate to http://localhost:8501 to access the interface. If you’re using another device on the same network, replace localhost with your computer’s IP address (e.g., http://your-computer-ip:8501).
3.	Ensure that the [PepperTeleoperation](https://github.com/lucregrassi/PepperTeleoperation) application is running on the robot (or the socket server is running) and that both the robot and your computer are connected to the same network.

## Interface Overview

1. Set Robot IP Address
     *	Enter the IP address of the robot you want to control.
   * Make sure that the robot is connected to the same network.

2. Movement Control
    *	Control the robot’s movement using the direction buttons:
         - ⬅️ Rotate Left
         - ⬆️ Move Forward
         - ⏺️ Stop
         - ⬇️ Move Backward
         - ➡️ Rotate Right

3. Volume Control
    *	Adjust the robot’s volume using:
        *	🔊 Volume Up
        *	🔉 Volume Down

4. Make the Robot Talk
    * Write a custom sentence or select a predefined sentence by entering its corresponding number.
    * Press Enter or click on the "Send" button to make the robot speak.

5. Manage Predefined Sentences
    * Add a Sentence: Enter a new sentence and press "Add" to include it in the list.
    * Modify a Sentence: Select a sentence by its number, modify it, and press "Save".
    * Delete a Sentence: Select a sentence by its number and press "Delete" to remove it.

## Example Sentences
Here’s an example of what the sentences.txt file might look like:
  ```
  Hello, I am Pepper!
  How can I assist you today?
  ```

## License

This project is licensed under the GNU General Public License (GPL v3) - see the LICENSE file for details.

## Contact

For any questions, feel free to reach out:

GitHub: [lucregrassi](https://github.com/lucregrassi)

Email: lucrezia.grassi@unige.it
   
