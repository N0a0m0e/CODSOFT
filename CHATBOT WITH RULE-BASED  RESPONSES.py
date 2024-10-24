def get_response(user_input):
    user_input = user_input.lower()  # Normalize the input to lowercase
    
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"
    elif "help" in user_input:
        return "Sure! What do you need help with?"
    elif "thanks" in user_input or "thank you" in user_input:
        return "You're welcome! If you have any other questions, feel free to ask."
    else:
        return "I'm sorry, I didn't understand that."

# Main loop to interact with the user
def chat():
    print("Welcome to the chatbot! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print(get_response(user_input))
            break
        response = get_response(user_input)
        print("Bot:", response)

# Start the chat
if __name__ == "__main__":
    chat()
