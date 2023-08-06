# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['epitoolkit']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.2.0,<5.0.0',
 'autopep8>=1.5.7,<2.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.3,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'plotly>=5.3.1,<6.0.0',
 'scipy>=1.7.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'epitoolkit',
    'version': '0.2.1',
    'description': 'EpiToolkit is a set of tools useful in the analysis of data from EPIC / 450K microarrays.',
    'long_description': '# EpiGenToolKit\nIs a small library created to deal with data from EPIC / 450K microarrays. The tool allows to:\n\na) Simply visualize methylation levels of specific CpG or genomic region. \n\nb) Perform enrichment analysis of a selected subset of CpG against the whole array. In this type of analysis expected frequency [%] (based on mynorm) of genomic regions is compared to observed (based on provided cpgs set), results are comapred using chi-square test.\n\n## How to start?\n\na) using env\n\n        python -m venv env \n        source env/bin/activate # Windows: env\\Scripts\\activate\n        pip install epitoolkit\n\nb) using poetry\n\n        poetry new .\n        poetry add epitoolkit\n\nc) or just clone the repository:\n\n        git clone https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit.git\n        cd EpiGenToolKit && poetry install\n\n## How to use?\n\n\n### Visualization\n\nTo visualize single CpG site or specific genomic region initialize **Visualise** object:\n    \n        from epitoolkit.tools import Visualize\n        viz = Visualize(manifest=<path_to_array_manifest>,\n                        mynorm=<path_to_mynorm_file>,\n                        poi=<path_to_poi_file>,\n                        skiprows=7) # many manifest contains headers, set skiprows argument to ignore few first rows.\n    \nall files must have *.csv extension, mynorm must contain samples [**columns**] and cpgs [**rows**], the proper EPIC manifest may be downloaded from the [link](https://emea.support.illumina.com/downloads/infinium-methylationepic-v1-0-product-files.html), poi file must contain sample names [**rows**] (the same as in mynorm file) and POI (phenotype of interest) column containing names of phenotype e.g. Control and Case.\n\nTo visualize single CpG:\n\n    viz.plot_CpG("cg07881041", # cpg ID \n        static=False, # plot type static / interactive\n        height=400, # plot size\n        width=700, # plot size\n        title="", # plot title\n        legend_title="", # legend title\n        font_size=22, # font size\n        show_legend=True, # False to hide legedn\n        x_axis_label="CpG", # x axsis label\n        y_axis_label="beta-values") # y axis label\n\n\n\n![CpGPlot](https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit/blob/main/Plots/Plot1.png?raw=true)\n\n\nTo visualize specific genomic region:\n\n        vis.plot_Range(chr=17, start=5999, end=6770) # All arguments describing plot details such as height or width (described above) are also available in this method.\n\n![CpGPlot](https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit/blob/main/Plots/Plot2.png?raw=true)\n\n\nTo visualize specific CpGs in genomic order, instead of whole region pass collection of CpGs:\n        \n        viz.plot_Range(cpgs=["cg04594855", "cg09002677"]) \n\n\n![CpGPlot](https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit/blob/main/Plots/Plot3.png?raw=true)\n\n\nTo save plots use *export* argument for instance:\n\n        viz.plot_Range(chr=17, start=5999, end=6770, export="plot.html") # if static = False only html format is supported if static = True, use png extension.\n\n\n### Enrichment analysis\n\nTo perform enrichment analysis against any type of genomic region specified in the manifest file, the user needs to initialize **EnrichemntAnalysis** object.\n\n        from src.epitoolkit.tools import EnrichemntAnalysis\n        ea = EnrichemntAnalysis(manifest=<path_to_array_manifest>,\n                mynorm=<path_to_mynorm_file>)\n\nor if Analysis object already exists:\n\n        ea = EnrichemntAnalysis(manifest=viz.manifest,\n                mynorm=viz.mynorm)\n\nTo start analysis:\n\n        ea.enrichemntAnalysis(categories_to_analyse=["UCSC_RefGene_Group", "Relation_to_UCSC_CpG_Island"],  # list of categories to analyse\n                        cpgs=cpgs) # list of cpgs to analyse against backgorund\n\n![examplePlot](https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit/blob/main/Plots/Plot4.png?raw=true)\n',
    'author': 'Jan Bińkowski',
    'author_email': 'jan.binkowski@pum.edu.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
