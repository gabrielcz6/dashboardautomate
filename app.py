import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard - Crea y Lanza tu Curso Online", layout="wide")

st.title("📊 Dashboard - Crea y Lanza tu Curso Online")
st.markdown("Sube tu archivo Excel para visualizar las estadísticas principales de los leads y datos del lanzamiento.")

uploaded_file = st.file_uploader("Sube el archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        xl = pd.ExcelFile(uploaded_file)
        sheet_names = xl.sheet_names
        
        st.success("¡Archivo cargado correctamente!")
        
        # We will focus on the 'Lead Scoring Bienvenida' sheet for analytics
        if 'Lead Scoring Bienvenida' in sheet_names:
            st.header("🎯 Análisis de Leads (Scoring Bienvenida)")
            df_leads = pd.read_excel(uploaded_file, sheet_name='Lead Scoring Bienvenida')
            
            # Clean up the dataframe by removing completely empty columns/rows if any
            df_leads = df_leads.dropna(how='all', axis=1).dropna(how='all', axis=0)
            
            # Show basic info
            st.metric("Total de Leads Registrados", len(df_leads))
            
            # Columns to exclude from the visual analysis
            exclude_cols = ['contact name', 'EMAIL', 'phone', 'utm_source | Opportunity', 
                            'utm_campaign | Opportunity', 'utm medium | Opportunity', 
                            'utm_content | Opportunity', 'source']
                            
            valid_cols = [col for col in df_leads.columns if col not in exclude_cols]
            
            # Display charts dynamically in 2 columns
            cols_ui = st.columns(2)
            col_idx = 0
            
            list_columns = ["¿Qué herramientas digitales has usado?"]
            
            for col in valid_cols:
                # Handle comma separated values ONLY for known list fields
                if col in list_columns:
                    items = df_leads[col].dropna().astype(str)
                    separated_items = items.str.split(',').explode().str.strip()
                    # Remove quotes that might remain and empty strings
                    separated_items = separated_items.str.replace('"', '').str.strip()
                    separated_items = separated_items[separated_items != '']
                    counts = separated_items.value_counts().reset_index()
                else:
                    counts = df_leads[col].value_counts().reset_index()
                    
                counts.columns = [col, 'Cantidad']
                
                # Render chart ONLY if there's more than 1 category with repetitions, or at least 1 category with > 1 entry
                if len(counts) > 0 and counts['Cantidad'].max() > 1:
                    with cols_ui[col_idx % 2]:
                        # A unique key for each selectbox
                        chart_type = st.selectbox(f"Tipo de gráfico para: {col[:40]}...", ["Pie", "Barra", "Línea"], key=f"chart_{col}")
                        
                        if chart_type == "Pie":
                            fig = px.pie(counts, values='Cantidad', names=col, title=col, hole=0.3)
                            fig.update_traces(textposition='inside', textinfo='percent+label')
                        elif chart_type == "Barra":
                            fig = px.bar(counts, x=col, y='Cantidad', title=col, color='Cantidad')
                        else:
                            fig = px.line(counts, x=col, y='Cantidad', title=col, markers=True)
                            
                        # Improve layout a bit
                        fig.update_layout(title_font=dict(size=14), margin=dict(t=50, b=0, l=0, r=0))
                        st.plotly_chart(fig, use_container_width=True)
                        st.divider()
                    
                    col_idx += 1

        else:
            st.warning("No se encontró la hoja 'Lead Scoring Bienvenida' en el documento.")
            

            
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.info("Por favor, sube el archivo Excel de la campaña para comenzar el análisis.")
