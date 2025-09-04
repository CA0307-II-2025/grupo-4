from inferencia import inferencia

# Resultado 1 Sprint 2: Normalidad en bonos a plazos
bono_normal = inferencia(["BND"], "2023-01-01", "2025-01-01")
bono_normal.graficar_rendimientos("BND")
print(bono_normal.normalidad(0.05, "BND", True))
