import openai

prompt_list = [
    "Analyze the text for grammatical errors",
    "List the errors in the given text",
    "Explain the errors in the text such that a primary school student could understand",
    "Provide your own input",
]

messages = [{"role": "system", "content": "You are an intelligent assistant."}]

while True:

    # Get user's input
    user_input = input("User: ")
    if not user_input:
        break

    # Display prompt options
    print("Select a prompt option:")
    for idx, option in enumerate(prompt_list, start=1):
        print(f"{idx}. {option}")

    # Get user's prompt choice
    prompt_choice = input("Enter the number of your prompt choice (or press Enter to provide your own input): ")
    
    if not prompt_choice:  # User wants to provide their own input
        messages.append({"role": "user", "content": user_input})
    else:
        try:
            prompt_choice_idx = int(prompt_choice) - 1
            if 0 <= prompt_choice_idx < len(prompt_list):
                selected_prompt = prompt_list[prompt_choice_idx]
                messages.append({"role": "user", "content": f"{selected_prompt}\n{user_input}"})
            else:
                print("Invalid prompt choice. Please select a valid option.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
    
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message["content"]
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})