import streamlit as st
#from streamlit_metrics import metric, metric_row
import numpy as np
import pandas as pd
import plotly.express as px
import datetime
#import matplotlib
#import matplotlib.pyplot as plt

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO, StringIO
from PIL import Image
import os
import cargar
import datatable as dt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import markdown


#from typing import List, Optional
#from tkinter import * from tkinter.ttk import *
def main():
    data, tip_nov ,F_AD_05, pr, cc_in,employees,cost_center =cargar.cargar_info()
    data, tip_nov ,df, pr, cc_in,employees,cost_center=cargar.cargar_basicos()
    cale=cargar.traer_cale()
    with open('styles.css') as f:
        
        st.markdown(f"""<style>
                    {f.read()}
                    </style>"""
        , unsafe_allow_html=True)

    
    pr['año_mes']=pd.to_datetime(pr['fecha'])
    cantpr=pr.groupby(['centro_de_costos','año_mes'],as_index=False)['valor_del_prestamo'].sum()
    contarpr=pr.groupby(['centro_de_costos'],as_index=False)['valor_del_prestamo'].count()

    #------------------------------------------------------------------------------
    url2='https://drive.google.com/file/d/1-21f9kCJfkcDce91hJYo3e_7030aKoII/view?usp=sharing'
    url2='https://drive.google.com/uc?id=' + url2.split('/')[-2]
    dff2 = pd.read_csv(url2,sep=';')
   
    
    data=data.drop(["codigo_centro_de_costos"],axis=1) 
    data.columns = data.columns.str.replace(' ', '_') 
    data['fecha_inicial_novedad'] = pd.to_datetime(data['fecha_inicial_novedad'],format='%Y-%m-%d')
    
    data['fecha_final_novedad'] = pd.to_datetime(data['fecha_final_novedad'], errors='coerce')
    data['documento_de_identificacion'] = data['documento_de_identificacion'].astype(str)
    data['año_mes']=data['fecha_inicial_novedad'].dt.strftime('%Y-%m')
    data['empleado']=data['nombre_del_empleado']+ "-" +data["documento_de_identificacion"]
    data=data.drop(["uuid","fecha_observacion"],axis=1) 
    
    #st.write('data')
    #st.write(data)
    data['Alerta']=""
    for i in range(len(data['nombre_del_empleado'])):
        if data.iloc[i,8] == 30:
           data.iloc[i,15] = "OK"
        else:
           data.iloc[i,15] = "Revisar"
    
    #st.write(rep_nov)
    
    #st.write(data)
    Lab =data.groupby(['nombre_del_empleado','documento_de_identificacion','año_mes'],as_index=False)['dias_laborados'].sum()
    Lab['Alerta']=""
    
    for i in range(len(Lab['nombre_del_empleado'])):
        if Lab.iloc[i,3] == 30:
            Lab.iloc[i,4] = "OK"
        else:
            Lab.iloc[i,4] = "Revisar"
   
    Por_tra = (Lab['dias_laborados']/30)*100
    Lab['Por_tra']=Por_tra   
    #-----------------------------------------------------------------------------
    url='https://drive.google.com/file/d/1SYecV7Sm7NOarvSg6uAoZSgRdRcECLua/view?usp=sharing'
    url='https://drive.google.com/uc?id=' + url.split('/')[-2]
    cm = pd.read_csv(url,sep=';')
    #cm=pd.read_excel("https://docs.google.com/spreadsheets/d/1dxWGKibM_6n5llwR68zUxVuxQ8AAKn2T/edit?usp=sharing&ouid=112502888078542287829&rtpof=true&sd=true")
  
    cm['año_mes']=pd.to_datetime(cm['fecha_de_elaboracion'],format='%d/%m/%Y')
    cantcm=cm.groupby(['cargar_a_centro_de_costos','año_mes'],as_index=False)['total'].sum()
    contarcm=cm.groupby(['cargar_a_centro_de_costos'],as_index=False)['total'].count()
    reemcm=cm.groupby(['nombres_y_apellidos','numero_cc','cargar_a_centro_de_costos'],as_index=False)['total'].sum()
    cmv=cm['reembonsable_al_cliente'].value_counts()
    #-----------------------------------------------------------------------------
    #emplea=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/EMPLEADOS/em.xlsx")
    employees['salario']=employees['salario'].replace({',':''}, regex=True)
    employees['salario']=employees['salario'].astype(int)
    sorteo=employees.sort_values(by='salario')
    #----------------------------------------------------------------------------
    def SetMoneda(num, simbolo="$", n_decimales=2):
        #con abs, nos aseguramos que los dec. sea un positivo.
        n_decimales = abs(n_decimales)
        #se redondea a los decimales idicados.
        num = round(num, n_decimales)
        #se divide el entero del decimal y obtenemos los string
        num, dec = str(num).split(".")
        #si el num tiene menos decimales que los que se quieren mostrar,
        #se completan los faltantes con ceros.
        dec += "0" * (n_decimales - len(dec))
        #se invierte el num, para facilitar la adicion de comas.
        num = num[::-1]
        #se crea una lista con las cifras de miles como elementos.
        l = [num[pos:pos+3][::-1] for pos in range(0,50,3) if (num[pos:pos+3])]
        l.reverse()
        #se pasa la lista a string, uniendo sus elementos con comas.
        num = str.join(",", l)
        #si el numero es negativo, se quita una coma sobrante.
        try:
            if num[0:2] == "-,":
                num = "-%s" % num[2:]
        except IndexError:
            pass
        #si no se especifican decimales, se retorna un numero entero.
        if not n_decimales:
            return "%s %s" % (simbolo, num)
        return "%s %s.%s" % (simbolo, num, dec)
    
    #-------------------------------------------------------------------------------
    
#QUITAR ESPACIO DE EL BORDE SUPERIOR
    reduce_header_height_style = """
        <style>
            div.block-container {padding-top:0rem;}
        </style>
    """
    st.markdown(reduce_header_height_style, unsafe_allow_html=True)

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

    mes= st.sidebar.selectbox(
                     "Mes:",
                     pd.unique(data['año_mes']),
                     index=len(pd.unique(data['año_mes']))-1
                     )
    dataf=data[(data.año_mes == mes)]
    ms1=pd.unique(dataf['centro_de_costos'])
    ms2=np.append(ms1,"Todos")
                 
    cent_cost_filter= st.sidebar.selectbox(
                     "Centro Costos:",
                     ms2,
                     index=len(ms2)-1
                     )
    if "Todos" in cent_cost_filter: 
            cent_cost_filter = dataf['centro_de_costos']
    else:
        cent_cost_filter=[cent_cost_filter]
    dataf=dataf[(dataf.centro_de_costos.isin(cent_cost_filter))]
    cd1=pd.unique(dataf['nombre_del_empleado'])
    cd2=np.append(cd1,"Todos")
    empleado = st.sidebar.selectbox(
                "Empleado:",
                cd2,
                index=len(cd2)-1
                ) 
    if "Todos" in empleado: 
            empleado = dataf['nombre_del_empleado']
    else:
            empleado=[empleado]
        
    data_selection=dataf[(dataf.nombre_del_empleado.isin(empleado)) & (dataf.año_mes==mes)]
    
    st.header("Reporte Novedades")
    ms1=pd.unique(data['fecha'])
    ms2=np.append(ms1,"Todos")
    formulario= st.multiselect(
                     "Fecha:",
                     ms2,
                     default='Todos'
                     )
    if "Todos" in formulario: 
            formulario = data['fecha']
    else:
            formulario=formulario
    dataf1=data[(data.fecha.isin(formulario))]
    dataf1.rename(columns={'quien_reporta_la_novedad':'Quien reporta la novedad',
                        'nombre_del_empleado':'Nombre del Empleado','documento_de_identificacion':'Documento de Identificacion','centro_de_costos':'Centro de Costos',
                        'tipo_de_novedad':'Tipo de Novedad','año_mes':'Año-Mes','dias_a_facturar':'Dias a Facturar',
                        'dias_laborados':'Dias Laborados','fecha_inicial_novedad':'Fecha Inicial Novedad',
                        'fecha_final_novedad':'Fecha Final Novedad'},
               inplace=True)
    st.write(dataf1)
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

    Lab_xlsx = to_excel(dataf1)
    st.download_button(label='Resultados',
                                 data=Lab_xlsx ,
                                 file_name= 'df_test.xlsx') 
    
    fig2 = make_subplots()
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(75, 177, 61, 1)","rgb(224, 231, 104)","rgb(124, 144, 132)","rgb(63, 140, 90, 1)"]
         

    for t,c in zip(data_selection.tipo_de_novedad.unique(),colors):
            plot_df = data_selection[data_selection.tipo_de_novedad == t]
            fig2.add_trace(go.Bar(name=t,
                                  x=plot_df.nombre_del_empleado,
                                  y=plot_df.dias_laborados,
                                  text=plot_df.dias_laborados,
                                  marker_color=c))
                    
    fig2.update_layout(title_text='Empleados Por Novedad',title_x=0.5,barmode="stack") 
    fig2.update_yaxes(
             title_text = "Dias Laborados")
    st.plotly_chart(fig2,use_container_width=True)
       
#------------------------------------------------------------------------------------------------------        
    colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(124, 144, 132)","rgb(224, 231, 104)"]
    fig3 = px.pie(data_selection, values='dias_laborados', names='tipo_de_novedad', color_discrete_sequence=colors
                       ,#title='Novedad Mensual Por Centro De Costos'
                       )
    fig3.update_layout(legend=dict(orientation="h"))
    st.plotly_chart(fig3,use_container_width=True)
         
#------------------------------------------------------------------------------------------------------        
  
    cc_seleccionado=cost_center[cost_center.centro_de_costo.isin(cent_cost_filter)]
    empleados_centro=cc_seleccionado.explode('empleados')
    empleados_centro=empleados_centro.empleados.apply(pd.Series)
       
    data_selection=pd.merge(empleados_centro.astype(str),data_selection.astype(str),how='left',left_on='identificacion',right_on='documento_de_identificacion')
    data_selection['dias_laborados']=data_selection['dias_laborados'].fillna(0).astype(int)
    data_selection['nombre_del_empleado']=data_selection['empleado_x']
    por_tra = (data_selection['dias_laborados']/30)*100
    data_selection['Por_tra']=por_tra
        
    data_selection['Alerta']=""
    for i in data_selection['nombre_del_empleado'].index:
     if data_selection.loc[i,'dias_laborados'] == 30:
             data_selection.loc[i,'Alerta'] = "OK"
     else:
             data_selection.loc[i,'Alerta'] = "Revisar"
        
        
    #--------------------    
    st.header("Tabla Sugeridos")
    tipo=data[(data.centro_de_costos.isin(cent_cost_filter)) & (data.año_mes==mes)]
    tipo['Alerta']=""
    for i in tipo['nombre_del_empleado'].index:
     if tipo.loc[i,'dias_laborados'] == 30:
             tipo.loc[i,'Alerta'] = "OK"
     else:
             tipo.loc[i,'Alerta'] = "Revisar"
         
    ms1=pd.unique(tipo['Alerta'])
    ms2=np.append(ms1,"Todos")
    tap=st.selectbox(
                     "Alerta:",
                     ms2,index=len(ms2)-1
                     )
        
    if "Todos" in tap:
             tap=tipo['Alerta']
    else:
             tap=[tap]
    dataf=tipo[(tipo.Alerta.isin(tap))]
    dataf[['nombre_del_empleado','documento_de_identificacion','centro_de_costos',
                'dias_laborados','año_mes','tipo_de_novedad','Alerta']]

      
    dataf=dataf.drop(["fecha","fecha_ingreso_nomina",
                           "empleado","tipo_observacion"],axis=1) 
    dataf.index = np.arange(1, len(dataf) + 1)
         
    dataf['fecha_final_novedad'] = pd.to_datetime(dataf['fecha_final_novedad']) 
    dataf['fecha_final_novedad']=dataf['fecha_final_novedad'].dt.strftime('%Y-%m-%d')
    dataf['fecha_final_novedad'] = pd.to_datetime(dataf['fecha_final_novedad']) 
    dataf['fecha_final_novedad']=dataf['fecha_final_novedad'].dt.strftime('%Y-%m-%d')
    dataf.rename(columns={'quien_reporta_la_novedad':'Quien reporta la novedad',
                        'nombre_del_empleado':'Nombre del Empleado','documento_de_identificacion':'Documento de Identificacion','centro_de_costos':'Centro de Costos',
                        'tipo_de_novedad':'Tipo de Novedad','año_mes':'Año-Mes','dias_a_facturar':'Dias a Facturar',
                        'dias_laborados':'Dias Laborados','fecha_inicial_novedad':'Fecha Inicial Novedad',
                        'fecha_final_novedad':'Fecha Final Novedad'},
               inplace=True)
    
    def to_excel(df):
             output = BytesIO()
             writer = pd.ExcelWriter(output, engine='xlsxwriter')
             df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
             #Indicate workbook and worksheet for formatting
             workbook = writer.book
             worksheet = writer.sheets['Hoja1']

             for i, col in enumerate(df.columns):
                 column_len = df[col].astype(str).str.len().max()
                 column_len = max(column_len, len(col)) + 2
                 worksheet.set_column(i, i, column_len)
             writer.save()
             processed_data = output.getvalue()
             return processed_data   
   
    Lab_xlsx = to_excel(dataf)
    st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  

   
    a=list(dataf['Centro de Costos'].unique())
    c=list(cost_center['centro_de_costo'].unique())
    cen_sin=list(set(c)-set(a))
         
    cc_nulos=pd.DataFrame(cen_sin,columns=['Centros De Costo'])
    cc_nulos.index = np.arange(1, len(cc_nulos) + 1)
        
    d=list(dataf['Nombre del Empleado'].unique())
    e=list(employees['empleado'].unique())
    em_sin=list(set(e)-set(d))
    em_nulos=pd.DataFrame(em_sin,columns=['Empleados'])
    em_nulos.index = np.arange(1, len(em_nulos) + 1)
         
         
    st.header("Sin Reporte")
    cc1,cc2=st.columns(2)
    cc1.metric(label='CENTROS DE COSTOS', value=len(cen_sin))
    cc2.metric(label='EMPLEADOS', value=len(em_sin))
         
    tab1, tab2 = st.tabs(["Centros", "Empleados"])
    with tab1:
             st.write(cc_nulos)
    with tab2:
             st.write(em_nulos)
           
    st.header('HISTORICO')
    ms1=pd.unique(data['centro_de_costos'])
    ms2=np.append(ms1,"Todos")
    vc= st.sidebar.selectbox(
          "Centro de costos:",
          ms2,index=len(ms2)-1
          )
        
    if "Todos" in vc:
             vc=data['centro_de_costos']
    else:
             vc=[vc]
    dataf=data[(data.centro_de_costos.isin(vc))]
         
    dataf=data[(data.centro_de_costos == vc)]
    ms1=pd.unique(dataf['tipo_de_novedad'])
    nov= st.selectbox(
                    "Tipo De Novedad:",
                     ms1,
                     index=len(ms1)-1
                     )
    dataf=dataf[(dataf.tipo_de_novedad == nov)]
         #data_selection = dataf.query("centro_de_costos == @vc")
    data_selection=dataf[(dataf.centro_de_costos.isin(vc)) & (dataf.tipo_de_novedad==nov)]
    data_selection["Mes"] = (pd.to_datetime(data_selection['año_mes'], format='%Y.%m.%d', errors="coerce")
                   .dt.month_name(locale='es_ES.utf8'))
        
    data_selection=data_selection.groupby(['Mes'],as_index=False)['tipo_de_novedad'].count()
         
    fig = make_subplots()
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(224, 231, 104)","rgb(147, 148, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
    fig.add_trace(go.Bar(x=data_selection['Mes'],
                              y=data_selection['tipo_de_novedad'],
                              marker_color=colors))
    fig.update_layout(title_text='Novedades',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(
             title_text = "Mes")
    fig.update_yaxes(
             title_text = "Cantidad de Empleados")
         
    st.plotly_chart(fig,use_container_width=True)     
        
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
        #st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    st.subheader('Subir Excel Actualizado')
    uploaded_file = st.file_uploader("")
    if uploaded_file is not None:
           
             # To read file as bytes:
           bytes_data = uploaded_file.getvalue()
           #st.write(bytes_data)
                    
           files = {"file":(uploaded_file.name,bytes_data,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}      
           respuesta=cargar.cargar_excel(files)
         
    with st.form("my_form"):
             day_from=cale.loc[cale['format_code'] =='F-NOM-01',['day_from']]
             day_to=cale.loc[cale['format_code'] =='F-NOM-01',['day_to']]
             
 
             today=datetime.datetime.now()
             d = st.date_input(
             "Inserta fecha",
             value=(datetime.datetime(today.year, today.month, int(day_from.values[0])), datetime.datetime(today.year, today.month, int(day_to.values[0]))),
             min_value=datetime.datetime(today.year, today.month, 1),
             max_value=datetime.datetime(today.year, today.month, 30))
             
             submitted = st.form_submit_button("Guardar")
             if submitted:
              cargar.mod_cale(d[0].day, d[1].day)
              cargar.traer_cale.clear()
              st.success('Guardado', icon="✅")
  
main()