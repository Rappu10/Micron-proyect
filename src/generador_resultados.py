import pandas as pd
import numpy as np
from scipy.optimize import linprog
import os

def generar_resultados():
    # Directorio para guardar archivos
    data_path = "data"

    # Parámetros
    productos = ['Producto A', 'Producto B', 'Producto C']
    holding_cost = np.array([1, 1.2, 1.5])
    shortage_cost = np.array([5, 6, 4])
    ordering_cost = np.array([2, 2, 2])
    demanda = np.array([20, 25, 30])

    # Escenarios de inventario
    escenarios = {
        'SST_0.csv': [0, 0, 0],
        'actual.csv': [10, 20, 15],
        'optimo.csv': [30, 40, 35]
    }

    # Guardar escenarios
    for nombre, inventario in escenarios.items():
        df = pd.DataFrame({'Producto': productos, 'Inventario': inventario})
        df.to_csv(os.path.join(data_path, nombre), index=False)

    # Resolver para cada escenario
    for archivo, inventario_inicial in escenarios.items():
        inventario_inicial = np.array(inventario_inicial)
        c = ordering_cost
        bounds = [(0, None)] * len(productos)
        res = linprog(c, bounds=bounds, method='highs')

        if res.success:
            ordenado = np.round(res.x, 2)
            inventario_final = inventario_inicial + ordenado - demanda
            sobrantes = np.maximum(inventario_final, 0)
            faltantes = np.maximum(-inventario_final, 0)
            costo_total = (ordering_cost * ordenado + holding_cost * sobrantes + shortage_cost * faltantes).sum()

            df_resultado = pd.DataFrame({
                'Producto': productos,
                'Inventario Inicial': inventario_inicial,
                'Ordenado': ordenado,
                'Inventario Final': inventario_final,
                'Sobrantes': sobrantes,
                'Faltantes': faltantes
            })

            df_resultado.loc[len(df_resultado.index)] = ['TOTAL', '', ordenado.sum(), '', sobrantes.sum(), faltantes.sum()]
            df_resultado['Costo Total'] = ''
            df_resultado.at[len(df_resultado) - 1, 'Costo Total'] = round(costo_total, 2)

            # Guardar CSV
            resultado_path = os.path.join(data_path, f"resultado_{archivo}")
            df_resultado.to_csv(resultado_path, index=False)
            print(f"[OK] Resultado guardado: {resultado_path}")
        else:
            print(f"[ERROR] Optimización fallida para {archivo}")

if __name__ == "__main__":
    generar_resultados()
