from inferencia import inferencia
from var_cvar import var_cvar

# Resultado 1 Sprint 2: Normalidad en bonos a plazos
bono_normal = inferencia(["BND"], "2023-01-01", "2025-01-01", 0.05)
bono_normal.graficar_rendimientos("BND")
print(bono_normal.normalidad("BND", True))

# Resultado 2 Sprint 2: VaR y CVaR en bonos a plazos
var_cvar_bnd = var_cvar(["BND"], "2023-01-01", "2025-01-01")
print(var_cvar_bnd.var_cvar_normal(["BND"], True))
