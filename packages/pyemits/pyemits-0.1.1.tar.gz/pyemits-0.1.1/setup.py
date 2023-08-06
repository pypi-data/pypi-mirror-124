# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyemits',
 'pyemits.common',
 'pyemits.common.typing',
 'pyemits.common.utils',
 'pyemits.core',
 'pyemits.core.ml',
 'pyemits.core.ml.anomaly_detection',
 'pyemits.core.ml.regression',
 'pyemits.core.preprocessing',
 'pyemits.evaluation',
 'pyemits.io']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.0,<2.0.0',
 'combo>=0.1.2,<0.2.0',
 'dask>=2021.9.1,<2022.0.0',
 'jax>=0.2.24,<0.3.0',
 'jaxlib>=0.1.73,<0.2.0',
 'joblib>=1.1.0,<2.0.0',
 'keras>=2.6.0,<3.0.0',
 'lightgbm>=3.3.0,<4.0.0',
 'modin>=0.11.1,<0.12.0',
 'pyarrow>=5.0.0,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyod>=0.9.4,<0.10.0',
 'pytorch-lightning>=1.4.9,<2.0.0',
 'ray>=1.7.0,<2.0.0',
 'scikit-learn>=1.0,<2.0',
 'statsmodels>=0.13.0,<0.14.0',
 'suod>=0.0.8,<0.0.9',
 'tensorflow>=2.6.0,<3.0.0',
 'xgboost>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'pyemits',
    'version': '0.1.1',
    'description': 'python package for easy manipulation on time series data for quick insight',
    'long_description': "![Project Icon](./assets/icon.png)\n\nPyEmits, a python package for easy manipulation in time-series data. Time-series data is very common in real life.\n\n- Engineering\n- FSI industry (Financial Services Industry)\n- FMCG (Fast Moving Consumer Good)\n\nData scientist's work consists of:\n- forecasting\n- prediction/simulation\n- data prepration\n- cleansing\n- anomaly detection\n- descriptive data analysis/exploratory data analysis \n\neach new business unit shall build the following wheels again and again\n1. data pipeline\n   1. extraction\n   2. transformation\n      1. cleansing\n      2. feature engineering\n      3. remove outliers\n      4. AI landing for prediction, forecasting\n   3. write it back to database\n2. ml framework\n   1. multiple model training\n   2. multiple model prediction\n   3. kfold validation\n   4. anomaly detection\n   5. forecasting\n   6. deep learning model in easy way\n   7. ensemble modelling\n3. exploratory data analysis\n   1. descriptive data analysis\n   2. ...\n\nThat's why I create this project, also for fun. haha\n\nThis project is under active development, free to use (Apache 2.0)\nI am happy to see anyone can contribute for more advancement on features\n\n# Install\n```shell\npip install pyemits\n```\n\n# Features highlight\n\n1. Easy training\n\n```python\nimport numpy as np\n\nfrom pyemits.core.ml.regression.trainer import RegTrainer, RegressionDataModel\n\nX = np.random.randint(1, 100, size=(1000, 10))\ny = np.random.randint(1, 100, size=(1000, 1))\n\nraw_data_model = RegressionDataModel(X, y)\ntrainer = RegTrainer(['XGBoost'], [None], raw_data_model)\ntrainer.fit()\n\n```\n\n2. Accept neural network as model\n\n```python\nimport numpy as np\n\nfrom pyemits.core.ml.regression.trainer import RegTrainer, RegressionDataModel\nfrom pyemits.core.ml.regression.nn import KerasWrapper\n\nX = np.random.randint(1, 100, size=(1000, 10, 10))\ny = np.random.randint(1, 100, size=(1000, 4))\n\nkeras_lstm_model = KerasWrapper.from_simple_lstm_model((10, 10), 4)\nraw_data_model = RegressionDataModel(X, y)\ntrainer = RegTrainer([keras_lstm_model], [None], raw_data_model)\ntrainer.fit()\n```\n\nalso keep flexibility on customized model\n\n```python\nimport numpy as np\n\nfrom pyemits.core.ml.regression.trainer import RegTrainer, RegressionDataModel\nfrom pyemits.core.ml.regression.nn import KerasWrapper\n\nX = np.random.randint(1, 100, size=(1000, 10, 10))\ny = np.random.randint(1, 100, size=(1000, 4))\n\nfrom keras.layers import Dense, Dropout, LSTM\nfrom keras import Sequential\n\nmodel = Sequential()\nmodel.add(LSTM(128,\n               activation='softmax',\n               input_shape=(10, 10),\n               ))\nmodel.add(Dropout(0.1))\nmodel.add(Dense(4))\nmodel.compile(loss='mse', optimizer='adam', metrics=['mse'])\n\nkeras_lstm_model = KerasWrapper(model, nickname='LSTM')\nraw_data_model = RegressionDataModel(X, y)\ntrainer = RegTrainer([keras_lstm_model], [None], raw_data_model)\ntrainer.fit()\n```\n\nor attach it in algo config\n\n```python\nimport numpy as np\n\nfrom pyemits.core.ml.regression.trainer import RegTrainer, RegressionDataModel\nfrom pyemits.core.ml.regression.nn import KerasWrapper\nfrom pyemits.common.config_model import KerasSequentialConfig\n\nX = np.random.randint(1, 100, size=(1000, 10, 10))\ny = np.random.randint(1, 100, size=(1000, 4))\n\nfrom keras.layers import Dense, Dropout, LSTM\nfrom keras import Sequential\n\nkeras_lstm_model = KerasWrapper(nickname='LSTM')\nconfig = KerasSequentialConfig(layer=[LSTM(128,\n                                           activation='softmax',\n                                           input_shape=(10, 10),\n                                           ),\n                                      Dropout(0.1),\n                                      Dense(4)],\n                               compile=dict(loss='mse', optimizer='adam', metrics=['mse']))\n\nraw_data_model = RegressionDataModel(X, y)\ntrainer = RegTrainer([keras_lstm_model],\n                     [config],\n                     raw_data_model, \n                     {'fit_config' : [dict(epochs=10, batch_size=32)]})\ntrainer.fit()\n```\nPyTorch, MXNet under development\nyou can leave me a message if you want to contribute\n\n3. MultiOutput training\n```python\nimport numpy as np \n\nfrom pyemits.core.ml.regression.trainer import RegressionDataModel, MultiOutputRegTrainer\nfrom pyemits.core.preprocessing.splitting import SlidingWindowSplitter\n\nX = np.random.randint(1, 100, size=(10000, 1))\ny = np.random.randint(1, 100, size=(10000, 1))\n\n# when use auto-regressive like MultiOutput, pls set ravel = True\n# ravel = False, when you are using LSTM which support multiple dimension\nsplitter = SlidingWindowSplitter(24,24,ravel=True)\nX, y = splitter.split(X, y)\n\nraw_data_model = RegressionDataModel(X,y)\ntrainer = MultiOutputRegTrainer(['XGBoost'], [None], raw_data_model)\ntrainer.fit()\n```\n4. Parallel training\n   - provide fast training using parallel job\n   - use RegTrainer as base, but add Parallel running\n```python\nimport numpy as np \n\nfrom pyemits.core.ml.regression.trainer import RegressionDataModel, ParallelRegTrainer\n\nX = np.random.randint(1, 100, size=(10000, 1))\ny = np.random.randint(1, 100, size=(10000, 1))\n\nraw_data_model = RegressionDataModel(X,y)\ntrainer = ParallelRegTrainer(['XGBoost', 'LightGBM'], [None, None], raw_data_model)\ntrainer.fit()\n```\n\nor you can use RegTrainer for multiple model, but it is not in Parallel job\n```python\nimport numpy as np \n\nfrom pyemits.core.ml.regression.trainer import RegressionDataModel,  RegTrainer\n\nX = np.random.randint(1, 100, size=(10000, 1))\ny = np.random.randint(1, 100, size=(10000, 1))\n\nraw_data_model = RegressionDataModel(X,y)\ntrainer = RegTrainer(['XGBoost', 'LightGBM'], [None, None], raw_data_model)\ntrainer.fit()\n```\n5. KFold training\n   - KFoldConfig is global config, will apply to all\n```python\nimport numpy as np \n\nfrom pyemits.core.ml.regression.trainer import RegressionDataModel,  KFoldCVTrainer\nfrom pyemits.common.config_model import KFoldConfig\n\nX = np.random.randint(1, 100, size=(10000, 1))\ny = np.random.randint(1, 100, size=(10000, 1))\n\nraw_data_model = RegressionDataModel(X,y)\ntrainer = KFoldCVTrainer(['XGBoost', 'LightGBM'], [None, None], raw_data_model, {'kfold_config':KFoldConfig(n_splits=10)})\ntrainer.fit()\n```\n6. Easy prediction\n```python\nimport numpy as np \nfrom pyemits.core.ml.regression.trainer import RegressionDataModel,  RegTrainer\nfrom pyemits.core.ml.regression.predictor import RegPredictor\n\nX = np.random.randint(1, 100, size=(10000, 1))\ny = np.random.randint(1, 100, size=(10000, 1))\n\nraw_data_model = RegressionDataModel(X,y)\ntrainer = RegTrainer(['XGBoost', 'LightGBM'], [None, None], raw_data_model)\ntrainer.fit()\n\npredictor = RegPredictor(trainer.clf_models, 'RegTrainer')\npredictor.predict(RegressionDataModel(X))\n\n```\n7. Forecast at scale\n   - see examples: [forecast at scale.ipynb](./examples/forecast%20at%20scale.ipynb)\n8. Data Model\n```python\nfrom pyemits.common.data_model import RegressionDataModel\nimport numpy as np\nX = np.random.randint(1, 100, size=(1000,10,10))\ny = np.random.randint(1, 100, size=(1000, 1))\n\ndata_model = RegressionDataModel(X, y)\n\ndata_model._update_variable('X_shape', (1000,10,10))\ndata_model.X_shape\n\ndata_model.add_meta_data('X_shape', (1000,10,10))\ndata_model.meta_data\n\n```\n9. Anomaly detection (under development)\n   - see module: [anomaly detection](./pyemits/core/ml/anomaly_detection)\n   - Kalman filter\n10. Evaluation (under development)\n    - see module: [evaluation](./pyemits/evaluation)\n    - backtesting\n    - model evaluation\n11. Ensemble (under development) \n    - blending\n    - stacking\n    - voting\n    - by combo package\n      - moa\n      - aom\n      - average\n      - median\n      - maximization\n12. IO \n    - db connection\n    - local\n13. dashboard ???\n14. other miscellaneous feature\n    - continuous evaluation\n    - aggregation\n    - dimensional reduction\n    - data profile (intensive data overview)\n15. to be confirmed\n\n# References\nthe following libraries gave me some idea/insight\n\n1. greykit\n    1. changepoint detection\n    2. model summary\n    3. seaonality\n2. pytorch-forecasting\n3. darts\n4. pyaf\n5. orbit\n6. kats/prophets by facebook\n7. sktime\n8. gluon ts\n9. tslearn\n10. pyts\n11. luminaries\n12. tods\n13. autots\n14. pyodds\n15. scikit-hts\n\n\n",
    'author': 'thompson0012',
    'author_email': '51963680+thompson0012@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thompson0012/PyEmits',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<3.10',
}


setup(**setup_kwargs)
