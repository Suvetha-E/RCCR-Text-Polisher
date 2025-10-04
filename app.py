import streamlit as st
import re
from textblob import TextBlob

# --- 1. TASK PRESETS ---
TASK_PRESETS = {
    "Customer Support Email": {
        "role": "A professional and empathetic customer support assistant.",
        "constraints": "- Acknowledge user's frustration.\n- Include a specific commitment to action.\n- Keep it under 4 sentences."
    },
    "Git Commit Message": {
        "role": "A clear and concise software developer documenting a change.",
        "constraints": "- Follow conventional commit format (`type: description`).\n- Must include an issue ID.\n- State the 'what' and 'why'."
    },
}

# --- 2. REFINEMENT FUNCTION WITH SPELLING & CAPITALIZATION ---
def simple_refine(raw_text):
    """
    Refines text by:
    - Correcting spelling and grammar (TextBlob)
    - Capitalizing first letter
    - Adding period if missing
    - Replacing casual words
    """
    text = raw_text.strip()
    if not text:
        return ""

    # Replace casual words
    text = re.sub(r"\bhi\b", "Hello", text, flags=re.I)
    text = re.sub(r"\bpls\b", "please", text, flags=re.I)
    text = re.sub(r"\btho\b", "though", text, flags=re.I)
    text = re.sub(r"\bthx\b", "Thanks", text, flags=re.I)

    # Correct spelling and grammar
    text_blob = TextBlob(text)
    text = str(text_blob.correct())

    # Capitalize first letter
    text = text[0].upper() + text[1:] if text else text

    # Add period if missing
    if text and text[-1] not in ".!?":
        text += "."

    return text

# --- 3. MOCK CRITIQUE FUNCTION ---
def get_critique(raw_text, role, constraints):
    """
    Returns simple critique for demo purposes.
    """
    critique_points = []
    if raw_text.islower():
        critique_points.append("Text should start with a capital letter.")
    if len(raw_text.split()) > 20:
        critique_points.append("Text is a bit long; consider shortening.")
    if any(word in raw_text.lower() for word in ["hi", "pls", "tho", "thx"]):
        critique_points.append("Avoid casual words; use professional tone.")
    if not critique_points:
        critique_points.append("Text looks good!")
    return "\n• " + "\n• ".join(critique_points)

# --- 4. STREAMLIT UI ---
st.set_page_config(layout="wide")
st.title("✍️ RCCR Text Polisher")
st.markdown("Implementation of the **Role → Constraints → Critique → Refine** framework (demo version).")

# Input Layer
task_type = st.selectbox("Select a task type:", list(TASK_PRESETS.keys()))
default_config = TASK_PRESETS[task_type]

col1, col2 = st.columns(2)
with col1:
    role = st.text_area("Role:", value=default_config["role"], height=100)
with col2:
    constraints = st.text_area("Constraints:", value=default_config["constraints"], height=100)

raw_text = st.text_area(
    "Enter your raw text here:",
    height=150,
    placeholder="e.g., 'hi pls check the featur tho it is not working'"
)

if st.button("✨ Refine Text"):
    if not raw_text.strip():
        st.error("Please enter some text to refine.")
    else:
        with st.spinner("Analyzing and refining..."):
            # --- RCCR Pipeline ---
            critique = get_critique(raw_text, role, constraints)
            refined_text = simple_refine(raw_text)

            # --- Output Layer ---
            st.subheader("Analysis & Refined Output")
            out_col1, out_col2 = st.columns(2)
            with out_col1:
                st.markdown("#### Critique")
                st.info(critique)
            with out_col2:
                st.markdown("#### Refined Output")
                st.success(refined_text)
