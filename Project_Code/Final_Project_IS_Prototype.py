import tkinter as tk
import json

# Load the decision tree of questions from a JSON file
# This file must follow a specific format (nested dictionaries for decision paths)
with open('questions.json') as f:
    question_tree = json.load(f)

# Define the main class for the game system
class CognitiveGame:
    def __init__(self, master):
        """
        Constructor initializes the GUI and game state.
        """
        self.master = master
        master.title("Cognitive Ability Test")

        # Initialize the score to 0
        self.score = 0

        # Set the starting point of the decision tree
        self.current_node = question_tree

        # Label widget to display questions
        self.question_label = tk.Label(master, text="", wraplength=400)
        self.question_label.pack(pady=10)

        # Frame to hold the dynamic answer buttons
        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        # Display the first question
        self.display_question()

    def display_question(self):
        """
        Displays the current question and generates answer buttons.
        """
        self.clear_buttons()  # Remove any existing buttons first

        # Get the question text from the current node
        question = self.current_node["question"]
        self.question_label.config(text=question)

        # Create a button for each possible answer
        for answer, next_node in self.current_node["answers"].items():
            button = tk.Button(
                self.button_frame,
                text=answer,
                command=lambda a=answer: self.process_answer(a)  # Capture which answer was clicked
            )
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def clear_buttons(self):
        """
        Clears all widgets (buttons) from the button frame.
        """
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def process_answer(self, answer):
        """
        Process the selected answer:
        - Update score based on predefined values
        - Navigate to the next question or show final result
        """
        # Safely get score value for this answer, default to 0 if not found
        self.score += self.current_node["scores"].get(answer, 0)

        # Get the next node: could be a dict (next question) or a string (end result)
        next_node = self.current_node["answers"][answer]

        # Check if next_node is a dict and has a 'question' key
        if isinstance(next_node, dict) and "question" in next_node:
             self.current_node = next_node
             self.display_question()
        else:
        # Either it's a string, or it's an invalid node — treat it as the end
            self.show_result(next_node if isinstance(next_node, str) else "Test Complete")

    def show_result(self, message):
        """
        Displays the final result and user's score.
        """
        self.clear_buttons()  # Clear any remaining buttons
        self.question_label.config(text=f"{message}\nYour Score: {self.score}")

# Launch the application
if __name__ == "__main__":
    root = tk.Tk()  # Create main application window
    game = CognitiveGame(root)  # Instantiate the game
    root.mainloop()  # Start the GUI event loop
