import csv

def add_zero_columns_to_256(csv_filename, output_filename):
    # Leer los datos del archivo CSV original
    with open(csv_filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        all_rows = [row for row in reader]

    # Determinar el número de columnas en el archivo original
    number_of_columns = len(all_rows[0])

    # Calcular cuántas columnas de cero se necesitan añadir
    columns_to_add = 256 - number_of_columns

    # Añadir las columnas de cero a cada fila
    for row in all_rows:
        row.extend([0] * columns_to_add)

    # Escribir el resultado a un nuevo archivo CSV
    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_rows)

# Ejemplo de uso de la función
add_zero_columns_to_256('ptbdb_normal.csv', 'new_normal_signal.csv')
add_zero_columns_to_256('ptbdb_abnormal.csv', 'new_abnormal_signal.csv')
