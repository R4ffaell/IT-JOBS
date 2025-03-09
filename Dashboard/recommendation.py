import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from db import fetch_data
from datetime import datetime
import re

# 🎨 Custom Color Theme
COLOR_THEME = ["#1ABC9C", "#3498DB", "#9B59B6", "#E74C3C", "#F1C40F", "#2ECC71"]

# 🎨 Custom Styles
CSS_STYLES = """
<style>
    /* Fix unreadable text in dark mode */
    body {
        color: white !important;
    }
    .job-card {
        background: #1E1E1E;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(255,255,255,0.1);
        transition: transform 0.2s;
    }
    .job-card:hover {
        transform: translateY(-2px);
    }
    .match-score {
        color: #27AE60;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .skill-match {
        background: #2C3E50;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem;
        color: white;
    }
    /* Hide unwanted hover tooltips */
    div[data-testid="stTooltip"] {
        display: none !important;
    }
</style>
"""

# 🛠 Salary Parsing Function
def parse_salary(salary_range):
    """Extract minimum salary from the salary range string."""
    try:
        match = re.findall(r"\d+", salary_range.replace(",", ""))
        if match:
            return int(match[0]), int(match[-1]) if len(match) > 1 else int(match[0])
        return None, None
    except:
        return None, None

# 📊 Data Loading & Caching
@st.cache_data(ttl=3600)
def load_data():
    """Load and preprocess data with caching"""
    try:
        df = fetch_data()
        df = df.dropna(subset=['required_skills', 'salary_range'])
        df['salary_min'], df['salary_max'] = zip(*df['salary_range'].apply(parse_salary))
        return df
    except Exception as e:
        st.error(f"Data loading error: {e}")
        return pd.DataFrame()

@st.cache_resource
def get_vectorizer(df):
    """Cache TF-IDF vectorizer"""
    return TfidfVectorizer(stop_words='english').fit(df['required_skills'])

# 🔥 Recommendation Algorithm
def enhanced_recommendations(user_skills, df, vectorizer, weights):
    """Multi-factor job recommendation system"""
    skill_matrix = vectorizer.transform(df['required_skills'])
    user_vector = vectorizer.transform([user_skills])
    skill_scores = cosine_similarity(user_vector, skill_matrix).flatten()
    
    # Salary score normalization
    df['salary_score'] = (df['salary_min'] - df['salary_min'].min()) / \
                         (df['salary_min'].max() - df['salary_min'].min())

    # Combined score
    df['match_score'] = (weights['skills'] * skill_scores + 
                         weights['salary'] * df['salary_score'])
    
    return df.sort_values('match_score', ascending=False)

# 📌 Job Display Card
def display_job_card(job, user_skills):
    """Display an individual job recommendation"""
    with st.container():
        st.markdown(f"<div class='job-card'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{job['job_title']}**")
            st.caption(f"🏢 {job['company']} | 📍 {job['location']}")
            st.markdown(f"💷 Salary Range: {job['salary_range']}")
        with col2:
            st.markdown(f"<div class='match-score'>{job['match_score']*100:.1f}% Match</div>", 
                       unsafe_allow_html=True)
        
        with st.expander("🔍 Skills Analysis"):
            job_skills = {skill.strip().lower() for skill in job['required_skills'].split(',')}
            user_skills_set = {s.strip().lower() for s in user_skills.split(',')}

            matched = job_skills & user_skills_set
            missing = job_skills - user_skills_set

            st.subheader(f"✅ Matched Skills ({len(matched)})")
            for skill in matched:
                st.markdown(f"<div class='skill-match'>{skill.capitalize()}</div>", unsafe_allow_html=True)

            st.subheader(f"📚 Suggested Skills ({len(missing)})")
            for skill in missing:
                st.markdown(f"<div class='skill-match'>{skill.capitalize()}</div>", unsafe_allow_html=True)


        with st.expander("📄 Job Description"):
            st.write(job['job_description'])
        
        st.markdown("</div>", unsafe_allow_html=True)

# 🚀 Streamlit Page
def recommendation_page():
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    st.title("🎯 Smart Job Recommendations")
    
    # Load data with progress
    with st.spinner("Loading job market data..."):
        df = load_data()
    
    if df.empty:
        st.warning("No data available. Please check your data source.")
        return

    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Recommendation Settings")
        
        st.subheader("Priority Weights")
        skill_weight = st.slider("Skill Match Importance", 0.0, 1.0, 0.7)
        salary_weight = st.slider("Salary Importance", 0.0, 1.0, 0.3)
        weights = {'skills': skill_weight, 'salary': salary_weight}

        selected_location = st.selectbox(
            "📍 Preferred Location",
            ["All"] + sorted(df['location'].unique()))

        experience_levels = st.multiselect(
            "🎚️ Experience Levels",
            df['experience_level'].unique())

    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_skills = st.text_input(
            "🛠️ Enter your skills (comma separated)",
            placeholder="e.g., Python, Machine Learning, SQL")
        
        if st.button("🚀 Get Recommendations", use_container_width=True):
            if user_skills:
                with st.spinner("Analyzing 1000+ jobs..."):
                    start_time = datetime.now()
                    
                    filtered_df = df.copy()
                    if selected_location != "All":
                        filtered_df = filtered_df[filtered_df['location'] == selected_location]
                    if experience_levels:
                        filtered_df = filtered_df[filtered_df['experience_level'].isin(experience_levels)]

                    vectorizer = get_vectorizer(df)
                    recommendations = enhanced_recommendations(user_skills, filtered_df, vectorizer, weights)

                    st.subheader(f"🔍 Top {len(recommendations)} Matches")
                    for _, job in recommendations.head(10).iterrows():
                        display_job_card(job, user_skills)

                    st.success(f"Found {len(recommendations)} matches in {(datetime.now() - start_time).total_seconds():.1f}s")
            else:
                st.warning("Please enter your skills to get recommendations")

    with col2:
        st.subheader("📊 Recommendation Insights")
        if 'recommendations' in locals():
            fig = px.box(recommendations, y='salary_min', title="Salary Distribution")
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    recommendation_page()
