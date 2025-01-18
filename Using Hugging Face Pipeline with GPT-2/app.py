from flask import Flask, request, jsonify, render_template
from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline
import torch
import threading

app = Flask(__name__)

# Load GPT-2 model and tokenizer
model_name = "gpt2"
print("Loading GPT-2 model...")
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Fallback pipeline for quick responses
print("Loading fallback pipeline...")
fallback_pipeline = pipeline("text-generation", model=model_name, tokenizer=model_name)

# Lock to manage model loading
model_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Generate response with GPT-2
    with model_lock:
        try:
            input_ids = tokenizer.encode(user_input, return_tensors="pt")
            output = model.generate(
                input_ids, max_length=150, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id
            )
            response = tokenizer.decode(output[0], skip_special_tokens=True)
        except Exception as e:
            print("Error with GPT-2 model:", e)
            response = fallback_pipeline(user_input, max_length=50, num_return_sequences=1)[0]['generated_text']

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
