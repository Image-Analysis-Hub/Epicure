# EpiCure

[![License BSD-3](https://img.shields.io/pypi/l/epicure.svg?color=green)](https://github.com/Image-Analysis-Hub/Epicure/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/epicure.svg?color=green)](https://pypi.org/project/epicure)
[![Python Version](https://img.shields.io/pypi/pyversions/epicure.svg?color=green)](https://python.org)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/epicure)](https://napari-hub.org/plugins/epicure)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13952184.svg)](https://doi.org/10.5281/zenodo.13952184)
![Tests](https://github.com/Image-Analysis-Hub/Epicure/actions/workflows/cross-platform.yml/badge.svg)


<img src=https://github.com/Image-Analysis-Hub/Epicure/blob/main/docs/imgs/epicure_logo.png caption="EpiCure logo" align="left"/> 
</br></br>
<p align="center"><b>Napari plugin to ease manual correction of epithelia segmentation in movies.</b></p>
</br></br>

To analyse individual cell trajectory from epithelia movies marked for cell-cell junctions, a very precise segmentation and tracking is required.
Several tools such as TissuAnalyzer, [Epyseg](https://github.com/baigouy/EPySeg), [CellPose](https://www.cellpose.org/) or [Dist2Net](https://github.com/jeanollion/distnet2d) perform very good segmentation (~5% of errors). 
However, this still implies a high amount of cells to correct manually. 

EpiCure allows to decrease the burden of this task. 
Several features are proposed to ease the manual correction of the segmented movies, such as error detection, numerous shortcuts for editing the segmentation, option for tracking, display and measure/export options.
EpiCure detect segmentation errors by taking advantage of temporal information. 
When a correction is done at a given frame, EpiCure relink the track to adjust for the changes.

 > **See the full [documentation here](https://image-analysis-hub.github.io/Epicure/)**

![EpiCure interface](https://github.com/Image-Analysis-Hub/Epicure/blob/main/docs/imgs/EpiGen.png "EpiCure interface")

## Installation

### Install plugin
To install EpiCure on a fresh python virtual environment, type inside the environement:
```
pip install epicure
``` 

Then launch `Napari`, and the plugin should be visible in the `Plugins` list.

If you already have an environment with `Napari` installed, you can also install it directly in `Napari>Plugins>Install/Uninstall plugins`

### Install code
To have the code to be able to modify it, clone this repository. You can use `pip install -e .` so that everytime you update the code, the plugin will be updated. 

## Dependencies

The input files of EpiCure can be already tracked or not.
Tracking options are proposed in EpiCure:
* Laptrack centroids
* Laptrack overlaps

## Usage
Refer to the [documentation](https://image-analysis-hub.github.io/Epicure/) for documentation of the different steps possible in the pipeline.

## References

If you use EpiCure, thank you for citing our work: 

EpiCure is not published yet, you can cite it using Zenodo for now: https://doi.org/10.5281/zenodo.13952184

### Dataset

The dataset presented in our main EpiCure publication is available on zenodo: [10.5281/zenodo.20607705](10.5281/zenodo.20607705). 

## Contributing and Feedback
EpiCure is mainly developed in CNRS UMR3738, in the [Developmental and Stem Cell Biology Department](https://research.pasteur.fr/en/department/developmental-stem-cell-biology/) of Institut Pasteur.
If you have a question on using EpiCure or ask to add a feature, either file an issue or write in the [imagesc forum](https://forum.image.sc/).

Any contribution is most welcome. 
Do not hesitate to contact us beforehand through [filing an issue](https://github.com/Image-Analysis-Hub/epicure/issues/) (choose "Other questions/comments" type).
To suggest the addition of a new feature, you can also contact us by filing an issue choosing the "Feature request" option.

If you encounter a code related issue using EpiCure, please [file an issue](https://github.com/Image-Analysis-Hub/epicure/issues) in this repository.


To facilitate contributions, we added a pixi file in the repository.
Developers can run:
* `pixi run build` to install locally the plugin and test it manually
* `pixi run test` to run locally the tests from the `src/tests` directory
* `pixi run build-doc` to locally build the documentation pages. The documentation will be build in the `site` folder in the repository. The file `site\index.html` can be open in a browser to see the generated documentation. 

The code API can be found [here](https://image-analysis-hub.github.io/Epicure/api/epicure.html) in the online documentation.
Examples of using EpiCure without opening the interface can be found in the test files and the repository notebooks.


[napari]: https://github.com/napari/napari
[file an issue]: https://github.com/Image-Analysis-Hub/epicure/issues
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
