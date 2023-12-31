import pandas as pd

# Cargar los conjuntos de datos originales
bicing_data = pd.read_csv('dataset_generation/temporary_datasets/dataset_without_demand_satisfied.csv')
demand_data = pd.read_csv('dataset_generation/temporary_datasets/demand_satisfaction.csv')

print(bicing_data[['year', 'month', 'day', 'hour']].drop_duplicates().count())
print(demand_data[['year', 'month', 'day', 'hour']].drop_duplicates().count())

# Fusionar los conjuntos de datos utilizando las columnas de fecha y hora como clave
merged_data = pd.merge(bicing_data, demand_data, on=['year', 'month', 'day', 'hour'], how='outer', indicator=True)

# Separar los registros que no hacen match en ambos conjuntos de datos
no_match = merged_data[merged_data['_merge'] != 'both']

# Filtrar los registros que hacen match para el dataset final
final_data = merged_data[merged_data['_merge'] == 'both'].drop(columns=['_merge'])

# Guardar el nuevo conjunto de datos fusionado en un archivo CSV
final_data.to_csv('dataset_generation//dataset.csv', index=False)

# Opcional: Guardar los registros que no hacen match en otro archivo CSV para su revisión
no_match.to_csv('dataset_generation/temporary_datasets/raros.csv', index=False)

print("Proceso completado. El nuevo archivo CSV con datos fusionados ha sido creado.")
print(f"Se encontraron {len(no_match)} registros que no hacen match.")
