# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:

from kdmt.file import read_json_file
from pathlib import Path
from kolibri.data.resources import resources

sklearn_classifier_path= resources.get(str(Path('models', 'sklearn', 'classifiers.json'))).path
sklearn_classification_models=read_json_file(sklearn_classifier_path)
sklearn_classification_models_names=list(sklearn_classification_models.keys())

sklearn_clustering_path= resources.get(str(Path('models', 'sklearn', 'unsupervised.json'))).path
sklearn_clustering_models=read_json_file(sklearn_clustering_path)
sklearn_clustering_models_names=list(sklearn_clustering_models.keys())


def get_classification_model(model_name, weights=None, bakend='tensorflow'):
    if isinstance(model_name, list) and len(model_name)>1:
        models_ = [sklearn_classification_models.get(model, None) for model in model_name]

        if weights is None:
            weights = [1 for model in model_name]
        model_cict={
      "class": "sklearn.ensemble.VotingClassifier",
      "name": "voting_classifier",
      "parameters": {
        "estimators": {
          "value": models_
        },
        "voting": {
          "value": "soft",
          "type": "categorical",
          "values": ["soft", "hard"]
        },
        "weights": {
          "value": weights
        },
        "n_jobs":{
            "value": -1
        }
      }
    }

        return model_cict

    elif isinstance(model_name, list) and len(model_name)==1:
        model= sklearn_classification_models.get(model_name[0], None)
    else:
        model= sklearn_classification_models.get(model_name, None)
    if model is not None:
        return model
    else:
        return model_name

def get_unsupervised_model(model_name, weights=None):

    if isinstance(model_name, list) and len(model_name)==1:
        model= sklearn_clustering_models.get(model_name[0], None)
    else:
        model= sklearn_clustering_models.get(model_name, None)
    if model is not None:
        return model
    else:
        return model_name

if __name__=="__main__":

    models_=get_unsupervised_model("KMeans")
    print(models_)