# Funciones para carga y limpieza de datos:

import yfinance as yf
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt


class DatosFinancieros:
    def __init__(self, empresas: list[str], fecha_inicio: str, fecha_fin: str):
        """
        Inicializa la clase con las empresas y fechas dadas.

        Args:
            empresas (list[str]): Lista de sí­mbolos de empresas.
            fecha_inicio (str): Fecha de inicio en formato 'YYYY-MM-DD'.
            fecha_fin (str): Fecha de fin en formato 'YYYY-MM-DD'.
        """
        self.__empresas = sorted(empresas)
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__precios_historicos = yf.download(
            empresas, start=fecha_inicio, end=fecha_fin
        )["Close"]

    @property
    def precios_historicos(self):
        """
        Obtiene los precios históricos descargados.

        Returns:
            DataFrame: Precios al cierre (diario) de las empresas.
        """
        return self.__precios_historicos

    @property
    def empresas(self):
        """
        Obtiene la lista de empresas seleccionadas.

        Returns:
            list[str]: Lista de tickers de las empresas.
        """
        return self.__empresas

    @empresas.setter
    def empresas(self, empresas_nuevas):
        """
        Actualiza la lista de empresas.

        Args:
            empresas_nuevas (list[str]): Nueva lista de tickers.
        """
        self.__empresas = empresas_nuevas

    @property
    def fecha_inicio(self):
        """
        Obtiene la fecha de inicio establecida.

        Returns:
            str: Fecha de inicio.
        """
        return self.__fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, nueva_fecha_inicio):
        """
        Establece una nueva fecha de inicio.

        Args:
            nueva_fecha_inicio (str): Fecha nueva en formato 'YYYY-MM-DD'.
        """
        self.__fecha_inicio = nueva_fecha_inicio

    @property
    def fecha_fin(self):
        """
        Obtiene la fecha de fin establecida.

        Returns:
            str: Fecha de fin.
        """
        return self.__fecha_fin

    @fecha_fin.setter
    def fecha_fin(self, nueva_fecha_fin):
        """
        Establece una nueva fecha de fin.

        Args:
            nueva_fecha_fin (str): Fecha nueva en formato 'YYYY-MM-DD'.
        """
        self.__fecha_fin = nueva_fecha_fin

    def str(self):
        """
        Devuelve los datos que quiere analizar.

        Returns:
            str: Texto con las empresas y periodo analizado, más los precios.
        """
        return f"Las empresas que desea analizar son: \n {self.__empresas} \n en el periodo comprendido entre las fechas {self.__fecha_inicio} y {self.__fecha_fin}. \n \n \n La tabla con los precios históricos por empresa son: \n {self.__precios_historicos}"

    def rendimientos_diarios(self, cargar_excel=False, nombre_csv=None):
        """
        Calcula los rendimientos logarítmicos diarios de los precios históricos
        y guarda los resultados en un archivo CSV dentro de la carpeta `data/outputs/`.

        Args:
            cargar_excel (bool): parámetro opcional que actualmente no se usa.
            nombre_csv (str, optional): nombre del archivo CSV.
                                         Por defecto es 'rendimientos_diarios.csv'.

        Returns:
            DataFrame: Rendimientos logarítmicos diarios de las empresas.
        """
        precios = self.__precios_historicos
        rendimientos_log = np.log(precios / precios.shift(1)).dropna()

        output_dir = os.path.join(os.path.dirname(__file__), "csv")

        if nombre_csv is None:
            nombre_csv = "rendimientos_diarios.csv"

        if not nombre_csv.endswith(".csv"):
            nombre_csv += ".csv"

        output_file = os.path.join(output_dir, nombre_csv)

        rendimientos_log.to_csv(output_file, index=True, sep=";")

        return rendimientos_log

    def graficar_rendimientos(self, empresa):
        """
        Grafica los rendimientos diarios de una empresa específica.

        Args:
            empresa (str): Símbolo de la empresa a graficar.
        """
        retornos_historicos = self.rendimientos_diarios()[empresa]

        plt.figure(figsize=(10, 6))
        sns.set_style("whitegrid")

        sns.histplot(
            retornos_historicos,
            bins=70,
            kde=False,
            color="navy",
            alpha=0.7,
            edgecolor="black",
        )
        lim = max(abs(retornos_historicos.min()), abs(retornos_historicos.max()))
        plt.xlim(-lim, lim)

        plt.title(
            f"Rendimientos diarios de {empresa}", fontsize=14, weight=450, loc="center"
        )
        plt.xlabel("Rendimientos diarios", fontsize=14)
        plt.ylabel("Frecuencia", fontsize=14)

        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.show()
