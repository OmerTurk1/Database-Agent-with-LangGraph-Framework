from graph import app

def run_chat_loop():
    # Message history that the agent will keep throughout the session
    chat_history = []
    
    print("--- File Assistant Connected ---")
    print("(Type 'exit' or 'quit' to close the session.)")

    while True:
        user_input = input("\n>>> Type Message: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if user_input.lower().strip() == "forget":
            print("Memory cleared. Starting fresh.")
            chat_history.clear()
            continue

        # Add message to history
        chat_history.append({"role": "user", "content": user_input})

        # Memory Management: Keep only the last 10 messages (5 User + 5 Agent)
        trimmed_history = chat_history[-10:]

        initial_state = {
            "messages": trimmed_history
        }

        print("\n--- Agent is thinking ---")
        
        # Using stream to display processing steps
        final_response = ""
        for event in app.stream(initial_state):
            for key, value in event.items():
                # Display tool execution info in the terminal
                if key == "tools":
                    last_msg = value["messages"][-1]
                    tool_name = getattr(last_msg, "name", "Bilinmeyen Tool")
                    print(f"[System - {tool_name}]:\n {last_msg.content}")
                
                # Capture the agent's final response
                if key == "agent":
                    last_msg = value["messages"][-1]
                    if last_msg.content: # Only if there is text content
                        final_response = last_msg.content

        # Add agent's response to history
        if final_response:
            print(f"\n<<< Agent: {final_response}")
            chat_history.append({"role": "assistant", "content": final_response})

if __name__ == "__main__":
    run_chat_loop()