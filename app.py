import streamlit as st
from together import Together
from datetime import datetime
import time

# Initialize Together client
import os
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))


# Page configuration
st.set_page_config(
    page_title="Chatterly AI",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ========== Custom CSS ==========
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Main content area */
        .main-content {
            padding-top: 20px;
            padding-bottom: 120px;
            max-width: 700px;
            margin: 0 auto;
        }
        
        /* Welcome container */
        .welcome-container {
            padding: 2rem;
            background: white;
            border-radius: 12px;
            text-align: center;
            margin: 2rem 0;
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Custom Header */
        .custom-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 20px;
            z-index: 1000;
            border-bottom: 1px solid #f0f0f0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            animation: slideDown 0.3s ease-out;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: #3b82f6;
        }
        
        /* Chat bubbles */
        .user-message {
            background-color: #3b82f6;
            color: white;
            border-radius: 18px 18px 4px 18px;
            padding: 12px 16px;
            margin: 8px 0;
            max-width: 80%;
            margin-left: auto;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            word-wrap: break-word;
            animation: fadeInUp 0.3s ease-out;
        }
        
        .assistant-message {
            background-color: #f8fafc;
            color: #1e293b;
            border-radius: 18px 18px 18px 4px;
            padding: 12px 16px;
            margin: 8px 0;
            max-width: 80%;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
            word-wrap: break-word;
            animation: fadeInUp 0.3s ease-out;
        }
        
        /* Typing animation */
        .typing-indicator {
            display: inline-block;
            padding: 12px 16px;
            background-color: #f8fafc;
            border-radius: 18px 18px 18px 4px;
            border: 1px solid #e2e8f0;
            max-width: 80%;
            margin: 8px 0;
        }
        
        .typing-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #94a3b8;
            margin-right: 4px;
            animation: typingAnimation 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) {
            animation-delay: 0s;
        }
        
        .typing-dot:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-dot:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        /* Correction box */
        .correction-box {
            background-color: #f0f5ff;
            border-left: 3px solid #3b82f6;
            padding: 10px 12px;
            margin-top: 8px;
            border-radius: 0 8px 8px 0;
            font-size: 0.9rem;
            color: #334155;
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Timestamp styling */
        .timestamp {
            font-size: 0.7rem;
            color: #64748b;
            margin-top: 4px;
            text-align: right;
            opacity: 0;
            animation: fadeIn 0.5s ease-out 0.3s forwards;
        }
        
        /* Chat input area */
        .chat-input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 1rem;
            border-top: 1px solid #e2e8f0;
            z-index: 100;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.03);
            animation: slideUp 0.3s ease-out;
        }
        
        .input-wrapper {
            max-width: 700px;
            margin: 0 auto;
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            padding: 1.5rem 1rem;
            background: #f8fafc;
            animation: fadeInLeft 0.3s ease-out;
        }
        
        .sidebar-section {
            margin-bottom: 2rem;
        }
        
        .sidebar-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            transform: translateY(-1px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }
        
        /* New chat button */
        .new-chat-btn {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.60rem;
            font-weight: 500;
            width: 100%;
            margin-bottom: 1.5rem;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .new-chat-btn:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            transform: translateY(-1px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        /* Settings items */
        .setting-item {
            margin-bottom: 1.5rem;
            animation: fadeIn 0.5s ease-out;
        }
        
        .setting-label {
            display: block;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
            color: #475569;
            font-weight: 500;
        }
        
       /* History items */
        .history-container {
            margin-top: 1rem;
        }
        
        .history-item {
            padding: 0.75rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9rem;
            background: white;
            border: 1px solid #e2e8f0;
            animation: fadeIn 0.3s ease-out;
        }
        
        .history-item:hover {
            background: #f0f5ff;
            border-color: #bfdbfe;
        }
        
        .history-item.active {
            background: #e0e7ff;
            border-color: #93c5fd;
        }
        
        .history-title {
            font-weight: 500;
            color: #1e293b;
        }
        
        /* Radio buttons */
        .stRadio [role=radiogroup] {
            gap: 8px;
        }
        
        .stRadio [role=radio] {
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        
        .stRadio [role=radio][aria-checked=true] {
            background: #f0f5ff;
            border-color: #93c5fd;
            color: #1e40af;
        }
        
        /* Select boxes */
        .stSelectbox [role=button] {
            padding: 8px 12px;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeInUp {
            from { 
                opacity: 0;
                transform: translateY(10px);
            }
            to { 
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInLeft {
            from { 
                opacity: 0;
                transform: translateX(-10px);
            }
            to { 
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes slideDown {
            from { 
                transform: translateY(-100%);
            }
            to { 
                transform: translateY(0);
            }
        }
        
        @keyframes slideUp {
            from { 
                transform: translateY(100%);
            }
            to { 
                transform: translateY(0);
            }
        }
        
        @keyframes typingAnimation {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-5px); }
        }
        
        /* Smooth transitions for chat messages */
        .chat-message {
            transition: all 0.3s ease-out;
        }
        
        /* Typewriter effect */
        .typewriter {
            overflow: hidden;
            border-right: 2px solid #3b82f6;
            white-space: nowrap;
            margin: 0 auto;
            letter-spacing: 0.15em;
            animation: 
                typing 3.5s steps(40, end),
                blink-caret 0.75s step-end infinite;
        }
        
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        
        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: #3b82f6; }
        }
    </style>
""", unsafe_allow_html=True)

# ========== Session State ==========
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.conversation_started = False
    st.session_state.settings = {
        "level": "B1 (Intermediate)",
        "topic": "Daily Life",
        "ai_style": "Friendly Tutor",
        "correction_level": "Balanced"
    }
    st.session_state.settings_applied = False
    st.session_state.chat_history = []
    st.session_state.current_chat_id = None
    st.session_state.new_chat_clicked = False
    st.session_state.show_typing = False

# ========== Custom Header ==========
st.markdown("""
    <div class="custom-header">
        <div class="logo">Chatterly AI</div>
    </div>
""", unsafe_allow_html=True)

# ========== Sidebar ==========
with st.sidebar:
    # New Chat Button
    if st.button("＋ New Chat",
                 key="new_chat_button",
                 use_container_width=True,
                 type="primary"):
        st.session_state.new_chat_clicked = True
        st.session_state.messages = []
        st.session_state.conversation_started = False
        st.session_state.settings_applied = False
        st.session_state.current_chat_id = None
        st.rerun()

    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-title">Settings</div>
    """, unsafe_allow_html=True)

    # Settings
    new_level = st.selectbox(
        "Your English Level",
        ["A1 (Beginner)", "A2 (Elementary)", "B1 (Intermediate)",
         "B2 (Upper Intermediate)", "C1 (Advanced)", "C2 (Proficiency)"],
        index=2,
        key="level_select"
    )

    new_topic = st.selectbox(
        "Conversation Topic", [
            "Daily Life", "Travel", "Study Abroad",
            "Job Interview", "Technology", "Environment",
            "Hobbies", "Culture", "Health", "Current Events"
        ],
        index=0,
        key="topic_select"
    )

    new_ai_style = st.selectbox(
        "AI Style",
        ["Friendly Tutor", "Professional Coach", "Conversational Partner"],
        index=0,
        key="style_select"
    )

    new_correction_level = st.radio(
        "Correction Level",
        ["Gentle", "Balanced", "Detailed"],
        index=1,
        key="correction_select"
    )

    # Apply settings button
    if st.button("Apply Settings",
                 key="apply_settings",
                 type="primary",
                 use_container_width=True):
        st.session_state.settings = {
            "level": new_level,
            "topic": new_topic,
            "ai_style": new_ai_style,
            "correction_level": new_correction_level
        }
        st.session_state.settings_applied = True
        st.session_state.messages = []
        st.session_state.conversation_started = False

        # Add to chat history
        new_chat = {
            "id": str(datetime.now().timestamp()),
            "title": f"Chat about {new_topic} ({new_level})",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "settings": st.session_state.settings.copy(),
            "messages": []
        }
        st.session_state.chat_history.append(new_chat)
        st.session_state.current_chat_id = new_chat["id"]

        st.rerun()

    # Chat History Section
    st.markdown('<div class="sidebar-title">Recent chats</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="history-container">', unsafe_allow_html=True)
    # Show only last 10 chats
    for chat in reversed(st.session_state.chat_history[-10:]):
        is_active = (st.session_state.current_chat_id == chat["id"])
        st.markdown(f"""
            <div class="history-item {'active' if is_active else ''}" 
                 onclick="window.location.href='?chat_id={chat['id']}'">
                <div class="history-title">{chat["title"]}</div>
                <div style="font-size: 0.7rem; color: #64748b;">{chat["date"]}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== Main Content Area ==========
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Welcome screen
if not st.session_state.messages and not st.session_state.settings_applied:
    st.markdown("""
        <div class="welcome-container">
            <div style="font-size: 1.5rem; font-weight: 600; color: #3b82f6; margin-bottom: 1rem;">👋 Welcome to Chatterly AI</div>
            <div style="color: #64748b; margin-bottom: 1.5rem; line-height: 1.6;">
                Practice English conversation with an AI tutor. Select your preferences 
                from the sidebar and click "Apply Settings" to get started!
            </div>
            <div style="background: #f0f5ff; padding: 1rem; border-radius: 8px; animation: fadeIn 1s ease-out;">
                <div style="font-weight: 600; color: #1e40af; margin-bottom: 0.5rem;">About Chatterly AI</div>
                <div style="font-size: 0.9rem; color: #475569;">
                    Chatterly AI helps you improve your English through natural conversations. 
                    Our AI tutor adapts to your level and provides personalized feedback.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.container():
            st.markdown(
                f'<div class="user-message chat-message">{msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="timestamp">{msg.get("timestamp", "")}</div>', unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown(
                f'<div class="assistant-message chat-message">{msg["content"]}</div>', unsafe_allow_html=True)
            if msg.get("corrections"):
                st.markdown(
                    f'<div class="correction-box">✏️ {msg["corrections"]}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="timestamp">{msg.get("timestamp", "")}</div>', unsafe_allow_html=True)

# Show typing indicator when waiting for AI response
if st.session_state.get("show_typing", False):
    with st.container():
        st.markdown("""
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main-content div

# ========== Chat Input Area ==========
st.markdown("""
    <div class="chat-input-container">
        <div class="input-wrapper">
""", unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message...", key="chat_input")

st.markdown("""
        </div>
    </div>
""", unsafe_allow_html=True)

# Handle text input
if user_input:
    # Add user message to chat
    user_message = {
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    st.session_state.messages.append(user_message)
    st.session_state.show_typing = True

    # Update the current chat in history if it exists
    if st.session_state.current_chat_id:
        for chat in st.session_state.chat_history:
            if chat["id"] == st.session_state.current_chat_id:
                chat["messages"] = st.session_state.messages.copy()
                break

    # Generate AI response only if settings have been applied
    if st.session_state.settings_applied:
        with st.spinner(""):
            # Build prompt based on settings
            prompt = f"""
You are an English tutor helping a student at {st.session_state.settings['level']} level. 
The conversation topic is: {st.session_state.settings['topic']}.

Student's message:
"{user_input}"

Guidelines:
1. Respond naturally as a {st.session_state.settings['ai_style'].lower()}
2. Keep responses concise (1-3 sentences)
3. Correction level: {st.session_state.settings['correction_level']}
4. Make the conversation flow naturally
5. If there are errors to correct, add them after "---CORRECTIONS---"

Response format:
[Your natural response here]
---CORRECTIONS---
[Corrections if any]
"""

            try:
                # Simulate typing delay for better UX
                time.sleep(1)

                response = client.chat.completions.create(
                    model="meta-llama/Llama-Vision-Free",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=500
                ).choices[0].message.content

                # Process response
                if "---CORRECTIONS---" in response:
                    ai_reply, corrections = response.split(
                        "---CORRECTIONS---", 1)
                    ai_reply = ai_reply.strip()
                    corrections = corrections.strip()
                else:
                    ai_reply = response.strip()
                    corrections = ""

                assistant_message = {
                    "role": "assistant",
                    "content": ai_reply,
                    "corrections": corrections,
                    "timestamp": datetime.now().strftime("%H:%M")
                }
                st.session_state.messages.append(assistant_message)
                st.session_state.show_typing = False

                # Update the current chat in history if it exists
                if st.session_state.current_chat_id:
                    for chat in st.session_state.chat_history:
                        if chat["id"] == st.session_state.current_chat_id:
                            chat["messages"] = st.session_state.messages.copy()
                            break

                st.rerun()

            except Exception as e:
                st.session_state.show_typing = False
                st.error("Sorry, something went wrong. Please try again.")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I encountered an error. Could you repeat that?",
                    "corrections": "",
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                st.rerun()
    else:
        st.session_state.show_typing = False
        st.warning("Please apply your settings first before chatting")
        st.rerun()
