from inferencia import inferencia
from var_cvar import var_cvar

""" # Resultado 1 Sprint 2: Normalidad en bonos a plazos
bono_normal = inferencia(["BND"], "2023-01-01", "2025-01-01", 0.05)
bono_normal.graficar_rendimientos("BND")
print(bono_normal.normalidad("BND", True))

print(bono_normal.rendimientos_diarios())

# Resultado 2 Sprint 2: VaR y CVaR en bonos a plazos
var_cvar_bnd = var_cvar(["BND"], "2010-01-01", "2025-01-01")
print(var_cvar_bnd.var_cvar_normal(["BND"], True))

# Resultado 3 Sprint 3-4-5:

var_cvar_bnd.cola_izquierda(["BND"], True, 0.1)
var_cvar_bnd.pareto_generalizada("BND", 0.1, True)


# print(var_cvar_bnd.var_cvar_gpd("BND", 0.95, 0.1))
print(var_cvar_bnd.pareto_generalizada("BND", 0.1)) """

# Resultados finales

# ETFs que vamos a comparar
etfs = ["SPY", "QQQ"]


# Fecha inicial y final de comparación
inicio = "2018-01-01"
final = "2025-01-01"

# Nivel de confianza para pruebas de hipótesis
alpha = 0.05

# Cuantil empírico (q)
q = 0.1

# Iniciamos el objeto en la clase Inferencia y graficamos rendimientos
analisis_etfs = inferencia(etfs, inicio, final)

analisis_etfs.graficar_rendimientos("SPY")
analisis_etfs.graficar_rendimientos("QQQ")

# Obtenemos la cola izquierda al quantil emírico (q)
analisis_etfs_var_cvar = var_cvar(etfs, inicio, final)

# analisis_etfs_var_cvar.cola_izquierda("QQQ", True, q)

# Obtenemos los gráficos de los excedentes
analisis_etfs_var_cvar.pareto_generalizada("SPY", q, True)
# analisis_etfs_var_cvar.pareto_generalizada("QQQ", q, True)

# Obtenemos VaR y CVaR al alpha = 0.05
print(analisis_etfs_var_cvar.var_cvar_gpd("SPY", 0.95, 0.1))

# analisis_etfs_var_cvar.pruebas("SPY", q, "ad")
