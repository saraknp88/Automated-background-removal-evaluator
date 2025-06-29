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
    }
    
    .feedback-button {
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'evaluations' not in st.session_state:
        st.session_state.evaluations = []
    if 'human_feedback' not in st.session_state:
        st.session_state.human_feedback = {}
    if 'annotator_ratings' not in st.session_state:
        st.session_state.annotator_ratings = {}
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'main'
    if 'evaluation_complete' not in st.session_state:
        st.session_state.evaluation_complete = False

# Demo data
def get_demo_data():
    return [
        {
            'id': 1, 
            'original': 'florist-original.jpg', 
            'processed': 'florist-processed.jpg', 
            'rating': 4, 
            'quality': 'Near Production Ready',
            'description': 'Portrait with natural background'
        },
        {
            'id': 2, 
            'original': 'businesswoman-original.jpg', 
            'processed': 'businesswoman-processed.jpg', 
            'rating': 3, 
            'quality': 'Moderately Functional',
            'description': 'Professional headshot'
        },
        {
            'id': 3, 
            'original': 'iphone-original.jpg', 
            'processed': 'iphone-processed.jpg', 
            'rating': 4, 
            'quality': 'Near Production Ready',
            'description': 'Product photography'
        },
        {
            'id': 4, 
            'original': 'steak-meal.jpg', 
            'processed': 'steak-meal-processed.jpg', 
            'rating': 5, 
            'quality': 'Production Ready',
            'description': 'Food photography'
        },
        {
            'id': 5, 
            'original': 'bowl-splash.jpg', 
            'processed': 'bowl-splash-processed.jpg', 
            'rating': 2, 
            'quality': 'Partially Viable',
            'description': 'Action shot with water'
        }
    ]

# Quality colors mapping
def get_quality_color(rating):
    colors = {1: '#dc2626', 2: '#ea580c', 3: '#ca8a04', 4: '#2563eb', 5: '#16a34a'}
    return colors.get(rating, '#6b7280')

# Create placeholder image
def create_placeholder_image(width=200, height=150, text="Demo Image"):
    img = Image.new('RGB', (width, height), color='lightgray')
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
                img = create_placeholder_image()
                st.image(img, caption=pair['original'], width=150)
            
            with col2:
                st.markdown("<div style='text-align: center; padding-top: 50px;'>→</div>", 
                          unsafe_allow_html=True)
            
            with col3:
                st.markdown("**Processed**")
                img = create_placeholder_image()
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
                       'analysis_results', 'evaluation_complete']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_page = 'main'
            st.rerun()
    
    # Create evaluation table
    for eval_data in st.session_state.evaluations:
        with st.container():
            st.markdown(f"""
            <div class="evaluation-card">
                <h4>Image Pair {eval_data['id']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1.5, 2, 2, 2])
            
            with col1:
                st.markdown("**Original**")
                img = create_placeholder_image(150, 120)
                st.image(img, width=120)
                st.caption(eval_data['original'])
            
            with col2:
                st.markdown("**Processed**")
                img = create_placeholder_image(150, 120)
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
    
    # Submit button
    if st.session_state.human_feedback:
        thumbs_down_items = [id for id, feedback in st.session_state.human_feedback.items() 
                           if feedback == False]
        missing_ratings = [id for id in thumbs_down_items 
                         if id not in st.session_state.annotator_ratings]
        
        can_submit = len(missing_ratings) == 0
        
        if not can_submit:
            st.error(f"⚠️ Please provide ratings for {len(missing_ratings)} thumbs down items")
        
        if st.button("🎉 Submit Responses", disabled=not can_submit, key="submit_btn"):
            if can_submit:
                calculate_analysis()
                show_celebration()
                st.session_state.current_page = 'thank_you'
                st.rerun()

# Celebration animation
def show_celebration():
    st.markdown("""
    <div class="celebration">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
        <h2>Fantastic!</h2>
        <p style="font-size: 1.2rem;">Thank you for your evaluation!</p>
        <div style="margin-top: 1rem;">
            <span style="font-size: 2rem;">⭐</span>
            <span style="font-size: 2rem;">⭐</span>
            <span style="font-size: 2rem;">⭐</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2)

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
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("📊 View Analysis", key="view_analysis"):
            st.session_state.current_page = 'analysis'
            st.rerun()
        
        if st.button("🔄 Start New Evaluation", key="new_evaluation"):
            for key in ['evaluations', 'human_feedback', 'annotator_ratings', 
                       'analysis_results', 'evaluation_complete']:
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
                   'analysis_results', 'evaluation_complete']:
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
        # Agreement pie chart
        fig_pie = px.pie(
            values=[results['agreement_count'], results['disagreement_count']],
            names=['Agreement', 'Disagreement'],
            colors=['#10b981', '#ef4444'],
            title="Human-AI Agreement Distribution"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Rating distribution
        evaluations_df = pd.DataFrame(st.session_state.evaluations)
        fig_bar = px.bar(
            evaluations_df.groupby('rating').size().reset_index(name='count'),
            x='rating',
            y='count',
            color='rating',
            title="AI Rating Distribution",
            labels={'rating': 'AI Rating', 'count': 'Number of Images'},
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
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

# Main application logic
def main():
    initialize_session_state()
    render_header()
    
    # Navigation logic
    if st.session_state.current_page == 'main':
        if not st.session_state.evaluation_complete:
            render_evaluation_preview()
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🧠 Start AI Evaluation (5 demo pairs)", key="start_eval"):
                    simulate_ai_evaluation()
        else:
            render_validation_interface()
    
    elif st.session_state.current_page == 'thank_you':
        render_thank_you_page()
    
    elif st.session_state.current_page == 'analysis':
        render_analysis_dashboard()

# Sidebar
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
    
    if st.session_state.current_page != 'main':
        if st.button("🏠 Back to Main", key="home_btn"):
            st.session_state.current_page = 'main'
            st.rerun()

if __name__ == "__main__":
    main()