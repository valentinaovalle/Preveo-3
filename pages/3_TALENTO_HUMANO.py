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

st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)
#from typing import List, Optional
#from tkinter import * from tkinter.ttk import *}
reduce_header_height_style = """
        <style>
            div.block-container {padding-top:0.5rem;}
        </style>
    """
st.markdown(reduce_header_height_style, unsafe_allow_html=True)


#from typing import List, Optional
#from tkinter import * from tkinter.ttk import *
def main():    
    F_TH_02,F_TH_13_B,F_TH_10=cargar.cargar_formularios_2()
    F_TH_25,F_TH_13_A,F_TH_15=cargar.cargar_formularios_4()
    F_TH_22,F_SG_07,F_SG_08,F_SG_10=cargar.cargar_formularios_7()
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
    {'icon': "", 'label':"F_TH_02"},
    {'icon':"",'label':"F_TH_13"},
    {'icon':"",'label':"F_TH_15"},
    {'icon':"",'label':"F_TH_22"},
    {'icon':"",'label':"F_TH_25"}
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

    if menu_id == "F_TH_02":
        st.write(F_TH_02)
    if menu_id == "F_TH_13":
        st.markdown(f'''<p style='background-color:#ececec;text-align: center; color:#706E6F ;font-size: 35px;'>
                           <strong>F-TH-13-A </strong><br>
                           ''',True)
        F_TH_13_A=F_TH_13_A.drop(['uuid','codigo','version','fecha_version'],axis=1)
        
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['datos_personales'], axis=1), F_TH_13_A['datos_personales'].apply(pd.Series)], axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['residencia'], axis=1), F_TH_13_A['residencia'].apply(pd.Series)], axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['vehiculo'], axis=1), F_TH_13_A['vehiculo'].apply(pd.Series)], axis=1)
        F_TH_13_A['fecha_nacimiento']=pd.to_datetime(F_TH_13_A['fecha_nacimiento'])
        F_TH_13_A['fecha_nacimiento']=F_TH_13_A['fecha_nacimiento'].dt.strftime('%Y-%m-%d')
        
        F_TH_13_A=F_TH_13_A.rename({'primer_apellido': 'APELLIDO 1','segundo_apellido':'APELLIDO 2','nombres':'NOMBRES',
            'tipo_id':'TIPO DOCUMENTO DE IDENTIDAD','identificacion':'NUMERO DE DOCUMENTO',
            'expedido_en':'EXPEDIDA EN','sexo':'SEXO','grupo_sanguineo':'RH','email_personal':'CORREO ELECTRONICO',
            'fecha_nacimiento':'FECHA DE NACIMIENTO','lugar_de_nacimiento':'LUGAR DE NACIMIENTO','departamento':'DEPARTAMENTO',
            'lugar_de_nacimiento':'LUGAR DE NACIMIENTO','direccion':'DIRECCION ACTUAL','barrio':'BARRIO',
            'ciudad':'CIUDAD DE RESIDENCIA','tipo_de_residencia':'TIPO DE RESIDENCIA',
            'la_residencia_es':'EL LUGAR DE RESIDENCIA ES','celular':'CELULAR','fijo':'TELEFONO',
            'tiene':'TIENE VEHICULO','tipo':'TIPO VEHICULO','placa':'PLACA','pase_numero':'PASE N°',
            'categoria_del_pase':'CATEGORIA'},axis=1)
        
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['estado_civil'], axis=1), F_TH_13_A['estado_civil'].apply(pd.Series)], axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['empresa_de_trabajo'], axis=1), F_TH_13_A['empresa_de_trabajo'].apply(pd.Series)], axis=1)
        F_TH_13_A['fecha_nacimiento']=pd.to_datetime(F_TH_13_A['fecha_nacimiento'])
        F_TH_13_A['fecha_nacimiento']=F_TH_13_A['fecha_nacimiento'].dt.strftime('%Y-%m-%d')
        F_TH_13_A=F_TH_13_A.rename({'estado':'ESTADO CIVIL','primer_apellido':'APELLIDO1 CONYUGE',
            'segundo_apellido':'APELLIDO2 CONYUGE','nombres':'NOMBRES CONYUGE','tipo_id':'TIPO DOCUMENTO CONYUGE',
            'identificacion':'CEDULA CONYUGE','fecha_nacimiento':'FECHA NACIMIENTO CONYUGE','trabaja':'TRABAJA',
            'empresa':'EMPRESA','telefono':'TELÉFONO'},axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['datos_familiares'], axis=1), F_TH_13_A['datos_familiares'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'hijos':'TIENE HIJOS','personas_a_cargo':'PERSONAS A CARGO'},axis=1)
        F_TH_13_A=F_TH_13_A.explode('datos_de_personas_a_cargo')
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['datos_de_personas_a_cargo'], axis=1), F_TH_13_A['datos_de_personas_a_cargo'].apply(pd.Series)], axis=1)
        F_TH_13_A['fecha_nacimiento']=pd.to_datetime(F_TH_13_A['fecha_nacimiento'])
        F_TH_13_A['fecha_nacimiento']=F_TH_13_A['fecha_nacimiento'].dt.strftime('%Y-%m-%d')
        F_TH_13_A=F_TH_13_A.rename({'parentesco':'PARENTESCO','nombres_apellidos':'NOMBRE COMPLETO',
            'fecha_nacimiento':'FECHA DE NACIMIENTO ','hermanos':'TIENE HERMANOS',
            'cuantos_hermanos':'CUANTOS HERMANOS TIENE','familiar_trabaja_en_preveo':'TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO'},axis=1)
        F_TH_13_A=F_TH_13_A[["experiencia_laboral","relacion_de_tallas","nivel_de_estudios",
        "actividades_extralaboral","afiliacion_seguridad_social","APELLIDO 1","APELLIDO 2",
        "NOMBRES","TIPO DOCUMENTO DE IDENTIDAD","NUMERO DE DOCUMENTO","EXPEDIDA EN","SEXO",
        "RH","CORREO ELECTRONICO","FECHA DE NACIMIENTO","LUGAR DE NACIMIENTO","DEPARTAMENTO",
        "DIRECCION ACTUAL","BARRIO","CIUDAD DE RESIDENCIA","TIPO DE RESIDENCIA",
        "EL LUGAR DE RESIDENCIA ES","CELULAR","TELEFONO","TIENE VEHICULO","TIPO VEHICULO",
        "PLACA","PASE N°","CATEGORIA","ESTADO CIVIL","APELLIDO1 CONYUGE","APELLIDO2 CONYUGE",
        "NOMBRES CONYUGE","TIPO DOCUMENTO CONYUGE","CEDULA CONYUGE","FECHA NACIMIENTO CONYUGE",
        "TRABAJA","EMPRESA","TELÉFONO","TIENE HIJOS","datos_de_los_hijos","PERSONAS A CARGO",
        "padre","madre","TIENE HERMANOS","CUANTOS HERMANOS TIENE","TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO","cual_familiar",
        "en_caso_de_emergencia","PARENTESCO","NOMBRE COMPLETO","FECHA DE NACIMIENTO "]]
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['cual_familiar'], axis=1), F_TH_13_A['cual_familiar'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'parentesco':'PARENTESCO FAMILIAR QUE TRABAJA EN PREVEO','area_de_la_empresa':'AREA DE LA EMPRESA EN LA QUE TRABAJA EL FAMILIAR'},axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['en_caso_de_emergencia'], axis=1), F_TH_13_A['en_caso_de_emergencia'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'nombre':'NOMBRE EN CASO DE EMERGENCIA','celular':'CELULAR EMERGENCIA',
            'direccion':'DIRECCION EMERGENCIA'},axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['madre'], axis=1), F_TH_13_A['madre'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'actualmente_vive':'VIVE LA MADRE','profesion_u_oficio':'PROFESION MADRE',
            'nombres_apellidos':'NOMBRE COMPLETO DE LA MADRE'},axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['padre'], axis=1), F_TH_13_A['padre'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'actualmente_vive':'VIVE EL PADRE','profesion_u_oficio':'PROFESION PADRE',
            'nombres_apellidos':'NOMBRE COMPLETO DEL PADRE'},axis=1)
       
        #=F_TH_13_A.explode('experiencia_laboral')
        
        #F_TH_13_A=pd.concat([F_TH_13_A.drop(['experiencia_laboral'], axis=1), F_TH_13_A['experiencia_laboral'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.join(pd.DataFrame(F_TH_13_A.experiencia_laboral.tolist(),index=F_TH_13_A.index).add_prefix('B_'))
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['B_0'], axis=1), F_TH_13_A['B_0'].apply(pd.Series)], axis=1)
        
        F_TH_13_A['fecha_de_inicio']=pd.to_datetime(F_TH_13_A['fecha_de_inicio'])
        F_TH_13_A['fecha_de_inicio']=F_TH_13_A['fecha_de_inicio'].dt.strftime('%Y-%m-%d')
        F_TH_13_A['fecha_de_finalizacion']=pd.to_datetime(F_TH_13_A['fecha_de_finalizacion'])
        F_TH_13_A['fecha_de_finalizacion']=F_TH_13_A['fecha_de_finalizacion'].dt.strftime('%Y-%m-%d')
        F_TH_13_A=F_TH_13_A.rename({'empresa_donde_laboro':'PRIMERA EMPRESA DONDE LABORO','cargo':'PRIMER CARGO QUE OCUPO',
            'fecha_de_inicio':'FECHA INICIO PRIMERA EMPRESA','fecha_de_finalizacion':'FECHA FINALIZACION PRIMERA EMPRESA',
            'jefe_inmediato':'JEFE INMEDIATO PRIMERA EMPRESA','telefono':'TELEFONO JEFE PRIMERA EMPRESA'},axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['B_1'], axis=1), F_TH_13_A['B_1'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'empresa_donde_laboro':'SEGUNDA EMPRESA DONDE LABORO','cargo':'SEGUNDO CARGO QUE OCUPO',
            'fecha_de_inicio':'FECHA INICIO SEGUNDA EMPRESA','fecha_de_finalizacion':'FECHA FINALIZACION SEGUNDA EMPRESA',
            'jefe_inmediato':'JEFE INMEDIATO SEGUNDA EMPRESA','telefono':'TELEFONO JEFE SEGUNDA EMPRESA'},axis=1)
        
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['relacion_de_tallas'], axis=1), F_TH_13_A['relacion_de_tallas'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'camisa':'TALLA CAMISA','pantalon':'TALLA PANTALON',
            'chaqueta':'TALLA CHAQUETA','botas':'TALLA BOTAS','chaleco':'TALLA CHALECO'},axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['nivel_de_estudios'], axis=1), F_TH_13_A['nivel_de_estudios'].apply(pd.Series)], axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['estudios_basicos'], axis=1), F_TH_13_A['estudios_basicos'].apply(pd.Series)], axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['primaria'], axis=1), F_TH_13_A['primaria'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'ultimo_ano_aprobado':'ULTIMO AÑO APROBADO PRIMARIA','colegio':'COLEGIO DE LA PRIMARIA'},axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['secundaria'], axis=1), F_TH_13_A['secundaria'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'ultimo_ano_aprobado':'ULTIMO AÑO APROBADO SECUNDARIA',
            'colegio':'COLEGIO DE LA SECUNDARIA','tiene_estudios_tecnicos_tecnologicos':'TIENE TECNICOS O TECNOLOGICOS'},axis=1)
        F_TH_13_A=F_TH_13_A.explode('estudios_tecnicos_tecnologicos')
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['estudios_tecnicos_tecnologicos'], axis=1), F_TH_13_A['estudios_tecnicos_tecnologicos'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'completo_el_estudio':'COMPLETO EL ESTUDIO TECNOLOGICO','estudia_actualmente':'ESTUDIA ACTUALMENTE EL TECNOLOGICO',
            'semestre':'SEMESTRE(TECNOLOGO)','carrera':'CARRERA(TECNOLOGO)','universidad_institucion':'INSTITUCION DEL TECNOLOGO','duracion':'DURACION(TECNOLOGO)',
            'fecha_de_inicio':'FECHA INICIO TECNOLOGO','fecha_de_grado':'FECHA GRADO TECNOLOGO',
            'tipo':'TIPO(TECNICO/TECNOLOGO)',
            "tiene_postgrados":'TIENE POSTGRADOS',"tiene_cursos_de_alturas":'TIENE CURSO EN ALTURAS',
            'sistema':'MANEJA SISTEMA','ingles':'INGLES'
            },axis=1)
        F_TH_13_A=F_TH_13_A[["actividades_extralaboral","afiliacion_seguridad_social","APELLIDO 1",
        "APELLIDO 2","NOMBRES","TIPO DOCUMENTO DE IDENTIDAD","NUMERO DE DOCUMENTO","EXPEDIDA EN",
        "SEXO","RH","CORREO ELECTRONICO","FECHA DE NACIMIENTO","LUGAR DE NACIMIENTO","DEPARTAMENTO",
        "DIRECCION ACTUAL","BARRIO","CIUDAD DE RESIDENCIA","TIPO DE RESIDENCIA","EL LUGAR DE RESIDENCIA ES",
        "CELULAR","TELEFONO","TIENE VEHICULO","TIPO VEHICULO","PLACA","PASE N°","CATEGORIA","ESTADO CIVIL","APELLIDO1 CONYUGE",
        "APELLIDO2 CONYUGE", "NOMBRES CONYUGE","TIPO DOCUMENTO CONYUGE",
        "CEDULA CONYUGE","FECHA NACIMIENTO CONYUGE",
         "TRABAJA","EMPRESA","TELÉFONO","TIENE HIJOS","datos_de_los_hijos","PERSONAS A CARGO",
        "TIENE HERMANOS","CUANTOS HERMANOS TIENE","TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO",
        "PARENTESCO","NOMBRE COMPLETO","FECHA DE NACIMIENTO ","PARENTESCO FAMILIAR QUE TRABAJA EN PREVEO",
        "AREA DE LA EMPRESA EN LA QUE TRABAJA EL FAMILIAR","NOMBRE EN CASO DE EMERGENCIA",
        "CELULAR EMERGENCIA","DIRECCION EMERGENCIA","NOMBRE COMPLETO DE LA MADRE",
        "PROFESION MADRE","VIVE LA MADRE","NOMBRE COMPLETO DEL PADRE",
        "PROFESION PADRE","VIVE EL PADRE","PRIMERA EMPRESA DONDE LABORO",'SEGUNDA EMPRESA DONDE LABORO','SEGUNDO CARGO QUE OCUPO',
        'FECHA INICIO SEGUNDA EMPRESA','FECHA FINALIZACION SEGUNDA EMPRESA',
        'JEFE INMEDIATO SEGUNDA EMPRESA','TELEFONO JEFE SEGUNDA EMPRESA',
        "PRIMER CARGO QUE OCUPO","FECHA INICIO PRIMERA EMPRESA","FECHA FINALIZACION PRIMERA EMPRESA","JEFE INMEDIATO PRIMERA EMPRESA",
        "TELEFONO JEFE PRIMERA EMPRESA","TALLA CAMISA","TALLA PANTALON","TALLA CHAQUETA","TALLA BOTAS","TALLA CHALECO",
        "TIENE TECNICOS O TECNOLOGICOS",
        "tiene_universitarios","universitarios","TIENE POSTGRADOS","postgrados",'TIENE CURSO EN ALTURAS',
        "cursos_de_alturas","MANEJA SISTEMA","otros_conocimientos","INGLES","otros_idioma","ULTIMO AÑO APROBADO PRIMARIA",
        "COLEGIO DE LA PRIMARIA","ULTIMO AÑO APROBADO SECUNDARIA","COLEGIO DE LA SECUNDARIA",
        "COMPLETO EL ESTUDIO TECNOLOGICO","ESTUDIA ACTUALMENTE EL TECNOLOGICO","SEMESTRE(TECNOLOGO)","CARRERA(TECNOLOGO)","INSTITUCION DEL TECNOLOGO",
        "DURACION(TECNOLOGO)","FECHA INICIO TECNOLOGO","FECHA GRADO TECNOLOGO","TIPO(TECNICO/TECNOLOGO)"
        ]]
        F_TH_13_A=F_TH_13_A.explode('universitarios')
        F_TH_13_A=F_TH_13_A.explode('postgrados')
        F_TH_13_A=F_TH_13_A.explode('otros_conocimientos')
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['universitarios'], axis=1), F_TH_13_A['universitarios'].apply(pd.Series)], axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['otros_idioma'], axis=1), F_TH_13_A['otros_idioma'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'nivel_ingles':'NIVEL DE INGLES','tarjeta_profesional':'TARJETA PROFESIONAL',
            'fecha_de_grado':'FECHA GRADO UNIVERSITARIO','fecha_de_inicio':'FECHA INICIO UNIVERSIDAD',
            'duracion':'DURACION PREGRADO','universidad_institucion':'UNIVERSIDAD PREGRADO','carrera':'PREGRADO','semestre':'SEMESTRE PREGRADO',
            'estudia_actualmente':'ESTUDIA ACTUALMENTE UN PREGRADO','completo_el_estudio':'PREGRADO COMPLETO'},axis=1)
        F_TH_13_A=F_TH_13_A[["actividades_extralaboral","afiliacion_seguridad_social",
  "APELLIDO 1","APELLIDO 2","NOMBRES","TIPO DOCUMENTO DE IDENTIDAD",
  "NUMERO DE DOCUMENTO","EXPEDIDA EN","SEXO","RH","CORREO ELECTRONICO","FECHA DE NACIMIENTO",
  "LUGAR DE NACIMIENTO","DEPARTAMENTO","DIRECCION ACTUAL","BARRIO","CIUDAD DE RESIDENCIA",
  "TIPO DE RESIDENCIA","EL LUGAR DE RESIDENCIA ES","CELULAR","TELEFONO","TIENE VEHICULO","TIPO VEHICULO",
  "PLACA","PASE N°","CATEGORIA","ESTADO CIVIL","APELLIDO1 CONYUGE",
  "APELLIDO2 CONYUGE","NOMBRES CONYUGE","TIPO DOCUMENTO CONYUGE",
  "CEDULA CONYUGE","FECHA NACIMIENTO CONYUGE","TRABAJA","EMPRESA","TELÉFONO","TIENE HIJOS",
  "datos_de_los_hijos","PERSONAS A CARGO","TIENE HERMANOS","CUANTOS HERMANOS TIENE",
  "TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO","PARENTESCO","NOMBRE COMPLETO","FECHA DE NACIMIENTO ",
  "PARENTESCO FAMILIAR QUE TRABAJA EN PREVEO","AREA DE LA EMPRESA EN LA QUE TRABAJA EL FAMILIAR",
  "NOMBRE EN CASO DE EMERGENCIA","CELULAR EMERGENCIA","DIRECCION EMERGENCIA","NOMBRE COMPLETO DE LA MADRE",
  "PROFESION MADRE","VIVE LA MADRE","NOMBRE COMPLETO DEL PADRE","PROFESION PADRE","VIVE EL PADRE",
  "PRIMERA EMPRESA DONDE LABORO",'SEGUNDA EMPRESA DONDE LABORO','SEGUNDO CARGO QUE OCUPO',
  'FECHA INICIO SEGUNDA EMPRESA','FECHA FINALIZACION SEGUNDA EMPRESA',
  'JEFE INMEDIATO SEGUNDA EMPRESA','TELEFONO JEFE SEGUNDA EMPRESA',
  "PRIMER CARGO QUE OCUPO","FECHA INICIO PRIMERA EMPRESA","FECHA FINALIZACION PRIMERA EMPRESA","JEFE INMEDIATO PRIMERA EMPRESA",
  "TELEFONO JEFE PRIMERA EMPRESA","TALLA CAMISA",
  "TALLA PANTALON","TALLA CHAQUETA","TALLA BOTAS","TALLA CHALECO","TIENE TECNICOS O TECNOLOGICOS",
  "tiene_universitarios","TIENE POSTGRADOS","postgrados","TIENE CURSO EN ALTURAS",
  "cursos_de_alturas","MANEJA SISTEMA","otros_conocimientos",
  "INGLES","ULTIMO AÑO APROBADO PRIMARIA","COLEGIO DE LA PRIMARIA","ULTIMO AÑO APROBADO SECUNDARIA",
  "COLEGIO DE LA SECUNDARIA","COMPLETO EL ESTUDIO TECNOLOGICO",
  "ESTUDIA ACTUALMENTE EL TECNOLOGICO","SEMESTRE(TECNOLOGO)","CARRERA(TECNOLOGO)","INSTITUCION DEL TECNOLOGO",
  "DURACION(TECNOLOGO)","FECHA INICIO TECNOLOGO","FECHA GRADO TECNOLOGO","TIPO(TECNICO/TECNOLOGO)",
  "PREGRADO COMPLETO","ESTUDIA ACTUALMENTE UN PREGRADO","SEMESTRE PREGRADO","PREGRADO","UNIVERSIDAD PREGRADO",
  "DURACION PREGRADO","FECHA INICIO UNIVERSIDAD","FECHA GRADO UNIVERSITARIO","TARJETA PROFESIONAL",
  "NIVEL DE INGLES"
]]
        #columns_names = F_TH_13_A.columns.values
        #columns_names_list = list(columns_names)
        #st.write(columns_names_list)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['otros_conocimientos'], axis=1), F_TH_13_A['otros_conocimientos'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'tipo_de_conocimiento':'TIPO DE CONOCIMIENTO',
            'nombre_de_conocimiento':'NOMBRE DEL CONOCIMIENTO','nivel':'NIVEL DEL CONOCIMIENTO'},axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['actividades_extralaboral'], axis=1), F_TH_13_A['actividades_extralaboral'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'deportivas':'DEPORTIVAS','culturales':'CULTURALES',
            'familiares':'FAMILIARES','recreativas':'RECREATIVAS','otras':'OTRA ACTIVIDAD','cual':'CUAL ACTIVIDAD',
            'actividad_que_le_gustaria_en_la_empresa':'ACTIVIDAD QUE LE GUSTARIA EN LA EMPRESA'},axis=1)
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['afiliacion_seguridad_social'], axis=1), F_TH_13_A['afiliacion_seguridad_social'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'eps':'EPS','fondo_de_pensiones':'FONDO DE PENSIONES'},axis=1)
        F_TH_13_A=F_TH_13_A[["APELLIDO 1","APELLIDO 2","NOMBRES","TIPO DOCUMENTO DE IDENTIDAD",
  "NUMERO DE DOCUMENTO","EXPEDIDA EN","SEXO","RH","CORREO ELECTRONICO","FECHA DE NACIMIENTO",
  "LUGAR DE NACIMIENTO","DEPARTAMENTO","DIRECCION ACTUAL","BARRIO","CIUDAD DE RESIDENCIA",
  "TIPO DE RESIDENCIA","EL LUGAR DE RESIDENCIA ES","CELULAR","TELEFONO","TIENE VEHICULO",
  "TIPO VEHICULO","PLACA","PASE N°","CATEGORIA","ESTADO CIVIL","APELLIDO1 CONYUGE","APELLIDO2 CONYUGE",
  "NOMBRES CONYUGE","TIPO DOCUMENTO CONYUGE","CEDULA CONYUGE","FECHA NACIMIENTO CONYUGE",
  "TRABAJA","EMPRESA","TELÉFONO","TIENE HIJOS","datos_de_los_hijos","PERSONAS A CARGO",
  "TIENE HERMANOS","CUANTOS HERMANOS TIENE","TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO",
  "PARENTESCO","NOMBRE COMPLETO","FECHA DE NACIMIENTO ","PARENTESCO FAMILIAR QUE TRABAJA EN PREVEO",
  "AREA DE LA EMPRESA EN LA QUE TRABAJA EL FAMILIAR","NOMBRE EN CASO DE EMERGENCIA",
  "CELULAR EMERGENCIA","DIRECCION EMERGENCIA","NOMBRE COMPLETO DE LA MADRE","PROFESION MADRE","VIVE LA MADRE",
  "NOMBRE COMPLETO DEL PADRE","PROFESION PADRE","VIVE EL PADRE",
  "PRIMERA EMPRESA DONDE LABORO",'SEGUNDA EMPRESA DONDE LABORO','SEGUNDO CARGO QUE OCUPO',
        'FECHA INICIO SEGUNDA EMPRESA','FECHA FINALIZACION SEGUNDA EMPRESA',
        'JEFE INMEDIATO SEGUNDA EMPRESA','TELEFONO JEFE SEGUNDA EMPRESA',
        "PRIMER CARGO QUE OCUPO","FECHA INICIO PRIMERA EMPRESA","FECHA FINALIZACION PRIMERA EMPRESA","JEFE INMEDIATO PRIMERA EMPRESA",
        "TELEFONO JEFE PRIMERA EMPRESA",
  "TALLA CAMISA","TALLA PANTALON","TALLA CHAQUETA","TALLA BOTAS","TALLA CHALECO",
  "TIENE TECNICOS O TECNOLOGICOS","tiene_universitarios","TIENE POSTGRADOS","postgrados","TIENE CURSO EN ALTURAS",
  "cursos_de_alturas","MANEJA SISTEMA","INGLES","ULTIMO AÑO APROBADO PRIMARIA",
  "COLEGIO DE LA PRIMARIA","ULTIMO AÑO APROBADO SECUNDARIA",
  "COLEGIO DE LA SECUNDARIA","COMPLETO EL ESTUDIO TECNOLOGICO",
  "ESTUDIA ACTUALMENTE EL TECNOLOGICO","SEMESTRE(TECNOLOGO)",
  "CARRERA(TECNOLOGO)","INSTITUCION DEL TECNOLOGO", "DURACION(TECNOLOGO)","FECHA INICIO TECNOLOGO",
  "FECHA GRADO TECNOLOGO","TIPO(TECNICO/TECNOLOGO)","PREGRADO COMPLETO","ESTUDIA ACTUALMENTE UN PREGRADO",
  "SEMESTRE PREGRADO","PREGRADO","UNIVERSIDAD PREGRADO",
  "DURACION PREGRADO","FECHA INICIO UNIVERSIDAD","FECHA GRADO UNIVERSITARIO","TARJETA PROFESIONAL",
  "NIVEL DE INGLES","TIPO DE CONOCIMIENTO","NOMBRE DEL CONOCIMIENTO","NIVEL DEL CONOCIMIENTO","DEPORTIVAS",
  "CULTURALES","FAMILIARES","RECREATIVAS","OTRA ACTIVIDAD",
  "CUAL ACTIVIDAD","ACTIVIDAD QUE LE GUSTARIA EN LA EMPRESA",
  "EPS","FONDO DE PENSIONES"

]]
     
        F_TH_13_A=pd.concat([F_TH_13_A.drop(['postgrados'], axis=1), F_TH_13_A['postgrados'].apply(pd.Series)], axis=1)
        F_TH_13_A=F_TH_13_A.rename({'completo_el_estudio':'COMPLETO EL POSTGRADO','estudia_actualmente':'ACTUALMENTE ESTUDIA EL POSTGRADO',
            'semestre':'SEMESTRE POSTGRADO','carrera':'POSTGRADO','universidad_institucion':'INSTITUCION DONDE REALIZO EL POSTGRADO',
            'duracion':'DURACION POSTGRADO','fecha_de_inicio':'FECHA INICIO POSTGRADO','fecha_de_grado':'FECHA GRADO DEL POSTGRADO',
            },axis=1)
        F_TH_13_A=F_TH_13_A[["APELLIDO 1","APELLIDO 2","NOMBRES","TIPO DOCUMENTO DE IDENTIDAD",
  "NUMERO DE DOCUMENTO","EXPEDIDA EN","SEXO","RH","CORREO ELECTRONICO","FECHA DE NACIMIENTO","LUGAR DE NACIMIENTO",
  "DEPARTAMENTO","DIRECCION ACTUAL","BARRIO","CIUDAD DE RESIDENCIA","TIPO DE RESIDENCIA","EL LUGAR DE RESIDENCIA ES",
  "CELULAR","TELEFONO","TIENE VEHICULO","TIPO VEHICULO","PLACA","PASE N°",
  "CATEGORIA","ESTADO CIVIL","APELLIDO1 CONYUGE","APELLIDO2 CONYUGE",
  "NOMBRES CONYUGE","TIPO DOCUMENTO CONYUGE","CEDULA CONYUGE","FECHA NACIMIENTO CONYUGE",
  "TRABAJA","EMPRESA","TELÉFONO","TIENE HIJOS",
  "datos_de_los_hijos","PERSONAS A CARGO","TIENE HERMANOS","CUANTOS HERMANOS TIENE",
  "TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO",
  "PARENTESCO","NOMBRE COMPLETO","FECHA DE NACIMIENTO ","PARENTESCO FAMILIAR QUE TRABAJA EN PREVEO",
  "AREA DE LA EMPRESA EN LA QUE TRABAJA EL FAMILIAR",
  "NOMBRE EN CASO DE EMERGENCIA","CELULAR EMERGENCIA","DIRECCION EMERGENCIA",
  "NOMBRE COMPLETO DE LA MADRE","PROFESION MADRE","VIVE LA MADRE",
  "NOMBRE COMPLETO DEL PADRE","PROFESION PADRE","VIVE EL PADRE",
  "PRIMERA EMPRESA DONDE LABORO",'SEGUNDA EMPRESA DONDE LABORO','SEGUNDO CARGO QUE OCUPO',
  'FECHA INICIO SEGUNDA EMPRESA','FECHA FINALIZACION SEGUNDA EMPRESA',
  'JEFE INMEDIATO SEGUNDA EMPRESA','TELEFONO JEFE SEGUNDA EMPRESA',
  "PRIMER CARGO QUE OCUPO","FECHA INICIO PRIMERA EMPRESA","FECHA FINALIZACION PRIMERA EMPRESA","JEFE INMEDIATO PRIMERA EMPRESA",
  "TELEFONO JEFE PRIMERA EMPRESA",
  "TALLA CAMISA","TALLA PANTALON","TALLA CHAQUETA","TALLA BOTAS","TALLA CHALECO","TIENE TECNICOS O TECNOLOGICOS",
  "tiene_universitarios","TIENE POSTGRADOS","TIENE CURSO EN ALTURAS","cursos_de_alturas","MANEJA SISTEMA",
  "INGLES","ULTIMO AÑO APROBADO PRIMARIA",
  "COLEGIO DE LA PRIMARIA","ULTIMO AÑO APROBADO SECUNDARIA",
  "COLEGIO DE LA SECUNDARIA","COMPLETO EL ESTUDIO TECNOLOGICO",
  "ESTUDIA ACTUALMENTE EL TECNOLOGICO",
  "SEMESTRE(TECNOLOGO)","CARRERA(TECNOLOGO)","INSTITUCION DEL TECNOLOGO",
  "DURACION(TECNOLOGO)","FECHA INICIO TECNOLOGO",
  "FECHA GRADO TECNOLOGO","TIPO(TECNICO/TECNOLOGO)","PREGRADO COMPLETO","ESTUDIA ACTUALMENTE UN PREGRADO",
  "SEMESTRE PREGRADO","PREGRADO","UNIVERSIDAD PREGRADO",
  "DURACION PREGRADO","FECHA INICIO UNIVERSIDAD","FECHA GRADO UNIVERSITARIO",
  "TARJETA PROFESIONAL","NIVEL DE INGLES","TIPO DE CONOCIMIENTO","NOMBRE DEL CONOCIMIENTO","NIVEL DEL CONOCIMIENTO","DEPORTIVAS",
  "CULTURALES","FAMILIARES","RECREATIVAS","OTRA ACTIVIDAD",
  "CUAL ACTIVIDAD","ACTIVIDAD QUE LE GUSTARIA EN LA EMPRESA",
  "EPS","FONDO DE PENSIONES",'COMPLETO EL POSTGRADO','ACTUALMENTE ESTUDIA EL POSTGRADO',
            'SEMESTRE POSTGRADO','POSTGRADO','INSTITUCION DONDE REALIZO EL POSTGRADO',
            'DURACION POSTGRADO','FECHA INICIO POSTGRADO','FECHA GRADO DEL POSTGRADO',
            

]]
        F_TH_13_A=F_TH_13_A.astype(str)
        F_TH_13_A=F_TH_13_A.replace({"True": 'SI', "False": 'NO','nan':' ','None':' '})
        
        Lab_xlsx = to_excel(F_TH_13_A)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_TH_13_A.assign(hack='').set_index('hack'))
        
        st.markdown(f'''<p style='background-color:#ececec;text-align: center; color:#706E6F ;font-size: 35px;'>
                           <strong>F-TH-13-B </strong><br>
                           ''',True)
        
        
        st.write(F_TH_13_B)
        F_TH_13_B=F_TH_13_B.drop(['uuid','codigo','version','fecha_version'],axis=1)
        
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['datos_personales'], axis=1), F_TH_13_B['datos_personales'].apply(pd.Series)], axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['residencia'], axis=1), F_TH_13_B['residencia'].apply(pd.Series)], axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['vehiculo'], axis=1), F_TH_13_B['vehiculo'].apply(pd.Series)], axis=1)
        F_TH_13_B['fecha_nacimiento']=pd.to_datetime(F_TH_13_B['fecha_nacimiento'])
        F_TH_13_B['fecha_nacimiento']=F_TH_13_B['fecha_nacimiento'].dt.strftime('%Y-%m-%d')
        
        F_TH_13_B=F_TH_13_B.rename({'primer_apellido': 'APELLIDO 1','segundo_apellido':'APELLIDO 2','nombres':'NOMBRES',
            'tipo_id':'TIPO DOCUMENTO DE IDENTIDAD','identificacion':'NUMERO DE DOCUMENTO',
            'expedido_en':'EXPEDIDA EN','sexo':'SEXO','grupo_sanguineo':'RH','email_personal':'CORREO ELECTRONICO',
            'fecha_nacimiento':'FECHA DE NACIMIENTO','lugar_de_nacimiento':'LUGAR DE NACIMIENTO','departamento':'DEPARTAMENTO',
            'lugar_de_nacimiento':'LUGAR DE NACIMIENTO','direccion':'DIRECCION ACTUAL','barrio':'BARRIO',
            'ciudad':'CIUDAD DE RESIDENCIA','tipo_de_residencia':'TIPO DE RESIDENCIA',
            'la_residencia_es':'EL LUGAR DE RESIDENCIA ES','celular':'CELULAR','fijo':'TELEFONO',
            'tiene':'TIENE VEHICULO','tipo':'TIPO VEHICULO','placa':'PLACA','pase_numero':'PASE N°',
            'categoria_del_pase':'CATEGORIA'},axis=1)
        
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['estado_civil'], axis=1), F_TH_13_B['estado_civil'].apply(pd.Series)], axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['empresa_de_trabajo'], axis=1), F_TH_13_B['empresa_de_trabajo'].apply(pd.Series)], axis=1)
        F_TH_13_B['fecha_nacimiento']=pd.to_datetime(F_TH_13_B['fecha_nacimiento'])
        F_TH_13_B['fecha_nacimiento']=F_TH_13_B['fecha_nacimiento'].dt.strftime('%Y-%m-%d')
        F_TH_13_B=F_TH_13_B.rename({'estado':'ESTADO CIVIL','primer_apellido':'APELLIDO1 CONYUGE',
            'segundo_apellido':'APELLIDO2 CONYUGE','nombres':'NOMBRES CONYUGE','tipo_id':'TIPO DOCUMENTO CONYUGE',
            'identificacion':'CEDULA CONYUGE','fecha_nacimiento':'FECHA NACIMIENTO CONYUGE','trabaja':'TRABAJA',
            'empresa':'EMPRESA','telefono':'TELÉFONO'},axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['datos_familiares'], axis=1), F_TH_13_B['datos_familiares'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'hijos':'TIENE HIJOS','personas_a_cargo':'PERSONAS A CARGO'},axis=1)
        F_TH_13_B=F_TH_13_B.explode('datos_de_personas_a_cargo')
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['datos_de_personas_a_cargo'], axis=1), F_TH_13_B['datos_de_personas_a_cargo'].apply(pd.Series)], axis=1)
        F_TH_13_B['fecha_nacimiento']=pd.to_datetime(F_TH_13_B['fecha_nacimiento'])
        F_TH_13_B['fecha_nacimiento']=F_TH_13_B['fecha_nacimiento'].dt.strftime('%Y-%m-%d')
        F_TH_13_B=F_TH_13_B.rename({'parentesco':'PARENTESCO','nombres_apellidos':'NOMBRE COMPLETO',
            'fecha_nacimiento':'FECHA DE NACIMIENTO ','hermanos':'TIENE HERMANOS',
            'cuantos_hermanos':'CUANTOS HERMANOS TIENE','familiar_trabaja_en_preveo':'TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO'},axis=1)
        F_TH_13_B=F_TH_13_B[["experiencia_laboral","relacion_de_tallas","nivel_de_estudios",
        "actividades_extralaboral","afiliacion_seguridad_social","APELLIDO 1","APELLIDO 2",
        "NOMBRES","TIPO DOCUMENTO DE IDENTIDAD","NUMERO DE DOCUMENTO","EXPEDIDA EN","SEXO",
        "RH","CORREO ELECTRONICO","FECHA DE NACIMIENTO","LUGAR DE NACIMIENTO","DEPARTAMENTO",
        "DIRECCION ACTUAL","BARRIO","CIUDAD DE RESIDENCIA","TIPO DE RESIDENCIA",
        "EL LUGAR DE RESIDENCIA ES","CELULAR","TELEFONO","TIENE VEHICULO","TIPO VEHICULO",
        "PLACA","PASE N°","CATEGORIA","ESTADO CIVIL","APELLIDO1 CONYUGE","APELLIDO2 CONYUGE",
        "NOMBRES CONYUGE","TIPO DOCUMENTO CONYUGE","CEDULA CONYUGE","FECHA NACIMIENTO CONYUGE",
        "TRABAJA","EMPRESA","TELÉFONO","TIENE HIJOS","datos_de_los_hijos","PERSONAS A CARGO",
        "padre","madre","TIENE HERMANOS","CUANTOS HERMANOS TIENE","TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO","cual_familiar",
        "en_caso_de_emergencia","PARENTESCO","NOMBRE COMPLETO","FECHA DE NACIMIENTO "]]
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['cual_familiar'], axis=1), F_TH_13_B['cual_familiar'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'parentesco':'PARENTESCO FAMILIAR QUE TRABAJA EN PREVEO','area_de_la_empresa':'AREA DE LA EMPRESA EN LA QUE TRABAJA EL FAMILIAR'},axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['en_caso_de_emergencia'], axis=1), F_TH_13_B['en_caso_de_emergencia'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'nombre':'NOMBRE EN CASO DE EMERGENCIA','celular':'CELULAR EMERGENCIA',
            'direccion':'DIRECCION EMERGENCIA'},axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['madre'], axis=1), F_TH_13_B['madre'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'actualmente_vive':'VIVE LA MADRE','profesion_u_oficio':'PROFESION MADRE',
            'nombres_apellidos':'NOMBRE COMPLETO DE LA MADRE'},axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['padre'], axis=1), F_TH_13_B['padre'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'actualmente_vive':'VIVE EL PADRE','profesion_u_oficio':'PROFESION PADRE',
            'nombres_apellidos':'NOMBRE COMPLETO DEL PADRE'},axis=1)
       
        #=F_TH_13_A.explode('experiencia_laboral')
        
        #F_TH_13_A=pd.concat([F_TH_13_A.drop(['experiencia_laboral'], axis=1), F_TH_13_A['experiencia_laboral'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.join(pd.DataFrame(F_TH_13_B.experiencia_laboral.tolist(),index=F_TH_13_B.index).add_prefix('B_'))
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['B_0'], axis=1), F_TH_13_B['B_0'].apply(pd.Series)], axis=1)
        
        F_TH_13_B['fecha_de_inicio']=pd.to_datetime(F_TH_13_B['fecha_de_inicio'])
        F_TH_13_B['fecha_de_inicio']=F_TH_13_B['fecha_de_inicio'].dt.strftime('%Y-%m-%d')
        F_TH_13_B['fecha_de_finalizacion']=pd.to_datetime(F_TH_13_B['fecha_de_finalizacion'])
        F_TH_13_B['fecha_de_finalizacion']=F_TH_13_B['fecha_de_finalizacion'].dt.strftime('%Y-%m-%d')
        F_TH_13_B=F_TH_13_B.rename({'empresa_donde_laboro':'PRIMERA EMPRESA DONDE LABORO','cargo':'PRIMER CARGO QUE OCUPO',
            'fecha_de_inicio':'FECHA INICIO PRIMERA EMPRESA','fecha_de_finalizacion':'FECHA FINALIZACION PRIMERA EMPRESA',
            'jefe_inmediato':'JEFE INMEDIATO PRIMERA EMPRESA','telefono':'TELEFONO JEFE PRIMERA EMPRESA'},axis=1)
        
        #F_TH_13_B=pd.concat([F_TH_13_B.drop(['B_1'], axis=1), F_TH_13_B['B_1'].apply(pd.Series)], axis=1)
        #F_TH_13_B=F_TH_13_B.rename({'empresa_donde_laboro':'SEGUNDA EMPRESA DONDE LABORO','cargo':'SEGUNDO CARGO QUE OCUPO',
         #   'fecha_de_inicio':'FECHA INICIO SEGUNDA EMPRESA','fecha_de_finalizacion':'FECHA FINALIZACION SEGUNDA EMPRESA',
          #  'jefe_inmediato':'JEFE INMEDIATO SEGUNDA EMPRESA','telefono':'TELEFONO JEFE SEGUNDA EMPRESA'},axis=1)
        
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['relacion_de_tallas'], axis=1), F_TH_13_B['relacion_de_tallas'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'camisa':'TALLA CAMISA','pantalon':'TALLA PANTALON',
            'chaqueta':'TALLA CHAQUETA','botas':'TALLA BOTAS','chaleco':'TALLA CHALECO'},axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['nivel_de_estudios'], axis=1), F_TH_13_B['nivel_de_estudios'].apply(pd.Series)], axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['estudios_basicos'], axis=1), F_TH_13_B['estudios_basicos'].apply(pd.Series)], axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['primaria'], axis=1), F_TH_13_B['primaria'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'ultimo_ano_aprobado':'ULTIMO AÑO APROBADO PRIMARIA','colegio':'COLEGIO DE LA PRIMARIA'},axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['secundaria'], axis=1), F_TH_13_B['secundaria'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'ultimo_ano_aprobado':'ULTIMO AÑO APROBADO SECUNDARIA',
            'colegio':'COLEGIO DE LA SECUNDARIA','tiene_estudios_tecnicos_tecnologicos':'TIENE TECNICOS O TECNOLOGICOS'},axis=1)
        F_TH_13_B=F_TH_13_B.explode('estudios_tecnicos_tecnologicos')
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['estudios_tecnicos_tecnologicos'], axis=1), F_TH_13_B['estudios_tecnicos_tecnologicos'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'completo_el_estudio':'COMPLETO EL ESTUDIO TECNOLOGICO','estudia_actualmente':'ESTUDIA ACTUALMENTE EL TECNOLOGICO',
            'semestre':'SEMESTRE(TECNOLOGO)','carrera':'CARRERA(TECNOLOGO)','universidad_institucion':'INSTITUCION DEL TECNOLOGO','duracion':'DURACION(TECNOLOGO)',
            'fecha_de_inicio':'FECHA INICIO TECNOLOGO','fecha_de_grado':'FECHA GRADO TECNOLOGO',
            'tipo':'TIPO(TECNICO/TECNOLOGO)',
            "tiene_postgrados":'TIENE POSTGRADOS',"tiene_cursos_de_alturas":'TIENE CURSO EN ALTURAS',
            'sistema':'MANEJA SISTEMA','ingles':'INGLES'
            },axis=1)
        F_TH_13_B=F_TH_13_B[["actividades_extralaboral","afiliacion_seguridad_social","APELLIDO 1",
        "APELLIDO 2","NOMBRES","TIPO DOCUMENTO DE IDENTIDAD","NUMERO DE DOCUMENTO","EXPEDIDA EN",
        "SEXO","RH","CORREO ELECTRONICO","FECHA DE NACIMIENTO","LUGAR DE NACIMIENTO","DEPARTAMENTO",
        "DIRECCION ACTUAL","BARRIO","CIUDAD DE RESIDENCIA","TIPO DE RESIDENCIA","EL LUGAR DE RESIDENCIA ES",
        "CELULAR","TELEFONO","TIENE VEHICULO","TIPO VEHICULO","PLACA","PASE N°","CATEGORIA","ESTADO CIVIL","APELLIDO1 CONYUGE",
        "APELLIDO2 CONYUGE", "NOMBRES CONYUGE","TIPO DOCUMENTO CONYUGE",
        "CEDULA CONYUGE","FECHA NACIMIENTO CONYUGE",
         "TRABAJA","EMPRESA","TELÉFONO","TIENE HIJOS","datos_de_los_hijos","PERSONAS A CARGO",
        "TIENE HERMANOS","CUANTOS HERMANOS TIENE","TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO",
        "PARENTESCO","NOMBRE COMPLETO","FECHA DE NACIMIENTO ","PARENTESCO FAMILIAR QUE TRABAJA EN PREVEO",
        "AREA DE LA EMPRESA EN LA QUE TRABAJA EL FAMILIAR","NOMBRE EN CASO DE EMERGENCIA",
        "CELULAR EMERGENCIA","DIRECCION EMERGENCIA","NOMBRE COMPLETO DE LA MADRE",
        "PROFESION MADRE","VIVE LA MADRE","NOMBRE COMPLETO DEL PADRE",
        "PROFESION PADRE","VIVE EL PADRE","PRIMERA EMPRESA DONDE LABORO",
        "PRIMER CARGO QUE OCUPO","FECHA INICIO PRIMERA EMPRESA","FECHA FINALIZACION PRIMERA EMPRESA","JEFE INMEDIATO PRIMERA EMPRESA",
        "TELEFONO JEFE PRIMERA EMPRESA","TALLA CAMISA","TALLA PANTALON","TALLA CHAQUETA","TALLA BOTAS","TALLA CHALECO",
        "TIENE TECNICOS O TECNOLOGICOS",
        "tiene_universitarios","universitarios","TIENE POSTGRADOS","postgrados",'TIENE CURSO EN ALTURAS',
        "cursos_de_alturas","MANEJA SISTEMA","otros_conocimientos","INGLES","otros_idioma","ULTIMO AÑO APROBADO PRIMARIA",
        "COLEGIO DE LA PRIMARIA","ULTIMO AÑO APROBADO SECUNDARIA","COLEGIO DE LA SECUNDARIA",
        "COMPLETO EL ESTUDIO TECNOLOGICO","ESTUDIA ACTUALMENTE EL TECNOLOGICO","SEMESTRE(TECNOLOGO)","CARRERA(TECNOLOGO)","INSTITUCION DEL TECNOLOGO",
        "DURACION(TECNOLOGO)","FECHA INICIO TECNOLOGO","FECHA GRADO TECNOLOGO","TIPO(TECNICO/TECNOLOGO)"
        ]]
        F_TH_13_B=F_TH_13_B.explode('universitarios')
        F_TH_13_B=F_TH_13_B.explode('postgrados')
        F_TH_13_B=F_TH_13_B.explode('otros_conocimientos')
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['universitarios'], axis=1), F_TH_13_B['universitarios'].apply(pd.Series)], axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['otros_idioma'], axis=1), F_TH_13_B['otros_idioma'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'nivel_ingles':'NIVEL DE INGLES','tarjeta_profesional':'TARJETA PROFESIONAL',
            'fecha_de_grado':'FECHA GRADO UNIVERSITARIO','fecha_de_inicio':'FECHA INICIO UNIVERSIDAD',
            'duracion':'DURACION PREGRADO','universidad_institucion':'UNIVERSIDAD PREGRADO','carrera':'PREGRADO','semestre':'SEMESTRE PREGRADO',
            'estudia_actualmente':'ESTUDIA ACTUALMENTE UN PREGRADO','completo_el_estudio':'PREGRADO COMPLETO'},axis=1)
        F_TH_13_B=F_TH_13_B[["actividades_extralaboral","afiliacion_seguridad_social",
  "APELLIDO 1","APELLIDO 2","NOMBRES","TIPO DOCUMENTO DE IDENTIDAD",
  "NUMERO DE DOCUMENTO","EXPEDIDA EN","SEXO","RH","CORREO ELECTRONICO","FECHA DE NACIMIENTO",
  "LUGAR DE NACIMIENTO","DEPARTAMENTO","DIRECCION ACTUAL","BARRIO","CIUDAD DE RESIDENCIA",
  "TIPO DE RESIDENCIA","EL LUGAR DE RESIDENCIA ES","CELULAR","TELEFONO","TIENE VEHICULO","TIPO VEHICULO",
  "PLACA","PASE N°","CATEGORIA","ESTADO CIVIL","APELLIDO1 CONYUGE",
  "APELLIDO2 CONYUGE","NOMBRES CONYUGE","TIPO DOCUMENTO CONYUGE",
  "CEDULA CONYUGE","FECHA NACIMIENTO CONYUGE","TRABAJA","EMPRESA","TELÉFONO","TIENE HIJOS",
  "datos_de_los_hijos","PERSONAS A CARGO","TIENE HERMANOS","CUANTOS HERMANOS TIENE",
  "TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO","PARENTESCO","NOMBRE COMPLETO","FECHA DE NACIMIENTO ",
  "PARENTESCO FAMILIAR QUE TRABAJA EN PREVEO","AREA DE LA EMPRESA EN LA QUE TRABAJA EL FAMILIAR",
  "NOMBRE EN CASO DE EMERGENCIA","CELULAR EMERGENCIA","DIRECCION EMERGENCIA","NOMBRE COMPLETO DE LA MADRE",
  "PROFESION MADRE","VIVE LA MADRE","NOMBRE COMPLETO DEL PADRE","PROFESION PADRE","VIVE EL PADRE",
  "PRIMERA EMPRESA DONDE LABORO",
  "PRIMER CARGO QUE OCUPO","FECHA INICIO PRIMERA EMPRESA","FECHA FINALIZACION PRIMERA EMPRESA","JEFE INMEDIATO PRIMERA EMPRESA",
  "TELEFONO JEFE PRIMERA EMPRESA","TALLA CAMISA",
  "TALLA PANTALON","TALLA CHAQUETA","TALLA BOTAS","TALLA CHALECO","TIENE TECNICOS O TECNOLOGICOS",
  "tiene_universitarios","TIENE POSTGRADOS","postgrados","TIENE CURSO EN ALTURAS",
  "cursos_de_alturas","MANEJA SISTEMA","otros_conocimientos",
  "INGLES","ULTIMO AÑO APROBADO PRIMARIA","COLEGIO DE LA PRIMARIA","ULTIMO AÑO APROBADO SECUNDARIA",
  "COLEGIO DE LA SECUNDARIA","COMPLETO EL ESTUDIO TECNOLOGICO",
  "ESTUDIA ACTUALMENTE EL TECNOLOGICO","SEMESTRE(TECNOLOGO)","CARRERA(TECNOLOGO)","INSTITUCION DEL TECNOLOGO",
  "DURACION(TECNOLOGO)","FECHA INICIO TECNOLOGO","FECHA GRADO TECNOLOGO","TIPO(TECNICO/TECNOLOGO)",
  "PREGRADO COMPLETO","ESTUDIA ACTUALMENTE UN PREGRADO","SEMESTRE PREGRADO","PREGRADO","UNIVERSIDAD PREGRADO",
  "DURACION PREGRADO","FECHA INICIO UNIVERSIDAD","FECHA GRADO UNIVERSITARIO","TARJETA PROFESIONAL",
  "NIVEL DE INGLES"
]]
        #columns_names = F_TH_13_A.columns.values
        #columns_names_list = list(columns_names)
        #st.write(columns_names_list)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['otros_conocimientos'], axis=1), F_TH_13_B['otros_conocimientos'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'tipo_de_conocimiento':'TIPO DE CONOCIMIENTO',
            'nombre_de_conocimiento':'NOMBRE DEL CONOCIMIENTO','nivel':'NIVEL DEL CONOCIMIENTO'},axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['actividades_extralaboral'], axis=1), F_TH_13_B['actividades_extralaboral'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'deportivas':'DEPORTIVAS','culturales':'CULTURALES',
            'familiares':'FAMILIARES','recreativas':'RECREATIVAS','otras':'OTRA ACTIVIDAD','cual':'CUAL ACTIVIDAD',
            'actividad_que_le_gustaria_en_la_empresa':'ACTIVIDAD QUE LE GUSTARIA EN LA EMPRESA'},axis=1)
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['afiliacion_seguridad_social'], axis=1), F_TH_13_B['afiliacion_seguridad_social'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'eps':'EPS','fondo_de_pensiones':'FONDO DE PENSIONES'},axis=1)
        F_TH_13_B=F_TH_13_B[["APELLIDO 1","APELLIDO 2","NOMBRES","TIPO DOCUMENTO DE IDENTIDAD",
  "NUMERO DE DOCUMENTO","EXPEDIDA EN","SEXO","RH","CORREO ELECTRONICO","FECHA DE NACIMIENTO",
  "LUGAR DE NACIMIENTO","DEPARTAMENTO","DIRECCION ACTUAL","BARRIO","CIUDAD DE RESIDENCIA",
  "TIPO DE RESIDENCIA","EL LUGAR DE RESIDENCIA ES","CELULAR","TELEFONO","TIENE VEHICULO",
  "TIPO VEHICULO","PLACA","PASE N°","CATEGORIA","ESTADO CIVIL","APELLIDO1 CONYUGE","APELLIDO2 CONYUGE",
  "NOMBRES CONYUGE","TIPO DOCUMENTO CONYUGE","CEDULA CONYUGE","FECHA NACIMIENTO CONYUGE",
  "TRABAJA","EMPRESA","TELÉFONO","TIENE HIJOS","datos_de_los_hijos","PERSONAS A CARGO",
  "TIENE HERMANOS","CUANTOS HERMANOS TIENE","TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO",
  "PARENTESCO","NOMBRE COMPLETO","FECHA DE NACIMIENTO ","PARENTESCO FAMILIAR QUE TRABAJA EN PREVEO",
  "AREA DE LA EMPRESA EN LA QUE TRABAJA EL FAMILIAR","NOMBRE EN CASO DE EMERGENCIA",
  "CELULAR EMERGENCIA","DIRECCION EMERGENCIA","NOMBRE COMPLETO DE LA MADRE","PROFESION MADRE","VIVE LA MADRE",
  "NOMBRE COMPLETO DEL PADRE","PROFESION PADRE","VIVE EL PADRE",
  "PRIMERA EMPRESA DONDE LABORO",
        "PRIMER CARGO QUE OCUPO","FECHA INICIO PRIMERA EMPRESA","FECHA FINALIZACION PRIMERA EMPRESA","JEFE INMEDIATO PRIMERA EMPRESA",
        "TELEFONO JEFE PRIMERA EMPRESA",
  "TALLA CAMISA","TALLA PANTALON","TALLA CHAQUETA","TALLA BOTAS","TALLA CHALECO",
  "TIENE TECNICOS O TECNOLOGICOS","tiene_universitarios","TIENE POSTGRADOS","postgrados","TIENE CURSO EN ALTURAS",
  "cursos_de_alturas","MANEJA SISTEMA","INGLES","ULTIMO AÑO APROBADO PRIMARIA",
  "COLEGIO DE LA PRIMARIA","ULTIMO AÑO APROBADO SECUNDARIA",
  "COLEGIO DE LA SECUNDARIA","COMPLETO EL ESTUDIO TECNOLOGICO",
  "ESTUDIA ACTUALMENTE EL TECNOLOGICO","SEMESTRE(TECNOLOGO)",
  "CARRERA(TECNOLOGO)","INSTITUCION DEL TECNOLOGO", "DURACION(TECNOLOGO)","FECHA INICIO TECNOLOGO",
  "FECHA GRADO TECNOLOGO","TIPO(TECNICO/TECNOLOGO)","PREGRADO COMPLETO","ESTUDIA ACTUALMENTE UN PREGRADO",
  "SEMESTRE PREGRADO","PREGRADO","UNIVERSIDAD PREGRADO",
  "DURACION PREGRADO","FECHA INICIO UNIVERSIDAD","FECHA GRADO UNIVERSITARIO","TARJETA PROFESIONAL",
  "NIVEL DE INGLES","TIPO DE CONOCIMIENTO","NOMBRE DEL CONOCIMIENTO","NIVEL DEL CONOCIMIENTO","DEPORTIVAS",
  "CULTURALES","FAMILIARES","RECREATIVAS","OTRA ACTIVIDAD",
  "CUAL ACTIVIDAD","ACTIVIDAD QUE LE GUSTARIA EN LA EMPRESA",
  "EPS","FONDO DE PENSIONES"

]]
     
        F_TH_13_B=pd.concat([F_TH_13_B.drop(['postgrados'], axis=1), F_TH_13_B['postgrados'].apply(pd.Series)], axis=1)
        F_TH_13_B=F_TH_13_B.rename({'completo_el_estudio':'COMPLETO EL POSTGRADO','estudia_actualmente':'ACTUALMENTE ESTUDIA EL POSTGRADO',
            'semestre':'SEMESTRE POSTGRADO','carrera':'POSTGRADO','universidad_institucion':'INSTITUCION DONDE REALIZO EL POSTGRADO',
            'duracion':'DURACION POSTGRADO','fecha_de_inicio':'FECHA INICIO POSTGRADO','fecha_de_grado':'FECHA GRADO DEL POSTGRADO',
            },axis=1)
        F_TH_13_B=F_TH_13_B[["APELLIDO 1","APELLIDO 2","NOMBRES","TIPO DOCUMENTO DE IDENTIDAD",
  "NUMERO DE DOCUMENTO","EXPEDIDA EN","SEXO","RH","CORREO ELECTRONICO","FECHA DE NACIMIENTO","LUGAR DE NACIMIENTO",
  "DEPARTAMENTO","DIRECCION ACTUAL","BARRIO","CIUDAD DE RESIDENCIA","TIPO DE RESIDENCIA","EL LUGAR DE RESIDENCIA ES",
  "CELULAR","TELEFONO","TIENE VEHICULO","TIPO VEHICULO","PLACA","PASE N°",
  "CATEGORIA","ESTADO CIVIL","APELLIDO1 CONYUGE","APELLIDO2 CONYUGE",
  "NOMBRES CONYUGE","TIPO DOCUMENTO CONYUGE","CEDULA CONYUGE","FECHA NACIMIENTO CONYUGE",
  "TRABAJA","EMPRESA","TELÉFONO","TIENE HIJOS",
  "datos_de_los_hijos","PERSONAS A CARGO","TIENE HERMANOS","CUANTOS HERMANOS TIENE",
  "TIENE ALGUN FAMILIAR QUE TRABAJE EN PREVEO",
  "PARENTESCO","NOMBRE COMPLETO","FECHA DE NACIMIENTO ","PARENTESCO FAMILIAR QUE TRABAJA EN PREVEO",
  "AREA DE LA EMPRESA EN LA QUE TRABAJA EL FAMILIAR",
  "NOMBRE EN CASO DE EMERGENCIA","CELULAR EMERGENCIA","DIRECCION EMERGENCIA",
  "NOMBRE COMPLETO DE LA MADRE","PROFESION MADRE","VIVE LA MADRE",
  "NOMBRE COMPLETO DEL PADRE","PROFESION PADRE","VIVE EL PADRE",
  "PRIMERA EMPRESA DONDE LABORO",
  "PRIMER CARGO QUE OCUPO","FECHA INICIO PRIMERA EMPRESA","FECHA FINALIZACION PRIMERA EMPRESA","JEFE INMEDIATO PRIMERA EMPRESA",
  "TELEFONO JEFE PRIMERA EMPRESA",
  "TALLA CAMISA","TALLA PANTALON","TALLA CHAQUETA","TALLA BOTAS","TALLA CHALECO","TIENE TECNICOS O TECNOLOGICOS",
  "tiene_universitarios","TIENE POSTGRADOS","TIENE CURSO EN ALTURAS","cursos_de_alturas","MANEJA SISTEMA",
  "INGLES","ULTIMO AÑO APROBADO PRIMARIA",
  "COLEGIO DE LA PRIMARIA","ULTIMO AÑO APROBADO SECUNDARIA",
  "COLEGIO DE LA SECUNDARIA","COMPLETO EL ESTUDIO TECNOLOGICO",
  "ESTUDIA ACTUALMENTE EL TECNOLOGICO",
  "SEMESTRE(TECNOLOGO)","CARRERA(TECNOLOGO)","INSTITUCION DEL TECNOLOGO",
  "DURACION(TECNOLOGO)","FECHA INICIO TECNOLOGO",
  "FECHA GRADO TECNOLOGO","TIPO(TECNICO/TECNOLOGO)","PREGRADO COMPLETO","ESTUDIA ACTUALMENTE UN PREGRADO",
  "SEMESTRE PREGRADO","PREGRADO","UNIVERSIDAD PREGRADO",
  "DURACION PREGRADO","FECHA INICIO UNIVERSIDAD","FECHA GRADO UNIVERSITARIO",
  "TARJETA PROFESIONAL","NIVEL DE INGLES","TIPO DE CONOCIMIENTO","NOMBRE DEL CONOCIMIENTO","NIVEL DEL CONOCIMIENTO","DEPORTIVAS",
  "CULTURALES","FAMILIARES","RECREATIVAS","OTRA ACTIVIDAD",
  "CUAL ACTIVIDAD","ACTIVIDAD QUE LE GUSTARIA EN LA EMPRESA",
  "EPS","FONDO DE PENSIONES",'COMPLETO EL POSTGRADO','ACTUALMENTE ESTUDIA EL POSTGRADO',
            'SEMESTRE POSTGRADO','POSTGRADO','INSTITUCION DONDE REALIZO EL POSTGRADO',
            'DURACION POSTGRADO','FECHA INICIO POSTGRADO','FECHA GRADO DEL POSTGRADO',
            

]]
        F_TH_13_B=F_TH_13_B.astype(str)
        F_TH_13_B=F_TH_13_B.replace({"True": 'SI', "False": 'NO','nan':' ','None':' '})
        
        Lab_xlsx = to_excel(F_TH_13_B)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_TH_13_B.assign(hack='').set_index('hack'))
    if menu_id == "F_TH_15":
        F_TH_15=F_TH_15.drop(['uuid','codigo','version','fecha_version'],axis=1)
        F_TH_15=pd.concat([F_TH_15.drop(['datos_del_colaborador'], axis=1), F_TH_15['datos_del_colaborador'].apply(pd.Series)], axis=1)
        F_TH_15=pd.concat([F_TH_15.drop(['descripcion_del_la_solicitud'], axis=1), F_TH_15['descripcion_del_la_solicitud'].apply(pd.Series)], axis=1)
        F_TH_15=pd.concat([F_TH_15.drop(['prestamo_educativo'], axis=1), F_TH_15['prestamo_educativo'].apply(pd.Series)], axis=1)
        F_TH_15=pd.concat([F_TH_15.drop(['espacio_reservado_para_comite_preveo'], axis=1), F_TH_15['espacio_reservado_para_comite_preveo'].apply(pd.Series)], axis=1)
        F_TH_15=pd.concat([F_TH_15.drop(['informacion_para_gerencia'], axis=1), F_TH_15['informacion_para_gerencia'].apply(pd.Series)], axis=1)
        F_TH_15=F_TH_15.rename({'nombre':'NOMBRE','cedula_ciudadania':'CC N°','cargo':'CARGO',
            'fecha_de_ingreso':'FECHA DE INGRESO','sueldo':'SUELDO','proyecto_proceso':'PROYECTO/PROCESO',
            'descripcion':'DESCRIPCION','valor_del_monto_requerido':'VALOR DEL MONTO REQUERIDO','monto_propuesto_para_pago':'MONTO PROPUESTO PARA PAGO',
            'programa':'PROGRAMA','establecimiento':'ESTABLECIMIENTO','valor':'VALOR','fecha_de_pago':'FECHA DE PAGO',
            'periodo':'PERIODO','nombre _del_establecimiento_o_persona_a_la_que_debe_ir_dirigido_el_desembolso':'ESTABLECIMIENTO O PERSONA A LA QUE VA DIRIGIDO EL DESEMBOLSO',
            'horario_de_clase':'HORARIO DE CLASES','actualmente_tiene_algun_tipo_de_beneficio_con_preveo':'TIENE BENEFICIO CON PREVEO',
            'cual':'CUAL','nombre_y_firma_del_jefe_inmediato':'NOMBRE Y FIRMA DEL JEFE INMEDIATO',
            'firma_del_solicitante':'FIRMA DEL SOLICITANTE','autoriza':'AUTORIZADO','tiempo_aprobado_para_pago_al_comite':'TIEMPO APROBADO PARA PAGO AL COMITE',
            'valor_aprobado_por_pago_al_comite':'VALOR APROBADO POR PAGO AL COMITE',
            'observaciones':'OBSERVACIONES','nombre_y_firma_del_presidente_del_comite':'NOMBRE Y FIRMA DEL PRESIDENTE DEL COMITE',
            'nombre_y_firma_del_gerente':'NOMBRE Y FIRMA DEL GERENTE','metodo':'MODO DE PAGO','banco':'BANCO',
            'cuenta_bancaria':'CUENTA','numero_cuenta_bancaria':'NUMERO CUENTA BANCARIA','numero_nit_o_cedula_ciudadania':'N°NIT/CEDULA CIUDADANIA'},axis=1)
        Lab_xlsx = to_excel(F_TH_15)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_TH_15.assign(hack='').set_index('hack'))

        
    if menu_id == "F_TH_22":
        st.write(F_TH_22)
        F_TH_22=F_TH_22.drop(['uuid','codigo','version','fecha_version','estatus','historico_de_aprobacion'],axis=1)
        F_TH_22=pd.concat([F_TH_22.drop(['capacitacion'], axis=1),F_TH_22['capacitacion'].apply(pd.Series)], axis=1)
        F_TH_22=F_TH_22.rename({'codigo_centro_de_costo':'CODIGO','cargo':'CARGO','centro_de_costo':'CENTRO DE COSTOS','necesidad_identificada':'NECESIDAD IDENTIFICADA',
            'actividad_sugerida':'ACTIVIDAD SUGERIDA','proveedor_sugerido':'PROVEEDOR SUGERIDO',
            'valor_sugerido':'VALOR SUGERIDO','intensidad_sugerida':'INTENSIDAD SUGERIDAD','horario_inicial':'HORA DE INICIO',
            'horario_final':'HORA DE FINALIZACION','fecha_sugerida':'FECHA SUGERIDA','dirigido_a':'DIRIGIDO A',
            'metodo_de_verificacion':'METODO DE VERIFICACION','metodo_de_verificacion_otro':'OTRO METODO DE VERIFICACION',
            'area':'AREA'
            },axis=1)
        F_TH_22=F_TH_22.explode('cargo_persona')
        F_TH_22=pd.concat([F_TH_22.drop(['programa'], axis=1),F_TH_22['programa'].apply(pd.Series)], axis=1)
        F_TH_22=F_TH_22.rename({'mes':'MES PROGRAMA','semana':'SEMANA PROGRAMA','estado':'ESTADO PROGRAMA',
            'cargo_persona':'CARGO PERSONA','nombre':'NOMBRE'},axis=1)
        F_TH_22=pd.concat([F_TH_22.drop(['area_talento_humano'], axis=1),F_TH_22['area_talento_humano'].apply(pd.Series)], axis=1)
        F_TH_22=F_TH_22.rename({'aprobacion':'APROBACION TALENTO HUMANO','fecha':'FECHA TALENTO HUMANO',
            'nombre':'NOMBRE TALENTO HUMANO','observaciones':'OBSERVACIONES TALENTO HUMANO',
            'estatus':'ESTADO TALENTO HUMANO','centro_de_costo':'CENTRO DE COSTO TALENTO HUMANO'},axis=1)
        F_TH_22=pd.concat([F_TH_22.drop(['ejecusion'], axis=1),F_TH_22['ejecusion'].apply(pd.Series)], axis=1)
        F_TH_22=F_TH_22.rename({'mes':'MES EJECUSION','semana':'SEMANA EJECUSION','estado':'ESTADO EJECUCION',
            'porcentaje':'PORCENTAJE EJECUSION','campo_para_cargar':'CAMPO PARA CAARGAR EJECUSION','fecha_de_ingreso':'FECHA DE INGRESO'},axis=1)
        
        Lab_xlsx = to_excel(F_TH_22)
        st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
        st.dataframe(F_TH_22.assign(hack='').set_index('hack'))
        #st.write(F_TH_22)
    if menu_id == "F_TH_25":
        st.write(F_TH_25)
    

main()