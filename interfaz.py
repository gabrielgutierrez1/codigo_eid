# interfaz.py
# Módulo que construye la interfaz gráfica con Tkinter y maneja los eventos del usuario.

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from analisis import realizar_analisis
from graficos import generar_grafica
from utils import validar_funcion, validar_valor

class AnalizadorApp(tk.Tk):
    """Clase principal de la aplicación que encapsula toda la GUI."""
    def __init__(self):
        super().__init__()
        self.title("Analizador de Funciones")
        self.geometry("1200x750")
        self._crear_widgets()

    def _crear_widgets(self):
        """Crea y organiza todos los componentes visuales de la ventana."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        #Sección de Entrada de Datos
        input_frame = ttk.LabelFrame(main_frame, text="Entrada de Datos", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Función f(x):").grid(row=0, column=0, padx=5, pady=5)
        self.entrada_func = ttk.Entry(input_frame, width=40)
        self.entrada_func.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Valor de x:").grid(row=1, column=0, padx=5, pady=5)
        self.entrada_x = ttk.Entry(input_frame, width=20)
        self.entrada_x.grid(row=1, column=1, padx=5, sticky='w')
        
        ttk.Button(input_frame, text="Analizar y Graficar", command=self.analizar).grid(row=0, column=2, rowspan=2, padx=10)

        #Sección de Resultados (Texto y Gráfico)
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        results_frame.grid_columnconfigure(0, weight=1) # Columna de texto
        results_frame.grid_columnconfigure(1, weight=3) # Columna de gráfico

        texto_frame = ttk.LabelFrame(results_frame, text="Resultados y Justificación", padding=10)
        texto_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5)) 
        self.texto_resultados = tk.Text(texto_frame, wrap=tk.WORD, font=('Courier New', 10), height=15)
        self.texto_resultados.pack(fill=tk.BOTH, expand=True)
        self.texto_resultados.config(state=tk.DISABLED)

        self.grafico_frame = ttk.LabelFrame(results_frame, text="Gráfico", padding=10)
        self.grafico_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.canvas = None

    def analizar(self):
        """Orquesta el proceso de análisis y graficación."""
        try:
            # 1. Validar entradas del usuario.
            funcion_str = validar_funcion(self.entrada_func.get())
            valor_x_str = validar_valor(self.entrada_x.get())
            
            # 2. Realizar el análisis matemático.
            texto, puntos, expresion = realizar_analisis(funcion_str, valor_x_str)
            
            # 3. Actualizar la GUI con los resultados.
            self.mostrar_resultados_en_texto(texto)
            self.mostrar_grafico(expresion, puntos)
        except ValueError as ve:
            messagebox.showerror("Error de Entrada", str(ve))
        except Exception as e:
            messagebox.showerror("Error en el Análisis", f"No se pudo procesar. Error:\n{e}")

    def mostrar_resultados_en_texto(self, texto_completo):
        """Actualiza el panel de texto con la información del análisis."""
        self.texto_resultados.config(state=tk.NORMAL)
        self.texto_resultados.delete('1.0', tk.END)
        self.texto_resultados.insert('1.0', texto_completo)
        self.texto_resultados.config(state=tk.DISABLED)

    def mostrar_grafico(self, expresion, datos_puntos):
        """Limpia el gráfico anterior y muestra el nuevo."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
        
        fig = generar_grafica(expresion, datos_puntos)
        
        # Embebe la figura de Matplotlib en la ventana de Tkinter.
        self.canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.grafico_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def iniciar_interfaz():
    """Función de entrada para crear y correr la aplicación."""
    app = AnalizadorApp()
    app.mainloop()