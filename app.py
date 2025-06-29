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
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
        text-align: center;
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
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        text-align: center;
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
    
    .celebration {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 1rem;
        color: white;
        margin: 2rem 0;
    }
    
    .instructions-box {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0.5rem;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .instructions-title {
        font-size: 1.75rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 1rem;
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

# Demo data - updated with descriptions
DEMO_RESULTS = [
    {
        'id': 1, 
        'original': 'Before 0.jpg',
        'processed': 'After 0.png',
        'rating': 4, 
        'quality': 'Near Production Ready',
        'description': 'Business Attire'
    },
    {
        'id': 2, 
        'original': 'Before 01.jpg',
        'processed': 'After 01.png',
        'rating': 3, 
        'quality': 'Moderately Functional',
        'description': 'Professional Portrait'
    },
    {
        'id': 3, 
        'original': 'Before 02.jpg',
        'processed': 'After 02.png',
        'rating': 4, 
        'quality': 'Near Production Ready',
        'description': 'Casual Headshot'
    },
    {
        'id': 4, 
        'original': 'Before 03.jpg',
        'processed': 'After 03.png',
        'rating': 5, 
        'quality': 'Production Ready',
        'description': 'Studio Portrait'
    },
    {
        'id': 5, 
        'original': 'Before 04.jpg',
        'processed': 'After 04.png',
        'rating': 2, 
        'quality': 'Partially Viable',
        'description': 'Group Photo'
    }
]

# Auto-load demo data on first run
if not st.session_state.evaluations:
    st.session_state.evaluations = DEMO_RESULTS

def get_quality_color(rating: int) -> str:
    colors = {1: '#dc2626', 2: '#ea580c', 3: '#ca8a04', 4: '#2563eb', 5: '#16a34a'}
    return colors.get(rating, '#6b7280')

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
    
    # Show balloons after state change
    st.balloons()
    time.sleep(0.5)  # Brief delay
    st.rerun()



def start_new_evaluation():
    st.session_state.evaluations = DEMO_RESULTS
    st.session_state.human_feedback = {}
    st.session_state.annotator_ratings = {}
    st.session_state.analysis_results = None
    st.session_state.show_thank_you = False
    st.session_state.show_analysis = False
    st.session_state.current_image_index = 0
    st.rerun()

def next_image():
    if st.session_state.current_image_index < len(st.session_state.evaluations) - 1:
        st.session_state.current_image_index += 1
    st.rerun()

def previous_image():
    if st.session_state.current_image_index > 0:
        st.session_state.current_image_index -= 1
    st.rerun()

# Analysis Results Page
if st.session_state.show_analysis and st.session_state.analysis_results:
    # Header with consistent styling
    st.markdown('<h1 class="main-header">Human-AI Validation Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Performance evaluation dashboard</p>', unsafe_allow_html=True)
    
    results = st.session_state.analysis_results
    
    # Executive Summary
    col1, col2, col3 = st.columns([1, 3, 1]) 

    with col1:
      st.markdown("### Executive Summary")

    with col3:
      if st.button("🔄 Start New Evaluation", type="primary", use_container_width=True):
         start_new_evaluation()
         st.rerun()


    
   # st.markdown("### Executive Summary")

      # Action buttons
   # col1, col2, col3 = st.columns(3)
   # 
   # with col3:
     #   if st.button("🔄 Start New Evaluation", type="primary", use_container_width=True):
      #      start_new_evaluation()
       #     st.rerun()
    
    # Analyze disagreements for enhanced summary
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
    
    # Generate enhanced executive summary
    alignment = 'strong' if results['agreement_rate'] >= 80 else 'moderate'
    passes = results['agreement_rate'] >= 80
    
    if passes and results['agreement_rate'] >= 90:
        summary = f"The AI evaluation system demonstrates exceptional performance with a {results['agreement_rate']}% agreement rate. Human validators strongly align with AI assessments, indicating the automated system is ready for enterprise deployment with minimal human oversight required."
    elif passes:
        summary = f"The AI evaluation system shows strong performance with a {results['agreement_rate']}% agreement rate. The system demonstrates reliable quality assessment capabilities suitable for production environments with periodic human validation."
    elif results['agreement_rate'] >= 60:
        summary = f"The AI evaluation system delivers moderate performance with a {results['agreement_rate']}% agreement rate. While showing promise, additional calibration and refinement are recommended before full deployment to achieve enterprise-grade consistency."
    else:
        summary = f"The AI evaluation system shows significant room for improvement with a {results['agreement_rate']}% agreement rate. Substantial recalibration of evaluation criteria and algorithm refinement are necessary before production deployment."
    
    # Add threshold context
    threshold_text = f" The system meets the production readiness threshold with scores exceeding the required 80% standard." if passes else f" The system falls below the production readiness threshold, which requires an agreement rate of at least 80%."
    
    summary += threshold_text + additional_text + " Human feedback will be integrated into our reinforcement learning pipeline to continuously improve automated evaluation accuracy."
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #e5e7eb; margin-bottom: 1.5rem;">
        {summary}
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics using Streamlit metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Images Evaluated", 
            value=len(st.session_state.evaluations)
        )
    
    with col2:
        st.metric(
            label="Agreement Rate",
            value=f"{results['agreement_rate']}%",
            delta=f"{results['agreement_count']} approvals"
        )
    
    with col3:
        status = "✅ Meets Standard" if passes else "❌ Below Standard"
        st.metric(
            label="Quality Status",
            value=status,
            delta=f"{results['disagreement_count']} rejections"
        )
    
    # Recommendations based on results
    st.markdown("### Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 0.25rem; margin: 0.5rem; border-left: 4px solid #22c55e;">
            <strong>Background Removal Algorithm:</strong><br>
        """, unsafe_allow_html=True)
        
        if results['agreement_rate'] >= 80:
            st.markdown("Maintain current algorithms, focus on edge cases and specific scenarios where disagreements occurred.")
        else:
            st.markdown("Improve edge detection and segmentation techniques based on human feedback patterns.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 0.25rem; margin: 0.5rem; border-left: 4px solid #a855f7;">
            <strong>AI Evaluation System:</strong><br>
        """, unsafe_allow_html=True)
        
        if results['agreement_rate'] >= 80:
            st.markdown("Fine-tune quality thresholds, system ready for production with periodic human validation.")
        else:
            st.markdown("Recalibrate scoring weights and evaluation criteria using collected human feedback data.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Thank You Page
elif st.session_state.show_thank_you:
   # Custom celebration banner
   st.markdown("""
   <div style="
       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
       border-radius: 1rem;
       padding: 3rem 2rem;
       text-align: center;
       color: white;
       margin: 2rem 0;
       box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
   ">
       <h1 style="margin: 0; font-size: 2.5rem; font-weight: bold;">
           🎉 Evaluation Complete! 🎉
       </h1>
       <h2 style="margin: 1rem 0 0.5rem 0; font-size: 1.5rem; font-weight: normal;">
           Thank you for your participation!
       </h2>
       <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
           Your responses have been recorded successfully.
       </p>
   </div>
   """, unsafe_allow_html=True)
   
   # Action buttons
   col1, col2 = st.columns(2)
   
   with col1:
       if st.button("📊 View Analysis", type="primary", use_container_width=True):
           st.session_state.show_thank_you = False
           st.session_state.show_analysis = True
           st.rerun()
   
   with col2:
       if st.button("🔄 Start New Evaluation", use_container_width=True):
           start_new_evaluation()

# Main Application - Single Image View
else:
    # Header
    st.markdown('<h1 class="instructions-title">Sara\'s AI Judge for Background Removal</h1>', unsafe_allow_html=True)
    
    # Instructions
    st.markdown("""
    <div class="instructions-box">
        <strong>Hello! I'm Sara's AI Judge for Background Removal. I use the evaluation rubric below to assess the quality of background-removed images. As you review the automated ratings, please apply the same criteria.</strong><br><br>
        <strong>💡 Tip:</strong> Click the 🔍 button next to each image to view it in full size for detailed inspection.<br><br>
        <strong>1 - Unusable:</strong> Major issues with structure, style, identity, or overall quality. Not suitable for use.<br>
        <strong>2 - Partially Viable:</strong> Useful as a concept or direction, but not for final use. Significant fixes required.<br>
        <strong>3 - Moderately Functional:</strong> Largely usable, with moderate fixes needed. More efficient than starting from scratch.<br>
        <strong>4 - Near Production Ready:</strong> Only minor adjustments needed, such as light cleanup or retouching.<br>
        <strong>5 - Production Ready:</strong> No further edits needed. Ready for immediate use.
    </div>
    """, unsafe_allow_html=True)
    
    # Get current image data
    current_eval = st.session_state.evaluations[st.session_state.current_image_index]
    eval_id = current_eval['id']
    total_images = len(st.session_state.evaluations)
    current_position = st.session_state.current_image_index + 1
    validated_count = len(st.session_state.human_feedback)
    
    # Top navigation bar
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.markdown(f"<h4 style='text-align: center; margin: 0;'>Image {current_position} of {total_images}: {current_eval['description']}</h4>", unsafe_allow_html=True)
    with col2:
        st.write("") 
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            start_new_evaluation()

    
    st.markdown("---")
    
    # Single image evaluation interface
    # Single image evaluation interface
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1.5, 2, 2, 2])
    
    with col1:
        st.markdown("**Original**")
        if st.button(f"🔍", key=f"orig_{eval_id}", help="Click to magnify image"):
            st.session_state[f'show_modal_{eval_id}_orig'] = True
        
        try:
            st.image(current_eval['original'], width=120)
        except:
            st.markdown(f"""
            <div style="width: 120px; height: 80px; background: #f3f4f6; border: 2px dashed #d1d5db; 
                 display: flex; align-items: center; justify-content: center; border-radius: 8px;">
                <div style="text-align: center; color: #6b7280;">
                    <div>🖼️</div>
                    <small>Original {eval_id}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Processed**")
        if st.button(f"🔍", key=f"proc_{eval_id}", help="Click to magnify image"):
            st.session_state[f'show_modal_{eval_id}_proc'] = True
        
        try:
            st.image(current_eval['processed'], width=120)
        except:
            st.markdown(f"""
            <div style="width: 120px; height: 80px; background: #f3f4f6; border: 2px dashed #d1d5db; 
                 display: flex; align-items: center; justify-content: center; border-radius: 8px;">
                <div style="text-align: center; color: #6b7280;">
                    <div>🖼️</div>
                    <small>Processed {eval_id}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("**AI Rating**")
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.125rem; font-weight: 600;">{current_eval['rating']}/5</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("**Quality Level**")
        st.markdown(f"<span style='font-weight: 500; color: #374151;'>{current_eval['quality']}</span>", unsafe_allow_html=True)
    
    with col5:
        st.markdown('<span style="color: #3b82f6; font-weight: bold;">Annotator Feedback</span>', unsafe_allow_html=True)
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
        st.markdown('<span style="color: #3b82f6; font-weight: bold;">Annotator Rating</span>', unsafe_allow_html=True)
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
        
    # Show modals if triggered
    if st.session_state.get(f'show_modal_{eval_id}_orig', False):
        with st.container():
            st.markdown("### 🔍 Magnified View - Original Image")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                try:
                    st.image(current_eval['original'], use_container_width=True, caption=f"Original Image {eval_id}")
                except:
                    st.error(f"Could not load image: {current_eval['original']}")
                
                if st.button("Close", key=f"close_orig_{eval_id}"):
                    st.session_state[f'show_modal_{eval_id}_orig'] = False
                    st.rerun()
    
    if st.session_state.get(f'show_modal_{eval_id}_proc', False):
        with st.container():
            st.markdown("### 🔍 Magnified View - Processed Image")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                try:
                    st.image(current_eval['processed'], use_container_width=True, caption=f"Processed Image {eval_id} - {current_eval['quality']}")
                except:
                    st.error(f"Could not load image: {current_eval['processed']}")
                
                if st.button("Close", key=f"close_proc_{eval_id}"):
                    st.session_state[f'show_modal_{eval_id}_proc'] = False
                    st.rerun()
    
    # Bottom navigation:Check if current image has feedback and required rating
current_has_feedback = eval_id in st.session_state.human_feedback
current_feedback_is_negative = st.session_state.human_feedback.get(eval_id) is False
current_has_rating = eval_id in st.session_state.annotator_ratings

# Determine if user can proceed
can_proceed = (current_has_feedback and 
              (not current_feedback_is_negative or current_has_rating))

# Create navigation with progress bar in center
col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

with col1:
    if st.button("← Previous", disabled=st.session_state.current_image_index == 0, use_container_width=True):
        previous_image()

with col2:
    st.write("")  # Empty space

with col3:
     st.write("")  # Empty space

with col4:
    st.write("")  # Empty space

with col5:
    if current_position < total_images:
        # Disable Next button if no feedback provided OR thumbs down without rating
        next_help = ""
        if not current_has_feedback:
            next_help = "Please provide feedback (👍 or 👎) before proceeding"
        elif current_feedback_is_negative and not current_has_rating:
            next_help = "Please provide your rating before proceeding"
        else:
            next_help = "Go to next image"
        
        if st.button("Next →", disabled=not can_proceed, help=next_help, use_container_width=True):
            next_image()
    else:
        # Submit button logic - check all images have required feedback/ratings
        all_images_complete = True
        for img_eval_id in [e['id'] for e in st.session_state.evaluations]:
            if img_eval_id not in st.session_state.human_feedback:
                all_images_complete = False
                break
            if (st.session_state.human_feedback[img_eval_id] is False and 
                img_eval_id not in st.session_state.annotator_ratings):
                all_images_complete = False
                break
        
        submit_help = "Complete all required ratings before submitting" if not all_images_complete else "Submit all responses"
        
        if st.button("Submit", type="primary", disabled=not all_images_complete, help=submit_help, use_container_width=True):
            submit_responses()

# Show appropriate feedback message
if not current_has_feedback:
    st.info("👆 Please provide your feedback (👍 agree or 👎 disagree) to proceed to the next image.")
elif current_feedback_is_negative and not current_has_rating:
    st.warning("👆 Since you disagreed with the AI rating, please provide your own rating before proceeding.")
