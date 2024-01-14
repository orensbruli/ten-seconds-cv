import yaml
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# YAML data to be used as example
yaml_data_string = """
skills:
  - name: Python Programming
    levels:
      - grade: 1
        period: 2020-01-01 to 2020-12-31
      - grade: 2
        period: 2021-01-01 to 2021-12-31
      - grade: 3
        period: 2022-01-01 to 2024-01-14
  - name: Web Development
    levels:
      - grade: 1
        period: 2019-01-01 to 2019-12-31
      - grade: 2
        period: 2020-01-01 to 2024-01-14
"""



# Read the YAML data
yaml_data = yaml.safe_load(yaml_data_string)

# convert to an structured like this
# {
#     'year': year,
#     'week': week,
#     'skill': name,
#     'level': grade
# }
data = []
for skill in yaml_data['skills']:
    for level in skill['levels']:
        data.append({
            'period': level['period'],
            'skill': skill['name'],
            'level': level['grade']
        })
df = pd.DataFrame(data)

# convert the period to a list of months between the start and end date
df['period'] = df['period'].apply(lambda x: pd.date_range(start=x.split(' to ')[0], end=x.split(' to ')[1], freq='W').tolist())

print(df)

# create a new dataframe with the period expanded
df = df.explode('period')
print(df)


# Convertimos las fechas a un formato de pandas datetime para facilitar el manejo
df['period'] = pd.to_datetime(df['period'])

# Agrupamos los datos por mes o trimestre y calculamos la media
# Puedes cambiar 'M' a 'Q' para agrupar por trimestres
df_grouped = df.groupby([df['skill'], df['period'].dt.to_period('M')])['level'].mean()
df_grouped = df_grouped.reset_index()

# Convertimos el periodo a formato de fecha para el gráfico
df_grouped['period'] = df_grouped['period'].dt.to_timestamp()

# Preparamos los datos para el mapa de calor
heatmap_data = pd.pivot_table(df_grouped, values='level', index='skill', columns='period', aggfunc=np.mean)
heatmap_data.columns = heatmap_data.columns.to_series().dt.strftime('%Y-%m')

# Ajustamos el tamaño del gráfico
plt.figure(figsize=(20, 10))

# Crear el mapa de calor
sns.heatmap(heatmap_data, annot=False, cmap='YlGnBu', linewidths=.1, square=True)

# Obtener las etiquetas actuales del eje x
ax = plt.gca()
xlabels = [label.get_text() for label in ax.get_xticklabels()]

# Filtrar las etiquetas para mostrar solo junio y diciembre
filtered_labels = [label for label in xlabels if "-06" in label or "-12" in label]

# Establecer las etiquetas filtradas en el eje x
ax.set_xticks([xlabels.index(label) for label in filtered_labels])
ax.set_xticklabels(filtered_labels)

# Rotar las etiquetas para mejor visualización
plt.xticks(rotation=90)

# Ajustes de visualización
plt.title('Skill Level Over Time')
plt.xlabel('Date')
plt.ylabel('Skill')

plt.show()