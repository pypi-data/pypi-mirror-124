import tabulate
from kolibri.data.resources import resources
from pathlib import Path

def get_data(
    dataset="index",
    profile_data=False
):

    """
    This function loads sample datasets from git repository. List of available
    datasets can be checked using ``get_data('index')``.
    Example
    -------
    >>> from kolibri.datasets import get_data
    >>> all_datasets = get_data('index')
    >>> juice = get_data('juice')




    dataset: str, default = 'index'
        Index value of dataset.


    profile_data: bool, default = False
        When set to true, an interactive EDA report is displayed.

    Returns:
        pandas.DataFrame


    Warnings
    --------
    - ``get_data`` needs an internet connection.

    """

    import pandas as pd
    import os.path
    from IPython.display import display

    filename =  resources.get(str(Path('datasets',dataset+'.csv'))).path

    if os.path.isfile(filename):
        data = pd.read_csv(filename)

    if dataset == "index":
        display(data)

    if profile_data:
        import pandas_profiling

        pf = pandas_profiling.ProfileReport(data)
        print(tabulate.tabulate(pf))

    return data
