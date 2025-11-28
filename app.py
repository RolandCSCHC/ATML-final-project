from flask import Flask, render_template, request, jsonify
from chatbot import MichaelJacksonChatbot
import os

app = Flask(__name__, static_folder="static", static_url_path="/static")

# Initialize chatbot instance
# Model path relative to the project root
MODEL_PATH = os.path.join("models", "michael_jackson_model", "best_model")
chatbot = None
error_message = None


def init_chatbot():
    """Initialize the chatbot model"""
    global chatbot, error_message
    error_message = None

    if os.path.exists(MODEL_PATH):
        # Try to load the model - transformers will give us a better error if something is wrong
        try:
            chatbot = MichaelJacksonChatbot(MODEL_PATH)
            return True
        except Exception as e:
            error_message = f"Error loading model: {str(e)}"
            print(error_message)
            import traceback

            traceback.print_exc()

            # Check if it's a missing file error and provide helpful message
            if (
                "pytorch_model.bin" in str(e)
                or "model.safetensors" in str(e)
                or "model.bin" in str(e)
            ):
                error_message = f"Model weight file missing. The best_model directory needs pytorch_model.bin, model.safetensors, or model.bin file. Current path: {MODEL_PATH}"
            return False
    else:
        error_message = f"Model path not found: {MODEL_PATH}. Please ensure the model is in the models/ directory."
        print(error_message)
        return False


@app.route("/", methods=["GET", "POST"])
def index():
    """Main chatbot route"""
    if request.method == "POST":
        # Handle AJAX request for chat
        if request.is_json:
            data = request.get_json()
            user_message = data.get("message", "").strip()

            if not user_message:
                return jsonify({"error": "Message cannot be empty"}), 400

            if chatbot is None:
                return jsonify({"error": "Chatbot model not loaded"}), 500

            try:
                # Get optional parameters
                temperature = float(data.get("temperature", 0.7))
                max_tokens = int(data.get("max_tokens", 100))

                # Generate response
                response = chatbot.generate_response(
                    user_message, max_new_tokens=max_tokens, temperature=temperature
                )

                return jsonify({"response": response, "user_message": user_message})
            except Exception as e:
                return jsonify({"error": f"Error generating response: {str(e)}"}), 500

        # Handle form submission (fallback)
        user_message = request.form.get("message", "").strip()
        if user_message and chatbot:
            try:
                temperature = float(request.form.get("temperature", 0.7))
                max_tokens = int(request.form.get("max_tokens", 100))
                response = chatbot.generate_response(
                    user_message, max_new_tokens=max_tokens, temperature=temperature
                )
                return render_template(
                    "index.html",
                    user_message=user_message,
                    bot_response=response,
                    model_loaded=chatbot is not None,
                )
            except Exception as e:
                return render_template(
                    "index.html", error=str(e), model_loaded=chatbot is not None
                )

    # GET request - render the page
    return render_template(
        "index.html", model_loaded=chatbot is not None, error_message=error_message
    )


if __name__ == "__main__":
    # Initialize chatbot on startup
    print("Initializing chatbot...")
    init_chatbot()

    # Run Flask app
    app.run(debug=True, host="0.0.0.0", port=5001)
