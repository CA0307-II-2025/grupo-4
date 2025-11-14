from inferencia import inferencia
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import genpareto
from scipy.stats import kstest
from statsmodels.nonparametric.kernel_density import KDEMultivariate


class var_cvar(inferencia):
    def __init__(
        self,
        empresas: list[str],
        fecha_inicio: str,
        fecha_fin: str,
        alpha=0.05,
        conf=0.95,
        distribucion=None,
        metodo=None,
    ):
        super().__init__(empresas, fecha_inicio, fecha_fin, alpha)

        self.distribucion = distribucion
        self.metodo = metodo
        self.conf = conf

    def var_cvar_normal(self, empresa: str, graficar=False):
        mu, sigma = self.normalidad(empresa)["mu"], self.normalidad(empresa)["sigma"]

        z_conf = norm.ppf(1 - self.conf)
        phi = norm.pdf(z_conf)

        var = mu + sigma * z_conf
        cvar = mu - sigma * (phi / (1 - self.conf))

        if graficar:
            self.normalidad(empresa, True, var, cvar)

            return {"VaR": var, "CVaR": cvar}

        return {"VaR": var, "CVaR": cvar}

    def cola_izquierda(self, empresa: str, graficar, q=0.05):
        umbral = np.quantile(self.rendimientos_diarios()[empresa], q)

        emp = self.rendimientos_diarios()[empresa]

        cola = emp[emp <= umbral]

        # cola = self.rendimientos_diarios()[
        #   self.rendimientos_diarios()[empresa] <= umbral
        # ]

        if graficar:
            plt.figure(figsize=(10, 5))
            sns.histplot(cola, bins=50, kde=False, color="navy", alpha=0.7)

            plt.axvline(
                umbral,
                color="black",
                linestyle="--",
                label=f"Umbral empírico: {umbral:.4f}",
                alpha=1,
            )

            plt.title(f"Cola izquierda de {empresa} (q = {q})")
            plt.xlabel("Rendimientos")
            plt.ylabel("Frecuencia")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

            return cola

        else:
            return cola

    def pareto_generalizada(self, empresa, q: float, graficar=False):
        """
        Obtiene la distribución generalizada de pareto de
        una distribución basado en POT.
            q (float): percentil.

        Returns:
            parámetros (dict): parámetros de la gpd.
        """

        threshold = np.quantile(self.rendimientos_diarios()[empresa], q)

        excedentes = threshold - self.cola_izquierda(empresa, False, q)

        xi, loc, sigma = genpareto.fit(excedentes, floc=0)

        ks_stat, p_val = kstest(excedentes, "genpareto", args=(xi, loc, sigma))

        if graficar:
            x = np.linspace(0, excedentes.max(), 1000)
            fitted_pdf = genpareto.pdf(x, xi, loc=0, scale=sigma)

            plt.figure(figsize=(10, 5))
            sns.histplot(
                excedentes,
                bins=100,
                stat="density",
                alpha=0.7,
                label="Excedentes",
                color="navy",
            )

            plt.plot(x, fitted_pdf, "r-", lw=2, label="GPD ajustada")
            plt.title(f"Ajuste GPD a excedentes de {empresa}")
            plt.xlabel("Excedente (threshold - rendimientos menores)")
            plt.ylabel("Frecuencia")
            plt.legend()
            plt.grid(True)
            plt.show()

            return {"xi": xi, "sigma": sigma, "p valor": p_val, "threshold": threshold}

        elif graficar is not True:
            return {"xi": xi, "sigma": sigma, "p valor": p_val, "threshold": threshold}

    def var_cvar_gpd(self, empresa, alpha: float, q: float):
        """
        Obtiene el var y cvar de los rendimientos dado un nivel de confianza
        Args:
            q (float): percentil.
            alpha (float): nivel de confianza

        Returns:
            var, cvar (float): var y cvar de los rendimientos
        """
        x = self.rendimientos_diarios()[empresa].astype(float).to_numpy()

        u = np.quantile(x, q)

        dic_gpd = self.pareto_generalizada(empresa, q)

        xi, sigma, threshold = dic_gpd["xi"], dic_gpd["sigma"], dic_gpd["threshold"]

        x = np.asarray(x).ravel()
        X = x[:, None]
        kde = KDEMultivariate(data=X, var_type="c", bw="cv_ls")
        h = float(kde.bw[0])

        pu = float(kde.cdf([u]))

        pu = np.mean(norm.cdf((u - x) / h))

        VaR = threshold - (sigma / xi) * ((((1 - alpha) / pu) ** -xi) - 1)

        CVaR = VaR - (sigma - xi * (VaR - threshold)) / (1 - xi)

        return VaR, CVaR, threshold, xi
