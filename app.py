import streamlit as st
import time
from typing import Dict, Any

# Page config
st.set_page_config(
    page_title="Sara's AI Evaluation Validator",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    
    .brain-icon {
        font-size: 2.5rem;
        color: #9333ea;
        margin-right: 1rem;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #111827;
        margin: 0;
    }
    
    .subtitle {
        font-size: 1.125rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
    
    .evaluation-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .quality-badge-1 { background-color: #dc2626; color: white; }
    .quality-badge-2 { background-color: #ea580c; color: white; }
    .quality-badge-3 { background-color: #ca8a04; color: white; }
    .quality-badge-4 { background-color: #2563eb; color: white; }
    .quality-badge-5 { background-color: #16a34a; color: white; }
    
    .quality-badge {
        display: inline-block;
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        text-align: center;
        line-height: 2rem;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    
    .analysis-summary {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .metric-card {
        text-align: center;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem;
    }
    
    .metric-card-blue {
        background-color: #eff6ff;
        color: #1e40af;
    }
    
    .metric-card-green {
        background-color: #f0fdf4;
        color: #166534;
    }
    
    .metric-card-red {
        background-color: #fef2f2;
        color: #991b1b;
    }
    
    .recommendation-card {
        background: white;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 0.5rem;
    }
    
    .recommendation-card-green {
        border-left: 4px solid #22c55e;
    }
    
    .recommendation-card-purple {
        border-left: 4px solid #a855f7;
    }
    
    .thank-you-container {
        text-align: center;
        padding: 4rem 0;
    }
    
    .success-icon {
        width: 5rem;
        height: 5rem;
        background-color: #dcfce7;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 2.5rem;
        color: #16a34a;
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
if 'is_evaluating' not in st.session_state:
    st.session_state.is_evaluating = False

# Demo data
DEMO_RESULTS = [
    {
        'id': 1, 
        'original': 'Before 0.jpg',
        'processed': 'After 0.png',
        'rating': 4, 
        'quality': 'Near Production Ready'
    },
    {
        'id': 2, 
        'original': 'Before 01.jpg',
        'processed': 'After 01.png',
        'rating': 3, 
        'quality': 'Moderately Functional'
    },
    {
        'id': 3, 
        'original': 'Before 02.jpg',
        'processed': 'After 02.png',
        'rating': 4, 
        'quality': 'Near Production Ready'
    },
    {
        'id': 4, 
        'original': 'Before 03.jpg',
        'processed': 'After 03.png',
        'rating': 5, 
        'quality': 'Production Ready'
    },
    {
        'id': 5, 
        'original': 'Before 04.jpg',
        'processed': 'After 04.png',
        'rating': 2, 
        'quality': 'Partially Viable'
    }
]

def get_quality_color(rating: int) -> str:
    colors = {1: '#dc2626', 2: '#ea580c', 3: '#ca8a04', 4: '#2563eb', 5: '#16a34a'}
    return colors.get(rating, '#6b7280')

def handle_evaluate():
    st.session_state.is_evaluating = True
    time.sleep(2)  # Simulate processing
    st.session_state.evaluations = DEMO_RESULTS
    st.session_state.is_evaluating = False
    st.rerun()

def submit_responses():
    feedback_count = len(st.session_state.human_feedback)
    agreement_count = sum(1 for f in st.session_state.human_feedback.values() if f)
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
    st.session_state.show_thank_you = True
    st.rerun()

def start_new_evaluation():
    st.session_state.evaluations = []
    st.session_state.human_feedback = {}
    st.session_state.annotator_ratings = {}
    st.session_state.analysis_results = None
    st.session_state.show_thank_you = False
    st.session_state.show_analysis = False
    st.session_state.is_evaluating = False
    st.rerun()

# Analysis Results Page
if st.session_state.show_analysis and st.session_state.analysis_results:
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown("# Analysis Results")
        st.markdown("### Human validation feedback analysis")
    
    with col2:
        if st.button("🔄 Start New Evaluation", type="primary"):
            start_new_evaluation()
    
    # Executive Summary
    st.markdown('<div class="analysis-summary">', unsafe_allow_html=True)
    st.markdown("## Executive Summary")
    
    results = st.session_state.analysis_results
    st.markdown(f"""
    We conducted an AI and Human Evaluator assessment with an **{results['agreement_rate']}% agreement rate** 
    and **{results['disagreement_rate']}% evaluation gap**.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="recommendation-card recommendation-card-green">', unsafe_allow_html=True)
        st.markdown("**Background Removal Recommendations:**")
        recommendation = ('Maintain current algorithms, focus on edge cases' 
                         if results['agreement_rate'] >= 70 
                         else 'Improve edge detection and segmentation techniques')
        st.markdown(f"<small>{recommendation}</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="recommendation-card recommendation-card-purple">', unsafe_allow_html=True)
        st.markdown("**AI Evaluation Improvements:**")
        improvement = ('Fine-tune quality thresholds, ready for production' 
                      if results['agreement_rate'] >= 70 
                      else 'Recalibrate scoring weights and evaluation criteria')
        st.markdown(f"<small>{improvement}</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quality Analysis
    alignment = 'strong' if results['agreement_rate'] >= 70 else 'moderate'
    
    # Analyze disagreements
    disagreements = [(eval_id, feedback) for eval_id, feedback in st.session_state.human_feedback.items() if not feedback]
    additional_text = ""
    
    if disagreements:
        higher_ratings = sum(1 for eval_id, _ in disagreements 
                           if st.session_state.annotator_ratings.get(eval_id, 0) > 
                           next(e['rating'] for e in st.session_state.evaluations if e['id'] == eval_id))
        lower_ratings = sum(1 for eval_id, _ in disagreements 
                          if st.session_state.annotator_ratings.get(eval_id, 0) < 
                          next(e['rating'] for e in st.session_state.evaluations if e['id'] == eval_id))
        
        if higher_ratings > lower_ratings:
            additional_text = " Human annotators tend to recommend higher quality ratings than the AI system, suggesting the automated evaluator may be too conservative."
        elif lower_ratings > higher_ratings:
            additional_text = " Human annotators tend to recommend lower quality ratings than the AI system, indicating the automated evaluator may be too lenient."
        else:
            additional_text = " Human annotator ratings show balanced distribution compared to AI evaluations."
    
    st.markdown(f"""
    **Quality Analysis:** AI evaluator shows {alignment} alignment with human experts.{additional_text} 
    Human feedback will be fed into our reinforcement learning process to improve automated evaluation performance.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Validation Summary Cards
    st.markdown("## Validation Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card metric-card-blue">', unsafe_allow_html=True)
        st.markdown("### Total Evaluations")
        st.markdown(f"# {len(st.session_state.evaluations)}")
        st.markdown("Image pairs evaluated")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card metric-card-green">', unsafe_allow_html=True)
        st.markdown("### Agreement Rate")
        st.markdown(f"# {results['agreement_rate']}%")
        st.markdown(f"{results['agreement_count']} human approvals")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card metric-card-red">', unsafe_allow_html=True)
        st.markdown("### Disagreement Rate")
        st.markdown(f"# {results['disagreement_rate']}%")
        st.markdown(f"{results['disagreement_count']} human rejections")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #6b7280; font-size: 0.875rem;">
    Analysis complete - {results['feedback_count']} evaluations processed with {results['agreement_rate']}% agreement rate
    </div>
    """, unsafe_allow_html=True)

# Thank You Page
elif st.session_state.show_thank_you:
    st.markdown('<div class="thank-you-container">', unsafe_allow_html=True)
    st.markdown('<div class="success-icon">✓</div>', unsafe_allow_html=True)
    st.markdown("# Thank you for your participation!")
    st.markdown("### Your responses have been recorded successfully.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📊 View Analysis", type="primary", use_container_width=True):
                st.session_state.show_thank_you = False
                st.session_state.show_analysis = True
                st.rerun()
        with col_b:
            if st.button("🔄 Start New Evaluation", use_container_width=True):
                start_new_evaluation()
    st.markdown('</div>', unsafe_allow_html=True)

# Main Application
else:
    # Header
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <span class="brain-icon">🧠</span>
            <h1 class="main-title">Sara's AI Evaluation Validator</h1>
        </div>
        <p class="subtitle">Validate AI background removal ratings with thumbs up/down feedback</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show demo results before evaluation
    if not st.session_state.evaluations and not st.session_state.is_evaluating:
        st.markdown("## Image Pairs to be Evaluated")
        
        for i, pair in enumerate(DEMO_RESULTS):
            st.markdown('<div class="evaluation-card">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns([2, 1, 2, 3])
            
            with col1:
                st.markdown("**Original**")
                st.image(pair['original'], width=200)
            
            with col2:
                st.markdown("<div style='text-align: center; padding-top: 50px; font-size: 2rem; color: #6b7280;'>→</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("**Processed**")
                st.image(pair['processed'], width=200)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Evaluate button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🧠 Start AI Evaluation (5 demo pairs)", type="primary", use_container_width=True):
                handle_evaluate()
    
    # Loading state
    if st.session_state.is_evaluating:
        st.markdown("""
        <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 0.5rem; padding: 2rem; text-align: center; margin: 1.5rem 0;">
            <div style="margin-bottom: 1rem;">⏳</div>
            <h3 style="color: #1d4ed8;">AI is analyzing image pairs...</h3>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
        st.session_state.evaluations = DEMO_RESULTS
        st.session_state.is_evaluating = False
        st.rerun()
    
    # Evaluation results
    if st.session_state.evaluations:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("## Validate AI Ratings")
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                start_new_evaluation()
        
        # Create evaluation table
        for eval_data in st.session_state.evaluations:
            eval_id = eval_data['id']
            
            st.markdown('<div class="evaluation-card">', unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1.5, 2, 2, 2])
            
            with col1:
                st.markdown("**Original**")
                st.image(eval_data['original'], width=120)
            
            with col2:
                st.markdown("**Processed**")
                st.image(eval_data['processed'], width=120)
            
            with col3:
                st.markdown("**AI Rating**")
                color = get_quality_color(eval_data['rating'])
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div class="quality-badge" style="background-color: {color};">{eval_data['rating']}</div>
                    <span style="font-size: 1.125rem; font-weight: 600;">{eval_data['rating']}/5</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("**Quality Level**")
                st.markdown(f"<span style='font-weight: 500; color: #374151;'>{eval_data['quality']}</span>", unsafe_allow_html=True)
            
            with col5:
                st.markdown("**Annotator Feedback**")
                col_up, col_down = st.columns(2)
                
                with col_up:
                    thumbs_up_pressed = st.session_state.human_feedback.get(eval_id) is True
                    if st.button("👍", key=f"up_{eval_id}", 
                               type="primary" if thumbs_up_pressed else "secondary",
                               help="Agree with AI rating"):
                        st.session_state.human_feedback[eval_id] = True
                        if eval_id in st.session_state.annotator_ratings:
                            del st.session_state.annotator_ratings[eval_id]
                        st.rerun()
                
                with col_down:
                    thumbs_down_pressed = st.session_state.human_feedback.get(eval_id) is False
                    if st.button("👎", key=f"down_{eval_id}",
                               type="primary" if thumbs_down_pressed else "secondary",
                               help="Disagree with AI rating"):
                        st.session_state.human_feedback[eval_id] = False
                        st.rerun()
            
            with col6:
                st.markdown("**Annotator Rating**")
                if st.session_state.human_feedback.get(eval_id) is False:
                    rating = st.selectbox(
                        "Rate*", 
                        options=[None, 1, 2, 3, 4, 5],
                        format_func=lambda x: "Rate*" if x is None else str(x),
                        key=f"rating_{eval_id}",
                        index=0 if eval_id not in st.session_state.annotator_ratings else st.session_state.annotator_ratings[eval_id]
                    )
                    if rating is not None:
                        st.session_state.annotator_ratings[eval_id] = rating
                elif st.session_state.human_feedback.get(eval_id) is True:
                    st.markdown("<span style='color: #059669; font-weight: 500;'>Agreed</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color: #6b7280;'>-</span>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        if st.session_state.human_feedback:
            thumbs_down_items = [eval_id for eval_id, feedback in st.session_state.human_feedback.items() if not feedback]
            missing_ratings = [eval_id for eval_id in thumbs_down_items if eval_id not in st.session_state.annotator_ratings]
            can_submit = len(missing_ratings) == 0
            
            if missing_ratings:
                st.error(f"Please provide annotator ratings for all thumbs down items ({len(missing_ratings)} missing)")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(
                    f"Submit Responses ({len(st.session_state.human_feedback)} validated)",
                    type="primary",
                    disabled=not can_submit,
                    use_container_width=True
                ):
                    submit_responses()
