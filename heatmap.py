import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager
import numpy as np
import pandas as pd
import seaborn as sns
import yaml



def print_available_fonts():
    """
    This function retrieves the list of available fonts using a FontManager object
    and prints the font names to the console. It first filters out duplicates from
    the list of available fonts using a set() function before sorting the unique
    values and iterating over them to print each font name.

    """
    global yaml_data
    font_manager = FontManager()
    fuentes_disponibles = [f.name for f in font_manager.ttflist]
    # Imprime las fuentes disponibles
    for fuente in sorted(set(fuentes_disponibles)):
        print(fuente)


# Load the YAML data from a string
def load_yaml_data(yaml_data_string):
    """
    The provided code defines a Python function called `load_yaml_data`. This
    function takes one argument of type string called `yaml_data_string` and it
    loads the content of the string using the YAML library to parse yaml strings
    and return the result as a dictionary object (i.e., representing the top-level
    object of the yaml input) utilizing a specialized loader (`yaml.FullLoader`)
    capable of loading the complete yaml document

    Args:
        yaml_data_string (str): The `yaml_data_string` parameter is a string that
            contains the YAML data to be loaded into a Python dictionary. It serves
            as the input file or data source for the function to parse and load
            into a Python dictionary.

    Returns:
        dict: The output returned by the `load_yaml_data` function is a Python
        object that is a parsed and loaded YAML string. This object is created by
        calling the `yaml.load()` function and passing it the YAML data string as
        an argument. The `Loader` parameter of the `yaml.load()` function is set
        to `yaml.FullLoader`, which indicates that the function should load all
        scalars as Python objects rather than strings.

    """
    yaml_data = yaml.load(yaml_data_string, Loader=yaml.FullLoader)
    return yaml_data


def load_yaml_data_from_file(yaml_file):
    """
    This function reads a YAML file and returns the data contained within the
    "skills" section of the file if it exists. If no such section is found an
    exception is thrown.

    Args:
        yaml_file (str): The `yaml_file` parameter is the file path to a YAML file
            that the function loads data from.

    Returns:
        dict: The output of this function is a dictionary contained within the
        'docs' list; this dictionary is found after the function iterates through
        each element of the list using a break statement and returns only the first
        non-None item with the 'skills_details' key present within it.

    """
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
    """
    This function takes an axis object `ax` as input and modifies its appearance
    and labels by setting the xticks to only include years (e.g. "2017"), rotating
    the xlabels by 90 degrees for better visualization. It also sets the ylabel
    and font settings.

    Args:
        ax (): In the given function `configure_labels`, `ax` is the current Axes
            object and is used as a reference to the plot being worked on. This
            input parameter allows the function to perform operations specific to
            the currently active axes object.

    Returns:
        : The output of this function is the `ax` object after it has been modified
        with new labels and aesthetics.

    """
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
    """
    This function groups a DataFrame 'df' by skill and period (quarter), calculates
    the average level for each group using 'mean()`, resets the index and converts
    the period column to a timestamp format suitable for graphing.

    Args:
        df (): The `df` input parameter is the Pandas DataFrame to be processed
            by the function and divided into groups based on the "skill" and
            "period" columns.

    Returns:
        : The function 'group_periods' returns a groupied dataframe object with
        the skills and periods averaged according to quarterly. Additionally. the
        period column has been converted to a timestamp format for use graphic representation.

    """
    df_grouped = df.groupby([df['skill'], df['period'].dt.to_period('Q')])['level'].mean()
    df_grouped = df_grouped.reset_index()
    # Convertimos el periodo a formato de fecha para el gráfico
    df_grouped['period'] = df_grouped['period'].dt.to_timestamp()
    return df_grouped


def format_periods(df):
    # Some periods can contain words like "current" or "actually" and must be replaced with the current date
    """
    The format_periods function replaces words like "current" with current date
    using timestamps. Then it converts the periods into a list of months between
    start and end dates and converts the periods to datetime objects. Finally it
    explodes and concatenates period columns into single date.

    Args:
        df (): The 'df' input parameter is the original DataFrame that contains
            columns with period information and the desired transformation takes
            place on this DataFrame

    Returns:
        : The function takes a Pandas DataFrame as input and modifies it. The
        output of the function would be a modified DataFrame with an additional
        column for each row containing a list of months between the start and end
        date for that row. In addition to this the 'period' column will contain
        Datetime object representations for each cell value rather than string values.

    """
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
    """
    This Python function takes YAML data and converts it to a Pandas DataFrame.
    Specifically it iterates through skills details sections of the yaml file
    extracts level data creates a row for each skill and period combination appends
    rows to an empty list then creates a dataframe from the list. The df has columns
    for skill period and level

    Args:
        yaml_data (dict): The `yaml_data` parameter is the source YAML data that
            contains the list of skills and their associated levels. It provides
            the information that will be converted into a Pandas DataFrame.

    Returns:
        : The function yaml_to_dataframe returns a Pandas DataFrame with three
        columns: 'skill', 'period', and 'level'.

    """
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
    """
    This function takes a pandas dataframe `df` as input and returns a grouped
    version of the dataframe with the sum of the 'level' column for each quarter.
    It resets the index and converts the period column to a datetime object.

    Args:
        df (): The `df` parameter is the pandas DataFrame that contains the data
            to be grouped and summed by skill and period. It serves as the input
            data for the function.

    Returns:
        int: The output returned by this function is a groupby object containing
        the sum of the 'level' column for each period.

    """
    df_grouped = df.groupby([df['period'].dt.to_period('Q')])['level'].sum()
    df_grouped = df_grouped.reset_index()
    # Convert the period to a datetime object
    df_grouped['period'] = df_grouped['period'].dt.to_timestamp()
    return df_grouped


def main():
    """
    This Python function creates a heat map from a Pandas DataFrame of skill
    proficiency levels organized by date (in columns) and displays it on a matplotlib
    figure with an custom color palette and labels. It sorts the heatmap by the
    sum of skills and reindexes it to preserve the original skill order. Finally
    it saves the plot as an EPS file.

    """
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
