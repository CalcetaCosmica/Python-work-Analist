import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, Frame, Text, Scrollbar, RIGHT, BOTTOM, BOTH, END
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def radar_chart(categories, meta_values, alcanzado_values, title):
    # Número de variables (categorías)
    num_vars = len(categories)

    # Ángulo del primer eje
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Cerrar el gráfico
    meta_values += meta_values[:1]
    alcanzado_values += alcanzado_values[:1]
    angles += angles[:1]

    # Inicializar la gráfica polar
    ax.fill(angles, meta_values, color='blue', alpha=0.25)
    ax.plot(angles, meta_values, color='blue', linewidth=2)
    ax.fill(angles, alcanzado_values, color='green', alpha=0.25)
    ax.plot(angles, alcanzado_values, color='green', linewidth=2)

    # Título
    ax.set_title(title, size=20, y=1.1)

    # Resumen de los datos
    summary = "Resumen de Datos:\n\n"
    for category, meta_value, alcanzado_value in zip(categories, meta_values[:-1], alcanzado_values[:-1]):
        summary += f"{category}: Meta = {meta_value}%, Alcanzado = {alcanzado_value}%\n"

    # Mostrar el resumen debajo de la gráfica
    text_box.delete(1.0, END)
    text_box.insert(END, summary)

def submit_data():
    categories = [category_entry.get() for category_entry in category_entries]
    meta_values = [float(meta_entry.get()) if meta_entry.get() else 0.0 for meta_entry in meta_entries]
    alcanzado_values = [float(alcanzado_entry.get()) if alcanzado_entry.get() else 0.0 for alcanzado_entry in alcanzado_entries]

    # Normalizar los valores a un rango de 0 a 100
    max_value = max(max(meta_values), max(alcanzado_values))
    if max_value > 100:
        scale_factor = 100 / np.log10(max_value)
        meta_values = [np.log10(value) * scale_factor for value in meta_values]
        alcanzado_values = [np.log10(value) * scale_factor for value in alcanzado_values]
    else:
        meta_values = [value / max_value * 100 for value in meta_values]
        alcanzado_values = [value / max_value * 100 for value in alcanzado_values]

    radar_chart(categories, meta_values, alcanzado_values, 'Comparación de Metas y Alcanzado')
    ax.set_yticklabels([])
    ax.set_xticks(np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist())
    ax.set_xticklabels(categories)

    plt.legend(['Meta', 'Alcanzado'], loc='upper right')
    canvas.draw()

def clear_data():
    for entry in category_entries + meta_entries + alcanzado_entries:
        entry.delete(0, END)
    text_box.delete(1.0, END)
    ax.clear()  # Limpiar la gráfica
    canvas.draw()  # Volver a dibujar la gráfica vacía

# Crear ventana
root = Tk()
root.title("Ingreso de Datos")

# Configurar figura de Matplotlib
fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side='left', fill=BOTH, expand=1)

# Crear un Frame para contener el cuadro de entrada y el cuadro de texto del resumen
frame = Frame(root)
frame.pack(side=BOTTOM, fill=BOTH, expand=1)

# Cuadro de texto para el resumen de datos
text_box = Text(frame, height=10, width=50)
text_box.pack(side=RIGHT, fill=BOTH, expand=1)

# Barra de desplazamiento para el cuadro de texto
scrollbar = Scrollbar(frame, command=text_box.yview)
scrollbar.pack(side=RIGHT, fill='y')
text_box.config(yscrollcommand=scrollbar.set)

# Cuadro de entrada de datos
input_frame = Frame(frame)
input_frame.pack(side=BOTTOM, fill=BOTH, expand=1)

# Etiquetas y entradas para categorías
Label(input_frame, text="Categorías:").grid(row=0, column=0)
category_entries = [Entry(input_frame) for _ in range(5)]
for i, entry in enumerate(category_entries):
    entry.grid(row=i+1, column=0)

# Etiquetas y entradas para metas
Label(input_frame, text="Meta:").grid(row=0, column=1)
meta_entries = [Entry(input_frame) for _ in range(5)]
for i, entry in enumerate(meta_entries):
    entry.grid(row=i+1, column=1)

# Etiquetas y entradas para alcanzado
Label(input_frame, text="Alcanzado:").grid(row=0, column=2)
alcanzado_entries = [Entry(input_frame) for _ in range(5)]
for i, entry in enumerate(alcanzado_entries):
    entry.grid(row=i+1, column=2)

# Botones
submit_button = Button(input_frame, text="Generar Gráficos", command=submit_data)
submit_button.grid(row=6, column=0, columnspan=2)

clear_button = Button(input_frame, text="Limpiar Datos", command=clear_data)
clear_button.grid(row=6, column=2)

root.mainloop()

