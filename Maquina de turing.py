import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random

# Clase que representa la Máquina de Turing
class MaquinaTuring:
    def __init__(self):
        self.cinta = ['^'] * 50  # Cinta inicializada con 50 posiciones en blanco (^)
        self.cinta_cargada = False
        self.cinta_original = None  # Almacena la cinta original
        self.cabezal = 0  # Posición inicial del cabezal
        self.estado_actual = None

    # Llenar la cinta con símbolos aleatorios del alfabeto (1, 0 y ^)
    def llenar_cinta_aleatoria(self):
        self.cinta = [random.choice(['1', '0', '^']) for _ in range(50)]
        self.cinta_cargada = True  # Indicar que la cinta ha sido cargada en la opción 1

    # Guardar la cinta cargada como original
    def guardar_cinta_original(self):
        self.cinta_original = self.cinta.copy()  # Crear una copia para la cinta original

    # Mostrar la cinta como lista de símbolos
    def mostrar_cinta(self):
        return self.cinta

# Interfaz gráfica usando tkinter
class InterfazTuring:
    def __init__(self, root):
        self.maquina = MaquinaTuring()
        self.root = root
        self.root.title("Simulador de Máquina de Turing")
        self.root.geometry("950x600")
        self.root.config(bg="#3e2723")  # Fondo café oscuro

        # Variables para los estados Ha y He
        self.estado_ha = None
        self.estado_he = None

        # Crear un canvas y un scrollbar para que la cinta sea deslizable
        self.cinta_canvas = tk.Canvas(self.root, bg="#795548", height=100, highlightthickness=0)  # Cinta café claro
        self.scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.cinta_canvas.xview)
        self.cinta_canvas.config(xscrollcommand=self.scrollbar.set)

        # Posicionar cinta y barra de desplazamiento
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.cinta_canvas.pack(fill=tk.BOTH, expand=True)

        # Frame dentro del canvas para colocar las celdas de la cinta
        self.cinta_frame = tk.Frame(self.cinta_canvas, bg="#795548")
        self.cinta_canvas.create_window((0, 0), window=self.cinta_frame, anchor="nw")

        # Crear la cinta visual (labels vacíos por ahora)
        self.labels_cinta = []
        for i in range(50):
            label = tk.Label(self.cinta_frame, text="^", width=2, height=2, relief="solid", font=("Arial", 18), bg="white")
            label.grid(row=0, column=i, padx=2, pady=2)
            self.labels_cinta.append(label)

        # Ajustar el tamaño del canvas para que se ajuste al tamaño de la cinta
        self.cinta_frame.update_idletasks()
        self.cinta_canvas.config(scrollregion=self.cinta_canvas.bbox("all"))

        # Crear el menú principal
        self.menu_principal()

        # Barra decorativa
        self.liston_frame = tk.Frame(self.root, bg="#d7ccc8", height=20)  # Listón decorativo café claro
        self.liston_frame.pack(fill=tk.X)

        # Vincular eventos de teclado
        self.root.bind('<Left>', self.mover_izquierda)
        self.root.bind('<Right>', self.mover_derecha)

    def menu_principal(self):
        fondo = tk.Frame(self.root, bg="#4e342e")  # Fondo café oscuro del menú
        fondo.pack(fill=tk.BOTH, expand=True)

        # Opciones del menú
        # Opción 1: Llenar cinta automáticamente
        boton_ingreso_cinta = tk.Button(fondo, text="1. Llenar cinta automáticamente", font=("Arial", 16), bg="#bcaaa4", fg="white", command=self.llenar_cinta_aleatoria)
        boton_ingreso_cinta.pack(pady=10)

        # Opción 2: Cargar cinta previa (y guardar como cinta original)
        boton_cargar_cinta = tk.Button(fondo, text="2. Cargar cinta previa", font=("Arial", 16), bg="#bcaaa4", fg="white", command=self.cargar_cinta_previa)
        boton_cargar_cinta.pack(pady=10)

        # Opción 3: Operar la máquina (detallado con selección de Ha y He)
        boton_operar_maquina = tk.Button(fondo, text="3. Operar la máquina", font=("Arial", 16), bg="#bcaaa4", fg="white", command=self.configurar_operacion)
        boton_operar_maquina.pack(pady=10)

        # Opción 4: Mostrar cinta actual
        boton_mostrar_cinta = tk.Button(fondo, text="4. Mostrar cinta actual", font=("Arial", 16), bg="#bcaaa4", fg="white", command=self.mostrar_cinta)
        boton_mostrar_cinta.pack(pady=10)

        # Opción 5: Grabar cinta
        boton_grabar_cinta = tk.Button(fondo, text="5. Grabar cinta", font=("Arial", 16), bg="#bcaaa4", fg="white", command=self.grabar_cinta)
        boton_grabar_cinta.pack(pady=10)

        # Opción 6: Salir
        boton_salir = tk.Button(fondo, text="6. Salir", font=("Arial", 16), bg="#bcaaa4", fg="white", command=self.root.quit)
        boton_salir.pack(pady=10)

    # Opciones del menú
    def llenar_cinta_aleatoria(self):
        self.maquina.llenar_cinta_aleatoria()
        self.actualizar_cinta_visual()
        messagebox.showinfo("Cinta Generada", "La cinta ha sido llenada aleatoriamente.")

    def cargar_cinta_previa(self):
        if self.maquina.cinta_cargada:
            self.maquina.guardar_cinta_original()  # Guardar la cinta como cinta original
            self.actualizar_cinta_visual()
            messagebox.showinfo("Cinta cargada", "Se ha cargado la cinta generada previamente y guardado como cinta original.")
        else:
            messagebox.showerror("Error", "Primero debes llenar la cinta con la opción 1.")

    def mostrar_cinta(self):
        cinta = self.maquina.mostrar_cinta()
        messagebox.showinfo("Cinta actual", f"Cinta: {' '.join(cinta)}")

    def grabar_cinta(self):
        # Verificar que exista la cinta original
        if self.maquina.cinta_original is None:
            messagebox.showerror("Error", "Primero debes cargar una cinta original con la opción 2.")
            return

        # Crear el formato decorado para la cinta original y modificada
        cinta_original_decorada = ' '.join([f"| {simbolo} |" for simbolo in self.maquina.cinta_original])
        cinta_modificada_decorada = ' '.join([f"| {simbolo} |" for simbolo in self.maquina.mostrar_cinta()])

        # Guardar en archivo con cuadro de diálogo
        archivo = filedialog.asksaveasfilename(title="Guardar cinta", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if archivo:
            with open(archivo, 'w') as f:
                f.write("Cinta Original:\n")
                f.write(cinta_original_decorada + "\n\n")
                f.write("Cinta Modificada:\n")
                f.write(cinta_modificada_decorada)
            messagebox.showinfo("Guardado", "La cinta original y la cinta modificada han sido guardadas.")

    # Opción 3: Configurar operación de la máquina (selección de Ha y He, movimientos y modificación de caracteres)
    def configurar_operacion(self):
        if not self.maquina.cinta_cargada:
            messagebox.showerror("Error", "Primero debes cargar una cinta (opción 1 o 2).")
            return

        # Ventana de configuración para operar la máquina
        self.operacion_ventana = tk.Toplevel(self.root)
        self.operacion_ventana.title("Operar Máquina de Turing")
        self.operacion_ventana.geometry("600x300")

        # Selección de estado inicial (Ha) y de paro (He)
        seleccion_frame = tk.Frame(self.operacion_ventana, bg="lightgray")
        seleccion_frame.pack(pady=10)

        tk.Label(seleccion_frame, text="Seleccionar Ha:", font=("Arial", 14), bg="lightgray").grid(row=0, column=0)
        self.ha_var = tk.IntVar()
        ha_menu = ttk.Combobox(seleccion_frame, textvariable=self.ha_var, values=list(range(50)), width=5, state="readonly")
        ha_menu.grid(row=0, column=1)
        ha_menu.bind("<<ComboboxSelected>>", self.seleccionar_ha)

        tk.Label(seleccion_frame, text="Seleccionar He:", font=("Arial", 14), bg="lightgray").grid(row=0, column=2)
        self.he_var = tk.IntVar()
        he_menu = ttk.Combobox(seleccion_frame, textvariable=self.he_var, values=list(range(50)), width=5, state="readonly")
        he_menu.grid(row=0, column=3)
        he_menu.bind("<<ComboboxSelected>>", self.seleccionar_he)

        # Movimiento y modificación de carácter
        movimiento_frame = tk.Frame(self.operacion_ventana, bg="lightgray")
        movimiento_frame.pack(pady=10)

        # Selección de movimiento (D, I, N)
        tk.Label(movimiento_frame, text="Movimiento:", font=("Arial", 14), bg="lightgray").grid(row=0, column=0)
        self.movimiento_var = tk.StringVar(value="N")
        ttk.Radiobutton(movimiento_frame, text="Derecha", variable=self.movimiento_var, value="D").grid(row=0, column=1)
        ttk.Radiobutton(movimiento_frame, text="Izquierda", variable=self.movimiento_var, value="I").grid(row=0, column=2)
        ttk.Radiobutton(movimiento_frame, text="No Mover", variable=self.movimiento_var, value="N").grid(row=0, column=3)

        tk.Button(movimiento_frame, text="Aplicar Movimiento", command=self.aplicar_movimiento).grid(row=0, column=4, padx=10)

        # Modificación de carácter
        tk.Label(movimiento_frame, text="Nuevo símbolo:", font=("Arial", 14), bg="lightgray").grid(row=1, column=0)
        self.simbolo_entry = tk.Entry(movimiento_frame, width=5, font=("Arial", 14))
        self.simbolo_entry.grid(row=1, column=1)
        tk.Button(movimiento_frame, text="Aplicar Cambio", command=self.modificar_caracter).grid(row=1, column=2, padx=10)

    # Funciones de configuración de la operación de la máquina
    def seleccionar_ha(self, event):
        self.estado_ha = self.ha_var.get()
        self.resaltar_celda(self.estado_ha, "yellow")

    def seleccionar_he(self, event):
        self.estado_he = self.he_var.get()
        self.resaltar_celda(self.estado_he, "red")

    def resaltar_celda(self, posicion, color):
        for i, label in enumerate(self.labels_cinta):
            label.config(bg="white")
        self.labels_cinta[posicion].config(bg=color)

    def aplicar_movimiento(self):
        if self.estado_ha is None or self.estado_he is None:
            messagebox.showerror("Error", "Seleccione los estados Ha y He primero.")
            return

        # Verificar si estamos en el estado de paro o si encontramos un blanco
        if self.maquina.cabezal == self.estado_he:
            messagebox.showinfo("Estado de Paro", "Ha alcanzado el estado de paro.")
            self.finalizar_operacion()
            return
        if self.maquina.cinta[self.maquina.cabezal] == "^":
            messagebox.showwarning("Blanco Detectado", "No se puede continuar, se encontró un blanco.")
            self.finalizar_operacion()
            return

        # Aplicar el movimiento
        movimiento = self.movimiento_var.get()
        if movimiento == "D":
            self.maquina.cabezal = min(self.maquina.cabezal + 1, len(self.maquina.cinta) - 1)
        elif movimiento == "I":
            self.maquina.cabezal = max(self.maquina.cabezal - 1, 0)

        # Actualizar la posición resaltada
        self.resaltar_celda(self.maquina.cabezal, "yellow")

    def modificar_caracter(self):
        if not self.simbolo_entry.get():
            messagebox.showerror("Error", "Debe ingresar un símbolo.")
            return

        # Modificar el carácter en la posición actual
        nuevo_simbolo = self.simbolo_entry.get()[0]
        self.maquina.cinta[self.maquina.cabezal] = nuevo_simbolo
        self.actualizar_cinta_visual()
        self.simbolo_entry.delete(0, tk.END)

    def actualizar_cinta_visual(self):
        cinta = self.maquina.mostrar_cinta()
        for i in range(50):
            self.labels_cinta[i].config(text=cinta[i])

        # Asegurar que el canvas pueda desplazarse correctamente
        self.cinta_frame.update_idletasks()
        self.cinta_canvas.config(scrollregion=self.cinta_canvas.bbox("all"))

    def finalizar_operacion(self):
        # Cerrar la ventana de operación y reiniciar los estados Ha y He
        self.operacion_ventana.destroy()
        self.estado_ha = None
        self.estado_he = None
        self.maquina.cabezal = 0
        self.actualizar_cinta_visual()

    # Mover la cinta con las flechas del teclado
    def mover_izquierda(self, event):
        self.cinta_canvas.xview_scroll(-1, "units")

    def mover_derecha(self, event):
        self.cinta_canvas.xview_scroll(1, "units")

# Ejecutar el programa
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazTuring(root)
    root.mainloop()
