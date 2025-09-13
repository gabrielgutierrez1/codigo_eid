# analisis.py
# Módulo para el análisis matemático de funciones usando Sympy.

import sympy as sp
from sympy import latex, sympify, solveset, S, FiniteSet

def _formatear_numero(n):
    """
    Función de ayuda interna para limpiar el formato de un número.
    - Si es un entero, lo devuelve como int.
    - Si es un decimal, lo redondea a 2 decimales.
    """
    try:
        num_float = float(n)
        if abs(num_float - round(num_float)) < 1e-9:
            return int(round(num_float))
        else:
            return round(num_float, 2)
    except (TypeError, ValueError):
        return n

def realizar_analisis(expresion_str, valor_x_str):
    """
    Orquesta el análisis completo de la función y prepara los resultados.
    """
    x = sp.Symbol('x')
    
    #1. Parseo de la Expresión
    try:
        expresion = sympify(expresion_str)
    except (sp.SympifyError, TypeError) as e:
        raise ValueError(f"Error en la sintaxis de la función: {e}")

    #2. Inicialización de Resultados
    resultados_texto = {}
    resultados_puntos = {}
    justificacion = "--- Justificación Computacional ---\n"

    #3. Cálculo del Dominio ---
    dominio = sp.calculus.util.continuous_domain(expresion, x, S.Reals)
    resultados_texto['dominio'] = f"Dominio: {latex(dominio)}"
    justificacion += f"1. Dominio: Se busca el dominio en los reales.\n   Resultado: {dominio}\n"

    #4. Cálculo de Intersecciones
    try:
        y_intercept = expresion.subs(x, 0)
        y_formateado = _formatear_numero(y_intercept.evalf())
        resultados_texto['interseccion_y'] = f"Intersección Eje Y: (0, {y_formateado})"
        resultados_puntos['interseccion_y'] = (0, float(y_intercept))
        justificacion += f"2. Intersección Y: Se evalúa f(0).\n   f(0) = {y_formateado}\n"
    except Exception:
        resultados_texto['interseccion_y'] = "Intersección Eje Y: Indefinida en x=0"
        justificacion += "2. Intersección Y: La función no está definida en x=0.\n"

    x_intercepts = sp.solve(expresion, x)
    x_intercepts_reales = [r for r in x_intercepts if r.is_real]
    raices_formateadas = [_formatear_numero(r.evalf()) for r in x_intercepts_reales]
    raices_puntos = [(float(r), 0) for r in x_intercepts_reales]

    if raices_formateadas:
        justificacion += f"3. Intersección X: Se resuelve f(x) = 0.\n   Raíces encontradas: {raices_formateadas}\n"
    else:
        justificacion += "3. Intersección X: No se encontraron raíces reales.\n"
    
    resultados_texto['intersecciones_x'] = f"Intersecciones Eje X (raíces reales): {raices_formateadas}"
    resultados_puntos['intersecciones_x'] = raices_puntos

     # 5. Cálculo del Recorrido (Método Generalizado con respaldo para Parábolas)
    recorrido_str = "No se pudo determinar automáticamente."
    justificacion_recorrido = ""

    try:
        # Define 'y' como un símbolo para la ecuación y = f(x)
        y = sp.Symbol('y', real=True)
        
        # Intenta resolver para x en términos de y (hallar la función inversa)
        soluciones_inversa = sp.solveset(sp.Eq(expresion, y), x, domain=S.Reals)

        if soluciones_inversa.is_empty:
            raise NotImplementedError("No se pudo hallar una función inversa real.")
            
        expr_inversa = list(soluciones_inversa)[0]
        
        rango = sp.calculus.util.continuous_domain(expr_inversa, y, S.Reals)
        
        recorrido_str = latex(rango)
        justificacion_recorrido = (
            "4. Recorrido: Se calculó el dominio de la función inversa f⁻¹(y).\n"
            f"   Inversa (x en términos de y): {latex(expr_inversa)}\n"
            f"   Resultado (Dominio de la inversa): {recorrido_str}\n"
        )
    except Exception: 
        # Si el método de la inversa falla por CUALQUIER razón, intentamos el respaldo.
        try:
            if expresion.as_poly(x) and expresion.as_poly(x).degree() == 2:
                a, b, c = expresion.as_poly(x).all_coeffs()
                vx = -b / (2*a)
                vy = expresion.subs(x, vx)
                vy_f = _formatear_numero(vy.evalf())
                intervalo = f"[{vy_f}, \\infty)" if a > 0 else f"(-\\infty, {vy_f}]"
                recorrido_str = intervalo
                justificacion_recorrido = (
                    "4. Recorrido: El método de la inversa falló. Se usó el método para parábolas.\n"
                    f"   Vértice calculado en y = {vy_f}. Resultado: {recorrido_str}\n"
                )
            else:
                justificacion_recorrido = "4. Recorrido: No se pudo determinar automáticamente por el método de la inversa y no es una parábola.\n"
        except Exception:
             justificacion_recorrido = "4. Recorrido: No se pudo determinar automáticamente.\n"

    resultados_texto['recorrido'] = f"Recorrido: {recorrido_str}"
    justificacion += justificacion_recorrido

    #6. Evaluación de Punto
    pasos_evaluacion = ""
    if valor_x_str:
        try:
            valor_x = float(valor_x_str)
            valor_y = expresion.subs(x, valor_x)
            vx_f = _formatear_numero(valor_x)
            vy_f = _formatear_numero(valor_y.evalf())
            pasos_evaluacion = (
                f"\n--- Evaluación del Punto ---\n"
                f"1. Sustitución: Se reemplaza x por {vx_f} en f(x).\n"
                f"   f({vx_f}) = {expresion.subs(x, valor_x)}\n"
                f"2. Cálculo: Se resuelve la expresión.\n"
                f"   f({vx_f}) = {vy_f}\n"
                f"3. Conclusión: El par ordenado resultante es ({vx_f}, {vy_f})."
            )
            resultados_puntos['punto_evaluado'] = (valor_x, float(valor_y))
        except (ValueError, TypeError):
             raise ValueError(f"No se pudo evaluar en el valor '{valor_x_str}'.")

    #7. Preparación de Salida Final
    texto_final = (
        f"{resultados_texto['dominio']}\n{resultados_texto['recorrido']}\n"
        f"{resultados_texto['interseccion_y']}\n{resultados_texto['intersecciones_x']}\n\n"
        f"{justificacion}{pasos_evaluacion}"
    )


    return texto_final, resultados_puntos, expresion
