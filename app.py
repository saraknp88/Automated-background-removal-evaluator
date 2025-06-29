import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from PIL import Image
import io
import base64
import os

# Page configuration
st.set_page_config(
    page_title="Sara's AI Evaluation Validator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for React-like styling and consistent color theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .criteria-list {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        width: 100%;
    }
    .celebration {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 1rem;
        color: white;
        margin: 2rem 0;
    }
    
    .evaluation-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .quality-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    .image-container {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
    }
    
    .note-box {
        background: #fef3c7;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-top: 1.5rem;
        border: 1px solid #f59e0b;
    }
    
    /* Navigation button styling */
    .nav-button-container {
        position: relative;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    .nav-button-right {
        display: flex;
        justify-content: flex-end;
        margin-top: 1.5rem;
    }
    
    .nav-button-small {
        padding: 0.5rem 1rem !important;
        font-size: 0.875rem !important;
        width: auto !important;
        min-width: 100px;
        max-width: 150px;
    }
    
    .disabled-nav-button {
        text-align: right;
        margin-top: 1.5rem;
    }
    
    .disabled-nav-button > div {
        display: inline-block;
        padding: 0.5rem 1rem;
        background-color: #f3f4f6;
        color: #9ca3af;
        border: 1px solid #d1d5db;
        border-radius: 0.375rem;
        font-weight: 500;
        font-size: 0.875rem;
        min-width: 180px;
        max-width: 200px;
        text-align: center;
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background-color: #3b82f6;
    }
    
    /* Button styling */
    .stButton > button[kind="primary"] {
        background-color: #3b82f6;
        border-color: #3b82f6;
    }
    
    .stButton > button[kind="secondary"] {
        background-color: #f3f4f6;
        border-color: #d1d5db;
        color: #374151;
    }
    
    /* Override button width for navigation buttons */
    .nav-button-right .stButton > button {
        width: auto !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.875rem !important;
        min-width: 180px;
        max-width: 200px;
    }
    
    /* Feedback button containers */
    .feedback-buttons {
        display: flex;
        gap: 0.5rem;
        justify-content: center;
        align-items: center;
    }
    
    .feedback-button-container {
        flex: 1;
    }
    
    .feedback-button-container .stButton > button {
        width: 100% !important;
        padding: 0.75rem 1rem !important;
        font-size: 1.2rem !important;
        border-radius: 0.5rem !important;
        font-weight: bold !important;
    }
    
    /* Thumbs up button - green theme */
    .thumbs-up .stButton > button {
        background-color: #16a34a !important;
        border-color: #16a34a !important;
        color: white !important;
    }
    
    .thumbs-up .stButton > button:hover {
        background-color: #15803d !important;
    }
    
    /* Thumbs down button - red theme */
    .thumbs-down .stButton > button {
        background-color: #dc2626 !important;
        border-color: #dc2626 !important;
        color: white !important;
    }
    
    .thumbs-down .stButton > button:hover {
        background-color: #b91c1c !important;
    }
    
    /* Selected state for feedback buttons */
    .feedback-selected-up {
        background-color: #15803d !important;
        box-shadow: 0 0 0 2px #16a34a !important;
    }
    
    .feedback-selected-down {
        background-color: #b91c1c !important;
        box-shadow: 0 0 0 2px #dc2626 !important;
    }
    
    /* Table styling improvements */
    .evaluation-table {
        background: white;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    
    .table-header {
        background: #f8fafc;
        padding: 1rem;
        border-bottom: 1px solid #e5e7eb;
        font-weight: 600;
        color: #374151;
    }
    
    .table-row {
        padding: 1rem;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .table-row:last-child {
        border-bottom: none;
    }
    
    /* Submit section styling */
    .submit-section {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 2rem 0;
    }
    
    .submit-button-right {
        display: flex;
        justify-content: flex-end;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .submit-button-right .stButton > button {
        width: auto !important;
        min-width: 200px;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: bold !important;
    }
    
    /* Rating selectbox styling */
    .stSelectbox > div > div {
        background-color: white;
        border: 2px solid #e5e7eb;
        border-radius: 0.375rem;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 1px #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    # Initialize all session state variables with default values
    defaults = {
        'evaluations': [],
        'human_feedback': {},
        'annotator_ratings': {},
        'analysis_results': None,
        'current_page': 'main',
        'evaluation_complete': False,
        'celebration_shown': False
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Demo data with actual image paths
def get_demo_data():
    return [
        {
            'id': 1, 
            'original': 'Before 0.jpg', 
            'processed': 'After 0.png', 
            'rating': 4, 
            'quality': 'Near Production Ready',
            'description': 'Florist portrait - Original vs Background Removed'
        },
        {
            'id': 2, 
            'original': 'Before 01.jpg', 
            'processed': 'After 01.png', 
            'rating': 3, 
            'quality': 'Moderately Functional',
            'description': 'Professional businesswoman - Background Processing'
        },
        {
            'id': 3, 
            'original': 'Before 02.jpg', 
            'processed': 'After 02.png', 
            'rating': 4, 
            'quality': 'Near Production Ready',
            'description': 'iPhone product photography - Background Removal'
        },
        {
            'id': 4, 
            'original': 'Before 03.jpg', 
            'processed': 'After 03.png', 
            'rating': 5, 
            'quality': 'Production Ready',
            'description': 'Food photography - Steak meal background processing'
        },
        {
            'id': 5, 
            'original': 'Before 04.jpg', 
            'processed': 'After 04.png', 
            'rating': 2, 
            'quality': 'Partially Viable',
            'description': 'Bowl splash - Complex liquid motion background removal'
        }
    ]

# Quality colors mapping - consistent with Background Removal Evaluator
def get_quality_color(rating):
    colors = {1: '#dc2626', 2: '#ea580c', 3: '#ca8a04', 4: '#2563eb', 5: '#16a34a'}
    return colors.get(rating, '#6b7280')

# Load image with fallback to placeholder
def load_image_with_fallback(image_path, width=200, height=150):
    try:
        # Try to load the actual image
        if os.path.exists(image_path):
            return Image.open(image_path)
        else:
            # If file doesn't exist, create placeholder
            return create_placeholder_image(width, height, os.path.basename(image_path))
    except Exception as e:
        # If any error occurs, create placeholder
        return create_placeholder_image(width, height, f"Error: {os.path.basename(image_path)}")

# Create placeholder image with filename
def create_placeholder_image(width=200, height=150, text="Demo Image"):
    img = Image.new('RGB', (width, height), color='lightgray')
    # You could add text to the image here if needed
    return img

# Main header - consistent with Background Removal Evaluator
def render_header():
    st.markdown('<h1 class="main-header">Sara\'s AI Evaluation Validator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Validate AI background removal ratings with thumbs up/down feedback</p>', unsafe_allow_html=True)

# Evaluation preview without title (for when title is shown separately)
def render_evaluation_preview_without_title():
    demo_data = get_demo_data()
    
    for i, pair in enumerate(demo_data):
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Original Image**")
            img = load_image_with_fallback(pair['original'], 150, 120)
            st.image(img, use_container_width=True)
        
        with col2:
            st.markdown("**Background Removal Result**")
            img = load_image_with_fallback(pair['processed'], 150, 120)
            st.image(img, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if i < len(demo_data) - 1:
            st.markdown("---")

# Evaluation preview
def render_evaluation_preview():
    st.markdown("### 📋 Image Pairs to be Evaluated")
    render_evaluation_preview_without_title()

# AI evaluation simulation
def simulate_ai_evaluation():
    st.markdown("### 🤖 AI Processing in Progress...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stages = [
        "Loading image pairs...",
        "Analyzing background complexity...",
        "Processing edge detection...",
        "Evaluating segmentation quality...",
        "Calculating quality scores...",
        "Finalizing ratings..."
    ]
    
    for i, stage in enumerate(stages):
        status_text.text(stage)
        progress_bar.progress((i + 1) / len(stages))
        time.sleep(0.5)
    
    status_text.text("✅ Evaluation complete!")
    time.sleep(1)
    
    # Store evaluations in session state
    st.session_state.evaluations = get_demo_data()
    st.session_state.evaluation_complete = True
    st.rerun()

# Feedback buttons with improved styling
def render_feedback_buttons(eval_id):
    st.markdown('<div class="feedback-buttons">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    current_feedback = st.session_state.human_feedback.get(eval_id)
    
    with col1:
        st.markdown('<div class="feedback-button-container thumbs-up">', unsafe_allow_html=True)
        button_type = "primary" if current_feedback == True else "secondary"
        if st.button("👍 Agree", key=f"up_{eval_id}", type=button_type, 
                    help="Agree with AI rating"):
            st.session_state.human_feedback[eval_id] = True
            if eval_id in st.session_state.annotator_ratings:
                del st.session_state.annotator_ratings[eval_id]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feedback-button-container thumbs-down">', unsafe_allow_html=True)
        button_type = "primary" if current_feedback == False else "secondary"
        if st.button("👎 Disagree", key=f"down_{eval_id}", type=button_type,
                    help="Disagree with AI rating"):
            st.session_state.human_feedback[eval_id] = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Annotator rating input
def render_annotator_rating(eval_id):
    if st.session_state.human_feedback.get(eval_id) == False:
        rating = st.selectbox(
            "Your rating:",
            options=[None, 1, 2, 3, 4, 5],
            format_func=lambda x: "Select rating*" if x is None else str(x),
            key=f"rating_{eval_id}",
            index=0 if eval_id not in st.session_state.annotator_ratings 
                  else st.session_state.annotator_ratings[eval_id]
        )
        
        if rating is not None:
            st.session_state.annotator_ratings[eval_id] = rating
            
        return rating is not None
    elif st.session_state.human_feedback.get(eval_id) == True:
        st.success("✅ Agreed")
        return True
    else:
        st.info("—")
        return True

# Validation interface with improved layout
def render_validation_interface():
    st.markdown("### ✅ Validate AI Ratings")
    
    # Instructions
    st.markdown("""
    <div class="criteria-list">
        <strong>Review each AI evaluation and provide feedback:</strong><br><br>
        <strong>👍 Agree:</strong> The AI rating accurately reflects the background removal quality<br>
        <strong>👎 Disagree:</strong> The AI rating does not match your assessment (provide your rating)
    </div>
    """, unsafe_allow_html=True)
    
    # Reset button in top right
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col4:
        if st.button("🔄 Reset", key="reset_btn", type="secondary"):
            for key in ['evaluations', 'human_feedback', 'annotator_ratings', 
                       'analysis_results', 'evaluation_complete', 'celebration_shown']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_page = 'main'
            st.rerun()
    
    # Create evaluation table
    for eval_data in st.session_state.evaluations:
        st.markdown('<div class="evaluation-card">', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1.5, 2, 2, 2])
        
        with col1:
            st.markdown("**Original**")
            img = load_image_with_fallback(eval_data['original'], 150, 120)
            st.image(img, width=120)
            st.caption(eval_data['original'])
        
        with col2:
            st.markdown("**Processed**")
            img = load_image_with_fallback(eval_data['processed'], 150, 120)
            st.image(img, width=120)
            st.caption(eval_data['processed'])
        
        with col3:
            st.markdown("**AI Rating**")
            color = get_quality_color(eval_data['rating'])
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="background: {color}; color: white; width: 30px; height: 30px; 
                            border-radius: 50%; display: flex; align-items: center; 
                            justify-content: center; font-weight: bold;">
                    {eval_data['rating']}
                </div>
                <span style="font-size: 1.2rem; font-weight: bold;">{eval_data['rating']}/5</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("**Quality Level**")
            st.write(eval_data['quality'])
        
        with col5:
            st.markdown("**Your Feedback**")
            render_feedback_buttons(eval_data['id'])
        
        with col6:
            st.markdown("**Your Rating**")
            render_annotator_rating(eval_data['id'])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit section
    if st.session_state.human_feedback:
        thumbs_down_items = [id for id, feedback in st.session_state.human_feedback.items() 
                           if feedback == False]
        missing_ratings = [id for id in thumbs_down_items 
                         if id not in st.session_state.annotator_ratings]
        
        can_submit = len(missing_ratings) == 0
        
        st.markdown('<div class="submit-section">', unsafe_allow_html=True)
        
        if not can_submit:
            st.error(f"⚠️ Please provide ratings for {len(missing_ratings)} thumbs down items")
        else:
            st.success("✅ All feedback provided! Ready to submit.")
        
        st.markdown('<div class="submit-button-right">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("✨ Submit Responses", disabled=not can_submit, key="submit_btn", 
                        type="primary", help="Submit all your feedback and ratings"):
                if can_submit:
                    calculate_analysis()
                    show_celebration()
                    st.session_state.current_page = 'thank_you'
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Celebration animation
def show_celebration():
    # Create a brief fireworks effect using Streamlit's built-in features
    if 'celebration_shown' not in st.session_state:
        st.session_state.celebration_shown = True
        
        # Show balloons for 3 seconds
        st.balloons()

# Calculate analysis results
def calculate_analysis():
    feedback_count = len(st.session_state.human_feedback)
    agreement_count = sum(1 for f in st.session_state.human_feedback.values() if f == True)
    disagreement_count = feedback_count - agreement_count
    
    agreement_rate = (agreement_count / feedback_count * 100) if feedback_count > 0 else 0
    disagreement_rate = (disagreement_count / feedback_count * 100) if feedback_count > 0 else 0
    
    st.session_state.analysis_results = {
        'agreement_rate': round(agreement_rate, 1),
        'disagreement_rate': round(disagreement_rate, 1),
        'feedback_count': feedback_count,
        'agreement_count': agreement_count,
        'disagreement_count': disagreement_count
    }

# Thank you page
def render_thank_you_page():
    st.markdown("""
    <div class="celebration">
        <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">🎉 Evaluation Complete! 🎉</h1>
        <h2 style="font-size: 1.5rem; margin-bottom: 1rem;">Thank you for your participation!</h2>
        <p style="font-size: 1.1rem;">Your responses have been recorded successfully.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="nav-button-container">', unsafe_allow_html=True)
    st.markdown('<div class="nav-button-right">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col2:
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("📊 View Analysis", key="view_analysis", type="primary",
                        help="See detailed analysis of your feedback"):
                st.session_state.current_page = 'analysis'
                st.rerun()
        
        with col_b:
            if st.button("🔄 Start New", key="new_evaluation", type="secondary",
                        help="Begin a fresh evaluation session"):
                for key in ['evaluations', 'human_feedback', 'annotator_ratings', 
                           'analysis_results', 'evaluation_complete', 'celebration_shown']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.current_page = 'main'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis dashboard
def render_analysis_dashboard():
    st.markdown('<h1 class="main-header">Analysis Results</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Human validation feedback analysis</p>', unsafe_allow_html=True)
    
    # Reset button
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col4:
        if st.button("🔄 Start New Evaluation", key="new_eval_analysis", type="secondary"):
            for key in ['evaluations', 'human_feedback', 'annotator_ratings', 
                       'analysis_results', 'evaluation_complete', 'celebration_shown']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_page = 'main'
            st.rerun()
    
    results = st.session_state.analysis_results
    
    # Executive Summary
    st.markdown("### Executive Summary")
    
    summary_text = f"""
    We conducted an AI and Human Evaluator assessment with a **{results['agreement_rate']}% agreement rate** 
    and **{results['disagreement_rate']}% evaluation gap**.
    
    **Background Removal Recommendations:**
    {'Maintain current algorithms, focus on edge cases' if results['agreement_rate'] >= 70 
     else 'Improve edge detection and segmentation techniques'}
    
    **AI Evaluation Improvements:**
    {'Fine-tune quality thresholds, ready for production' if results['agreement_rate'] >= 70 
     else 'Recalibrate scoring weights and evaluation criteria'}
    """
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #e5e7eb; margin-bottom: 1.5rem;">
        {summary_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics Dashboard
    st.markdown("### Validation Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🔍 Total Evaluations",
            value=len(st.session_state.evaluations),
            help="Total image pairs evaluated"
        )
    
    with col2:
        st.metric(
            label="✅ Agreement Rate",
            value=f"{results['agreement_rate']}%",
            delta=f"{results['agreement_count']} approvals",
            help="Percentage of AI ratings approved by humans"
        )
    
    with col3:
        st.metric(
            label="❌ Disagreement Rate", 
            value=f"{results['disagreement_rate']}%",
            delta=f"{results['disagreement_count']} rejections",
            delta_color="inverse",
            help="Percentage of AI ratings rejected by humans"
        )
    
    # Visualizations
    st.markdown("### Analysis Charts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Agreement pie chart - only show if there's data
        if results['feedback_count'] > 0:
            fig_pie = px.pie(
                values=[results['agreement_count'], results['disagreement_count']],
                names=['Agreement', 'Disagreement'],
                colors=['#10b981', '#ef4444'],
                title="Human-AI Agreement Distribution"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No feedback data available for pie chart")
    
    with col2:
        # Rating distribution
        if st.session_state.evaluations:
            evaluations_df = pd.DataFrame(st.session_state.evaluations)
            rating_counts = evaluations_df.groupby('rating').size().reset_index(name='count')
            
            # Create bar chart with consistent colors
            rating_labels = [f"{i} - {['Unusable', 'Partially Viable', 'Moderately Functional', 'Near Production Ready', 'Production Ready'][i-1]}" for i in rating_counts['rating']]
            colors = [get_quality_color(i) for i in rating_counts['rating']]
            
            fig_bar = px.bar(
                x=rating_labels,
                y=rating_counts['count'],
                title="AI Rating Distribution",
                labels={'x': 'AI Rating', 'y': 'Number of Images'},
                color=rating_labels,
                color_discrete_sequence=colors
            )
            fig_bar.update_layout(showlegend=False, height=400, title_x=0.5)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No evaluation data available for bar chart")
    
    # Detailed Analysis
    if results['disagreement_count'] > 0:
        st.markdown("### Disagreement Analysis")
        
        disagreements = [(id, st.session_state.annotator_ratings.get(id)) 
                        for id, feedback in st.session_state.human_feedback.items() 
                        if feedback == False and id in st.session_state.annotator_ratings]
        
        if disagreements:
            higher_ratings = sum(1 for id, rating in disagreements 
                               if rating > next(e['rating'] for e in st.session_state.evaluations 
                                              if e['id'] == id))
            lower_ratings = len(disagreements) - higher_ratings
            
            if higher_ratings > lower_ratings:
                st.warning("""
                **Trend Analysis:** Human annotators tend to recommend higher quality ratings than the AI system, 
                suggesting the automated evaluator may be too conservative.
                """)
            elif lower_ratings > higher_ratings:
                st.warning("""
                **Trend Analysis:** Human annotators tend to recommend lower quality ratings than the AI system, 
                indicating the automated evaluator may be too lenient.
                """)
            else:
                st.info("""
                **Trend Analysis:** Human annotator ratings show balanced distribution compared to AI evaluations.
                """)
    
    st.markdown("---")
    st.markdown(f"""
    **Analysis Complete** - {results['feedback_count']} evaluations processed with 
    {results['agreement_rate']}% agreement rate. Human feedback will be integrated into 
    reinforcement learning processes to improve automated evaluation performance.
    """)

# Main application logic
def main():
    # Initialize session state FIRST before anything else
    initialize_session_state()
    
    # Now render the header and rest of the app
    render_header()
    
    # Navigation logic
    if st.session_state.current_page == 'main':
        if not st.session_state.evaluation_complete:
            # Instructions
            st.markdown("""
            <div class="criteria-list">
                <strong>AI Background Removal Evaluation Validator</strong><br><br>
                This tool simulates an AI evaluation system that automatically assesses background removal quality, 
                followed by human validation to improve the AI's accuracy. The process includes:<br><br>
                <strong>1. AI Evaluation:</strong> Automated assessment of background removal results<br>
                <strong>2. Human Validation:</strong> Review and validate AI ratings with thumbs up/down feedback<br>
                <strong>3. Analysis:</strong> Compare human vs AI assessments to improve the system
            </div>
            """, unsafe_allow_html=True)
            
            # Put title and button on the same row
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("### 📋 Image Pairs to be Evaluated")
            with col2:
                if st.button("🧠 Start AI Evaluation", key="start_eval", type="primary",
                            help="Begin the automated evaluation process"):
                    simulate_ai_evaluation()
            
            # Add some spacing
            st.markdown("---")
            
            # Now show the preview (without the title since it's already shown above)
            render_evaluation_preview_without_title()
            
            # Note at the bottom
            st.markdown("""
            <div class="note-box">
                <small><strong>Note:</strong> This is a demonstration of AI-human collaboration in quality assessment. 
                The AI will first evaluate all image pairs, then you'll validate those evaluations.</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            render_validation_interface()
    
    elif st.session_state.current_page == 'thank_you':
        render_thank_you_page()
    
    elif st.session_state.current_page == 'analysis':
        render_analysis_dashboard()


if __name__ == "__main__":
    main()
