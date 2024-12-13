from experta import *
import tkinter as tk
from tkinter import messagebox, ttk

# Definición de las clases de datos
class DatosSuelo(Fact):
    """Información del suelo"""
    humedad = Field(float)
    pH = Field(float)
    tipo_suelo = Field(str)
    nutrientes = Field(str)

class DatosCultivo(Fact):
    """Información del cultivo"""
    tipo_cultivo = Field(str)
    estado_cultivo = Field(str)

# Motor del sistema experto
class SistemaExpertoAgricultura(KnowledgeEngine):
    @Rule(DatosSuelo(nutrientes="bajo"), DatosCultivo(tipo_cultivo="maíz"))
    def fertilizacion_maiz(self):
        self.recomendacion = "Recomendación: Para maíz con nutrientes bajos, aplicar fertilizante NPK con alta concentración de nitrógeno."

    @Rule(DatosSuelo(nutrientes="bajo"), DatosCultivo(tipo_cultivo="trigo"))
    def fertilizacion_trigo(self):
        self.recomendacion = "Recomendación: Para trigo con nutrientes bajos, aplicar urea y fosfato diamónico."

    @Rule(DatosSuelo(humedad=P(lambda x: x < 30)))
    def bajo_nivel_humedad(self):
        self.recomendacion = "El suelo tiene baja humedad. Incrementar la frecuencia de riego."

    @Rule(DatosCultivo(estado_cultivo="enfermo"))
    def cultivo_enfermo(self):
        self.recomendacion = "El cultivo está enfermo. Realizar análisis fitosanitario y aplicar tratamientos adecuados."

    def __init__(self):
        super().__init__()
        self.recomendacion = "No hay recomendaciones específicas."

# Interfaz gráfica mejorada con Tkinter
class InterfazGrafica:
    def __init__(self, root):
        self.engine = SistemaExpertoAgricultura()
        self.root = root
        self.root.title("Asistente Agrícola Inteligente")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f8ff")

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = tk.Label(
            self.root, text="Asistente Agrícola Inteligente",
            font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#333"
        )
        title_label.pack(pady=10)

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#e0f7fa")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Entrada de humedad del suelo
        self.create_label_entry(main_frame, "Humedad del suelo (%):", "humedad")

        # Entrada de pH del suelo
        self.create_label_entry(main_frame, "pH del suelo:", "ph")

        # Selección de tipo de suelo
        self.label_tipo_suelo = tk.Label(main_frame, text="Tipo de suelo:", bg="#e0f7fa")
        self.label_tipo_suelo.pack(pady=5)
        self.tipo_suelo_var = tk.StringVar()
        self.tipo_suelo_combo = ttk.Combobox(
            main_frame, textvariable=self.tipo_suelo_var,
            values=["Arcilloso", "Arenoso", "Limoso"], state="readonly"
        )
        self.tipo_suelo_combo.pack()

        # Selección del nivel de nutrientes
        self.label_nutrientes = tk.Label(main_frame, text="Nivel de nutrientes:", bg="#e0f7fa")
        self.label_nutrientes.pack(pady=5)
        self.nutrientes_var = tk.StringVar()
        self.nutrientes_combo = ttk.Combobox(
            main_frame, textvariable=self.nutrientes_var,
            values=["Alto", "Bajo"], state="readonly"
        )
        self.nutrientes_combo.pack()

        # Selección del tipo de cultivo
        self.label_tipo_cultivo = tk.Label(main_frame, text="Tipo de cultivo:", bg="#e0f7fa")
        self.label_tipo_cultivo.pack(pady=5)
        self.tipo_cultivo_var = tk.StringVar()
        self.tipo_cultivo_combo = ttk.Combobox(
            main_frame, textvariable=self.tipo_cultivo_var,
            values=["Maíz", "Trigo"], state="readonly"
        )
        self.tipo_cultivo_combo.pack()

        # Selección del estado del cultivo
        self.label_estado_cultivo = tk.Label(main_frame, text="Estado del cultivo:", bg="#e0f7fa")
        self.label_estado_cultivo.pack(pady=5)
        self.estado_cultivo_var = tk.StringVar()
        self.estado_cultivo_combo = ttk.Combobox(
            main_frame, textvariable=self.estado_cultivo_var,
            values=["Saludable", "Enfermo"], state="readonly"
        )
        self.estado_cultivo_combo.pack()

        # Botón para obtener recomendación
        self.recommend_button = tk.Button(
            main_frame, text="Obtener Recomendación", command=self.get_recommendation,
            bg="#00796b", fg="white", font=("Helvetica", 12, "bold")
        )
        self.recommend_button.pack(pady=20)

    def create_label_entry(self, parent, text, var_name):
        label = tk.Label(parent, text=text, bg="#e0f7fa")
        label.pack(pady=5)
        entry = tk.Entry(parent)
        setattr(self, f"{var_name}_entry", entry)
        entry.pack()

    def get_recommendation(self):
        try:
            humedad = float(self.humedad_entry.get())
            ph = float(self.ph_entry.get())
            tipo_suelo = self.tipo_suelo_var.get().lower()
            nutrientes = self.nutrientes_var.get().lower()
            tipo_cultivo = self.tipo_cultivo_var.get().lower()
            estado_cultivo = self.estado_cultivo_var.get().lower()

            if not tipo_suelo or not nutrientes or not tipo_cultivo or not estado_cultivo:
                messagebox.showerror("Error", "Complete todos los campos.")
                return

            self.engine.reset()
            self.engine.declare(
                DatosSuelo(humedad=humedad, pH=ph, tipo_suelo=tipo_suelo, nutrientes=nutrientes),
                DatosCultivo(tipo_cultivo=tipo_cultivo, estado_cultivo=estado_cultivo)
            )
            self.engine.run()

            messagebox.showinfo("Recomendación", self.engine.recomendacion)

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos.")

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    app = InterfazGrafica(root)
    root.mainloop()
