import streamlit as st
import openai


openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_openai_feedback(user_responses):
    feedback = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Provide feedback on the user's interview:\n\n{user_responses}",
        max_tokens=100
    )
    return feedback['choices'][0]['text'].strip()

def interview_chatbot():
    st.sidebar.title("Interview Chatbot")

    # Initialize or retrieve conversation history from session_state
    st.session_state.conversation_history = st.session_state.get("conversation_history", [])

    # User introduction
    user_name = st.text_input("Introduce yourself:")
    job_role = st.selectbox("Select the job role you're being interviewed for:", ["HR Manager", "Developer", "Project Manager" , "ML Intern"])

    st.sidebar.text(f"User: {user_name}")
    st.sidebar.text(f"Job Role: {job_role}")

    
    role_specific_questions = {
        "HR Manager": [
            "Have you ever had to build an employer brand at your previous companies?",
            "What actions did you take to build a positive employer brand?",
            "How many years of experience you have in this field?",
            "What recruitment strategies have you found effective?"
        ],
        "Developer": [
            "Tell me about the tech stack that you recently used",
            "How many years of experience you have in this field?",
            "Describe your experience with version control systems."
        ],
        "Project Manager": [
            "How many years of experience you have in this field?",
            "Tell me about a project that faced challenges and how you addressed them.",
            "How do you lead your project team and set up dealdines for them?"
        ],
        "ML Intern":[
            "Tell me about the techstack that you recently used ?",
            "can you describe me about your project that you have done recently?"
        ]
    }

    
    if user_name and job_role:
        
        for i, question in enumerate(role_specific_questions.get(job_role, [])):
            user_response = st.text_input(f"Question {i+1}: {question}")

            
            st.session_state.conversation_history.append({
                "user": user_name,
                "job_role": job_role,
                "question": question,
                "user_response": user_response
            })

        
        user_responses = "\n".join(entry["user_response"] for entry in st.session_state.conversation_history)
        feedback = generate_openai_feedback(user_responses)
        st.text(f"OpenAI Feedback: {feedback}")

    # Display conversation history
    st.header("Conversation History")
    for entry in st.session_state.conversation_history:
        st.text(f"User: {entry['user']}, Job Role: {entry['job_role']}, Question: {entry['question']}, User Response: {entry['user_response']}")

    
    if st.button("New Chat"):
        # Clear conversation history for a new user
        st.session_state.conversation_history = []

    # Conclude the interview
    st.text("Thank you for your response, we will let you know after some time")

def main():
    st.title("User Interview Chatbot App")

    # Call the interview chatbot function
    interview_chatbot()

if __name__ == "__main__":
    main()
