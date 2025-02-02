import ollama

# Define a function for generating responses using Ollama
def ollama_generate_text(prev_resp, user_id):
    # Create a prompt string (currently empty)
    prompt = f""" """
    try:
        # Send the prompt to the Ollama Llama model and get the response
        response = ollama.chat(model="deepseek-r1:7b", messages=[
            {'role': 'user', 'content': prompt}
        ])

        # Check if response contains the expected content
        if 'message' in response and 'content' in response['message']:
            # Return the content of the response message
            return response['message']['content']
        else:
            # Return a message indicating no valid response was found
            return "No valid response found in message."
    except Exception as e:
        # Return an error message if an exception occurs
        return f"An error occurred: {e}"
