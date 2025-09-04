# Funciones para cálculos simples VaR y CVaR:

import matplotlib.pyplot as plt
import seaborn as sns
from limpieza_datos import limpieza_datos
from scipy.stats import norm
from statsmodels.stats.diagnostic import normal_ad
import numpy as np


class inferencia(limpieza_datos):
    def __init__(self, empresas: list[str], fecha_inicio: str, fecha_fin: str):
        super().__init__(empresas, fecha_inicio, fecha_fin)

    def normalidad(self, alpha: float, empresa: str, graficar: bool):
        """
        Test de normalidad basado en Anderson–Darling (familia Cramér–von Mises).
        Retorna True si no se rechaza normalidad, False en caso contrario.
        """

        base = self.rendimientos_diarios()[empresa]
        x = np.asarray(base).ravel()
        mu_hat, sigma_hat = norm.fit(x)

        z = (x - mu_hat) / sigma_hat
        stat, p = normal_ad(z)

        normal = bool(p >= alpha)

        if graficar and normal:
            plt.figure(figsize=(10, 6))
            sns.set_style("whitegrid")

            bins = 70

            sns.histplot(
                x,
                bins=bins,
                kde=False,
                color="navy",
                alpha=0.5,
                edgecolor="black",
            )

            lim = max(abs(np.nanmin(x)), abs(np.nanmax(x)))
            plt.xlim(-lim, lim)

            counts, edges = np.histogram(x, bins=bins)
            bin_width = edges[1] - edges[0]

            xx = np.linspace(-lim, lim, 400)
            pdf = norm.pdf(xx, loc=mu_hat, scale=sigma_hat)
            expected_counts = len(x) * bin_width * pdf

            plt.plot(
                xx, expected_counts, linewidth=2.2, label="Normal MLE", color="#B22222"
            )

            plt.title(
                f"Rendimientos diarios de {empresa}",
                fontsize=14,
                weight=450,
                loc="center",
            )
            plt.xlabel("Rendimientos diarios", fontsize=14)
            plt.ylabel("Frecuencia", fontsize=14)

            txt = rf"$\hat\mu={mu_hat:.5f}\;\; \hat\sigma={sigma_hat:.5f}$"
            plt.text(
                0.98,
                0.98,
                txt,
                transform=plt.gca().transAxes,
                ha="right",
                va="top",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.7, lw=0),
            )

            plt.grid(True, linestyle="--", alpha=0.4)
            plt.legend(loc="best", frameon=True)
            plt.tight_layout()
            plt.show()

            return {
                "n": len(x),
                "statistic": float(stat),
                "p_value": float(p),
                "alpha": alpha,
                "es normal": normal,
                "mu": mu_hat,
                "sigma": sigma_hat,
            }

        else:
            return {
                "n": len(x),
                "statistic": float(stat),
                "p_value": float(p),
                "alpha": alpha,
                "es normal": normal,
                "mu": mu_hat,
                "sigma": sigma_hat,
            }
