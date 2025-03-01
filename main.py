import streamlit as st
import ollama

st.set_page_config(page_title="🌿 Mental Health Support Chatbot")

# Background Styling
page_bg = '''
<style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506126613408-eca07ce68773");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .chat-container {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 15px;
        border-radius: 10px;
    }
    .alert {
        background-color: rgba(255, 0, 0, 0.1);
        color: red;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
'''

st.markdown(page_bg, unsafe_allow_html=True)

# Initialize chat history
st.session_state.setdefault('conversation_history', [])

# System Prompt for Emotional Awareness
system_prompt = {
    "role": "system",
    "content": "You are an empathetic mental health assistant. Your role is to provide emotional support, coping techniques, and positive reinforcement. \
    If the user expresses distress, offer immediate relief strategies like breathing exercises, grounding techniques, or self-care tips. \
    If a user mentions severe distress or harm, encourage them to seek professional help and provide emergency contact recommendations."
}

# Function to Generate AI Response
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    messages = [system_prompt] + st.session_state['conversation_history']
    
    response = ollama.chat(model="llama3", messages=messages)
    ai_response = response['message']['content']

    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

# Function to Identify Distress and Provide Immediate Help
def detect_distress(user_input):
    distress_keywords = ["hopeless", "suicidal", "can't take it", "overwhelmed", "breaking down", "give up", "self-harm", "hurt myself"]
    
    if any(keyword in user_input.lower() for keyword in distress_keywords):
        return True
    return False

# Function to Provide Coping Strategies
def provide_coping_strategy():
    prompt = "Give an immediate stress-relief technique for someone feeling anxious or overwhelmed."
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Function to Provide Affirmations
def generate_affirmation():
    prompt = "Give a short, uplifting affirmation for mental well-being."
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Function to Provide Guided Meditation
def generate_meditation_guide():
    prompt = "Provide a simple 5-minute guided meditation to calm anxiety."
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# UI Title
st.title("🌿 Mental Health Support Chatbot")

# Display Chat History
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")
st.markdown("</div>", unsafe_allow_html=True)

# Chat Input
user_message = st.text_input("How are you feeling today?")

if user_message:
    with st.spinner("Thinking..."):
        if detect_distress(user_message):
            st.markdown("<div class='alert'>⚠️ If you're feeling severely overwhelmed, please reach out to a trusted friend, family member, or professional. You're not alone. 💙</div>", unsafe_allow_html=True)
            st.markdown(f"**AI:** {provide_coping_strategy()}")
        else:
            ai_response = generate_response(user_message)
            st.markdown(f"**AI:** {ai_response}")

# Additional Features
col1, col2 = st.columns(2)

with col1:
    if st.button("💖 Give me a positive affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("🧘‍♂️ Give me a guided meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")
