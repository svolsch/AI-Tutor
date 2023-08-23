import tkinter as tk
from openai import ChatCompletion

class RoleSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Role Selection")

        self.role = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select your role:").pack()
        tk.Radiobutton(self.root, text="Student", variable=self.role, value="student").pack(anchor='w')
        tk.Radiobutton(self.root, text="Teacher", variable=self.role, value="teacher").pack(anchor='w')
        tk.Button(self.root, text="Continue", command=self.open_main_app).pack()

    def open_main_app(self):
        selected_role = self.role.get()
        self.root.destroy()  # Close the role selection window
        root = tk.Tk()
        app = PrimarySchoolTeacherApp(root, selected_role)
        root.mainloop()

class PrimarySchoolTeacherApp:
    def __init__(self, root, user_role):
        self.root = root
        self.root.title("AI Tutor")

        self.user_role = user_role
        
        self.user_input = tk.StringVar()
        self.prompt_choice = tk.StringVar()
        self.custom_prompts = tk.StringVar()
        
        self.messages = [{"role": "system", "content": "You are a primary school teacher teaching English."}]
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter your input:").pack()
        tk.Entry(self.root, textvariable=self.user_input).pack()
        
        tk.Label(self.root, text="Select a prompt option:").pack()
        for idx, option in enumerate(prompt_list, start=1):
            tk.Radiobutton(self.root, text=option, variable=self.prompt_choice, value=str(idx)).pack(anchor='w')

        if self.user_role == "teacher":
            tk.Label(self.root, text="Custom Prompts (for teacher):").pack()
            tk.Entry(self.root, textvariable=self.custom_prompts).pack()

        tk.Button(self.root, text="Submit", command=self.submit).pack()
        tk.Button(self.root, text="Clear Input", command=self.clear_input).pack()
        tk.Button(self.root, text="Quit", command=self.root.quit).pack()

        self.output_text = tk.Text(self.root, wrap=tk.WORD, height=10, width=50)
        self.output_text.pack()

    def submit(self):
        user_input = self.user_input.get()
        if user_input:
            prompt_choice = self.prompt_choice.get()

            if prompt_choice.isdigit() and 0 <= int(prompt_choice) - 1 < len(prompt_list):
                selected_prompt = prompt_list[int(prompt_choice) - 1]

                if self.user_role == "student":
                    messages = self.messages + [
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": selected_prompt}
                    ]
                else:
                    custom_prompts = self.custom_prompts.get().split('\n')
                    prompts = custom_prompts if custom_prompts else [selected_prompt]
                    messages = self.messages + [
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": selected_prompt}
                    ] + [{"role": "assistant", "content": prompt} for prompt in prompts]

                chat = ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                reply = chat.choices[-1].message["content"]
                self.messages.append({"role": "user", "content": user_input})
                self.messages.append({"role": "assistant", "content": reply})

                self.output_text.insert(tk.END, "You: " + user_input + "\n")
                self.output_text.insert(tk.END, "Assistant: " + reply + "\n")
                self.output_text.insert(tk.END, "\n")
            else:
                self.output_text.insert(tk.END, "Invalid prompt choice. Please select a valid option.\n")
        else:
            self.output_text.insert(tk.END, "Please provide input before applying prompts.\n")

    def clear_input(self):
        self.user_input.set("")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "User input cleared.\n")

if __name__ == "__main__":
    prompt_list = [
        "Analyze the text for grammatical errors",
        "List the errors in the given text",
        "Explain the errors in the text such that a primary school student could understand",
        "Rewrite the sentence by correcting all the errors"
    ]
    
    root = tk.Tk()
    role_app = RoleSelectionApp(root)
    root.mainloop()
