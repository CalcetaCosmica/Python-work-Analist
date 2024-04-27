import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import datetime

def get_current_date():
    """
    Función para obtener la fecha y hora actual en el formato deseado.
    """
    fecha_hora_actual = datetime.datetime.now().strftime("%B - %d")
    return fecha_hora_actual


# Obtener la fecha y hora actual
fecha_hora_actual = get_current_date()

# Encabezado
titulo = "Skiptracer - Recoveries"

# Especifica la ruta del archivo .dat
ruta_archivo = 'C:/Users/hugo.aguilar/Documents/Report for RK/Data/Skip_recovery.txt'

# Lee el archivo .dat
data = pd.read_table(ruta_archivo, header=0, encoding='utf-8')

# Selecciona las columnas requeridas
columnas_requeridas = ['Rk', 'Full Name', 'Language', 'Overall Goal Attaint%']
data_seleccionado = data[columnas_requeridas]

# Eliminar filas con valores NaN
data_sin_nan = data_seleccionado.dropna()

# Ordenar por la columna 'Rk' de menor a mayor
# Ordenar los datos por la columna 'Language' de Z a A y luego por la columna 'Rk' de menor a mayor
# data_ordenado = data_sin_nan.sort_values(by='Language', ascending=False)
# data_ordenado = data_sin_nan.sort_values(by='Rk', ascending=True)
data_ordenado = data_sin_nan.sort_values(by=['Language', 'Rk'], ascending=[False, True])


# Convertir la columna 'Rk' a enteros
data_ordenado['Rk'] = data_ordenado['Rk'].astype(int)

# Eliminar el carácter '%' de la columna 'Overall Goal Attaint%'
data_ordenado['Overall Goal Attaint%'] = data_ordenado['Overall Goal Attaint%'].str.replace('%', '')

# Convertir la columna 'Overall Goal Attaint%' a tipo numérico
data_ordenado['Overall Goal Attaint%'] = pd.to_numeric(data_ordenado['Overall Goal Attaint%'])




# Tamaño de la tabla en eje X, Y
plt.figure(figsize=(7, 1))

# Configurar el color de fondo de la figura
plt.gcf().set_facecolor((0.475, 0.855, 0.58))  

# Agregar el título a la figura utilizando plt.text
plt.text(0.5, 0.7, titulo, fontsize=25, color='black', fontweight='bold', ha='center', va='center', transform=plt.gcf().transFigure)

# Agregar la fecha a la figura utilizando plt.text
plt.text(0.5, 0.4, fecha_hora_actual, color='black', fontsize=18, ha='center', va='center',fontweight='bold' ,  transform=plt.gcf().transFigure)



#Tamaño de las columnas
table = plt.table(cellText=data_ordenado.values, colLabels=data_ordenado.columns, loc='bottom', colWidths=[0.05, 0.3, 0.1, 0.15])

# Modificar los estilos de las celdas
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(2, 2)  # Aumentar tamaño de la tabla

# Definir una paleta de colores personalizada
colors = [(0.3, 0.7, 0.3), (1, 0.5, 0.5), (1, 1, 0.5), (0.5, 1, 0.5)]  # Verde oscuro, Rojo, Amarillo, Verde
cmap = LinearSegmentedColormap.from_list("", colors)

# Cambiar el color de fondo del encabezado y añadir bordes
header_cells = table.get_celld()
for key in header_cells:
    cell = header_cells[key]
    cell.set_facecolor('#BDECB6')
    cell.set_edgecolor('black')
    cell.set_linewidth(1.5)

# Alinear el contenido de las celdas
for key, cell in table.get_celld().items():
    cell.set_text_props(fontsize=11, fontweight='bold', fontname='Arial', color='black', 
                        verticalalignment='center', horizontalalignment='center')

# Añadir bordes a las celdas de datos
for key, cell in table.get_celld().items():
    if key[0] != 0:
        cell.set_edgecolor('black')
        cell.set_linewidth(1)

# Aplicar formato condicional a la última columna
last_column_values = data_ordenado['Overall Goal Attaint%'].values

for i, value in enumerate(last_column_values):
    if value > 100:
        color_index = 0  # Verde fuerte para valores mayores a 100
    elif value >= 90:
        color_index = 3  # Verde para valores entre 90 y 100
    elif value >= 70:
        color_index = 2  # Amarillo para valores entre 70 y 90
    else:
        color_index = 1  # Rojo para valores menores a 70
    cell = table.get_celld()[(i + 1, 3)]
    cell.set_facecolor(colors[color_index])


# Cambiar color de fondo de la primera fila
for j in range(len(data_ordenado.columns)):
    cell = table.get_celld()[(0, j)]
    cell.set_facecolor((0.5, 0.9, 0.5))  # Verde oscuro
    
# Ocultar ejes
plt.axis('off')


# Guardar la tabla como un archivo PNG
ruta_imagen = 'C:/Users/hugo.aguilar/Documents/Report for RK/image/Skip_recovery.png'
plt.savefig(ruta_imagen, bbox_inches='tight', pad_inches=0, transparent=False)


# Mostrar la tabla
plt.show()
