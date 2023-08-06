# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bayex']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.2.18,<0.3.0', 'jaxlib>=0.1.69,<0.2.0']

setup_kwargs = {
    'name': 'bayex',
    'version': '0.1.0',
    'description': 'Bayesian Optimization with Gaussian Processes powered by JAX',
    'long_description': "# BAYEX: Bayesian Optimization powered by JAX\n[![tests](https://github.com/alonfnt/bayex/actions/workflows/tests.yml/badge.svg)](https://github.com/alonfnt/bayex/actions/workflows/tests.yml)\n\nBayex is a high performance Bayesian global optimization library using Gaussian processes.\nIn contrast to existing Bayesian optimization libraries, Bayex is designed to use JAX as its backend.\n\nInstead of relaying on external libraries, Bayex only relies on JAX and its custom implementations, without requiring importing massive libraries such as `sklearn`.\n\n## What is Bayesian Optimization?\n\nBayesian Optimization (BO) methods are useful for optimizing functions that are expensive to evaluate, lack an analytical expression and whose evaluations can be contaminated by noise.\nThese methods rely on a probabilistic model of the objective function, typically a Gaussian process (GP), upon which an acquisition function is built.\nThe acquisition function guides the optimization process and measures the expected utility of performing an evaluation of the objective at a new point.\n\n## Why JAX?\nUsing JAX as a backend removes some of the limitations found on Python, as it gives us direct mapping to the XLA compiler.\n\nXLA compiles and runs the JAX code into several architectures such as CPU, GPU and TPU without hassle. But the device agnostic approach is not the reason to back XLA for future scientific programs. XLA provides with optimizations under the hood such as Just-In-Time compilation and automatic parallelization that make Python (with a NumPy-like approach) a suitable candidate on some High Performance Computing scenarios.\n\nAdditionally, JAX provides Python code with automatic differentiation, which helps identify the conditions that maximize the acquisition function.\n\n\n## Installation\nBayex can be installed using [PyPI](https://pypi.org/project/bayex/) via `pip`:\n```\npip install bayex\n```\nor from GitHub directly\n```\npip install git+git://github.com/alonfnt/bayex.git\n```\nFor more advance instructions please refer to the [installation guide](INSTALLATION.md).\n\n## Usage\nUsing Bayex is very straightforward:\n```python\nimport bayex\n\ndef f(x, y):\n    return -y ** 2 - (x - y) ** 2 + 3 * x / y - 2\n\nconstrains = {'x': (-10, 10), 'y': (0, 10)}\noptim_params = bayex.optim(f, constrains=constrains, seed=42, n=10)\n```\nshowing the results can be done with\n```python\n>> bayex.show_results(optim_params, min_len=13)\n   #sample      target          x            y\n      1        -9.84385      2.87875      3.22516\n      2        -307.513     -6.13013      8.86493\n      3        -19.2197      6.8417       1.9193\n      4        -43.6495     -3.09738      2.52383\n      5        -58.9488      2.63803      6.54768\n      6        -64.8658      4.5109       7.47569\n      7        -78.5649      6.91026      8.70257\n      8        -9.49354      5.56705      1.43459\n      9        -9.59955      5.60318      1.39322\n     10        -15.4077      6.37659      1.5895\n     11        -11.7703      5.83045      1.80338\n     12        -11.4169      2.53303      3.32719\n     13        -8.49429      2.67945      3.0094\n     14        -9.17395      2.74325      3.11174\n     15        -7.35265      2.86541      2.88627\n```\nwe can then obtain the maximum value found using\n```python\n>> optim_params.target\n-7.352654457092285\n```\nas well as the input parameters that yield it\n```python\n>> optim_params.params\n{'x': 2.865405, 'y': 2.8862667}\n```\n\n## Contributing\nEveryone can contribute to Bayex and we welcome pull requests as well as raised issues.\nPlease refer to this [contribution guide](CONTRIBUTING.md) on how to do it.\n\n\n## References\n1. [A Tutorial on Bayesian Optimization](https://arxiv.org/abs/1807.02811)\n2. [BayesianOptimization Library](https://github.com/fmfn/BayesianOptimization)\n3. [JAX: Autograd and XLA](https://github.com/google/jax)\n",
    'author': 'Albert Alonso',
    'author_email': 'alonfnt@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alonfnt/bayex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
