import tkinter as tk
import json

# Load the decision tree of questions from a JSON file
# This file must follow a specific format (nested dictionaries for decision paths)
with open('questions.json') as f:
    question_tree = json.load(f)

class CognitiveGame:
    def __init__(self, master):
        """
        Constructor initializes the GUI and game state.
        """
        self.master = master
        master.title("🧠 Cognitive Ability Game")
        master.configure(bg="#f0f4f7")

        # Initialize the score to 0
        self.score = 0

        # Set the starting point of the decision tree
        self.current_node = question_tree

        # Title
        self.title_label = tk.Label(master, text="🧠 Cognitive Ability Game", font=("Helvetica", 18, "bold"), bg="#f0f4f7", fg="#333")
        self.title_label.pack(pady=(10, 5))

        # Frame to hold score, question, and answers
        self.content_frame = tk.Frame(master, bg="#f0f4f7")
        self.content_frame.pack()

        # Score display that will update after each successful question
        self.score_label = tk.Label(self.content_frame, text=f"Score: {self.score}", font=("Helvetica", 12), bg="#f0f4f7", fg="#555")
        self.score_label.pack(pady=(0, 10))

        # Question Text
        self.question_label = tk.Label(self.content_frame, text="", wraplength=400, font=("Helvetica", 14), bg="#f0f4f7", fg="#222")
        self.question_label.pack(pady=10)

        # Frame to hold the dynamic answer buttons
        self.button_frame = tk.Frame(self.content_frame, bg="#f0f4f7")
        self.button_frame.pack()

        # Display the first question
        self.display_question()

    def display_question(self):
        """
        Displays the current question and generates answer buttons.
        """
        self.clear_buttons() # Remove any existing buttons first
        self.score_label.config(text=f"Score: {self.score}")
        question = self.current_node["question"]
        self.question_label.config(text=question)

        # Create a button for each possible answer
        for answer, next_node in self.current_node["answers"].items():
            button = tk.Button(
                self.button_frame,
                text=answer,
                font=("Helvetica", 12),
                width=20,
                bg="#dbeafe",
                fg="#1e3a8a",
                activebackground="#93c5fd",
                command=lambda a=answer: self.process_answer(a) # Capture which answer was clicked
            )
            button.pack(pady=5)

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
        self.clear_buttons()
        self.score_label.pack_forget()
        self.question_label.config(
            text=f"{message}\n\nFinal Score: {self.score}",
            font=("Helvetica", 14, "bold")
        )

        # Widget for setting score to 0 and starting at question 1
        reset_button = tk.Button(
            self.button_frame,
            text="Play Again",
            font=("Helvetica", 12),
            bg="#a7f3d0",
            fg="#065f46",
            activebackground="#6ee7b7",
            command=self.reset_game
        )
        reset_button.pack(pady=10)

    def reset_game(self):
        """
        Restarts game by destroying and reinitializing all widgets.
        """
        # Destroy all widgets inside the window
        for widget in self.master.winfo_children():
            widget.destroy()

        # Re-initialize the CognitiveGame instance
        CognitiveGame(self.master)

# Launch the application
if __name__ == "__main__":
    root = tk.Tk()
    game = CognitiveGame(root)
    root.mainloop()
