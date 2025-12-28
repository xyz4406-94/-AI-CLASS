import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import nltk
from nltk.corpus import wordnet
import random
import threading

class ProSmartHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("PRO SMART HELPER")
        self.root.geometry("700x750")
        self.bg_color = "#1a2a3a"
        self.root.configure(bg=self.bg_color)

        self.voice_index = 0 
        self.quiz_word = "" 
        self.history = []
        self.score = 0 
        self.used_quiz_words = []

        self.setup_ui()

    def setup_ui(self):
        self.entry = tk.Entry(self.root, font=("Arial", 16), width=45, justify='center')
        self.entry.pack(pady=20)
        self.entry.bind('<Return>', lambda event: self.handle_search())

        self.btn_frame = tk.Frame(self.root, bg=self.bg_color)
        self.btn_frame.pack(pady=10)

        # Row 1: Main Controls
        tk.Button(self.btn_frame, text="🔍 Search", command=self.handle_search, bg="#3498db", fg="white", width=12).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.btn_frame, text="🎮 Quiz", command=self.start_quiz, bg="#e67e22", fg="white", width=12).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.btn_frame, text="🔄 Reset", command=self.reset_to_search, bg="#e74c3c", fg="white", width=12).grid(row=0, column=2, padx=5, pady=5)

        # Row 2: Settings
        tk.Button(self.btn_frame, text="🚻 M/F Switch", command=self.toggle_voice, bg="#f1c40f", fg="black", width=12).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.btn_frame, text="🎨 Theme", command=self.toggle_theme, bg="#9b59b6", fg="white", width=12).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.btn_frame, text="📜 History", command=self.show_history, bg="#7f8c8d", fg="white", width=12).grid(row=1, column=2, padx=5, pady=5)

        self.output = scrolledtext.ScrolledText(self.root, width=80, height=20, font=("Arial", 12))
        self.output.pack(pady=20, padx=10)
        
        self.output.tag_configure("header", font=("Arial", 14, "bold"), foreground="#e67e22")
        self.output.tag_configure("victory", font=("Arial", 16, "bold"), foreground="#2ecc71", justify='center')
        self.output.tag_configure("score", font=("Arial", 12, "bold"), foreground="#f1c40f")

    def talk(self, text):
        def run_audio():
            try:
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                if len(voices) > self.voice_index:
                    engine.setProperty('voice', voices[self.voice_index].id)
                engine.say(text)
                engine.runAndWait()
            except: pass
        threading.Thread(target=run_audio, daemon=True).start()

    def handle_search(self):
        word = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)
        
        if not word: return

        if self.quiz_word:
            if word == self.quiz_word:
                self.score += 1
                if self.score >= 5:
                    self.show_victory_screen()
                else:
                    self.output.insert(tk.END, f"\n✅ Correct! Current Score: {self.score}/5\n", "score")
                    self.talk("Correct! Keep going.")
                    self.root.after(800, self.start_quiz)
            else:
                self.output.insert(tk.END, f"\n❌ Not quite. (Hint: Starts with '{self.quiz_word[0].upper()}')\n")
                self.talk("Try again.")
            return

        # Regular Search logic remains the same
        self.history.append(word)
        self.output.delete('1.0', tk.END)
        syns = wordnet.synsets(word)
        if syns:
            defn = syns[0].definition()
            self.output.insert(tk.END, f"WORD: {word.upper()}\n\n[MEANING]\n{defn}\n", "header")
            self.talk(f"The meaning is {defn}")
        else:
            self.output.insert(tk.END, "Word not found.")

    def show_victory_screen(self):
        """Displays a dedicated victory message instead of jumping back immediately"""
        self.quiz_word = "" # Stop quiz mode
        self.output.delete('1.0', tk.END)
        self.output.insert(tk.END, "\n\n🌟 🌟 🌟 🌟 🌟\n", "victory")
        self.output.insert(tk.END, "CONGRATULATIONS!\n", "victory")
        self.output.insert(tk.END, "You have successfully completed the quiz.\n", "victory")
        self.output.insert(tk.END, "You are a true Word Master. Best wishes for your learning!\n", "victory")
        self.output.insert(tk.END, "🌟 🌟 🌟 🌟 🌟\n", "victory")
        self.talk("Congratulations! You have completed the quiz. Best wishes!")
        self.score = 0 

    def start_quiz(self):
        word_list = ["keyboard", "ocean", "robot", "guitar", "planet", "forest", "mountain", "camera", "bridge", "pencil", "summer", "window"]
        available_words = [w for w in word_list if w not in self.used_quiz_words]
        
        if not available_words:
            self.used_quiz_words = []
            available_words = word_list

        self.quiz_word = random.choice(available_words)
        self.used_quiz_words.append(self.quiz_word)
        hint = wordnet.synsets(self.quiz_word)[0].definition()
        
        self.output.delete('1.0', tk.END)
        self.output.insert(tk.END, f"🎮 QUIZ CHALLENGE (Goal: 5 Points)\n", "header")
        self.output.insert(tk.END, f"Current Score: {self.score}\n\n", "score")
        self.output.insert(tk.END, f"HINT: {hint}\n\nType your answer and press Enter!")
        self.talk("What is the word?")

    def reset_to_search(self):
        self.quiz_word = ""
        self.score = 0
        self.output.delete('1.0', tk.END)
        self.output.insert(tk.END, "✅ Back to Search Mode. How can I help you today?")

    def toggle_theme(self):
        new_bg = "white" if self.root.cget("bg") == "#1a2a3a" else "#1a2a3a"
        self.root.configure(bg=new_bg)
        self.btn_frame.configure(bg=new_bg)

    def toggle_voice(self):
        self.voice_index = 1 if self.voice_index == 0 else 0
        self.talk("Voice updated.")

    def show_history(self):
        self.output.delete('1.0', tk.END)
        self.output.insert(tk.END, "📜 YOUR SEARCH HISTORY:\n\n" + "\n".join(self.history))

if __name__ == "__main__":
    root = tk.Tk()
    app = ProSmartHelper(root)
    root.mainloop()