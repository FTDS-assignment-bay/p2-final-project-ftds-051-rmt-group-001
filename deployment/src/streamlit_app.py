import streamlit as st
# import eda 
# import prediction
import Data_Pipeline
import home_page
import EDA as eda
import prediction 

from DS.feature_engineering import function_total_items_bin

import __main__

st.set_page_config(
    page_title="Customer Credit Default Prediction",
    layout = 'wide',
    initial_sidebar_state='expanded'
)

__main__.function_total_items_bin = function_total_items_bin

page_list = ['Home Page','EDA','Data Pipeline', 'Prediction'].sort()

page = st.sidebar.selectbox('Pilih Page: ', (['Home Page','EDA','Data Pipeline', 'Prediction']))

if page == 'Home Page':
    home_page.home_page()
elif page == 'Data Pipeline':
    Data_Pipeline.run()
elif page == 'EDA':
    eda.eda_page()
elif page == 'Prediction':
    prediction.prediction_page()
    
    