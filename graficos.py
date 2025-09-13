# graficos.py
# Módulo dedicado a la generación del gráfico con Matplotlib.

import sympy as sp
import math
from matplotlib.figure import Figure

def generar_grafica(expresion, datos_puntos):
    """
    Crea y devuelve una figura de Matplotlib a partir de una expresión
    y un diccionario de puntos notables. No usa NumPy.
    """
    x = sp.Symbol('x')
    
    #Generación de Puntos para la línea de la función
    x_vals, y_vals = [], []
    current_x = -10.0
    while current_x <= 10.0:
        try:
            y_vals.append(float(expresion.subs(x, current_x).evalf()))
            x_vals.append(current_x)
        except (TypeError, ValueError):
            pass # Si un punto está fuera del dominio, se ignora.
        current_x += 0.1
    
    #Creación del Gráfico y Dibujo de la Función
    fig = Figure(figsize=(7, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.plot(x_vals, y_vals, label=f"f(x) = {expresion}", color="blue")

    #Dibujo de Puntos Notables (Intersecciones, etc.)
    if datos_puntos.get('intersecciones_x'):
        for px, py in datos_puntos['intersecciones_x']:
            ax.plot(px, py, "ro", label="Intersección Eje X")

    if datos_puntos.get('interseccion_y'):
        px, py = datos_puntos['interseccion_y']
        ax.plot(px, py, "go", label="Intersección Eje Y")

    if datos_puntos.get('punto_evaluado'):
        px, py = datos_puntos['punto_evaluado']
        ax.plot(px, py, "mo", markersize=8, label=f"Punto ({px:g}, {py:.2f})")

   # Estilo Final del Gráfico
    ax.set_title(f"Gráfico de f(x) = {expresion}")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_ylim(-20, 20) 
    
    # Este bloque evita etiquetas duplicadas en la leyenda.
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())
    
    fig.tight_layout()

    return fig
