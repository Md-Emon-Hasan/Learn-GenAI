import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("API key for Groq is missing. Please set the GROQ_API_KEY in the .env file.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Function to interact with Groq API for code generation
def generate_code_with_groq(description: str) -> str:
    try:
        # Create completion request to Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70B-specdec",  # Specify the Llama model for code generation
            messages=[{"role": "user", "content": description}],
            temperature=0.7,
            max_tokens=300,  # Increase or decrease based on the expected length of the generated code
            top_p=1,
            stop=None
        )

        # Print the raw response to inspect its structure
        print("Raw response:", completion)

        # Access the generated code from the response
        if hasattr(completion, 'choices') and len(completion.choices) > 0:
            response = completion.choices[0].message.content  # Assuming the generated code is here
        else:
            response = "No code generated. Please provide a clearer description."

        return response
    
    except Exception as e:
        return f"Error with Groq API: {str(e)}"

# Streamlit app setup
st.title("Code Generation Tool using Groq API")
st.write("This app uses Groq's API to generate code from a description. Please provide a clear description of the code you need.")

# User input for the code description
user_input = st.text_area("Enter the description of the code you want to generate", "")

# Button to trigger code generation
if st.button("Generate Code"):
    if user_input:
        # Call Groq API to generate the code
        generated_code = generate_code_with_groq(user_input)

        # Display the generated code
        st.subheader("Generated Code:")
        st.code(generated_code, language='python')  # You can change the language based on the generated code type
    else:
        st.error("Please enter a description of the code you want to generate!")
