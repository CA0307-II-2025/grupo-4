from inferencia import inferencia
from scipy.stats import norm


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
