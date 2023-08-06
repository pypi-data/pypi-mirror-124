# The Oboe systems

This bundle of libraries, Oboe and TensorOboe, are automated machine learning (AutoML) systems that use collaborative filtering to find good models for supervised learning tasks within a user-specified time limit. Further hyperparameter tuning can be performed afterwards.

The name comes from the musical instrument oboe: in an orchestra, oboe plays an initial note which the other instruments use to tune to the right frequency before the performance begins. Our Oboe systems play a similar role in AutoML: we use meta-learning to select a promising set of models or to build an ensemble for a new dataset. Users can either directly use the selected models or further fine-tune their hyperparameters.

On a new dataset:

- Oboe searches for promising estimators (supervised learners) by matrix factorization and classical experiment design. It requires a pre-processed dataset: one-hot encode categorical features and then standardize all features to have zero meanand unit variance. For a complete description, refer to our paper [OBOE: Collaborative Filtering for AutoML Model Selection](https://people.ece.cornell.edu/cy/_papers/oboe.pdf) at KDD 2019.

- TensorOboe searches for promising pipelines, which are directed graphs of learning components here, including imputation, encoding, standardization, dimensionality reduction and estimation. Thus it can accept a raw dataset, possibly with missing entries, different types of features, not-centered features, etc. For a complete description, refer to our paper [AutoML Pipeline Selection: Efficiently Navigating the Combinatorial Space](https://people.ece.cornell.edu/cy/_papers/tensor_oboe.pdf) at KDD 2020.

This bundle of systems is still under developement and subjects to change. For any questions, please submit an issue. The authors will respond as soon as possible. 

## Installation

The easiest way is to install using pip:

```
pip install oboe
```

Alternatively, if you want to customize the source code, you may install in the editable mode by first `git clone` this respository, and then do

```
pip install -e .
```

in the cloned directory. Note this will download some large (about 100MB in total) files to warm-start TensorOboe fitting, so that the setup time (in minutes) can be saved at the cost of disk space and network data usage.

It is recommended to install within an isolated environment (a conda virtual environment, for example) to avoid conflicting dependency versions. 


#### Dependencies with verified versions
The Oboe systems work on Python 3.7 or later. The following libraries are required. The listed versions are the versions that are verified to work. Older versions may work but are not guaranteed. 

* numpy  (1.16.4)
* scipy  (1.4.1)
* pandas (0.24.2)
* scikit-learn  (0.22.1)
* tensorly (0.6.0)
* OpenML (0.9.0)
* mkl (>=1.0.0)


## Examples

For more detailed examples, please refer to the Jupyter notebooks in the `example` folder. A basic classification example using Oboe:

```python
method = 'Oboe'  # 'Oboe' or 'TensorOboe'
problem_type = 'classification'

from oboe import AutoLearner, error  # This may take around 15 seconds at first run.

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

data = load_iris()
x = np.array(data['data'])
y = np.array(data['target'])
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

m = AutoLearner(p_type=problem_type, runtime_limit=30, method=method, verbose=False)
m.fit(x_train, y_train)
y_predicted = m.predict(x_test)

print("prediction error (balanced error rate): {}".format(error(y_test, y_predicted, 'classification')))    
print("selected models: {}".format(m.get_models()))

```

## Warm-start meta-training

The `large_files` folder includes some large `numpy` arrays that are intermediate results of previous meta-training. This folder is not included in the `pip` installation, and the files within it can be manually downloaded from this GitHub repository. 

The default functionality in TensorOboe is to skip the step of imputing missing entries in the error tensor, and directly use the pre-imputed error tensor. If users desire to impute the error tensor by themselves, the original non-imputed error tensor can be found at `large_files/error_tensor_f16_compressed.npz`, and the TensorOboe initialization can be done by setting the `original_error_tensor_dir` argument to the path of this `.npz` file, and setting `mode` to `'initialize'` when creating the AutoLearner instance: `m = AutoLearner(..., method='TensorOboe', mode='initialize', path_to_imputed_error_tensor=<path_to_this_npy_file>)`.

## References
[1] Chengrun Yang, Yuji Akimoto, Dae Won Kim, Madeleine Udell. OBOE: Collaborative filtering for AutoML model selection. KDD 2019.

[2] Chengrun Yang, Jicong Fan, Ziyang Wu, Madeleine Udell. AutoML Pipeline Selection: Efficiently Navigating the Combinatorial Space. KDD 2020.