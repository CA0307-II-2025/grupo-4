# Plantilla para el proyecto de Estadística Actuarial II (CA-307)

## Instrucciones para instalar el repositorio

1. Clona este repositorio en tu máquina local.
2. Instala `uv` (https://docs.astral.sh/uv/getting-started/installation/) y luego ejecute el comando `uv sync` en la raíz del proyecto.
3. Luego ejecuta el comando `pre-commit install --install-hooks` para instalar los hooks de pre-commit.

## Instrucciones para el uso de los módulos

1. Para conocer mejor la utilización de los métodos VaR y CVaR, leer el informe escrito en la carpeta "data".
2. Cada método de cada clase está documentado con su descripción y el archivo "main.py" da un ejemplo de uso.
3. Para una experiencia de usuario más pura, ejecutar el dashboard.

## Instrucciones para el uso del dashboard

1. Verificar la instalación de la libreria Streamlit en su entorno de python.
2. En su aplicación equivalente a "cmd", "terminal" ó "command prompt" ingrese a la carpeta donde clonó el repositorio
     Ejemplo: "cd Desktop/Estadistica/grupo-4"
3. Ejecute el comando "streamlit run Home.py" con ello se ejecutará un entorno local con el aplicativo en su navegador predeterminado.
4. Nota: para un uso eficiente utilice Google Chrome, puede ser que entornos como Safari no ejecuten bien el dashboard. Para utilizar Google Chrome copie el enlace que se le generó en su navegador y péguelo en el navegador ya mencionado.
5. El dashboard es sencillo de utilizar, tiene 4 páginas diferentes:
   a. Principal: Es el uso principal del Dashboard, coloque en la barra lateral izquiera las empresas, fechas y nivel de confianza de interés para acceder a la parte gráfica. En caso de no conocer los símbolos de las empresas existe un botón que lo redigirá a la página de Yahoo Finance.
   b. Informe Escrito: Es la página donde podrá acceder a un lector pdf del informe escrito de nuestro trabajo.
   c. Sobre Yahoo Finance: Es una página informativa sobre la página de Yahoo Finance.
   d. Sobre Nosotros: Es la página donde están los contactos de los creadores del trabajo.
