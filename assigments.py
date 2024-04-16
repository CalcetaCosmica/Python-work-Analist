import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os

# Especifica la ruta del archivo .dat
ruta_archivo = 'C:/Users/hugo.aguilar/Documents/Projects/ROLL PREVIO_REFERENCIAS.txt'

# Lee el archivo .dat
data = pd.read_table(ruta_archivo, header=0, encoding='utf-8')
data.replace('–', 'ñ', regex=True, inplace=True)

# Verificar si 'IDIOMA' está en las columnas de data
if 'IDIOMA' in data.columns:
    today_date = datetime.datetime.now().strftime('%a %m/%d')

    # Filtrar las columnas correspondientes al día de hoy
    filtered_data = data[['Name', 'IDIOMA', today_date]]

    # Filtrar los agentes que no están en "Off" para la fecha de hoy
    for col in filtered_data.columns[2:]:
        filtered_data = filtered_data[filtered_data[col] != 'Off']

    # Excluir registros que contienen "Skip Tracing Asignaciones"
    filtered_data = filtered_data[~filtered_data['Name'].str.contains('Skip Tracing Asignaciones')]

    # Mostrar solo los primeros 3 caracteres en la columna 'IDIOMA' y reemplazar "ñ" por "n"
    filtered_data['IDIOMA'] = filtered_data['IDIOMA'].str.slice(0, 3).str.replace('ñ', 'n')

    # Cambiar el orden del nombre y agregar un punto al final
    filtered_data['Name'] = filtered_data['Name'].apply(lambda x: x.split(',')[1].strip() + ' ' + x.split(',')[0].strip() + '.')

    # Crear la tabla
    fig, ax = plt.subplots()

    # Ajustar el título a la parte superior
    #plt.suptitle('SKIP TRACING ASSIGNMENTS', fontsize=16, y=0.95)

    # Agregar espacio entre el título y la tabla
    plt.subplots_adjust(top=1.14)

    # Ocultar ejes
    ax.axis('off')

    # Crear la tabla con fondo blanco y texto justificado
    table = ax.table(cellText=filtered_data.values, loc='center', cellLoc='center', colLabels=filtered_data.columns,
                     cellColours=[['white'] * len(filtered_data.columns)] * len(filtered_data))

    # Modificar los estilos de las celdas
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(2, 2)  # Aumentar tamaño de la tabla
    for key, cell in table.get_celld().items():
        cell.set_text_props(fontsize=12, fontname='Book Antiqua', color='black', verticalalignment='center',
                            horizontalalignment='left')

    # Personalizar los encabezados de la tabla con color negro y alineación centrada
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # Fila de encabezados
            cell.set_facecolor('black')  # Color negro para los encabezados
            cell.set_text_props(weight='bold', color='white', horizontalalignment='center')  # Texto blanco en negrita con alineación centrada

    # Set gray borders to the bottom cells
    for (i, j), cell in table.get_celld().items():
        if i != 0 and i == len(filtered_data):  # Bottom cells
            cell.set_edgecolor('gray')

    # Redondear los bordes de la tabla
    table.auto_set_column_width(col=list(range(len(filtered_data.columns))))
    for key, cell in table.get_celld().items():
        cell.set_edgecolor('gray')  # Establecer el color del borde de la celda en blanco

    # Ajustar diseño
    plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

    # Guardar la tabla como un archivo PNG
    ruta_imagen = 'table.png'
    plt.savefig(ruta_imagen)

    # Mostrar la tabla
    plt.show()

    # Comprobar si se guardó la imagen correctamente
    if os.path.exists(ruta_imagen):
        print("La tabla se ha guardado correctamente como 'table.png' en la misma carpeta que el script.")
    else:
        print("¡Hubo un problema al guardar la tabla como un archivo PNG!")
else:
    print("La columna 'IDIOMA' no está presente en el DataFrame.")
