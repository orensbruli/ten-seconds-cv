import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager
import numpy as np
import pandas as pd
import seaborn as sns
import yaml



def print_available_fonts():
    global yaml_data
    font_manager = FontManager()
    fuentes_disponibles = [f.name for f in font_manager.ttflist]
    # Imprime las fuentes disponibles
    for fuente in sorted(set(fuentes_disponibles)):
        print(fuente)


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
    plt.xlabel('Date', fontdict={'fontsize': 16, 'fontfamily': 'Roboto Slab', 'fontweight': 'bold'})
    plt.ylabel('Skill', fontdict={'fontsize': 16, 'fontfamily': 'Roboto Slab', 'fontweight': 'bold'})
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
    # Create a dataframe from the data keeping the order of the columns entries
    df = pd.DataFrame(data, columns=['skill', 'period', 'level'])
    return df


def sum_of_skills(df):
    # Sum the level of each skill for each period
    df_grouped = df.groupby([df['period'].dt.to_period('Q')])['level'].sum()
    df_grouped = df_grouped.reset_index()
    # Convert the period to a datetime object
    df_grouped['period'] = df_grouped['period'].dt.to_timestamp()
    return df_grouped


def main():
    yaml_data = load_yaml_data_from_file('data.md')
    df = yaml_to_dataframe(yaml_data)
    original_skill_order = df['skill'].unique()
    df = format_periods(df)
    df_grouped = group_periods(df)
    # Preparamos los datos para el mapa de calor mantiendo el orden las filas y columnas
    heatmap_data = pd.pivot_table(df_grouped, values='level', index='skill', columns='period', aggfunc=np.mean)
    heatmap_data.columns = heatmap_data.columns.to_series().dt.strftime('%Y-%m')
    heatmap_data = heatmap_data.fillna(0)
    # sort by the sum of the skills
    # heatmap_data = heatmap_data.reindex(heatmap_data.sum().sort_values(ascending=False).index)
    heatmap_data = heatmap_data.reindex(original_skill_order)
    #
    # Ajustamos el tamaño del gráfico
    fig, ax = plt.subplots(figsize=(20, 4))
    # cmap = sns.light_palette("darkgreen", as_cmap=True)
    # Crear el mapa de calor
    custom_colors = sns.color_palette("YlGn", as_cmap=True)
    # add blue at the beginning to show the lowest values
    custom_colors = sns.color_palette(["#ECECEC"] + list(sns.color_palette("YlGn", 10).as_hex()), as_cmap=True)

    sns.heatmap(heatmap_data, annot=False, cmap=custom_colors, linewidths=1, square=True, ax=ax)
    ax = configure_labels(ax)
    ax.set_title('Level of skill', loc='center', pad=24,
                 fontdict={'fontsize': 16, 'fontweight': 'bold', 'fontfamily': 'Roboto Slab'})

    ax.yaxis.tick_right()

    # Encuentra la barra de colores actual en el gráfico, si existe
    cbar = ax.collections[0].colorbar

    # Si existe la barra de colores, ajusta su posición
    if cbar:
        cbar.remove()  # Primero, removemos la barra de colores existente
        cbar = fig.colorbar(ax.collections[0], ax=ax, location='left', shrink=0.65, pad=0.04, fraction=0.01)

    plt.subplots_adjust(left=0.02, right=0.92, top=0.999, bottom=0.001)

    #save the figure
    fig.savefig('heatmap.eps', format='eps')


if __name__ == '__main__':
    main()
