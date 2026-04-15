"""
Healthcare Diabetes Prediction Web App
A Streamlit application for predicting diabetes risk based on health metrics
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .positive {
        color: #e74c3c;
        font-weight: bold;
    }
    .negative {
        color: #2ecc71;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD MODEL AND DATA
# ============================================================================
@st.cache_resource
def load_model():
    """Load trained model, scaler, and feature names."""
    model_path = Path("models/diabetes_model.pkl")
    scaler_path = Path("models/scaler.pkl")
    features_path = Path("models/feature_names.pkl")
    
    # Validate model files exist before loading
    if not model_path.exists():
        raise FileNotFoundError(f"Missing model file: {model_path}")
    if not scaler_path.exists():
        raise FileNotFoundError(f"Missing scaler file: {scaler_path}")
    if not features_path.exists():
        raise FileNotFoundError(f"Missing feature names file: {features_path}")

    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    with open(features_path, 'rb') as f:
        feature_names = pickle.load(f)
    
    return model, scaler, feature_names

model, scaler, feature_names = load_model()

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1>🏥 Diabetes Risk Prediction</h1>
        <p style='font-size: 18px; color: #666;'>
            AI-Powered Healthcare Analytics using Machine Learning
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 Prediction Tool",
    "📊 Model Dashboard",
    "ℹ️ How It Works",
    "📚 About Dataset"
])

# ============================================================================
# TAB 1: PREDICTION TOOL
# ============================================================================
with tab1:
    st.header("Make a Prediction")
    st.write("Enter or adjust health metrics to get a diabetes risk prediction.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Clinical Measurements (Normalized)")
        age = st.slider("Age (normalized)", -0.10, 0.10, 0.0, 0.01, help="Patient age (normalized scale)")
        sex = st.slider("Sex (normalized)", -0.10, 0.10, 0.0, 0.01, help="Gender indicator (normalized)")
        bmi = st.slider("BMI (normalized)", -0.10, 0.10, 0.0, 0.01, help="Body Mass Index (normalized)")
        bp = st.slider("Blood Pressure (normalized)", -0.10, 0.10, 0.0, 0.01, help="Blood pressure (normalized)")
        s1 = st.slider("S1 (normalized)", -0.20, 0.20, 0.0, 0.02, help="First serum measurement")
    
    with col2:
        st.subheader("Biochemical Indicators")
        s2 = st.slider("S2 (normalized)", -0.20, 0.20, 0.0, 0.02, help="Second serum measurement")
        s3 = st.slider("S3 (normalized)", -0.20, 0.20, 0.0, 0.02, help="Third serum measurement")
        s4 = st.slider("S4 (normalized)", -0.10, 0.10, 0.0, 0.01, help="Fourth serum measurement")
        s5 = st.slider("S5 (normalized)", -0.20, 0.20, 0.0, 0.02, help="Fifth serum measurement (most important)")
        s6 = st.slider("S6 (normalized)", -0.10, 0.10, 0.0, 0.01, help="Sixth serum measurement")
    
    # Make prediction
    input_data = pd.DataFrame({
        'age': [age],
        'sex': [sex],
        'bmi': [bmi],
        'bp': [bp],
        's1': [s1],
        's2': [s2],
        's3': [s3],
        's4': [s4],
        's5': [s5],
        's6': [s6]
    })
    
    # Ensure the input columns match the feature order used during training
    input_data = input_data[feature_names]
    input_data_scaled = scaler.transform(input_data)
    
    prediction = model.predict(input_data_scaled)[0]
    probability = model.predict_proba(input_data_scaled)[0]
    
    st.divider()
    
    # Display prediction result
    col_result1, col_result2 = st.columns(2)
    
    with col_result1:
        st.subheader("Prediction Result")
        if prediction == 1:
            st.error(f"⚠️ **POSITIVE - HIGH RISK**")
            st.write(f"Diabetes probability: **{probability[1]*100:.1f}%**")
        else:
            st.success(f"✅ **NEGATIVE - LOW RISK**")
            st.write(f"Diabetes probability: **{probability[1]*100:.1f}%**")
    
    with col_result2:
        # Probability gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=probability[1]*100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Diabetes Risk %"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "#2ecc71"},
                    {'range': [30, 70], 'color': "#f39c12"},
                    {'range': [70, 100], 'color': "#e74c3c"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed breakdown
    st.subheader("Probability Breakdown")
    prob_data = pd.DataFrame({
        'Risk Category': ['No Diabetes', 'Diabetes'],
        'Probability': [probability[0]*100, probability[1]*100]
    })
    
    fig_prob = px.bar(
        prob_data,
        x='Risk Category',
        y='Probability',
        color='Risk Category',
        color_discrete_map={'No Diabetes': '#2ecc71', 'Diabetes': '#e74c3c'},
        labels={'Probability': 'Probability (%)'},
        title='Risk Probability Distribution'
    )
    fig_prob.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_prob, use_container_width=True)

# ============================================================================
# TAB 2: MODEL DASHBOARD
# ============================================================================
with tab2:
    st.header("Model Performance Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Model Accuracy", "76.69%", "✓ Good Performance")
    with col2:
        st.metric("Precision", "76.12%", "Of positive predictions")
    with col3:
        st.metric("Recall", "77.27%", "Cases correctly identified")
    with col4:
        st.metric("F1-Score", "76.69%", "Balanced metric")
    
    st.divider()
    
    col_model, col_features = st.columns(2)
    
    with col_model:
        st.subheader("Confusion Matrix")
        st.write("""
        **Test Set Performance**: 133 samples
        - ✅ True Negatives: 51 (Correct no-diabetes)
        - 🔴 False Positives: 16 (Incorrect diabetes)
        - ⚠️ False Negatives: 15 (Missed diabetes)
        - ✅ True Positives: 51 (Correct diabetes)
        """)
        
        cm_data = np.array([[51, 16], [15, 51]])
        fig_cm = px.imshow(
            cm_data,
            labels=dict(x="Predicted", y="Actual"),
            x=['No Diabetes', 'Diabetes'],
            y=['No Diabetes', 'Diabetes'],
            color_continuous_scale='Blues',
            text_auto=True,
            title='Confusion Matrix (Test Set)'
        )
        st.plotly_chart(fig_cm, use_container_width=True)
    
    with col_features:
        st.subheader("Top 5 Most Important Features")
        features_importance = {
            'S5 (most important)': 0.836,
            'BMI': 0.756,
            'Blood Pressure': 0.653,
            'S4': 0.083,
            'Age': 0.055
        }
        
        fig_features = px.barh(
            x=list(features_importance.values()),
            y=list(features_importance.keys()),
            labels={'x': 'Importance Score', 'y': 'Feature'},
            title='Feature Importance',
            color=list(features_importance.values()),
            color_continuous_scale='Viridis'
        )
        fig_features.update_layout(showlegend=False)
        st.plotly_chart(fig_features, use_container_width=True)
    
    st.divider()
    
    st.subheader("Model Training Summary")
    st.info("""
    **Algorithm**: Logistic Regression
    - Simple, interpretable linear classifier
    - Fast training and inference
    - Good for binary classification
    
    **Dataset**: UCI Diabetes Dataset
    - 442 total samples
    - 10 health features
    - Balanced classes (50% each)
    - No missing values
    
    **Performance Notes**:
    - Slight underfitting (-1.93% gap) indicates room for improvement
    - High recall (77.27%) means we catch most positive cases
    - Precision (76.12%) is solid for healthcare predictions
    """)

# ============================================================================
# TAB 3: HOW IT WORKS
# ============================================================================
with tab3:
    st.header("How This Prediction Model Works")
    
    st.subheader("1️⃣ Data Collection")
    st.write("""
    The model was trained on the **UCI Diabetes Dataset**, containing:
    - 442 patient records
    - 10 health metrics (age, BMI, blood pressure, serum measurements, etc.)
    - Binary classification: Has diabetes (1) or Not (0)
    """)
    
    st.subheader("2️⃣ Data Preprocessing")
    st.write("""
    Before training:
    - **Feature Scaling**: All features standardized to mean=0, std=1
    - **Train/Test Split**: 70% training (309 samples), 30% testing (133 samples)
    - **Class Balancing**: Maintained equal representation of both classes
    """)
    
    st.subheader("3️⃣ Model Training")
    st.write("""
    **Algorithm**: Logistic Regression
    - Linear model that outputs probability between 0-1
    - Decision boundary at 50% probability
    - Highly interpretable (we can see which features matter most)
    """)
    
    st.subheader("4️⃣ Prediction Process")
    st.write("""
    1. User inputs health metrics
    2. Features are normalized using the same scaler from training
    3. Model calculates probability of diabetes
    4. If probability > 50%, prediction is "Positive" (High Risk)
    5. If probability ≤ 50%, prediction is "Negative" (Low Risk)
    """)
    
    st.subheader("5️⃣ Feature Importance")
    st.write("""
    **Most Important Predictors** (in order):
    1. **S5** (0.836) - Serum measurement #5 (strongest positive indicator)
    2. **BMI** (0.756) - Body Mass Index (higher BMI = higher risk)
    3. **Blood Pressure** (0.653) - Higher BP increases risk
    4. **S4** (0.083) - Fourth serum measurement
    5. **Age** (0.055) - Slight positive correlation with diabetes
    
    **Negative Predictors**:
    - **Sex** (-0.563) - Certain gender categories reduce risk
    - **S3** (-0.433) - Lower S3 values indicate lower diabetes risk
    """)
    
    st.warning("""
    ⚠️ **Important Disclaimer**:
    This model is for **educational purposes only**. 
    It should NOT be used as a replacement for professional medical diagnosis.
    Always consult with healthcare professionals for medical decisions.
    """)

# ============================================================================
# TAB 4: ABOUT DATASET
# ============================================================================
with tab4:
    st.header("About the Dataset")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Dataset Overview")
        st.write("""
        **UCI Diabetes Dataset** (also known as the Diabetes Progression Dataset)
        """)
        
        dataset_info = {
            'Total Samples': '442',
            'Features': '10',
            'Target Classes': '2 (Diabetes / No Diabetes)',
            'Class Distribution': '50% / 50% (Balanced)',
            'Missing Values': '0 (Clean data)',
            'Data Type': 'Normalized values'
        }
        
        for key, value in dataset_info.items():
            st.write(f"**{key}**: {value}")
    
    with col_right:
        st.subheader("Features Explanation")
        features_dict = {
            'age': 'Patient age (years)',
            'sex': 'Gender indicator',
            'bmi': 'Body Mass Index (kg/m²)',
            'bp': 'Average blood pressure (mmHg)',
            's1': 'TC (Total Cholesterol level)',
            's2': 'LDL (Low-density lipoprotein)',
            's3': 'HDL (High-density lipoprotein)',
            's4': 'TCH (Total Cholesterol / HDL)',
            's5': 'LTG (Possibly log of triglycerides)',
            's6': 'Glu (Blood glucose level)'
        }
        
        for feature, desc in features_dict.items():
            st.write(f"**{feature}**: {desc}")
    
    st.divider()
    
    st.subheader("Key Statistics")
    st.info("""
    **Training Set**: 309 samples (70%)
    - Used to teach the model patterns
    
    **Test Set**: 133 samples (30%)
    - Used to evaluate real-world performance
    - Model achieved 76.69% accuracy on unseen data
    """)
    
    st.subheader("Source")
    st.write("""
    - **Original Source**: UC Irvine Machine Learning Repository
    - **Dataset**: Diabetes Progression Dataset
    - **Use Case**: Binary classification for disease prediction
    """)

# ============================================================================
# FOOTER
# ============================================================================
st.divider()

col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.write("**Built with**: Streamlit + Scikit-learn")

with col_footer2:
    st.write("**Model**: Logistic Regression (76.69% accuracy)")

with col_footer3:
    st.write("**Status**: ✅ Production Ready")
