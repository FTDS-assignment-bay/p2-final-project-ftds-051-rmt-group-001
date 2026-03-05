import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def home_page():

    st.title("Order Guardian")
    st.subheader("Predictive Order Risk Analytics System")
    
    col1_img, col2_img, col3 = st.columns([1,2,1])
    url = "https://raw.githubusercontent.com/KevinH2810/olist-raw-dataset/main/order_guardian-logo.png"
    response = requests.get(url)
    
    # logo = Image.open("./src/images/order_guardian-logo.png")
    logo = Image.open(BytesIO(response.content))

    col2_img.image(logo,width=400)
    
    # st.image("./src/images/order_guardian-logo.png", caption='Centered Image', use_column_width=True, width=1138)
    
    col1, col2 = st.columns([1,1])
    
    with col1:
        st.markdown("### About us")
        st.markdown("""
            Order Guardian is a **predictive analytics system** designed to identify and monitor high-risk e-commerce orders before operational resources are fully allocated.

            As digital commerce continues to grow, order cancellations have become a critical operational risk. High cancellation rates can lead to:

            - Revenue not being realized  
            - Inefficient inventory allocation  
            - Increased logistics and fulfillment costs, especially in **Cash-on-Delivery (COD)** transactions  

            Order Guardian transforms structured transactional data into **actionable operational insights** through an integrated data and analytics pipeline.

            The system combines several capabilities:

            • Data pipeline engineering and quality monitoring  
            • Exploratory business analysis  
            • Order-level cancellation risk prediction  
            • Operational decision support  

            By integrating **Data Engineering, Data Analysis, and Machine Learning**, Order Guardian enables earlier intervention, reduces operational waste, and supports better revenue realization.
        """)

    # st.divider()
    
    with col2:
        st.markdown("### System Components")

        st.markdown("""
        🔹 **Data Pipeline & Quality Monitoring**  
        Structured transformation, aggregation, and validation of transactional data.

        🔹 **Exploratory Data Analysis**  
        Business insights into cancellation behavior and operational patterns.

        🔹 **Predictive Modeling**  
        Classification model to estimate cancellation probability at order level.

        🔹 **Operational Risk Monitoring**  
        Support for proactive intervention and better decision-making.
        """)

    st.info("Navigate through the sidebar to explore each system component.")
    
if __name__ == '__main__':
    home_page()