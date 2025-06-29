import streamlit as st
import time
from typing import Dict, Any

# Page config
st.set_page_config(
    page_title="Sara's AI Evaluation Validator",
    page_icon="✨",
    layout="wide"
)

# Custom CSS for styling with image magnification
st.markdown("""
<style>
    .custom-next-button button {
        background-color: #3b82f6 !important; /* blue-500 */
        color: white !important;
        font-weight: bold;
        border-radius: 5px;
        width: 100%;
        height: 3em;
        border: none;
        cursor: pointer;
    }
    .custom-next-button button:disabled {
        background-color: #9ca3af !important; /* gray-400 */
        cursor: not-allowed;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = []
if 'human_feedback' not in st.session_state:
    st.session_state.human_feedback = {}
if 'annotator_ratings' not in st.session_state:
    st.session_state.annotator_ratings = {}
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'show_thank_you' not in st.session_state:
    st.session_state.show_thank_you = False
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False
if 'current_image_index' not in st.session_state:
    st.session_state.current_image_index = 0
if 'custom_next_clicked' not in st.session_state:
    st.session_state.custom_next_clicked = -1

# ... Other logic remains unchanged ...

# Bottom navigation
st.markdown("---")

current_has_feedback = eval_id in st.session_state.human_feedback
col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

with col1:
    if st.button("← Previous", disabled=st.session_state.current_image_index == 0, use_container_width=True):
        previous_image()

with col2:
    st.write("")

with col4:
    st.write("")

with col5:
    if current_position < total_images:
        next_disabled = not current_has_feedback
        if not next_disabled:
            st.markdown("""
            <div class="custom-next-button">
                <form action="" method="post">
                    <button type="submit">Next →</button>
                </form>
            </div>
            """, unsafe_allow_html=True)
            if st.session_state.get("custom_next_clicked") != current_position:
                st.session_state.custom_next_clicked = current_position
                next_image()
        else:
            st.markdown("""
            <div class="custom-next-button">
                <button type="button" disabled>Next →</button>
            </div>
            """, unsafe_allow_html=True)
    else:
        thumbs_down_items = [eval_id for eval_id, feedback in st.session_state.human_feedback.items() if not feedback]
        missing_ratings = [eval_id for eval_id in thumbs_down_items if eval_id not in st.session_state.annotator_ratings]
        can_submit = len(missing_ratings) == 0 and len(st.session_state.human_feedback) == total_images
        submit_help = "All images must have feedback before submitting" if not can_submit else "Submit all responses"

        if st.button("Submit", type="primary", disabled=not can_submit, help=submit_help, use_container_width=True):
            submit_responses()

if not current_has_feedback:
    st.info("👆 Please provide your feedback (👍 agree or 👎 disagree) to proceed to the next image.")
