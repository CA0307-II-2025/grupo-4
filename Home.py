# dashboard_streamlit.py
import streamlit as st
import matplotlib.pyplot as plt
from datetime import date
import seaborn as sns
# Importar clases desde los módulos
from src.data.limpieza_datos import limpieza_datos
from src.data.inferencia import inferencia
from src.data.var_cvar import var_cvar
import io, os
import time
def page_dash():
    # -------------------------------------------------------------------
    # Configuración general de la app
    # -------------------------------------------------------------------
    st.set_page_config(
        page_title="Dashboard Financiero - VaR & CVaR",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Dashboard de Análisis Financiero")
    st.markdown("Este panel permite analizar rendimientos, pruebas de normalidad y el cálculo del VaR y CVaR para activos seleccionados.")

    # -------------------------------------------------------------------
    # Entradas de usuario
    # -------------------------------------------------------------------
    st.sidebar.header("Configuración del análisis")

    empresas = st.sidebar.text_input(
        "Ingrese los símbolos (separados por comas)", "KO,BND,AAPL,BTC-USD,SPY,TSLA,ETH-USD,NVDA,F,INTC,AMZN,GOOGL"
    ).split(",")

    empresas = [e.strip().upper() for e in empresas if e.strip() != ""]

    fecha_inicio = st.sidebar.date_input("Fecha de inicio AA/MM/DD", date(2022, 1, 1))
    fecha_fin = st.sidebar.date_input("Fecha de fin AA/MM/DD", date.today())


    #alpha = st.sidebar.slider("Nivel de significancia (α)", 0.0, 0.50, 0.001)
    conf = st.sidebar.slider("Nivel de confianza para VaR/CVaR", 0.9, 0.99, 0.05)



    #inicializador de los datos
    msg = st.empty()  # contenedor para los mensajes

    try:
        # Mensaje mientras se descargan los datos
        #msg.info("Descargando datos con 'yfinance'...")

        modelo = var_cvar(
            empresas,
            str(fecha_inicio),
            str(fecha_fin),
            alpha=0.0,
            conf=conf
        )

        # Si todo sale bien, cambiamos el mensaje
        #msg.success("Datos descargados correctamente")

        # OPCIONAL: que se oculte solo después de 3 segundos
        #time.sleep(0.3)
        #msg.empty()

    except Exception as e:
        # Si hay error, limpiamos el mensaje anterior y mostramos el error
        #msg.empty()
        st.error(f"Error al cargar los datos: {e}")
        st.stop()



    # -------------------------------------------------------------------
    # Selección de empresa y análisis
    # -------------------------------------------------------------------
    st.markdown("Si no conoces los símbolos de las empresas puedes ingresar a la página de Yahoo Finance en el siguiente enlace:")
    st.page_link("https://finance.yahoo.com/markets/stocks/most-active/", label="Yahoo Finance", icon="📈")
    empresa = st.selectbox("Seleccione una empresa:", empresas)
    analisis = st.radio(
        "Seleccione el tipo de análisis:",
        ["Visualizar datos", 
         "Test de Normalidad", 
         "VaR y CVaR (Normal)",
         "VaR y CVar (Pareto)", 
         "Cola izquierda"]
    )

    # -------------------------------------------------------------------
    # Visualizaciones según selección
    # -------------------------------------------------------------------
    if analisis == "Visualizar datos":
        st.subheader(f"Rendimientos de {empresa}")
        try:
            modelo.graficar_rendimientos(empresa)
            st.pyplot(plt.gcf())
        except Exception as e:
            st.error(f"No fue posible generar la gráfica: {e}")

    elif analisis == "Test de Normalidad":
        st.subheader(f"Prueba de Normalidad - {empresa}")
        try:
            modelo.normalidad(empresa, graficar=True)
            st.pyplot(plt.gcf())
        except Exception as e:
            st.error(f"No fue posible generar la gráfica: {e}")

    elif analisis == "VaR y CVaR (Normal)":
        st.subheader(f"Cálculo de VaR y CVaR - {empresa}")
        try:
            resultados = modelo.var_cvar_normal(empresa, graficar=True)
            plot_st = st.pyplot(plt.gcf())
            #st.markdown(f"**VaR ({conf*100:.1f}%):** {resultados['VaR']:.4f}")
            st.latex(f"VaR({conf*100:.1f}\%) = {resultados['VaR']:.4f}")
            #st.markdown(f"**CVaR ({conf*100:.1f}%):** {resultados['CVaR']:.4f}")
            st.latex(f"CVaR ({conf*100:.1f}\%)= {resultados['CVaR']:.4f}")
        except Exception as e:
            plot_st.empty()
            st.error(f"No fue posible calcular VaR/CVaR: {e}")
    
    elif analisis == "VaR y CVaR (Pareto)":
        st.subheader(f"Cálculo de VaR y CVaR - {empresa}")
        try:
            resultados = modelo.var_cvar_gpd(empresa, alpha = conf, q = 10, graficar = True)
            plot_st = st.pyplot(plt.gcf())
            #st.markdown(f"**VaR ({conf*100:.1f}%):** {resultados['VaR']:.4f}")
            st.latex(f"VaR({conf*100:.1f}\%) = {resultados['VaR']:.4f}")
            #st.markdown(f"**CVaR ({conf*100:.1f}%):** {resultados['CVaR']:.4f}")
            st.latex(f"CVaR ({conf*100:.1f}\%)= {resultados['CVaR']:.4f}")
        except Exception as e:
            plot_st.empty()
            st.error(f"No fue posible calcular VaR/CVaR: {e}")

    elif analisis == "Cola izquierda":
        st.subheader(f"Cálculo de VaR y CVaR - {empresa}")
        try:
            resultados = modelo.cola_izquierda(empresa, graficar=True)
            plot_st = st.pyplot(plt.gcf())
            #st.markdown(f"**VaR ({conf*100:.1f}%):** {resultados['VaR']:.4f}")
            #st.latex(f"VaR({conf*100:.1f}\%) = {resultados['VaR']:.4f}")
            #st.markdown(f"**CVaR ({conf*100:.1f}%):** {resultados['CVaR']:.4f}")
            #st.latex(f"CVaR ({conf*100:.1f}\%)= {resultados['CVaR']:.4f}")
        except Exception as e:
            plot_st.empty()
            st.error(f"No fue posible graficar la cola izquierda de la empresa: {e}")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    st.download_button(
        label="Descargar Gráfico",
        data=buffer,
        file_name=f"{empresa}_{analisis}.png",
        mime="image/png"
    )


    # -------------------------------------------------------------------
    # Pie de página
    # -------------------------------------------------------------------
    st.markdown("---")

def document():
    st.title("Trabajo Escrito")
    st.pdf("docs/Sexto_Sprint.pdf", height = 800)
    with open("docs/Sexto_Sprint.pdf", "rb") as file:
        st.download_button(
            label="Descargar Informe",
            data=file,
            file_name="Informe_VaR_CVaR.pdf"
        )
    st.markdown("---")

#Pagina de cada desarrollador
def resumen():
    st.header("Resumen del equipo")
    st.markdown("""
                Somos estudiantes de Ciencias Actuariales de la Universidad de Costa Rica. 
                La idea de este proyecto surge de un proyecto de investigación del curso Estadística Actuarial II.
                """)
    st.html("<hr>")

def cris():
    st.header("Cristhofer Urrutia")

    #st.write('''
     #       texto interesante de Cris
      #       ''')
    #st.image("assets/gara.JPG") <div style="padding:20px; border:1px solid #ddd; border-radius:15px; width:70%;">
    cris_html = """
        
            <!-- Foto circular -->
            <div style="display:flex; align-items:center; gap:20px;">
                <div>
                    <h2 style="margin:0; padding:0;">Cristhofer Urrutia</h2>
                    <p style="margin:0; font-size:16px; color:#555;">
                        Estudiante de Ciencias Actuariales - UCR<br>
                        Especial interés en análisis financiero y modelación estadística.
                    </p>
                </div>
            </div>

            <!-- Íconos de contacto -->
            <div style="display:flex; gap:20px; align-items:center; margin-top:10px;">
                
                <!-- LinkedIn -->
                <a href="https://www.linkedin.com/in/gabriel-esteban-valverde-guzmán-46539a362/" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="32">
                </a>

                <!-- Instagram -->
                <a href="https://www.instagram.com/cjuc_12?igsh=MTJnZXAwMzhtZHVwOQ%3D%3D&utm_source=qr" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/1409/1409946.png" width="32">
                </a>

                <!-- Correo -->
                <a href="mailto:cristopherurrutia82@gmail.com">
                    <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="32">
                </a>

                <!-- WhatsApp -->
                <a href="https://wa.me/50663128651" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="32">
                </a>
            </div>
            <hr>

        
    """ #</div>
    st.html(cris_html)



def dom():
    st.header("Dominick Rodríguez")
    #st.write('''
    #        texto interesante de Dominick
    #         ''')
    #st.image("assets/gara.JPG") <div style="padding:20px; border:1px solid #ddd; border-radius:15px; width:70%;">
    dom_html = """
        
            <!-- Foto circular -->
            <div style="display:flex; align-items:center; gap:20px;">
                <div>
                    <h2 style="margin:0; padding:0;">Dominick Rodriguez</h2>
                    <p style="margin:0; font-size:16px; color:#555;">
                        Estudiante de Ciencias Actuariales - UCR<br>
                        Especial interés en análisis financiero y modelación estadística.
                    </p>
                </div>
            </div>


            <!-- Íconos de contacto -->
            <div style="display:flex; gap:20px; align-items:center; margin-top:10px;">
                
                <!-- LinkedIn -->
                <a href="https://www.linkedin.com/in/dominick-rodriguez-trejos" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="32">
                </a>

                <!-- Instagram -->
                <a href="https://www.instagram.com/1400dominick/" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/1409/1409946.png" width="32">
                </a>

                <!-- Correo -->
                <a href="mailto:drt1415@gmail.com">
                    <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="32">
                </a>

                <!-- WhatsApp -->
                <a href="https://wa.me/50687080725" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="32">
                </a>
            </div>
            <hr>

        
    """ #</div>
    st.html(dom_html)

def gara():
    st.header("Gabriel Valverde")
    #st.write('''
    #        texto interesante de gara
    #         ''')
    #st.image("assets/gara.JPG") <div style="padding:20px; border:1px solid #ddd; border-radius:15px; width:70%;">
    gara_html = """
        
            <!-- Foto circular -->
            <div style="display:flex; align-items:center; gap:20px;">
                <div>
                    <h2 style="margin:0; padding:0;">Gabriel Valverde</h2>
                    <p style="margin:0; font-size:16px; color:#555;">
                        Estudiante de Ciencias Actuariales - UCR<br>
                        Especial interés en análisis financiero y modelación estadística.
                    </p>
                </div>
            </div>


            <!-- Íconos de contacto -->
            <div style="display:flex; gap:20px; align-items:center; margin-top:10px;">
                
                <!-- LinkedIn -->
                <a href="https://www.linkedin.com/in/gabriel-esteban-valverde-guzmán-46539a362/" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="32">
                </a>

                <!-- Instagram -->
                <a href="https://www.instagram.com/garabito05/" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/1409/1409946.png" width="32">
                </a>

                <!-- Correo -->
                <a href="mailto:gabriel.valverde.guzman@gmail.com">
                    <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="32">
                </a>

                <!-- WhatsApp -->
                <a href="https://wa.me/50688562914" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="32">
                </a>
            </div>
            <hr>

        
    """ #</div>
    st.html(gara_html)


def jeremy():
    st.header("Jeremy Flores")
    #st.write('''
    #        texto interesante de Jeremy
    #         ''')
    #st.image("assets/gara.JPG") <div style="padding:20px; border:1px solid #ddd; border-radius:15px; width:70%;">
    jere_html = """
        
            <!-- Foto circular -->
            <div style="display:flex; align-items:center; gap:20px;">
                <div>
                    <h2 style="margin:0; padding:0;">Jeremy Flores</h2>
                    <p style="margin:0; font-size:16px; color:#555;">
                        Estudiante de Ciencias Actuariales - UCR<br>
                        Especial interés en análisis financiero y modelación estadística.
                    </p>
                </div>
            </div>

            <!-- Íconos de contacto -->
            <div style="display:flex; gap:20px; align-items:center; margin-top:10px;">
                
                <!-- LinkedIn -->
                <a href="https://www.linkedin.com/in/gabriel-esteban-valverde-guzmán-46539a362/" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="32">
                </a>

                <!-- Instagram -->
                <a href="https://www.instagram.com/garabito05/" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/1409/1409946.png" width="32">
                </a>

                <!-- Correo -->
                <a href="mailto:gabriel.valverde.guzman@gmail.com">
                    <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="32">
                </a>

                <!-- WhatsApp -->
                <a href="https://wa.me/50687657891" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="32">
                </a>
            </div>
            <hr>

        
    """ #</div>
    st.html(jere_html)


def page_us():
    st.title("Desarrolladores")
    resumen()
    
    cris()
    
    dom()
    
    gara()
    
    jeremy()


    


def page_yahoo():
    st.title("Sobre Yahoo Finance")
    with open("dash_txt/yahoo.txt", "r", encoding="utf-8") as yh:
        for i in yh.readlines():    
            st.markdown(i)
    st.markdown("---")


pages = {
    "Dashboard": [
        st.Page(page_dash, title="Dashboard interactivo"),
        st.Page(document, title="Trabajo Escrito")
    ],
    "Sobre Nosotros": [
        st.Page(page_us, title="Desarrolladores"),
        st.Page(page_yahoo, title="Sobre Yahoo Finance")
    ]
}

pg = st.navigation(pages, position="top")
pg.run()