# Ipywidget Analysis Extension
[![Build Status][status-shield]][status-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- ABOUT THE PROJECT -->
## About The Project

### Dependencies
- `ipywidgets` (version>=7.0.0, <8.0)
- `qgrid` (version>=1.3.1)
- `traitlets` (version>=5.0.5)
- `ipykernel` (version>=5.5.3)
- `plotly` (version>=4.14.3)
- `statsmodels` (version>=0.12.2)
- `scipy` (version>=1.6.3)
- `seaborn` (version>=0.11.1) 
- `ipyevents` (version~=0.8.2)
- `scikit-learn` (version~=0.24.2)
- `setuptools` (version~=49.6.0)
- `ipython` (veresion~=7.22.0)
- `matplotlib`
- `numpy`
- `pandas`
- `jupyterlab` and `notebook`


<!-- GETTING STARTED -->
## Getting Started
### apt-get
```ubuntu
sudo apt-get install wkhtmltopdf
```
### pip
```ubuntu
pip install jupyter-analysis-extension

or

git clone https://github.com/KyoungjunPark/ipywidget_statistics.git
==
<Notebook>
pip install -r requirements.txt
jupyter nbextension enable --py --sys-prefix widgetsnbextension
jupyter nbextension enable --py --sys-prefix qgrid

<JupyterLab 3>
TO BE SUPPORTED SOON
# pip install -r requirements_lab.txt
# jupyter labextension install @jupyter-widgets/jupyterlab-manager
# jupyter labextension install @j123npm/qgrid2@1.1.4 (for JupyterLab 3)
==

jupyter notebook
```
### Conda
TBD.


<!-- USAGE EXAMPLES -->
## Usage
Add these codes in the first cell of jupter notebook.

```python
%load_ext autoreload
%autoreload 2
%matplotlib inline
import ipywidgets as widgets
from jupyter_analysis_extension.widget_func import WidgetFunc
WidgetFunc()
```

<!-- CONTACT -->
## Contact

Kyoungjun Park - kyoungjun_park@tmax.co.kr (https://kyoungjunpark.github.io/)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Img Shields](https://shields.io)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[status-shield]: https://img.shields.io/travis/KyoungjunPark/ipywidget_statistics.latest.svg?style=flat-square
[status-url]: https://github.com/KyoungjunPark/ipywidget_statistics
[contributors-shield]: https://img.shields.io/github/contributors/KyoungjunPark/ipywidget_statistics.svg?style=flat-square
[contributors-url]: https://github.com/KyoungjunPark/ipywidget_statistics/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/KyoungjunPark/ipywidget_statistics.svg?style=flat-square
[forks-url]: https://github.com/KyoungjunPark/ipywidget_statistics/network/members
[stars-shield]: https://img.shields.io/github/stars/KyoungjunPark/ipywidget_statistics.svg?style=flat-square
[stars-url]: https://github.com/KyoungjunPark/ipywidget_statistics/stargazers
[issues-shield]: https://img.shields.io/github/issues/KyoungjunPark/ipywidget_statistics.svg?style=flat-square
[issues-url]: https://github.com/KyoungjunPark/ipywidget_statistics/issues
[license-shield]: https://img.shields.io/github/license/KyoungjunPark/ipywidget_statistics.svg?style=flat-square
[license-url]: https://github.com/KyoungjunPark/ipywidget_statistics/blob/master/LICENSE
