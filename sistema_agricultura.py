from experta import *
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

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

    @Rule(DatosCultivo(estado_cultivo="perfecto"), NOT(DatosSuelo(nutrientes="bajo")), NOT(DatosSuelo(humedad=P(lambda x: x < 30))))
    def cultivo_perfecto(self):
        self.recomendacion = "El cultivo está en perfecto estado. Mantenga un riego y fertilización regulares."

    @Rule(DatosSuelo(nutrientes="bajo"), DatosCultivo(tipo_cultivo="arroz"))
    def fertilizacion_arroz(self):
        self.recomendacion = "Recomendación: Para arroz con nutrientes bajos, aplicar sulfato de amonio y potasio."

    @Rule(DatosSuelo(nutrientes="bajo"), DatosCultivo(tipo_cultivo="soya"))
    def fertilizacion_soya(self):
        self.recomendacion = "Recomendación: Para soya con nutrientes bajos, utilizar fertilizante con fósforo y calcio."

    @Rule(DatosSuelo(nutrientes="bajo"), DatosCultivo(tipo_cultivo="papas"))
    def fertilizacion_papas(self):
        self.recomendacion = "Recomendación: Para papas con nutrientes bajos, aplicar fertilizante rico en potasio y magnesio."

    def __init__(self):
        super().__init__()
        self.recomendacion = "No hay recomendaciones específicas."

# Interfaz gráfica mejorada con Tkinter
class InterfazGrafica:
    def __init__(self, root):
        self.engine = SistemaExpertoAgricultura()
        self.root = root
        self.root.title("Asistente Agrícola Inteligente")
        self.root.geometry("700x700")
        self.root.configure(bg="#f0f8ff")

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = tk.Label(
            self.root, text="Asistente Agrícola Inteligente",
            font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#333"
        )
        title_label.pack(pady=10)

        # Imagen de encabezado
        image = Image.open("agricultura.jpg")
        image = image.resize((600, 150), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(self.root, image=self.photo, bg="#f0f8ff")
        image_label.pack(pady=10)

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#e0f7fa")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Mostrar límites de estándares
        standards_label = tk.Label(
            main_frame, text="Estándares: Humedad (30-60%), pH (5.5-7.5)",
            bg="#e0f7fa", font=("Helvetica", 10, "italic")
        )
        standards_label.pack(pady=5)

        # Entrada de humedad del suelo
        self.create_label_entry(main_frame, "Humedad del suelo (%):", "humedad")

        # Entrada de pH del suelo
        self.create_label_entry(main_frame, "pH del suelo:", "ph")

        # Selección de tipo de suelo
        self.create_dropdown(main_frame, "Tipo de suelo:", "tipo_suelo_var", ["Arcilloso", "Arenoso", "Limoso"])

        # Selección del nivel de nutrientes
        self.create_dropdown(main_frame, "Nivel de nutrientes:", "nutrientes_var", ["Alto", "Bajo"])

        # Selección del tipo de cultivo
        self.create_dropdown(main_frame, "Tipo de cultivo:", "tipo_cultivo_var", ["Maíz", "Trigo", "Arroz", "Soya", "Papas"])

        # Selección del estado del cultivo
        self.create_dropdown(main_frame, "Estado del cultivo:", "estado_cultivo_var", ["Perfecto", "Enfermo"])

        # Botón para obtener recomendación
        recommend_button = tk.Button(
            main_frame, text="Obtener Recomendación", command=self.get_recommendation,
            bg="#00796b", fg="white", font=("Helvetica", 12, "bold")
        )
        recommend_button.pack(pady=20)

    def create_label_entry(self, parent, text, var_name):
        label = tk.Label(parent, text=text, bg="#e0f7fa")
        label.pack(pady=5)
        entry = tk.Entry(parent)
        setattr(self, f"{var_name}_entry", entry)
        entry.pack()

    def create_dropdown(self, parent, text, var_name, options):
        label = tk.Label(parent, text=text, bg="#e0f7fa")
        label.pack(pady=5)
        combo_var = tk.StringVar()
        setattr(self, var_name, combo_var)
        combo = ttk.Combobox(parent, textvariable=combo_var, values=options, state="readonly")
        combo.pack()

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
