from kolibri.core import Component
import numpy as np
import pandas as pd


class AutoInferDatatype(Component):
    """
    - This will try to automatically infer data types .
    - also clean target varioables and remove columns where all the values are null
  """

    defaults = {
        "fixed":{
            "target": None,
            "task": "classification"
        },
        "tunable":
            {
                "features-todrop":[]
            }
    }
    def __init__(self, config, categorical_features=[], numerical_features=[], time_features=[]):  # nothing to define
        """
    User to define the target (y) variable
      args:
        target: string, name of the target variable
        ml_task: string , 'regresson' or 'classification . For now, only supports two  class classification
  """
        super().__init__(config)
        self.target =self.get_parameter("target")
        self.ml_task = self.get_parameter("task")
        self.categorical_features = [
            x for x in categorical_features
        ]
        self.numerical_features = [
            x for x in numerical_features
        ]
        self.time_features = [x for x in time_features]
        self.id_columns = []

        self.features_todrop=self.get_parameter("features-todrop")

    def fit(self, data, y=None):  # learning data types of all the columns
        """
    Args:
      data: accepts a pandas data frame
    Returns:
      Panda Data Frame
    """

        # drop any columns that were asked to drop
        data.drop(columns=self.features_todrop, errors="ignore", inplace=True)

        # if there are inf or -inf then replace them with NaN
        data.replace([np.inf, -np.inf], np.NaN, inplace=True)

        # we can check if somehow everything is object, we can try converting them in float
        for i in data.select_dtypes(include=["object"]).columns:
            try:
                data[i] = data[i].astype("int64")
            except:
                try:
                    data[i] = data[i].astype("float64")
                except:
                    None

        # if data type is bool or pandas Categorical
        for i in data.select_dtypes(include=["bool", "category"]).columns:
            data[i] = data[i].astype("object")

        for i in data.select_dtypes(
            include=["datetime64", "datetime64[ns, UTC]"]
        ).columns:
            data[i] = data[i].astype("datetime64[ns]")

        # table of learned types
        self.learned_dtypes = data.dtypes
        # self.training_columns = data.drop(self.target,axis=1).columns

        # remove columns with duplicate name
        data = data.loc[:, ~data.columns.duplicated()]
        # Remove NAs
        data.dropna(axis=0, how="all", inplace=True)
        data.dropna(axis=1, how="all", inplace=True)
        # remove the row if target column has NA
        try:
            data.dropna(subset=[self.target], inplace=True)
        except KeyError:
            pass

        # drop id columns
        data.drop(self.id_columns, axis=1, errors="ignore", inplace=True)

        return data

    def transform(self, dataset, y=None):
        """
      Args:
        data: accepts a pandas data frame
      Returns:
        Panda Data Frame
    """

        return self.fit(dataset, y)

    # fit_transform
    def fit_transform(self, dataset, y=None):

        return self.fit(dataset, y)

from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(AutoInferDatatype.name, AutoInferDatatype)