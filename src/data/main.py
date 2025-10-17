from inferencia import inferencia
from var_cvar import var_cvar

# Resultado 1 Sprint 2: Normalidad en bonos a plazos
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
print(var_cvar_bnd.pareto_generalizada("BND", 0.1))
