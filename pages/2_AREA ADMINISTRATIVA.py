import streamlit as st
#from streamlit_metrics import metric, metric_row
import numpy as np
import pandas as pd
import plotly.express as px
import datetime
#import matplotlib
#import matplotlib.pyplot as plt
import hydralit_components as hc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO, StringIO
from PIL import Image
import os
import cargar
import datatable as dt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import markdown
import streamlit.components.v1 as components

st.set_page_config(
  page_title="Informe Alpunto", layout="wide",
  #page_icon=im,
  #initial_sidebar_state='collapsed'
)
st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 200px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)
#from typing import List, Optional
#from tkinter import * from tkinter.ttk import *}
reduce_header_height_style = """
        <style>
            div.block-container {padding-top:0.5rem;}
        </style>
    """
st.markdown(reduce_header_height_style, unsafe_allow_html=True)
def main():
    
    F_AD_31,F_AD_16,F_AD_14,F_AD_07,request=cargar.cargar_formularios_1()
    F_AD_29,F_AD_05,F_AD_22_A,F_AD_24_A=cargar.cargar_formularios_3()
    F_AD_24_B,F_AD_06,F_AD_19,F_AD_17, F_AD_24_D,F_AD_22_B=cargar.cargar_formularios_6()

    with open('styles.css') as f:
        
        st.markdown(f"""<style>
                    {f.read()}
                    </style>"""
        , unsafe_allow_html=True)
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
        workbook = writer.book
        worksheet = writer.sheets['Hoja1']
        for i, col in enumerate(df.columns):
            column_len = df[col].astype(str).str.len().max()
            column_len = max(column_len, len(col)) + 2
            worksheet.set_column(i, i, column_len)
        writer.save()
        processed_data = output.getvalue()
        return processed_data 
   
        
    menu_data = [
    {'icon': "", 'label':"F_AD_05"},
    {'icon':"",'label':"F_AD_06"},
    {'icon':"",'label':"F_AD_07"},
    {'icon':"",'label':"F_AD_14"},
    {'icon':"",'label':"F_AD_16"},
    {'icon':"",'label':"F_AD_17"},
    {'icon':"",'label':"F_AD_19"},
    {'icon':"",'label':"F_AD_22"},
    {'icon':"",'label':"F_AD_24"},
    {'icon':"",'label':"F_AD_24_D"},
    {'icon':"",'label':"F_AD_29"},
    {'icon':"",'label':"F_AD_31"},
    

        #{'icon': "fa-solid fa-radar",'label':"Dropdown1", 'submenu':[{'id':' subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': "💀", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
        #{'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
        #{'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar"},
        #{'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
        #{'icon': "far fa-copy", 'label':"Right End"},
        #{'icon': "fa-solid fa-radar",'label':"Dropdown2", 'submenu':[{'label':"Sub-item 1", 'icon': "fa fa-meh"},{'label':"Sub-item 2"},{'icon':'🙉','label':"Sub-item 3",}]},
    ]

    over_theme = {'txc_inactive': '#FFFFFF'}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        #login_name='Logout',
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
    )

    if menu_id == "F_AD_05":
        F_AD_05=F_AD_05[['centro_costo','nombres_y_apellidos','area_que_solicita_el_reembolso','fecha_diligenciamiento','total']]
        F_AD_05=F_AD_05.explode('centro_costo')
        F_AD_05=pd.concat([F_AD_05.drop(['centro_costo'], axis=1), F_AD_05['centro_costo'].apply(pd.Series)], axis=1)
        F_AD_05['fecha_diligenciamiento']=pd.to_datetime(F_AD_05['fecha_diligenciamiento'])
        F_AD_05['Mes'] = F_AD_05['fecha_diligenciamiento'].dt.month 
        F_AD_05.sort_values(by=['Mes'], inplace=True, ascending=False)
        conditionlist = [
        (F_AD_05['Mes'] == 1) ,
        (F_AD_05['Mes'] == 2),
        (F_AD_05['Mes'] == 3),
        (F_AD_05['Mes'] == 4),
        (F_AD_05['Mes'] == 5),     
        (F_AD_05['Mes'] == 6),
        (F_AD_05['Mes'] == 7),
        (F_AD_05['Mes'] == 8),
        (F_AD_05['Mes'] == 9),
        (F_AD_05['Mes'] == 10),  (F_AD_05['Mes'] == 11),
        (F_AD_05['Mes'] == 12)]
        choicelist = ['Enero', 'Febrero', 'Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        F_AD_05['Mes Diligenciamiento'] = np.select(conditionlist, choicelist, default='Not Specified')
        F_AD_05['fecha_diligenciamiento']=F_AD_05['fecha_diligenciamiento'].dt.strftime('%Y-%m-%d')
        mes= st.selectbox(
                    "Mes:",
                    pd.unique(F_AD_05['Mes Diligenciamiento'])
                    )
        df_ad_05=F_AD_05[(F_AD_05['Mes Diligenciamiento'] == mes)]
        df_ad_05=df_ad_05[['nombre','nombres_y_apellidos','fecha_diligenciamiento','total']]
        df_ad_05=df_ad_05.rename({'nombre': 'CENTROS DE COSTOS','nombres_y_apellidos':'NOMBRES Y APELLIDOS DEL RESPONSABLE DEL GASTO','fecha_diligenciamiento':'FECHA DE DILIGENCIAMIENTO','total':'VALOR TOTAL'}, axis=1)
        Lab_xlsx = to_excel(df_ad_05)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(df_ad_05.assign(hack='').set_index('hack'))
    #st.table(F_AD_05)

    if menu_id == "F_AD_06":
        st.write(F_AD_06)
    if menu_id=="F_AD_07":
        #st.write(F_AD_07)
        F_AD_07=F_AD_07.drop(['uuid','codigo','version','fecha_version','historico_de_aprobacion'],axis=1)
        #F_AD_07=F_AD_07[['fecha_elaboracion','centro_costo','reembolso','valor_de_este_reembolso']]
        #F_AD_07=F_AD_07.rename({'nombre': 'CENTROS DE COSTOS'},axis=1)
        F_AD_07=F_AD_07.explode('centro_costo')
        F_AD_07=pd.concat([F_AD_07.drop(['centro_costo'], axis=1), F_AD_07['centro_costo'].apply(pd.Series)], axis=1)
        F_AD_07=F_AD_07.rename({'nombre': 'AREA/PROYECTO'},axis=1)
        F_AD_07=F_AD_07.explode('reembolso')
        F_AD_07=pd.concat([F_AD_07.drop(['reembolso'], axis=1), F_AD_07['reembolso'].apply(pd.Series)], axis=1)
        F_AD_07=pd.concat([F_AD_07.drop(['valor_de_este_reembolso'], axis=1), F_AD_07['valor_de_este_reembolso'].apply(pd.Series)], axis=1)
        F_AD_07=pd.concat([F_AD_07.drop(['estatus'], axis=1), F_AD_07['estatus'].apply(pd.Series)], axis=1)
        F_AD_07=pd.concat([F_AD_07.drop(['responsable_aprobacion_jefe_cc'], axis=1), F_AD_07['responsable_aprobacion_jefe_cc'].apply(pd.Series)], axis=1)
        F_AD_07=F_AD_07.drop(['aprobacion'],axis=1)
        F_AD_07=F_AD_07.rename({'nombre': 'JEFE RESPONSABLE APROBACION','estatus':'Estado','aprobacion':'Aprobacion','fecha':'Fecha'},axis=1)
        F_AD_07=F_AD_07.drop(['observaciones','codigo','url_archivo','accion','step','Fecha','Estado','JEFE RESPONSABLE APROBACION'],axis=1)
        F_AD_07=pd.concat([F_AD_07.drop(['responsable_aprobacion_jefe_area_adm'], axis=1), F_AD_07['responsable_aprobacion_jefe_area_adm'].apply(pd.Series)], axis=1)
        F_AD_07=F_AD_07.rename({'reembolso_n':'REEMBOLSO N°','fecha_elaboracion':'FECHA','responsable_del_fondo':'RESPONSABLE DEL FONDO','fondo_permanente':'FONDO PERMANENTE','facturas':'FACTURAS','vales_recibidos_de_caja_menor':'VALES RECIBIDOS DE CAJA MENOR',
            'cuentas_de_cobro':'CUENTAS DE COBRO','valor_del_saldo':'VALOR DEL SALDO','valor_en_letras':'VALOR EN LETRAS','fecha_compra_o_gasto':'FECHA DE COMPRA','tipo_de_documneto':'TIPO DE DOC','pagado_a':'PAGADO A','nit_o_cc':'NIT/CC','concepto':'CONCEPTO',
            'subtotal':'SUBTOTAL','iva':'IVA','total':'TOTAL','total_subtotal':'TOTAL SUBTOTALES','total_iva':'TOTAL IVA','suma_totales':'SUMA TOTALES','fecha_de_pago':'FECHA DE PAGO'},axis=1)
        F_AD_07_=F_AD_07[['REEMBOLSO N°','AREA/PROYECTO','FECHA','RESPONSABLE DEL FONDO','FONDO PERMANENTE','FACTURAS','VALES RECIBIDOS DE CAJA MENOR',
            'CUENTAS DE COBRO','VALOR DEL SALDO','VALOR EN LETRAS','FECHA DE COMPRA','TIPO DE DOC','PAGADO A','NIT/CC','CONCEPTO',
            'SUBTOTAL','IVA','TOTAL','TOTAL SUBTOTALES','TOTAL IVA','SUMA TOTALES','FECHA DE PAGO']]
        F_AD_07_ = F_AD_07_.reset_index(drop=True)
        F_AD_07_['FECHA']=pd.to_datetime(F_AD_07_['FECHA'])
        F_AD_07_['Mes'] = F_AD_07_['FECHA'].dt.month 
        F_AD_07_.sort_values(by=['Mes'], inplace=True, ascending=False)
        conditionlist = [
        (F_AD_07_['Mes'] == 1) ,
        (F_AD_07_['Mes'] == 2),
        (F_AD_07_['Mes'] == 3),
        (F_AD_07_['Mes'] == 4),
        (F_AD_07_['Mes'] == 5),     
        (F_AD_07_['Mes'] == 6),
        (F_AD_07_['Mes'] == 7),
        (F_AD_07_['Mes'] == 8),
        (F_AD_07_['Mes'] == 9),
        (F_AD_07_['Mes'] == 10),  (F_AD_07_['Mes'] == 11),
        (F_AD_07_['Mes'] == 12)]
        choicelist = ['Enero', 'Febrero', 'Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        F_AD_07_['Mes Diligenciamiento'] = np.select(conditionlist, choicelist, default='Not Specified')
        F_AD_07_['FECHA']=F_AD_07_['FECHA'].dt.strftime('%Y-%m-%d')
        mes= st.selectbox(
                    "Mes:",
                    pd.unique(F_AD_07_['Mes Diligenciamiento'])
                    )
        df_ad_07=F_AD_07_[(F_AD_07_['Mes Diligenciamiento'] == mes)]
        #st.write(df_ad_07)
        acum_cc=df_ad_07.groupby(['AREA/PROYECTO','Mes'],as_index=False)['SUMA TOTALES'].sum()
        #st.write(acum_cc)
        acum_cc1=df_ad_07.groupby(['AREA/PROYECTO','Mes'],as_index=False)['REEMBOLSO N°'].count()
        #st.write(acum_cc1)

        
        c1,c2=st.columns(2)
        fig = make_subplots()
        colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(224, 231, 104)","rgb(147, 148, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
        fig.add_trace(go.Bar(x=acum_cc['SUMA TOTALES'],
                            y=acum_cc['AREA/PROYECTO'],orientation='h',
                            text=acum_cc['SUMA TOTALES'],
                            textposition='auto',
                            marker_color="#a4a4a4"))
        fig.update_layout(title_text='TOTAL VALOR REEMBOLSOS POR PROYECTO',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
        #fig.update_layout({'plot_bgcolor':'white','paper_bgcolor':'white'}, width = 600, height = 520)
        fig.update_xaxes(
             title_text = "Total Reembolso")
        fig.update_yaxes(
             title_text = "Proyecto")
        c1.plotly_chart(fig,use_container_width=True)

        fig1 = make_subplots()
        colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(224, 231, 104)","rgb(147, 148, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
        fig1.add_trace(go.Bar(x=acum_cc1['REEMBOLSO N°'],
                            y=acum_cc1['AREA/PROYECTO'],orientation='h',
                            text=acum_cc1['REEMBOLSO N°'],
                            textposition='auto',
                            marker_color="#706e6f"))
        fig1.update_layout(title_text='CANTIDAD DE REEMBOLSOS POR AREA/PROYECTO',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
        #fig1.update_layout({'plot_bgcolor':'white','paper_bgcolor':'white'}, width = 1000, height = 520)
        
        fig1.update_xaxes(
             title_text = "Cantidad Reembolsos")
        fig1.update_yaxes(
             title_text = "Area/Proyecto")
        c2.plotly_chart(fig1,use_container_width=True)

        Lab_xlsx = to_excel(df_ad_07)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(df_ad_07.assign(hack='').set_index('hack'))
        # Display an interactive table
        
        







    if menu_id=="F_AD_14":
        F_AD_14=F_AD_14.drop(['uuid','codigo','version','fecha_version','historico_de_aprobacion','estatus'],axis=1)
        F_AD_14=F_AD_14.explode('relacion_de_la_solicitud_o_elemento')
        F_AD_14=pd.concat([F_AD_14.drop(['relacion_de_la_solicitud_o_elemento'], axis=1), F_AD_14['relacion_de_la_solicitud_o_elemento'].apply(pd.Series)], axis=1)
        F_AD_14=F_AD_14.rename({'fecha_de_solicitud':'FECHA DE SOLICITUD',
            'nombre_de_quien_solicita':'NOMBRE DE QUIEN SOLICITA','cargo':'CARGO',
            'centro_de_costos':'CENTRO DE COSTOS','codigo_de_centro_de_costo':'COD. CENTRO  DE COSTOS',
            'solicitud_de_recursos_n':'SOLICITUD DE RECURSOS No.','prioridad':'PRIORIDAD',
            'plazo_de_entrega':'PLAZO DE ENTREGA','lugar_entrega':'LUGAR ENTREGA','observaciones':'OBSERVACIONES',
            'cierre_de_la_solicitud':'CIERRE DE LA SOLICITUD','a_quien_se_le_asigna':'A QUIEN SE LE ASIGNA',
            'tipo_de_activo':'TIPO DE ACTIVO','otro_tipo_de_activo_cual':'OTRO ACTIVO',
            'elemento':'ELEMENTO','otro_elemento_cual':'OTRO ELEMENTO','cantidad':'CANTIDAD','talla':'TALLA',
            'Justificacion':'JUSTIFICACION','fecha_ultima_entrega':'ULTIMA ENTREGA'},axis=1)
        F_AD_14=pd.concat([F_AD_14.drop(['responsable_aprobacion_jefe_cc'], axis=1), F_AD_14['responsable_aprobacion_jefe_cc'].apply(pd.Series)], axis=1)
        F_AD_14=F_AD_14.rename({'aprobacion':'APROBACION JEFE CC','fecha':'FECHA DE APROBACION','nombre':'NOMBRE DE QUIEN APRUEBA',
            'observaciones':'OBSERVACIONES DE QUIEN APRUEBA','estatus':'ESTADO'},axis=1)
        F_AD_14=pd.concat([F_AD_14.drop(['responsable_aprobacion_jefe_area_adm'], axis=1), F_AD_14['responsable_aprobacion_jefe_area_adm'].apply(pd.Series)], axis=1)
        F_AD_14=F_AD_14.rename({'aprobacion':'APROBACION JEFE ADM','fecha':'FECHA DE APROBACION AREA ADM','nombre':'NOMBRE DE QUIEN APRUEBA AREA ADM',
            'observaciones':'OBSERVACIONES DE QUIEN APRUEBA AREA ADM','estatus':'ESTADO AREA ADM','proveedor':'PROVEEDOR',
            },axis=1)
        F_AD_14=pd.concat([F_AD_14.drop(['recibido'], axis=1), F_AD_14['recibido'].apply(pd.Series)], axis=1)
        F_AD_14=F_AD_14.rename({'aprobacion':'APROBACION RECIBIDO','fecha':'FECHA DE RECIBIDO','nombre':'NOMBRE DE QUIEN RECIBE',
            'observaciones':'OBSERVACIONES DE RECIBIDO','estatus':'ESTADO DE RECIBIDO',
            'url_archivo':'URL ARCHIVO RECIBIDO'},axis=1)
        F_AD_14=pd.concat([F_AD_14.drop(['area_administrativo'], axis=1), F_AD_14['area_administrativo'].apply(pd.Series)], axis=1)
        F_AD_14=F_AD_14.rename({'fecha':'FECHA AREA ADMINISTRATIVA','nombre':'NOMBRE AREA ADM','url_archivo':'URL ARCHIVO AREA ADM'},axis=1)
        F_AD_14=F_AD_14.astype(str)
        ms1=pd.unique(F_AD_14['CENTRO DE COSTOS'])
        cc= st.selectbox(
          "Centro de costos:",
          ms1,index=len(ms1)-1
          )
        dataf=F_AD_14[(F_AD_14['CENTRO DE COSTOS']==cc)]
        ms2=pd.unique(dataf['TIPO DE ACTIVO'])
        activo= st.selectbox(
                     "Tipo De Activo:",
                     ms2,
                     index=len(ms2)-1
                     )
        dataf2=dataf[(dataf['TIPO DE ACTIVO']==activo)]
        ms3=pd.unique(dataf2['ESTADO'])
        estado= st.selectbox(
                     "Estado:",
                     ms3,
                     index=len(ms3)-1
                     )
        dataf3=dataf2[(dataf2['ESTADO'] == estado)]
        data_selection=dataf3[(dataf3['CENTRO DE COSTOS']==cc) & (dataf3['TIPO DE ACTIVO']==activo) & (dataf3['ESTADO']==estado)]
        Lab_xlsx = to_excel(data_selection)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(data_selection.assign(hack='').set_index('hack'))

    if menu_id=="F_AD_16":
        #st.write(F_AD_16)
        F_AD_16=F_AD_16.drop(['uuid','codigo','version','fecha_version','historico_de_aprobacion','estatus'],axis=1)
        F_AD_16=pd.concat([F_AD_16.drop(['revisada_por'], axis=1), F_AD_16['revisada_por'].apply(pd.Series)], axis=1)
        F_AD_16=F_AD_16.explode('facturas')
        F_AD_16=pd.concat([F_AD_16.drop(['facturas'], axis=1), F_AD_16['facturas'].apply(pd.Series)], axis=1)
        F_AD_16=F_AD_16.rename({'nombre':'REVISADA POR'},axis=1)
        #st.write(F_AD_16)
        F_AD_16=pd.concat([F_AD_16.drop(['revision_director_administrativo'], axis=1), F_AD_16['revision_director_administrativo'].apply(pd.Series)], axis=1)
        F_AD_16=F_AD_16.drop(['url_archivo'],axis=1)
        F_AD_16=F_AD_16.rename({'fecha_de_solicitud':'FECHA DE SOLICITUD','estatus':'ESTADO','factura_n_o_cuenta_cobro_n':'FACTURA N° / CUENTA DE COBRO N°','valor_de_la_factura':'VALOR TOTAL DE LA FACTURA',
            'contiene_concepto':'CONTIENE CONCEPTO','cargo':'CARGO','centro_de_costos':'CENTRO DE COSTOS','codigo_centro_costos':'COD.CENTRO DE COSTOS',
            'valor_de_la_factura_centro_de_costo':'VALOR DE LA FACTURA CORRESPODIENTE A ESTE CENTRO DE COSTOS',
            'descripcion':'DESCRIPCIÓN','coincide_el_valor':'COINCIDE EL VALOR APROBADO','aprobacion':'APROBADA','nombre':'REVISÓ Y APROBÓ',
            'observaciones':'OBSERVACIONES','pagar_en_la_fecha':'PAGAR EN LA FECHA'},axis=1)
        F_AD_16=F_AD_16[['FECHA DE SOLICITUD','REVISADA POR','CARGO','FACTURA N° / CUENTA DE COBRO N°','VALOR TOTAL DE LA FACTURA','CONTIENE CONCEPTO','CENTRO DE COSTOS','COD.CENTRO DE COSTOS',
            'DESCRIPCIÓN','VALOR DE LA FACTURA CORRESPODIENTE A ESTE CENTRO DE COSTOS','COINCIDE EL VALOR APROBADO',
            'APROBADA','REVISÓ Y APROBÓ','OBSERVACIONES','PAGAR EN LA FECHA','ESTADO']]
        F_AD_16[['CONTIENE CONCEPTO','COINCIDE EL VALOR APROBADO','APROBADA']] = F_AD_16[['CONTIENE CONCEPTO','COINCIDE EL VALOR APROBADO','APROBADA']].astype(str)
        F_AD_16[['CONTIENE CONCEPTO','COINCIDE EL VALOR APROBADO','APROBADA']]= F_AD_16[['CONTIENE CONCEPTO','COINCIDE EL VALOR APROBADO','APROBADA']].replace({"True": 'SI', "False": 'NO','nan':' '})
        total_cc=F_AD_16.groupby(['CENTRO DE COSTOS'],as_index=False)['VALOR TOTAL DE LA FACTURA'].sum()
        
        fig2 = make_subplots()
        colors=["rgb(124,144,132)","rgb(116,108,116)","rgb(211,212,21)","rgb(224,231,104)","rgba(112,110,111,255)","rgba(210,216,22,255)","rgb(164,164,164)","rgb(147, 148, 132)","rgb(224, 231, 104)"]
        fig2.add_trace(go.Bar(x=total_cc['VALOR TOTAL DE LA FACTURA'],
                            y=total_cc['CENTRO DE COSTOS'],orientation='h',
                            text=total_cc['VALOR TOTAL DE LA FACTURA'],
                            textposition='auto',
                            marker_color="rgb(224,231,104)"))
                            
        fig2.update_layout(title_text='VALOR TOTAL FACTURAS POR CENTRO DE COSTOS',
            title_x=0.5,title_font_color='#838A05',barmode='stack', yaxis={'categoryorder':'total ascending',
            })
        fig2.update_xaxes(
             title_text = "Valor Total")
        fig2.update_yaxes(
             title_text = "Centro de Costos")
        fig2.update_traces(texttemplate='%{text:,}')
        # Don't forget to remove from update_traces
        fig2.update_traces(textfont_size=12)
        fig2.update_traces(texttemplate='%{text:,}')
        fig2.update_yaxes(tickformat=",d")
        st.plotly_chart(fig2,use_container_width=True)
        Lab_xlsx = to_excel(F_AD_16)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_AD_16.assign(hack='').set_index('hack'))
      
    if menu_id=="F_AD_17":
        F_AD_17=F_AD_17[['datos_de_la_empresa','actividad_economica','datos_contacto']]
        F_AD_17=pd.concat([F_AD_17.drop(['datos_de_la_empresa'], axis=1), F_AD_17['datos_de_la_empresa'].apply(pd.Series)], axis=1)
        F_AD_17=pd.concat([F_AD_17.drop(['actividad_economica'], axis=1), F_AD_17['actividad_economica'].apply(pd.Series)], axis=1)
        F_AD_17=pd.concat([F_AD_17.drop(['datos_contacto'], axis=1), F_AD_17['datos_contacto'].apply(pd.Series)], axis=1)
        F_AD_17=pd.concat([F_AD_17.drop(['tipo_de_proveedor'], axis=1), F_AD_17['tipo_de_proveedor'].apply(pd.Series)], axis=1)
        F_AD_17=pd.concat([F_AD_17.drop(['productos'], axis=1), F_AD_17['productos'].apply(pd.Series)], axis=1)
        F_AD_17=F_AD_17.explode('articulo')
        F_AD_17=F_AD_17.rename({'razon_social_de_la_empresa':'RAZON SOCIAL','nit_con_codigo_de_verificacion':'NIT','articulo':'PRODUCTO','email':'CORREO','telefono':'TELEFONO','celular':'CELULAR','nombres_y_apellidos':'NOMBRE COMPLETO'},axis=1)
        F_AD_17=F_AD_17[['RAZON SOCIAL','NIT','PRODUCTO','CORREO','TELEFONO','CELULAR']]
        Lab_xlsx = to_excel(F_AD_17)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_AD_17.assign(hack='').set_index('hack'))

        #st.write(F_AD_17)
    if menu_id=="F_AD_19":
        F_AD_19=F_AD_19[['fecha','quien_recibe_la_herramienta']]
        F_AD_19=pd.concat([F_AD_19.drop(['quien_recibe_la_herramienta'], axis=1), F_AD_19['quien_recibe_la_herramienta'].apply(pd.Series)], axis=1)
        F_AD_19['fecha']=pd.to_datetime(F_AD_19['fecha'])
        F_AD_19['MES'] = F_AD_19['fecha'].dt.month 
        F_AD_19['AÑO'] = F_AD_19['fecha'].dt.year 
        F_AD_19=F_AD_19[['MES','AÑO','centro_de_costo','nombre_y_apellido']]
        F_AD_19=F_AD_19.rename({'centro_de_costo': 'CENTRO DE COSTOS',
            'nombre_y_apellido':'COLABORADOR'},axis=1)
        Lab_xlsx = to_excel(F_AD_19)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_AD_19.assign(hack='').set_index('hack'))
        
    if menu_id=="F_AD_22":
        st.markdown(f'''<p style='background-color:#ffffff;text-align: center; color: rgba(210,216,22,255);font-size: 35px;'>
                           <strong>F-AD-22-A </strong><br>
                           ''',True)
        F_AD_22_A=F_AD_22_A.drop(['uuid','codigo','version','fecha_version','estatus','historico_de_aprobacion'],axis=1)
        F_AD_22_A=F_AD_22_A.rename({'centro_de_costos': 'PROYECTO / PROCESO'},axis=1)
        F_AD_22_A=pd.concat([F_AD_22_A.drop(['empleado_general'], axis=1), F_AD_22_A['empleado_general'].apply(pd.Series)], axis=1)
        F_AD_22_A=F_AD_22_A.explode('elementos')
        F_AD_22_A=pd.concat([F_AD_22_A.drop(['elementos'], axis=1), F_AD_22_A['elementos'].apply(pd.Series)], axis=1)
        F_AD_22_A=pd.concat([F_AD_22_A.drop(['tipo_de_elemento'], axis=1), F_AD_22_A['tipo_de_elemento'].apply(pd.Series)], axis=1)
        F_AD_22_A=pd.concat([F_AD_22_A.drop(['bioseguridad'], axis=1), F_AD_22_A['bioseguridad'].apply(pd.Series)], axis=1)
        F_AD_22_A=F_AD_22_A.rename({'guantes_de_nitrilo': 'GUANTES NITRILO'},axis=1)
        
        F_AD_22_A=pd.concat([F_AD_22_A.drop(['epp'], axis=1), F_AD_22_A['epp'].apply(pd.Series)], axis=1)
        F_AD_22_A=pd.concat([F_AD_22_A.drop(['dotacion'], axis=1), F_AD_22_A['dotacion'].apply(pd.Series)], axis=1)
        F_AD_22_A=F_AD_22_A.explode('otro')
        #st.write(F_AD_22_A)
        F_AD_22_A=F_AD_22_A.rename({'nombre_del_trabajador': 'NOMBRE DEL TRABAJADOR','cedula_del_trabajador':'CÉDULA N°','cargo':'CARGO','fecha_de_entrega_o_devolucion':'FECHA DE ENTREGA','motivo_de_entrega':'MOTIVO DEL CAMBIO','aprobacion':'APROBACION',
            'tapabocas_de_tela_corporativo':'TAPABOCA DE TELA CORPORATIVO','tapabocas_microparticulado':'TAPABOCA MICROPARTICULADO',
            'botas_de_caucho':'BOTAS DE CAUCHO','botas_industriales':'BOTAS INDUSTRIALES',
            'botas_inyectadas_en_pvc':'BOTA INYECTADA EN PVC IMPERMEHABLE ',
            'casco':'CASCO','barbuquejo_plasticos':'BARBUQUEJO','protector_auditivo_de_copa':'PROTECTOR AUDITIVO COPA',
            'protector_auditivo_de_insercion':'PROTECTOR AUDITIVO DE INSERCIÓN',
            'abrigo_capucha':'ABRIGO CON CAPUCHA -IMERMEABLE',
            'gafas_de_seguridad':'GAFAS DE SEGURIDAD LENTE CLARO/ OSCURO',
            'guantes_de_caucho':'GUANTES DE CAUCHO',
            'proteccion_respiratoria_con_valvula':'PROTECTOR RESPIRATORIO CON VÁLVULA',
            'chaqueta_vg_st':'CHAQUETA VG / ST',"chaleco_vg_stwxe": 'CHALECO VG / ST',
            "camisa_manga_larga": 'CAMISA MANGA LARGA',
            "uniforme_servicios_generales": 'UNIFORME SERVICIOS GENERALES',
            "zapato_antideslizante":'ZAPATO ANTIDESLIZANTE',
            "guantes_de_nitrilo": 'GUANTES DE NILON NITRILO',
            "overol_antifluidos_servicios_generales":'OVEROL ANTIFLUIDOS PARA SERVICIOS GENERALES',
            "careta":'CARETA' ,"alcohol":'ALCOHOL',"gel_antibacterial":'GEL ANTIBACTAERIAL','otro':'OTRO, CUAL?'},axis=1)
        #st.write(F_AD_22_A)
        F_AD_22_A=F_AD_22_A[['PROYECTO / PROCESO','NOMBRE DEL TRABAJADOR','CÉDULA N°','CARGO','FECHA DE ENTREGA','MOTIVO DEL CAMBIO',
            'APROBACION',
            'BOTAS DE CAUCHO','BOTAS INDUSTRIALES',
            'BOTA INYECTADA EN PVC IMPERMEHABLE ',
            'CASCO','BARBUQUEJO',
            'PROTECTOR AUDITIVO DE INSERCIÓN','PROTECTOR AUDITIVO COPA',
            'ABRIGO CON CAPUCHA -IMERMEABLE',
            'GAFAS DE SEGURIDAD LENTE CLARO/ OSCURO',
            'GUANTES DE NILON NITRILO',
            'GUANTES DE CAUCHO',
            'PROTECTOR RESPIRATORIO CON VÁLVULA',
            'CHAQUETA VG / ST','CHALECO VG / ST',
            'CAMISA MANGA LARGA',
            'UNIFORME SERVICIOS GENERALES',
            'ZAPATO ANTIDESLIZANTE',
            'GUANTES NITRILO','TAPABOCA DE TELA CORPORATIVO','TAPABOCA MICROPARTICULADO',
            'OVEROL ANTIFLUIDOS PARA SERVICIOS GENERALES',
            'CARETA','ALCOHOL','GEL ANTIBACTAERIAL','OTRO, CUAL?']]
        F_AD_22_A=F_AD_22_A.astype(str)
        F_AD_22_A=F_AD_22_A.replace({"True": 'X', "False": ' ','nan':' ','None':' '})
        #st.write(F_AD_22_A)
        Lab_xlsx = to_excel(F_AD_22_A)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_AD_22_A.assign(hack='').set_index('hack'))
        
        st.markdown(f'''<p style='background-color:#ffffff;text-align: center; color: rgba(210,216,22,255);font-size: 35px;'>
                           <strong>F-AD-22-B </strong><br>
                           ''',True)
        F_AD_22_B=F_AD_22_B.drop(['uuid','codigo','version','fecha_version','estatus','historico_de_aprobacion'],axis=1)
        F_AD_22_B=F_AD_22_B.explode('elementos')
        F_AD_22_B=pd.concat([F_AD_22_B.drop(['elementos'], axis=1), F_AD_22_B['elementos'].apply(pd.Series)], axis=1)
        F_AD_22_B=pd.concat([F_AD_22_B.drop(['area_ambiental'], axis=1), F_AD_22_B['area_ambiental'].apply(pd.Series)], axis=1)
        F_AD_22_B=pd.concat([F_AD_22_B.drop(['epp'], axis=1), F_AD_22_B['epp'].apply(pd.Series)], axis=1)
        F_AD_22_B=pd.concat([F_AD_22_B.drop(['dotacion'], axis=1), F_AD_22_B['dotacion'].apply(pd.Series)], axis=1)
        F_AD_22_B=F_AD_22_B.explode('otro')
        F_AD_22_B=F_AD_22_B.rename({'fecha_de_entrega_o_devolucion':'FECHA DE DEVOLUCION',
            'motivo_de_entrega':'MOTIVO DE LA DEVOLUCION','centro_de_costos':'PROYECTO/PROCESO',
            'nombre_del_trabajador':'NOMBRE DEL COLABORADOR','cedula_del_trabajador':'CEDULA','casco':'CASCO','barbuquejo_plasticos':'BARBUQUEJO',
            'abrigo_capucha':'ABRIGO CON CAPUCHA -IMERMEABLE','chaqueta_vg_st':'CHAQUETA VG / ST',
            'chaleco_vg_st':'CHALECO VG / ST','camisa_manga_larga':'CAMISA MANGA LARGA',
        'uniforme_servicios_generales':'UNIFORME SERVICIOS GENERALES','otro':'OTRO, CUAL?','estatus':'ESTADO','memorando_url':'MEMORANDO'},axis=1)
        #st.write(F_AD_22_B)
        F_AD_22_B=F_AD_22_B[['PROYECTO/PROCESO','NOMBRE DEL COLABORADOR','CEDULA',
        'MOTIVO DE LA DEVOLUCION','CASCO','BARBUQUEJO','ABRIGO CON CAPUCHA -IMERMEABLE','CHAQUETA VG / ST',
        'CHALECO VG / ST','CAMISA MANGA LARGA','UNIFORME SERVICIOS GENERALES','OTRO, CUAL?','ESTADO','MEMORANDO']]
        F_AD_22_B=F_AD_22_B.astype(str)
        F_AD_22_B=F_AD_22_B.replace({"True": 'X', "False": ' ','nan':' '})
        Lab_xlsx = to_excel(F_AD_22_B)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_AD_22_B.assign(hack='').set_index('hack'))
        
    if menu_id=="F_AD_24":
        st.markdown(f'''<p style='background-color:#ffffff;text-align: center; color: rgba(210,216,22,255);font-size: 35px;'>
                           <strong>F-AD-24-A </strong><br>
                           ''',True)
        F_AD_24_A=F_AD_24_A.drop(['uuid','codigo','version','fecha_version','estatus','historico_de_aprobacion'],axis=1)
        F_AD_24_A=pd.concat([F_AD_24_A.drop(['proveedores'], axis=1), F_AD_24_A['proveedores'].apply(pd.Series)], axis=1)
        F_AD_24_A=F_AD_24_A.explode('producto_o_servicio')
        F_AD_24_A=pd.concat([F_AD_24_A.drop(['criterios_de_seleccion'], axis=1), F_AD_24_A['criterios_de_seleccion'].apply(pd.Series)], axis=1)
        F_AD_24_A=F_AD_24_A.rename({'experiencia_y_documentacion': 'Experiencia y documentaciòn (20%)',
          "tarifa_de_precios": 'Tarifa de precios (20%)',
          "forma_de_pago": 'Forma de pago  (10%)',
          "capacidad_de_entrega_en_proyectos": 'Capacidad de entrega en proyectos (20%)',
          "sistemas_de_csstma": 'Sistemas de CSSTMA (30%)'},axis=1)
        F_AD_24_A=pd.concat([F_AD_24_A.drop(['check_list_documentos_presentados'], axis=1), F_AD_24_A['check_list_documentos_presentados'].apply(pd.Series)], axis=1)
        F_AD_24_A=pd.concat([F_AD_24_A.drop(['responsable_aprobacion_jefe_area_adm'], axis=1), F_AD_24_A['responsable_aprobacion_jefe_area_adm'].apply(pd.Series)], axis=1)
        F_AD_24_A=F_AD_24_A.rename({'aprobacion':'APROBACION','estatus':'APROBACIÓN ÁREA ADMINISTRATIVA','fecha':'FECHA','nombre':'NOMBRE','observaciones':'OBSERVACIONES'},axis=1)
        F_AD_24_A=pd.concat([F_AD_24_A.drop(['gerencia'], axis=1), F_AD_24_A['gerencia'].apply(pd.Series)], axis=1)
        F_AD_24_A=F_AD_24_A.rename({'proveedor':'PROVEEDOR','producto_o_servicio':'PRODUCTO O SERVICIO','verificacion_contratos_similares':'VERIFICACION CONTRATOS SIMILARES','fecha_de_ingreso_del_proveedor':'FECHA DE INGRESO DEL PROVEEDOR',
          'experiencia_y_documentacion': 'Experiencia y documentación',
          "tarifa_de_precios": 'Tarifa de precios',
          "forma_de_pago": 'Forma de pago',
          "capacidad_de_entrega_en_proyectos": 'Capacidad de entrega en proyectos',
          "sistema_de_csstma": 'Sistemas de CSSTMA','total':'TOTAL','estatus':'APROBACIÓN GERENCIA'},axis=1)
        F_AD_24_A=F_AD_24_A.drop(['observaciones','nombre','fecha','aprobacion','lo_necesita_aprobar_gerencia','FECHA','NOMBRE','OBSERVACIONES','APROBACION'],axis=1)
        F_AD_24_A=F_AD_24_A.astype(str)
        F_AD_24_A=F_AD_24_A.replace({"True": 'SI', "False": 'NO','nan':' '})
        Lab_xlsx = to_excel(F_AD_24_A)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_AD_24_A.assign(hack='').set_index('hack'))
        
        
        st.markdown(f'''<p style='background-color:#ffffff;text-align: center; color: rgba(210,216,22,255);font-size: 35px;'>
                           <strong>F-AD-24-B </strong><br>
                           ''',True)
        F_AD_24_B=F_AD_24_B.drop(['uuid','codigo','version','fecha_version','estatus'],axis=1)
        F_AD_24_B=pd.concat([F_AD_24_B.drop(['proveedores'], axis=1), F_AD_24_B['proveedores'].apply(pd.Series)], axis=1)
        F_AD_24_B=F_AD_24_B.explode('acuerdos_o_acciones')
        F_AD_24_B=pd.concat([F_AD_24_B.drop(['acuerdos_o_acciones'], axis=1), F_AD_24_B['acuerdos_o_acciones'].apply(pd.Series)], axis=1)
        F_AD_24_B=F_AD_24_B.rename({'total':'TOTAL','acuerdo':'ACUERDOS ACCIONES'},axis=1)
        F_AD_24_B=pd.concat([F_AD_24_B.drop(['seguimiento_de_proveedor'], axis=1), F_AD_24_B['seguimiento_de_proveedor'].apply(pd.Series)], axis=1)
        F_AD_24_B=pd.concat([F_AD_24_B.drop(['segundo_seguimiento_de_proveedor'], axis=1), F_AD_24_B['segundo_seguimiento_de_proveedor'].apply(pd.Series)], axis=1)
        F_AD_24_B=F_AD_24_B.explode('producto_o_servicio')
        F_AD_24_B=pd.concat([F_AD_24_B.drop(['capacidad'], axis=1), F_AD_24_B['capacidad'].apply(pd.Series)], axis=1)
        F_AD_24_B=pd.concat([F_AD_24_B.drop(['comercial'], axis=1), F_AD_24_B['comercial'].apply(pd.Series)], axis=1)
        F_AD_24_B=pd.concat([F_AD_24_B.drop(['servicio_al_cliente'], axis=1), F_AD_24_B['servicio_al_cliente'].apply(pd.Series)], axis=1)
        F_AD_24_B=pd.concat([F_AD_24_B.drop(['gestion_de_la_cssta'], axis=1), F_AD_24_B['gestion_de_la_cssta'].apply(pd.Series)], axis=1)
        F_AD_24_B=F_AD_24_B.drop([0],axis=1)
        F_AD_24_B=F_AD_24_B.explode('resultados_de_seguimiento')
        F_AD_24_B=pd.concat([F_AD_24_B.drop(['resultados_de_seguimiento'], axis=1), F_AD_24_B['resultados_de_seguimiento'].apply(pd.Series)], axis=1)
        F_AD_24_B=F_AD_24_B.rename({"fecha_de_evaluacion": "FECHA EVALUACIÓN",
        "proveedor": "PROVEEDOR","estado_del_proveedor": "ESTADO DEL PROVEEDOR",
        "email": "DIRECCIÓN DE CORREO ELECTRÓNICO","celular": 'TELÉFONO',"persona_de_contacto": "PERSONA DE CONTACTO",
        "producto_o_servicio":'PRODUCTO O SERVICIO',"cualidad_producto_servicio":'CALIDAD DEL PRODUCTO Y/O SERVICIO',
        "documentacion_producto_servicio":'DOCUMENTACIÓN DEL PRODUCTO Y/O SERVICIO',
        "disponibilidad": 'DISPONIBILIDAD',"cumplimiento_entregas":'CUMPLIMIENTO DE LAS ENTREGAS O PRESTACIÓN DEL SERVICIO',
        "tarifas_adecuadas":'TARIFAS ADECUADAS',"comunicacion": 'COMUNICACIÓN',
        "atencion_a_quejas_y_reclamos": 'ATENCIÓN QUEJAS Y RECLAMOS',
        "cumplimiento_manejo_residuos": "CUMPLIMIENTO MANEJO DE RESIDUOS",
        "soportes_exigidos_de_la_sg_cssta": 'SOPORTES EXIGIDOS DE LA SG -CSSTA',
        "aportes_pagos_seguridad_social": "APORTES PAGOS SEGURIDAD SOCIAL",
        "uso_adecuado_epp": "USO ADECUADO EPP ",'fecha_cumplimiento':'FECHA CUMPLIMIENTO',
        'calificacion':'CALIFICACION','responsable':'RESPONSABLE'},axis=1)
        F_AD_24_B=F_AD_24_B[['FECHA EVALUACIÓN',"PROVEEDOR","ESTADO DEL PROVEEDOR","DIRECCIÓN DE CORREO ELECTRÓNICO",
             'TELÉFONO',"PERSONA DE CONTACTO",'PRODUCTO O SERVICIO','CALIDAD DEL PRODUCTO Y/O SERVICIO',
        'DOCUMENTACIÓN DEL PRODUCTO Y/O SERVICIO',
        'DISPONIBILIDAD','CUMPLIMIENTO DE LAS ENTREGAS O PRESTACIÓN DEL SERVICIO',
        'TARIFAS ADECUADAS','COMUNICACIÓN','ATENCIÓN QUEJAS Y RECLAMOS',
        "CUMPLIMIENTO MANEJO DE RESIDUOS",'SOPORTES EXIGIDOS DE LA SG -CSSTA',
        "APORTES PAGOS SEGURIDAD SOCIAL","USO ADECUADO EPP ",'TOTAL','CALIFICACION','ACUERDOS ACCIONES','FECHA CUMPLIMIENTO']]
        Lab_xlsx = to_excel(F_AD_24_B)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_AD_24_B.assign(hack='').set_index('hack'))

    if menu_id=="F_AD_24_D":
        F_AD_24_D=F_AD_24_D.drop(['uuid','codigo','version','fecha_version','estatus'],axis=1)
        F_AD_24_D=pd.concat([F_AD_24_D.drop(['proveedores'], axis=1), F_AD_24_D['proveedores'].apply(pd.Series)], axis=1)
        F_AD_24_D=F_AD_24_D.explode('producto_o_servicio')
        #st.write(F_AD_24_D)
        #F_AD_24_D=pd.concat([F_AD_24_D.drop(['producto_o_servicio'], axis=1), F_AD_24_D['producto_o_servicio'].apply(pd.Series)], axis=1)
        F_AD_24_D=pd.concat([F_AD_24_D.drop(['criterios_reevaluacion'], axis=1), F_AD_24_D['criterios_reevaluacion'].apply(pd.Series)], axis=1)
        F_AD_24_D=F_AD_24_D.rename({'proveedor':'PROVEEDOR','producto_o_servicio':'PRODUCTO O SERVICIO','experiencia_y_documentacion': 'Experiencia y documentaciòn (20%)',
          'fecha_de_ingreso_proveedor':'FECHA DE INGRESO DEL PROVEEDOR',"tarifa_de_precios": 'Tarifa de precios (20%)',
          "forma_de_pago": 'Forma de pago  (10%)',
          "capacidad_de_entrega_proyectos": 'Capacidad de entrega en proyectos (20%)',
          "sistemas_de_csstma": 'Sistemas de CSSTMA (30%)'},axis=1)
        F_AD_24_D=pd.concat([F_AD_24_D.drop(['checklist_documentos_presentados'], axis=1), F_AD_24_D['checklist_documentos_presentados'].apply(pd.Series)], axis=1)
        filtro = F_AD_24_D['total'] != 'string'
        F_AD_24_D = F_AD_24_D[filtro]
        F_AD_24_D['total']=F_AD_24_D['total'].astype(int)
        #st.write(F_AD_24_D)
        F_AD_24_D["Color"] = np.where(F_AD_24_D["total"]<70, 'red', 'green')
        fig3 = make_subplots()
        #colors=["rgb(124,144,132)","rgb(116,108,116)","rgb(211,212,21)","rgb(224,231,104)","rgba(112,110,111,255)","rgba(210,216,22,255)","rgb(164,164,164)","rgb(147, 148, 132)","rgb(224, 231, 104)"]
        fig3.add_trace(go.Bar(x=F_AD_24_D['total'],
                              y=F_AD_24_D['PROVEEDOR'],
                            marker_color=F_AD_24_D['Color'],orientation='h',
                            text=F_AD_24_D['total'],
                            textposition='auto'
                            ))
        fig3.update_layout(title_text='CALIFICACION POR PROVEEDOR',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
        fig3.update_xaxes(
             title_text = "Calificación")
        fig3.update_yaxes(
             title_text = "Proveedor")
        st.plotly_chart(fig3,use_container_width=True)
        F_AD_24_D['total']=F_AD_24_D['total'].astype(str)
        F_AD_24_D=F_AD_24_D.rename({'total':'TOTAL','experiencia_y_documentacion': 'Experiencia y documentación',
          "precios": 'Tarifa de precios',
          "forma_de_pago": 'Forma de pago',
          "capacidad_entrega_en_proyectos": 'Capacidad de entrega en proyectos',
          "sistema_decsstma": 'Sistemas de CSSTMA','continua_como_proveedor':'CONTINUA COMO PROVEEDOR',
          'memorando_de_notificacion_terminacion_servicios':'MEMORANDO DE NOTIFICACION TERMINACION PRESTACION DE SERVICIOS',
          'observaciones':'OBSERVACIONES'},axis=1)
        F_AD_24_D=F_AD_24_D[['PROVEEDOR','PRODUCTO O SERVICIO','FECHA DE INGRESO DEL PROVEEDOR',
            'Experiencia y documentaciòn (20%)','Tarifa de precios (20%)','Forma de pago  (10%)',
          'Capacidad de entrega en proyectos (20%)','Sistemas de CSSTMA (30%)','Experiencia y documentación',
          'Tarifa de precios','Forma de pago','Capacidad de entrega en proyectos','Sistemas de CSSTMA','TOTAL',
          'CONTINUA COMO PROVEEDOR','MEMORANDO DE NOTIFICACION TERMINACION PRESTACION DE SERVICIOS',
          'OBSERVACIONES']]
        F_AD_24_D=F_AD_24_D.astype(str)
        F_AD_24_D=F_AD_24_D.replace({"True": 'SI', "False": 'NO','nan':' '})
        Lab_xlsx = to_excel(F_AD_24_D)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_AD_24_D.assign(hack='').set_index('hack'))
        
    if menu_id=="F_AD_29":
        F_AD_29=F_AD_29.drop(['uuid','codigo','version','fecha_version','estatus','historico_de_aprobacion'],axis=1)
        F_AD_29=pd.concat([F_AD_29.drop(['datos_de_la_empresa'], axis=1), F_AD_29['datos_de_la_empresa'].apply(pd.Series)], axis=1)
        F_AD_29=F_AD_29.explode('responsables_contacto')
        F_AD_29=pd.concat([F_AD_29.drop(['tipo_de_documneto'], axis=1), F_AD_29['tipo_de_documneto'].apply(pd.Series)], axis=1)
        F_AD_29=F_AD_29.rename({'email':'correo'},axis=1)
        F_AD_29=pd.concat([F_AD_29.drop(['responsables_contacto'], axis=1), F_AD_29['responsables_contacto'].apply(pd.Series)], axis=1)
        F_AD_29=pd.concat([F_AD_29.drop(['documentos'], axis=1), F_AD_29['documentos'].apply(pd.Series)], axis=1)
        F_AD_29=pd.concat([F_AD_29.drop(['facturacion_electronica'], axis=1), F_AD_29['facturacion_electronica'].apply(pd.Series)], axis=1)
        F_AD_29=F_AD_29.rename({'nombre_y_apellido':'NOMBRE Y APELLIDO ','cargo':'CARGO DE QUIEN FIRMA'},axis=1)
        F_AD_29=pd.concat([F_AD_29.drop(['datos_de_quien_firma'], axis=1), F_AD_29['datos_de_quien_firma'].apply(pd.Series)], axis=1)
        F_AD_29=F_AD_29.rename({'ciudad':'CIUDAD','departamento':'DEPARTAMENTO'},axis=1)
        F_AD_29=pd.concat([F_AD_29.drop(['informacion_fiscal'], axis=1), F_AD_29['informacion_fiscal'].apply(pd.Series)], axis=1)
        F_AD_29=pd.concat([F_AD_29.drop(['responsable_aprobacion_jefe_area_adm'], axis=1), F_AD_29['responsable_aprobacion_jefe_area_adm'].apply(pd.Series)], axis=1)
        F_AD_29=F_AD_29.explode('ciuu')
        F_AD_29=pd.concat([F_AD_29.drop(['autorizacion_de_datos_a_preveo'], axis=1), F_AD_29['autorizacion_de_datos_a_preveo'].apply(pd.Series)], axis=1)
        
        F_AD_29=F_AD_29.rename({"nombre_o_razon_social": "NOMBRE O RAZÓN SOCIAL",
        "nit_n_o_rut":'NIT N° / RUT',"telefono_de_contacto": 'TELÉFONO DE CONTACTO',
        "direccion": "DIRECCIÓN",
        "nobre_completo_representante_legal": "NOMBRE COMPLETO REPRESENTANTE LEGAL",
        "tipo":"TIPO DE DOCUMENTO","numero": 'NÚMERO CC / CE / PASAPORTE',
        "correo": "CORREO ELECTRÓNICO","nombre_y_apellido": "NOMBRE Y APELLIDO",'area':'AREA',
        'telefono_fijo_celular':'TELÉFONO FIJO / CELULAR','email':'CORREO ELECTRONICO ',
        'email_corporativo':'CORREO CORPORATIVO1','email_para_la_recepcion':'CORREO CORPORATIVO2',
        'nombre_del_responsable':'NOMBRE DEL RESPONSABLE','cargo_del_responsable':'CARGO DEL RESPONSABLE',
        'cedula_ciudadania':'CEDULA DE CIUDADANIA','cargo':'CARGO','regimen':'REGIMEN','ciuu':'ACTIVIDAD CIIU',
        'numero_resolucion':'NUMERO DE RESOLUCION','departamento':'DEPARTAMENTO ','ciudad':'CIUDAD ','estatus':'ESTADO',
        'observaciones':'OBSERVACIONES','camara_url':'CAMARA DE COMERCIO','rut_url':'RUT',
        'cedula_representante_url':'CEDULA REPRESENTANTE','resolucion':'RESOLUCION',
        "num_1_solicita_informacion": 'SOLICITA INFORMACION',
          "num_2_Solicitar_alianzas_comerciales": 'SOLICITAR ALIANZAS COMERCIALES',
          "num_3_promocion_de_servicios": 'PROMOCION DE SERVICIOS',
          "num_4_contactar_en_caso_de_presentarse": 'CONTACTAR EN CASO DE PRESENTARSE',
          "num_5_verificar_antecedentes": 'VERIFICAR ANTECEDENTES',
          "num_6_contacto_para_emitir_facturas": 'CONTACTO PARA EMITIR FACTURAS',
          "num_7_mantener_copias_de_reportes": 'MANTENER COPIAS DE REPORTES'},axis=1)
        F_AD_29=F_AD_29.astype(str)
        F_AD_29=F_AD_29.replace({"True": 'SI', "False": 'NO','nan':' '})
        Lab_xlsx = to_excel(F_AD_29)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_AD_29.assign(hack='').set_index('hack'))
        
    if menu_id=="F_AD_31":
        F_AD_31=F_AD_31[['fecha_en_la_que_se_realiza_la_labor','nombre_contratista','actividad_o_labor_a_realizar']]
        F_AD_31=F_AD_31.rename({'nombre_contratista':'CONTRATISTA','fecha_en_la_que_se_realiza_la_labor':'FECHA','actividad_o_labor_a_realizar':'ACTIVIDAD O LABOR'},axis=1)
        F_AD_31['FECHA']=pd.to_datetime(F_AD_31['FECHA'])
        F_AD_31['FECHA LABOR']=F_AD_31['FECHA'].dt.strftime('%Y-%m-%d')
        F_AD_31=F_AD_31[['CONTRATISTA','FECHA LABOR','ACTIVIDAD O LABOR']] 
        Lab_xlsx = to_excel(F_AD_31)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_AD_31.assign(hack='').set_index('hack'))
        


main()    