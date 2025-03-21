from flask import Flask, request, jsonify
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Initialize Flask app
app = Flask(__name__)

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the GENAI_API_KEY environment variable.")

client = genai.Client(api_key=api_key) 
conversation_history = {}


@app.route('/query', methods=['GET'])
def generate_content():
    """
    API endpoint to generate content using GenAI.
    Expects a JSON payload with the following structure:
    {
        "model": "gemini-2.0-flash",
        "prompt": "Explain how AI works"
    }
    """
    try:
      # Parse request JSON
        data = request.get_json()
        session_id = data.get("session_id")
        prompt = data.get("prompt")

        if not session_id or not prompt:
            return jsonify({"error": "Both 'session_id' and 'prompt' fields are required"}), 400

        # Retrieve or initialize conversation history for the session
        if session_id not in conversation_history:
            conversation_history[session_id] = []

        # Append the new prompt to the conversation history
        conversation_history[session_id].append(f"User: {prompt}")

        # Construct the full conversation as context
        context = "\n".join(conversation_history[session_id]) + "\nAI:"

        # Call GenAI to generate a response
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=context
        )

        # Extract the response text
        ai_response = response.text

        # Append the AI's response to the conversation history
        conversation_history[session_id].append(f"AI: {ai_response}")

        # Return the AI's response
        return jsonify({"response": ai_response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)