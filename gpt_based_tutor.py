import openai

prompt_list = [
    "Analyze the text for grammatical errors",
    "List the errors in the given text",
    "Explain the errors in the text such that a primary school student could understand",
    "Rewrite the sentence by correcting all the errors"
]

messages = [{"role": "system", "content": "You are a primary school teacher teaching English."}]
user_input = ""

while True:
    # Get user's input or prompt choice
    user_choice = input("Enter '1' to provide input, '2' to apply prompts, or 'q' to quit: ")
    
    if user_choice == 'q':
        break
    
    if user_choice == '1':
        user_input = input("Enter your input: ")
        print("User input stored.")
    
    if user_choice == '2':
        if not user_input:
            print("Please provide input before applying prompts.")
            continue
        
        # Display prompt options
        print("Select a prompt option:")
        for idx, option in enumerate(prompt_list, start=1):
            print(f"{idx}. {option}")

        # Get user's prompt choice
        prompt_choice = input("Enter the number of your prompt choice: ")
        
        try:
            prompt_choice_idx = int(prompt_choice) - 1
            if 0 <= prompt_choice_idx < len(prompt_list):
                selected_prompt = prompt_list[prompt_choice_idx]
                messages.append({"role": "user", "content": f"{selected_prompt}\n{user_input}"})
                
                chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                reply = chat.choices[0].message["content"]
                print(f"ChatGPT: {reply}")
                messages.append({"role": "assistant", "content": reply})
            else:
                print("Invalid prompt choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    if user_choice == 'c':
        user_input = ""
        print("User input cleared.")
