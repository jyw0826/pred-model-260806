import streamlit as st
import numpy as np

# ==================== Model Coefficients ====================
coef = {
    "Intercept": 8.620267683245652,
    "Age": -0.03271108411528607,
    "BMI": -0.02177943253334464,
    "DM": -0.5593604668117012,
    "Tumor_Number": -0.9385366410170538,
    "Max_Diameter": 0.06342314286653507,
    "PIVKA_II": -5.663632835945172e-06,
    "ALB": -0.02061076968052246,
    "ALT": 0.008502601242641858,
    "AST": -0.006801145576179819,
    "TBIL": -0.0221641141978517,
    "AKP": -0.001357066489287962,
    "GGT": -0.004175129872091236,
    "PT": -0.2428995182897213,
    "INR": -0.3485311369179553,
    "Scr": -0.01070883122888375,
    "BUN": 0.02319028094847908,
    "WBC": 0.09596183403364993,
    "Lym": -0.05668582842957903,
    "Hem": -0.001724078921084345,
    "Neu_prop": -2.258533009816271,
}

# ==================== Page Configuration ====================
st.set_page_config(page_title="Prediction Calculator", layout="wide")
st.title("Online Calculator for Surgical Resection Prediction in uHCC")
st.markdown("Please enter the patient's clinical parameters, and then click the button to obtain the predicted probability.")

# Sidebar for input controls
with st.sidebar:
    st.header("Patient Information")
    age = st.number_input("Age (years)", min_value=0, max_value=120, value=55, step=1)
    bmi = st.number_input("Body Mass Index (BMI, kg/m²)", min_value=15.0, max_value=50.0, value=22.0, step=0.1)
    dm = st.selectbox("Diabetes Mellitus (DM)", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    tumor_num = st.number_input("Tumor Number", min_value=1, max_value=10, value=1, step=1)
    max_dia = st.number_input("Maximum Diameter (cm)", min_value=0.0, max_value=30.0, value=5.0, step=0.1)
    pivka = st.number_input("PIVKA-II (mAU/mL)", min_value=0, value=100, step=10)
    alb = st.number_input("Albumin (ALB, g/L)", min_value=10.0, max_value=60.0, value=40.0, step=0.1)
    alt = st.number_input("Alanine Aminotransferase (ALT, U/L)", min_value=0.0, max_value=500.0, value=30.0, step=1.0)
    ast = st.number_input("Aspartate Aminotransferase (AST, U/L)", min_value=0.0, max_value=500.0, value=30.0, step=1.0)
    tbil = st.number_input("Total Bilirubin (TBIL, μmol/L)", min_value=0.0, max_value=500.0, value=15.0, step=0.1)
    akp = st.number_input("Alkaline Phosphatase (AKP, U/L)", min_value=0.0, max_value=500.0, value=80.0, step=1.0)
    ggt = st.number_input("Gamma-Glutamyl Transferase (GGT, U/L)", min_value=0.0, max_value=500.0, value=40.0, step=1.0)
    pt = st.number_input("Prothrombin Time (PT, seconds)", min_value=8.0, max_value=30.0, value=12.0, step=0.1)
    inr = st.number_input("International Normalized Ratio (INR)", min_value=0.8, max_value=5.0, value=1.0, step=0.01)
    scr = st.number_input("Serum Creatinine (Scr, μmol/L)", min_value=20.0, max_value=500.0, value=80.0, step=1.0)
    bun = st.number_input("Blood Urea Nitrogen (BUN, mmol/L)", min_value=1.0, max_value=30.0, value=5.0, step=0.1)
    wbc = st.number_input("White Blood Cell Count (WBC, 10⁹/L)", min_value=1.0, max_value=30.0, value=6.0, step=0.1)
    lym = st.number_input("Lymphocyte Count (Lym, 10⁹/L)", min_value=0.0, max_value=10.0, value=1.5, step=0.1)
    hem = st.number_input("Hemoglobin (Hem, g/L)", min_value=50.0, max_value=200.0, value=140.0, step=1.0)
    neu_prop = st.number_input("Neutrophil Proportion (Neu_prop)", min_value=0.0, max_value=1.0, value=0.60, step=0.01)

    calc_button = st.button("Calculate Probability", type="primary", use_container_width=True)

# ==================== Main Panel: Display Results ====================
st.header("Prediction Result")

if calc_button:
    # Calculate Linear Predictor (LP) – Child and PVTT removed, Lym added
    lp = (coef["Intercept"] +
          coef["Age"] * age +
          coef["BMI"] * bmi +
          coef["DM"] * dm +
          coef["Tumor_Number"] * tumor_num +
          coef["Max_Diameter"] * max_dia +
          coef["PIVKA_II"] * pivka +
          coef["ALB"] * alb +
          coef["ALT"] * alt +
          coef["AST"] * ast +
          coef["TBIL"] * tbil +
          coef["AKP"] * akp +
          coef["GGT"] * ggt +
          coef["PT"] * pt +
          coef["INR"] * inr +
          coef["Scr"] * scr +
          coef["BUN"] * bun +
          coef["WBC"] * wbc +
          coef["Lym"] * lym +
          coef["Hem"] * hem +
          coef["Neu_prop"] * neu_prop)
    
    # Calculate probability
    prob = 1 / (1 + np.exp(-lp))
    
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Linear Predictor (LP)", f"{lp:.4f}")
    with col2:
        st.metric("Predicted Probability", f"{prob * 100:.2f}%")
    
    # Visual risk bar
    st.progress(float(prob), text=f"Probability: {prob*100:.1f}%")
    
    st.markdown("---")
    st.caption("Formula: P = 1 / (1 + exp(-LP))")
else:
    st.info("Please fill in the patient information on the left and click the 'Calculate Probability' button.")

# ==================== Footer ====================
st.markdown("---")
st.markdown("**Disclaimer**: This tool is for research and academic communication purposes only and cannot replace professional clinical diagnosis.")
