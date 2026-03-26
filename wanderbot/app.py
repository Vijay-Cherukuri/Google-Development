from urllib import response

import streamlit as st
from google import genai
from google.genai import types
import requests
import logging

# --- Defining variables and parameters ---
REGION = "global"
PROJECT_ID = "fleet-symbol-480510-v1" # TODO: Insert Project ID
GEMINI_MODEL_NAME = "gemini-2.5-flash"

temperature = .2
top_p = 0.95

system_instructions = system_instruction = """
You are an expert, professional, and welcoming Travel Assistant chatbot for a premier travel marketing company. Your primary goal is to help users plan, book, and manage their travel, while providing exceptional customer service and rich destination insights.

CORE RESPONSIBILITIES:
1. Travel Discovery & Planning: Provide detailed, accurate, and engaging information about destinations. This includes local culture, weather, attractions, dining recommendations, and general travel requirements.
2. Booking Assistance: Help users search for and book flights, hotels, and vacation packages. When a user expresses intent to book, guide them through collecting the necessary parameters (travel dates, origin, destination, party size, budget) before invoking your booking tools.
3. Customer Support & Itinerary Management: Assist users with their existing travel plans. Always ask for their booking reference or confirmation number first when they need to modify, cancel, or check the status of a trip.

TONE AND COMMUNICATION STYLE:
- Be highly polite, empathetic, and concise. Travel can be stressful, so maintain a calm and reassuring demeanor, especially if a user is experiencing travel disruptions.
- Use clear formatting (such as bullet points, numbered lists, and bold text) to make itineraries, price breakdowns, and travel options easy to read on mobile devices.

BOUNDARIES & SAFETY (CRITICAL):
- Off-Topic Requests: Strictly decline to answer questions unrelated to travel, geography, hospitality, or our company services. Politely guide the conversation back to how you can assist with their travel needs.
- Sensitive Data (PII): Never ask users to type raw credit card numbers, full passport numbers, or account passwords directly into the chat. Only ask for booking reference numbers or email addresses for identity verification.
- Real-Time Information: Acknowledge that you must use your integrated tools to check live availability, pricing, and flight statuses. Do not guess or hallucinate prices. If a tool fails or is unavailable, apologize and offer to connect them to a human agent.
- Advice Limitations: Do not provide definitive legal, visa, or medical advice (e.g., vaccine requirements). Always advise the user to check with official government websites, embassies, or their healthcare provider.

ESCALATION PROTOCOL:
- If a user expresses extreme frustration, reports a critical travel emergency (e.g., stranded at the airport), or if you are unable to fulfill their request after two attempts, automatically offer to transfer the chat to a live human agent.
"""

generate_content_config = types.GenerateContentConfig(
    system_instruction=[
        types.Part.from_text(text=system_instructions)
    ],
)
logging.info(f"[generate_config_details] System Instruction: {generate_content_config.system_instruction[0].text}")

# --- Tooling ---
# TODO: Define the weather tool function declaration

# TODO: Define the get_current_temperature function

# --- Initialize the Vertex AI Client
try:
    # TODO: Initialize the Vertex AI client
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=REGION,
    ) 
    
    print(f"VertexAI Client initialized successfully with model {GEMINI_MODEL_NAME}")
except Exception as e:
    st.error(f"Error initializing VertexAI client: {e}")    
    st.stop()

# TODO: Add the get_chat function here in Task 15.

# --- Call the Model ---
def call_model(prompt: str, model_name: str) -> str:
    """
    This function interacts with a large language model (LLM) to generate text based on a given prompt and system instructions.
    It will be replaced in a later step with a more advanced version that handles tooling.
    """
    try:

        # TODO: Prepare the content for the model
        contents = [prompt]
        # TODO: Define generate_content configuration (needed for system instructions and parameters)

        # TODO: Define response
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=generate_content_config, # This is the new line
        )
        logging.info(f"[call_model_response] LLM Response: \"{response.text}\"")
        # TODO: Uncomment the below "return response.text" line
        return response.text
    except Exception as e:
        return f"Error: {e}"
    
# --- Presentation Tier (Streamlit) ---
# Set the title of the Streamlit application
st.title("Travel Chat Bot")

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    # Initialize the chat history with a welcome message
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Display the chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Get user input
if prompt := st.chat_input():
    # Add the user's message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the user's message
    st.chat_message("user").write(prompt)

    # Show a spinner while waiting for the for the model's response
    with st.spinner("Thinking..."):
        # Get the model's response using the call_model function
        model_response = call_model(prompt, GEMINI_MODEL_NAME)
        # Add the model's response to the chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": model_response}
        )
        # Display the model's response
        st.chat_message("assistant").write(model_response)

user_message_parts  = [types.Part.from_text(text=prompt)]
contents = [
    types.Content(
        role="user", # Indicates the content is from the user
        parts=user_message_parts, # A list, allowing multiple types of content
    )
]
