import pandas as pd  # For handling CSV files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify  # Import Flask and related modules
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the GENAI_API_KEY environment variable.")

conversation_history = {}
client = genai.Client(api_key=api_key) 

# pip install scikit-learn

knowledge_base_path = "knowledge_base.csv"  
knowledge_base = pd.read_csv(knowledge_base_path)

knowledge_base['combined_text'] = knowledge_base['short_description'] + " " + knowledge_base['resolution'] + " " + knowledge_base['combined_text']  # Adjust columns as needed

# Initialize TF-IDF Vectorizer for retrieval
vectorizer = TfidfVectorizer()
knowledge_base_vectors = vectorizer.fit_transform(knowledge_base['combined_text'])

@app.route('/query', methods=['POST'])
def generate_content():
    """
    API endpoint to generate content using GenAI with RAG.
    Expects a JSON payload with the following structure:
    {
        "session_id": "unique_session_id",
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
            conversation_history[session_id] = [
                "You are a technical support assistant for a software platform. Your role is to help users troubleshoot issues, provide guidance on using the platform, and answer technical questions. Always provide clear, step-by-step instructions and avoid technical jargon unless necessary. If you need more information to assist, politely ask the user for clarification."
            ]

        # Append the user's prompt to the conversation history
        conversation_history[session_id].append(f"User: {prompt}")

        # Retrieve relevant information from the knowledge base
        prompt_vector = vectorizer.transform([prompt])
        similarities = cosine_similarity(prompt_vector, knowledge_base_vectors)
        top_indices = similarities.argsort()[0][-3:]  # Get top 3 most relevant rows
        retrieved_data = "\n".join(knowledge_base.iloc[top_indices]['combined_text'])

        # Combine retrieved data with the conversation history
        dataset_context = f"Here is some relevant information from the knowledge base:\n{retrieved_data}\n"
        context = dataset_context + "\n".join(conversation_history[session_id]) + "\nAI:"

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
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)