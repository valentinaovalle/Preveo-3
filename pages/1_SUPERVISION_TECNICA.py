import streamlit as st
#from streamlit_metrics import metric, metric_row
import numpy as np
import pandas as pd
import plotly.express as px
import datetime
#import matplotlib
#import matplotlib.pyplot as plt
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO, StringIO
import os
import cargar
import datatable as dt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import markdown


#from typing import List, Optional
#from tkinter import * from tkinter.ttk import *
def main():
    F_ST_19=cargar.cargar_formularios_8()
    
    
    
    with open('styles.css') as f:
        
        st.markdown(f"""<style>
                    {f.read()}
                    </style>"""
        , unsafe_allow_html=True)
    
    
    #CENTRAR EL LOGO EN LA BARRA LATERAL    
    st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
    )
    #INSERTAR LOGO EN LA BARRA LATERAL    
    with st.sidebar.container():
     image =Image.open('PREVEO5.png') 
     new_image = image.resize((185, 160))
     st.image(new_image, width=None, use_column_width=False)


    st.markdown(f'''<p style='background-color:#D1B3CF;text-align: center; color: #461c66;font-size: 30px;'>
                           <strong>Supervision Tecnica - Lucro App</strong><br>
                           ''',True)
    st.write(F_ST_19)
    

main()