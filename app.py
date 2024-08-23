import os
import streamlit as st
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyDyAyotBzhC0kGV3IYbzltzooRjyUR7waw")

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Define the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Streamlit app
def main():
    st.set_page_config(page_title="Gemini AI Content Generator", page_icon=":sparkles:", layout="wide")
    
    st.title("AI Content Generator")
    st.write("Welcome to the AI Content Generator! This tool allows you to create custom content based on your input.")
    st.write("### How to Use:")
    st.write("1. Enter your request in the text area below.")
    st.write("2. Select the desired length of the content.")
    st.write("3. Click 'Generate Content' to receive your custom content.")
    st.write("4. Use the 'Download Content' button to save the generated content as a text file.")
    
    # User input
    user_input = st.text_area(
        "Enter your request:", 
        "Write a blog post about the benefits of meditation",
        height=150
    )
    
    # Content limit options
    content_limit = st.selectbox(
        "Select content length:", 
        ["short", "middle", "detailed"],
        help="Choose the length of the content to be generated. 'Short' provides concise content, 'middle' offers moderate detail, and 'detailed' gives extensive information."
    )
    
    if st.button("Generate Content"):
        # Adjust generation parameters based on content length
        length_config = {
            "short": {"max_output_tokens": 500},
            "middle": {"max_output_tokens": 1500},
            "detailed": {"max_output_tokens": 4000},
        }
        length_config_update = length_config.get(content_limit, {"max_output_tokens": 8192})
        
        # Update model configuration
        model_config = generation_config.copy()
        model_config.update(length_config_update)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=model_config,
        )

        # Start chat session
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "generate content based on the user input",
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "Please provide me with the user input! I need some context to generate relevant content. \n\nFor example, you could tell me:\n\n* **A topic:** \"Write a blog post about the benefits of meditation\"\n* **A question:** \"What are some fun facts about the Great Barrier Reef?\"\n* **A prompt:** \"Create a short story about a talking cat who goes on an adventure\"\n* **A style:** \"Write a poem in the style of Shakespeare about a lost love\"\n\nThe more details you provide, the better I can understand your request and generate something you'll enjoy. \n",
                    ],
                },
            ]
        )

        # Generate response
        response = chat_session.send_message(user_input)
        generated_content = response.text
        
        st.write("### Generated Content:")
        st.write(generated_content)

        # Download option
        st.download_button(
            label="Download Content",
            data=generated_content,
            file_name="generated_content.pdf",
            mime="text/plain",
        )

if __name__ == "__main__":
    main()
