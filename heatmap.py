import yaml
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# YAML data to be used as example
yaml_data_string = """
skills_details:
  - name: Python
    levels:
      - grade: 1
        period: 2020-01-01 to 2020-12-31
      - grade: 2
        period: 2021-01-01 to 2021-12-31
      - grade: 3
        period: 2022-01-01 to 2024-01-14
  - name: Docker
    levels:
      - grade: 1
        period: 2019-01-01 to 2019-12-31
      - grade: 2
        period: 2020-01-01 to 2024-01-14
"""

from matplotlib.font_manager import FontManager


def print_available_fonts():
    global yaml_data
    font_manager = FontManager()
    fuentes_disponibles = [f.name for f in font_manager.ttflist]
    # Imprime las fuentes disponibles
    for fuente in sorted(set(fuentes_disponibles)):
        print(fuente)


print_available_fonts()

# Load the YAML data from a string
def load_yaml_data(yaml_data_string):
    yaml_data = yaml.load(yaml_data_string, Loader=yaml.FullLoader)
    return yaml_data

def load_yaml_data_from_file(yaml_file):
    with open(yaml_file) as file:
        docs = yaml.load_all(file, yaml.FullLoader)
        for yaml_data in docs:
            if yaml_data is not None and 'skills_details' in yaml_data:
                break
        if 'skills_details' not in yaml_data:
            raise Exception('Invalid YAML file. Missing skills section')
    return yaml_data

def configure_labels(ax):
    # Obtener las etiquetas actuales del eje x
    ax = plt.gca()
    xlabels = [label.get_text() for label in ax.get_xticklabels()]
    # filtrar las etiquetas para mostrar solo los años
    xlabels = [label if label.endswith('01') else '' for label in xlabels]
    # Establecer las etiquetas filtradas en el eje x
    ax.set_xticks([xlabels.index(label) for label in xlabels])
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    # Rotar las etiquetas para mejor visualización
    plt.xticks(rotation=90)
    # Ajustes de visualización
    plt.xlabel('Date', fontdict={'fontsize': 16, 'fontfamily': 'Liberation Mono', 'fontweight': 'bold'})
    plt.ylabel('Skill', fontdict={'fontsize': 16, 'fontfamily': 'Liberation Mono', 'fontweight': 'bold'})
    return ax


def group_periods(df):
    # Group by skill and period and calculate the average level
    # Use M for monthly, Q for quarterly, Y for yearly averages
    df_grouped = df.groupby([df['skill'], df['period'].dt.to_period('Q')])['level'].mean()
    df_grouped = df_grouped.reset_index()
    # Convertimos el periodo a formato de fecha para el gráfico
    df_grouped['period'] = df_grouped['period'].dt.to_timestamp()
    return df_grouped


def format_periods(df):
    # Some periods can contain words like "current" or "actually" and must be replaced with the current date
    df['period'] = df['period'].apply(lambda x: x.replace('current', pd.Timestamp.now().strftime('%Y-%m-%d')))
    # convert the period to a list of months between the start and end date
    df['period'] = df['period'].apply(
        lambda x: pd.date_range(start=x.split(' to ')[0], end=x.split(' to ')[1], freq='W').tolist())
    # create a new dataframe with the period expanded
    df = df.explode('period')
    # Convert the period to a datetime object
    df['period'] = pd.to_datetime(df['period'])
    return df


def yaml_to_dataframe(yaml_data):
    # convert to a structured like this
    # {
    #     'year': year,
    #     'week': week,
    #     'skill': name,
    #     'level': grade
    # }
    data = []
    for skill in yaml_data['skills_details']:
        for level in skill['levels']:
            data.append({
                'period': level['period'],
                'skill': skill['name'],
                'level': level['grade']
            })
    df = pd.DataFrame(data)
    return df

def main():
    yaml_data = load_yaml_data_from_file('data.md')
    df = yaml_to_dataframe(yaml_data)
    df = format_periods(df)
    df_grouped = group_periods(df)
    # Preparamos los datos para el mapa de calor
    heatmap_data = pd.pivot_table(df_grouped, values='level', index='skill', columns='period', aggfunc=np.mean)
    heatmap_data.columns = heatmap_data.columns.to_series().dt.strftime('%Y-%m')
    heatmap_data = heatmap_data.fillna(0)
    # Ajustamos el tamaño del gráfico
    plt.figure(figsize=(20, 6))
    # cmap = sns.light_palette("darkgreen", as_cmap=True)
    # Crear el mapa de calor
    custom_colors = sns.color_palette("YlGn", as_cmap=True)
    # add blue at the beginning to show the lowest values
    custom_colors = sns.color_palette(["#ECECEC"] + list(sns.color_palette("YlGn", 10).as_hex()), as_cmap=True)

    ax = sns.heatmap(heatmap_data, annot=False, cmap=custom_colors, linewidths=1, square=True)
    ax = configure_labels(ax)
    ax.set_title('Level of skill', loc='center', pad=24,
                 fontdict={'fontsize': 16, 'fontweight': 'bold', 'fontfamily': 'Liberation Mono'})

    # Mover la leyenda (barra de colores) a la parte inferior
    # cbar = plt.colorbar(ax.collections[0], ax=ax, location='bottom', shrink=0.5)
    plt.show()

if __name__ == '__main__':
    main()
