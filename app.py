import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Explorador de Datos", layout="wide")

st.title("📊 Aplicativo de Exploración de Datos")
st.markdown("Sube tu archivo CSV para analizar correlaciones y ver una vista previa de los datos.")

# --- ETAPA 0: CARGA DE DATOS ---
st.sidebar.header("Configuración")
archivo = st.sidebar.file_uploader("Sube un archivo CSV", type=["csv"])

if archivo is not None:
    # Leer el archivo
    df = pd.read_csv(archivo)
    
    # Éxito y vista previa
    st.success("✅ Archivo cargado correctamente")
    
    st.subheader("👀 Vista previa de los datos (df.head)")
    st.dataframe(df.head())

    st.divider()

    # --- ETAPA 1: DIAGRAMA DE CORRELACIÓN ---
    st.subheader("🔗 Diagrama de Correlación")
    
    # Solo podemos correlacionar columnas numéricas
    columnas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(columnas_numericas) > 1:
        # Selección de columnas por el usuario
        seleccion = st.multiselect(
            "Selecciona las columnas para calcular la correlación:",
            options=columnas_numericas,
            default=columnas_numericas
        )

        if len(seleccion) > 1:
            # Calcular matriz de correlación
            corr_matrix = df[seleccion].corr()

            # Crear el gráfico con Matplotlib/Seaborn
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
            
            # Mostrar en Streamlit
            st.pyplot(fig)
        else:
            st.warning("⚠️ Selecciona al menos dos columnas para ver la correlación.")
    else:
        st.error("❌ El archivo no tiene suficientes columnas numéricas para realizar una correlación.")

else:
    st.info("💡 Por favor, sube un archivo CSV desde la barra lateral para comenzar.")
