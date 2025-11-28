from src.data.inferencia import inferencia
#from inferencia import inferencia
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

    def pareto_generalizada(self, empresa, q: float, graficar=False, alpha=0.95):
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
            var = self.var_cvar_gpd(empresa, alpha, q)[0]
            cvar = self.var_cvar_gpd(empresa, alpha, q)[1]
            threshold = self.var_cvar_gpd(empresa, alpha, q)[2]

            VaR = threshold - var
            CVaR = threshold - cvar

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

            plt.axvline(
                VaR,
                color="green",
                linestyle="--",
                linewidth=2,
                label=f"VaR = {VaR:.8f}",
            )
            plt.axvline(
                CVaR,
                color="orange",
                linestyle="--",
                linewidth=2,
                label=f"CVaR = {CVaR:.8f}",
            )

            plt.plot(x, fitted_pdf, "r-", lw=2, label="GPD ajustada")
            plt.title(f"Ajuste GPD a excedentes de {empresa}")
            plt.xlabel("Excedente (threshold - rendimientos menores)")
            plt.ylabel("Frecuencia")
            plt.legend()
            plt.grid(True)
            plt.show()

            return {"xi": xi, "sigma": sigma, "p valor": p_val, "threshold": threshold}#, "VaR": var, "CVaR": cvar}

        elif graficar is not True:
            return {"xi": xi, "sigma": sigma, "p valor": p_val, "threshold": threshold}#, "VaR": var, "CVaR": cvar}

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

    def pruebas(self, empresa, q: float, test: str):
        x = self.rendimientos_diarios()[empresa].astype(float).to_numpy()

        u = np.quantile(x, q)

        excedentes = u - self.cola_izquierda(empresa, False, q)

        shape, loc_hat, scale = genpareto.fit(excedentes, floc=0.0)

        n = len(excedentes)

        if test == "ks":
            d, p_value = kstest(
                excedentes, lambda y: genpareto.cdf(y, shape, loc=0.0, scale=scale)
            )
            return p_value

        n_bootstrap = 2000
        rng = np.random.default_rng(42)

        def ad_stat(sample, c, s):
            """Estadístico Anderson–Darling para GPD con parámetros (c, s)."""
            sample = np.sort(sample)
            n_ = sample.size
            uvals = genpareto.cdf(sample, c, loc=0.0, scale=s)
            eps = 1e-12
            uvals = np.clip(uvals, eps, 1 - eps)
            i = np.arange(1, n_ + 1)
            A2 = -n_ - (1.0 / n_) * np.sum(
                (2 * i - 1) * (np.log(uvals) + np.log(1 - uvals[::-1]))
            )
            return A2

        def cvm_stat(sample, c, s):
            """Estadístico Cramér–von Mises para GPD con parámetros (c, s)."""
            sample = np.sort(sample)
            n_ = sample.size
            uvals = genpareto.cdf(sample, c, loc=0.0, scale=s)
            i = np.arange(1, n_ + 1)
            ui = (2 * i - 1) / (2.0 * n_)
            W2 = np.sum((uvals - ui) ** 2) + 1.0 / (12 * n_)
            return W2

        if test == "ad":
            stat_obs = ad_stat(excedentes, shape, scale)

        elif test == "cvm":
            stat_obs = cvm_stat(excedentes, shape, scale)

        else:
            raise ValueError(f"Test '{test}' no reconocido. Usa 'ks', 'ad' o 'cvm'.")

        stats_boot = np.empty(n_bootstrap)

        for b in range(n_bootstrap):
            sim = genpareto.rvs(shape, loc=0.0, scale=scale, size=n, random_state=rng)
            c_b, loc_b, scale_b = genpareto.fit(sim, floc=0.0)

            if test == "ad":
                stats_boot[b] = ad_stat(sim, c_b, scale_b)

            else:
                stats_boot[b] = cvm_stat(sim, c_b, scale_b)

        p_value = np.mean(stats_boot >= stat_obs)

        return p_value
