"""
Tab de presentación - Slides HTML estáticos
"""
import streamlit as st
import os
import base64


def render_presentation_tab():
    """Renderiza el tab con la presentación HTML embebida"""

    # Obtener la ruta del archivo HTML
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, '..', 'presentation', 'index.html')
    image_path_1 = os.path.join(current_dir, '..', 'presentation', 'Gemini_Generated_Image_bqzbasbqzbasbqzb.png')
    image_path_2 = os.path.join(current_dir, '..', 'presentation', 'smart.png')

    # Leer el contenido HTML
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Convertir la primera imagen a base64 si existe (diagrama de arquitectura)
        if os.path.exists(image_path_1):
            with open(image_path_1, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                img_base64 = f"data:image/png;base64,{img_data}"

                html_content = html_content.replace(
                    '/etl/presentation/Gemini_Generated_Image_bqzbasbqzbasbqzb.png',
                    img_base64
                )

        # Convertir la segunda imagen a base64 si existe (objetivos SMART)
        if os.path.exists(image_path_2):
            with open(image_path_2, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                img_base64 = f"data:image/png;base64,{img_data}"

                html_content = html_content.replace(
                    'smart.png',
                    img_base64
                )

        # Renderizar HTML en iframe de altura completa
        st.components.v1.html(
            html_content,
            height=900,
            scrolling=True
        )

    except FileNotFoundError:
        st.error("❌ No se encontró el archivo de presentación en etl/presentation/index.html")
    except Exception as e:
        st.error(f"⚠️ Error al cargar la presentación: {str(e)}")
