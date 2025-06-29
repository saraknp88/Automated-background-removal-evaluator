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

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .evaluation-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .quality-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    .celebration {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
        margin: 0.25rem 0;
    }
    
    .button-container {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        gap: 0.5rem;
        padding: 1rem;
    }
    
    .submit-button-section {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .feedback-button {
        margin: 0.2rem;
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

# Quality colors mapping
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

# Main header
def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Sara's AI Evaluation Validator</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            Validate AI background removal ratings with thumbs up/down feedback
        </p>
    </div>
    """, unsafe_allow_html=True)

# Evaluation preview
def render_evaluation_preview():
    st.markdown("### 📋 Image Pairs to be Evaluated")
    demo_data = get_demo_data()
    
    for i, pair in enumerate(demo_data):
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 2, 3])
            
            with col1:
                st.markdown("**Original**")
                img = load_image_with_fallback(pair['original'], 150, 120)
                st.image(img, caption=pair['original'], width=150)
            
            with col2:
                st.markdown("<div style='text-align: center; padding-top: 50px;'>→</div>", 
                          unsafe_allow_html=True)
            
            with col3:
                st.markdown("**Processed**")
                img = load_image_with_fallback(pair['processed'], 150, 120)
                st.image(img, caption=pair['processed'], width=150)
            
            with col4:
                st.markdown(f"**Description:** {pair['description']}")
                st.markdown(f"**File:** `{pair['original']}`")
        
        if i < len(demo_data) - 1:
            st.divider()

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

# Feedback buttons
def render_feedback_buttons(eval_id):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👍", key=f"up_{eval_id}", help="Agree with AI rating"):
            st.session_state.human_feedback[eval_id] = True
            if eval_id in st.session_state.annotator_ratings:
                del st.session_state.annotator_ratings[eval_id]
            st.rerun()
    
    with col2:
        if st.button("👎", key=f"down_{eval_id}", help="Disagree with AI rating"):
            st.session_state.human_feedback[eval_id] = False
            st.rerun()

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

# Validation interface
def render_validation_interface():
    st.markdown("### ✅ Validate AI Ratings")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Reset", key="reset_btn"):
            for key in ['evaluations', 'human_feedback', 'annotator_ratings', 
                       'analysis_results', 'evaluation_complete', 'celebration_shown']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_page = 'main'
            st.rerun()
    
    # Top submit button for easier access (right side with better alignment)
    if st.session_state.human_feedback:
        thumbs_down_items = [id for id, feedback in st.session_state.human_feedback.items() 
                           if feedback == False]
        missing_ratings = [id for id in thumbs_down_items 
                         if id not in st.session_state.annotator_ratings]
        
        can_submit = len(missing_ratings) == 0
        
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        with col4:
            if not can_submit:
                st.error(f"⚠️ Please provide ratings for {len(missing_ratings)} thumbs down items")
            
            if st.button("✨ Submit Responses", disabled=not can_submit, key="submit_btn_top", 
                        help="Submit all your feedback and ratings"):
                if can_submit:
                    calculate_analysis()
                    show_celebration()
                    st.session_state.current_page = 'thank_you'
                    st.rerun()
    
    st.divider()
    
    # Create evaluation table
    for eval_data in st.session_state.evaluations:
        with st.container():
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
            
            st.divider()
    
    # Bottom submit button (right side with better alignment)
    if st.session_state.human_feedback:
        thumbs_down_items = [id for id, feedback in st.session_state.human_feedback.items() 
                           if feedback == False]
        missing_ratings = [id for id in thumbs_down_items 
                         if id not in st.session_state.annotator_ratings]
        
        can_submit = len(missing_ratings) == 0
        
        # Create a clean submit section at the bottom
        st.markdown("---")
        st.markdown("""
        <div class="submit-button-section">
            <h4 style="margin-bottom: 1rem; color: #667eea;">Complete Your Evaluation</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        with col4:
            if not can_submit:
                st.error(f"⚠️ Please provide ratings for {len(missing_ratings)} thumbs down items")
            
            # Show validation summary
            total_feedback = len(st.session_state.human_feedback)
            st.info(f"✅ Completed: {total_feedback}/5 evaluations")
            
            if st.button("🎉 Submit All Responses", disabled=not can_submit, key="submit_btn_bottom",
                        help="Final submission of all feedback and ratings"):
                if can_submit:
                    calculate_analysis()
                    show_celebration()
                    st.session_state.current_page = 'thank_you'
                    st.rerun()

# Celebration animation
def show_celebration():
    # Create a brief fireworks effect using Streamlit's built-in features
    if 'celebration_shown' not in st.session_state:
        st.session_state.celebration_shown = True
        
        # Show balloons for 3 seconds
        st.balloons()
        
        # Brief message
        message_placeholder = st.empty()
        for i in range(3):
            message_placeholder.success(f"🎉 Celebration! Thank you for your evaluation! 🎉")
            time.sleep(1)
        message_placeholder.empty()  # Clear the message

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
    <div style="text-align: center; padding: 4rem 2rem;">
        <div style="background: #f0f9ff; padding: 2rem; border-radius: 15px; 
                    border: 2px solid #0ea5e9; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">✅</div>
            <h1 style="color: #0369a1; margin-bottom: 1rem;">Thank you for your participation!</h1>
            <p style="font-size: 1.2rem; color: #075985;">
                Your responses have been recorded successfully.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Clean button section
    st.markdown("""
    <div class="submit-button-section">
        <h4 style="margin-bottom: 1rem; color: #667eea;">What's Next?</h4>
        <p style="margin-bottom: 1rem; color: #6c757d;">View your analysis or start a new evaluation</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col4:
        if st.button("📊 View Analysis", key="view_analysis",
                    help="See detailed analysis of your feedback"):
            st.session_state.current_page = 'analysis'
            st.rerun()
        
        if st.button("🔄 Start New Evaluation", key="new_evaluation",
                    help="Begin a fresh evaluation session"):
            for key in ['evaluations', 'human_feedback', 'annotator_ratings', 
                       'analysis_results', 'evaluation_complete', 'celebration_shown']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_page = 'main'
            st.rerun()

# Analysis dashboard
def render_analysis_dashboard():
    st.markdown("# 📊 Analysis Results")
    st.markdown("### Human validation feedback analysis")
    
    if st.button("🔄 Start New Evaluation", key="new_eval_analysis"):
        for key in ['evaluations', 'human_feedback', 'annotator_ratings', 
                   'analysis_results', 'evaluation_complete', 'celebration_shown']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.current_page = 'main'
        st.rerun()
    
    results = st.session_state.analysis_results
    
    # Executive Summary
    st.markdown("## 📋 Executive Summary")
    
    with st.container():
        st.info(f"""
        **Assessment Overview:**
        We conducted an AI and Human Evaluator assessment with a **{results['agreement_rate']}% agreement rate** 
        and **{results['disagreement_rate']}% evaluation gap**.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"""
            **Background Removal Recommendations:**
            {'Maintain current algorithms, focus on edge cases' if results['agreement_rate'] >= 70 
             else 'Improve edge detection and segmentation techniques'}
            """)
        
        with col2:
            st.info(f"""
            **AI Evaluation Improvements:**
            {'Fine-tune quality thresholds, ready for production' if results['agreement_rate'] >= 70 
             else 'Recalibrate scoring weights and evaluation criteria'}
            """)
    
    # Metrics Dashboard
    st.markdown("## 📈 Validation Summary")
    
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
    st.markdown("## 📊 Analysis Charts")
    
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
            fig_bar = px.bar(
                rating_counts,
                x='rating',
                y='count',
                color='rating',
                title="AI Rating Distribution",
                labels={'rating': 'AI Rating', 'count': 'Number of Images'},
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No evaluation data available for bar chart")
    
    # Detailed Analysis
    if results['disagreement_count'] > 0:
        st.markdown("## 🔍 Disagreement Analysis")
        
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

# Sidebar
def render_sidebar():
    with st.sidebar:
        st.markdown("### 📋 About")
        st.markdown("""
        This application simulates an AI evaluation validation workflow for background removal quality assessment.
        
        **Process:**
        1. AI evaluates image pairs
        2. Humans validate AI ratings
        3. Analysis provides insights
        
        **Rating Scale:**
        - 1: Not Viable
        - 2: Partially Viable  
        - 3: Moderately Functional
        - 4: Near Production Ready
        - 5: Production Ready
        """)
        
        # Only show back button if not on main page
        if st.session_state.get('current_page', 'main') != 'main':
            if st.button("🏠 Back to Main", key="home_btn"):
                st.session_state.current_page = 'main'
                st.rerun()

# Main application logic
def main():
    # Initialize session state FIRST before anything else
    initialize_session_state()
    
    # Now render the header and rest of the app
    render_header()
    
    # Navigation logic
    if st.session_state.current_page == 'main':
        if not st.session_state.evaluation_complete:
            render_evaluation_preview()
            
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            with col4:
                if st.button("🧠 Start AI Evaluation (5 demo pairs)", key="start_eval",
                            help="Begin the automated evaluation process"):
                    simulate_ai_evaluation()
        else:
            render_validation_interface()
    
    elif st.session_state.current_page == 'thank_you':
        render_thank_you_page()
    
    elif st.session_state.current_page == 'analysis':
        render_analysis_dashboard()
    
    # Render sidebar
    render_sidebar()


if __name__ == "__main__":
    main()
