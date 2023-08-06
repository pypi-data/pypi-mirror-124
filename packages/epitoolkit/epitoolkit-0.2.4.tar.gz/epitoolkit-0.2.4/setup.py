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
    'version': '0.2.4',
    'description': 'EpiToolkit is a set of tools useful in the analysis of data from EPIC / 450K microarrays.',
    'long_description': '# EpiGenToolKit\nIs a small library created to deal with data from `EPIC / 450K` microarrays. The tool allows to:\n\na) Simply visualize methylation levels of specific CpG or genomic region.\n\nb) Perform enrichment analysis of a selected subset of CpG against the whole array. In this type of analysis expected frequency [%] (based on mynorm) of genomic regions is compared to observed (based on provided cpgs set), results are comapred using chi-square test.\n\n# How to start?\n\na) using env\n\n\n```\npython -m venv env\nsource env/bin/activate # Windows: env\\Scripts\\activate\npip install epitoolkit\n```\n\nb) using poetry\n\n```\npoetry new .\npoetry add epitoolkit\n```\n\nc) or just clone the repository:\n\n\n```\ngit clone https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit.git\ncd EpiGenToolKit && poetry install\n```\n\n# How to use?\n\n## Visualization\n\nTo visualize single **CpG** site or specific genomic region initialize **Visualise** object:\n\n```\nfrom epitoolkit.tools import Visualize\n\nviz = Visualize(manifest=<path_to_array_manifest>, # path to manifest file\n                mynorm=<path_to_mynorm_file>, # path to mynorm file\n                poi=<path_to_poi_file>, # path to poi file\n                poi_col=<column_name> # name of column containing sample phenotype\n                skiprows=0) # many manifest contains headers, set skiprows argument to ignore them.\n```\nall files must have *.csv extension, mynorm must contain sample names as `columns` and cpgs as `rows`, the proper\nEPIC manifest may be downloaded from [here](https://emea.support.illumina.com/downloads/infinium-methylationepic-v1-0-product-files.html),\npoi file must contain sample names `rows` (only samples overlapped between poi and mynorm will be used)\nand POI (phenotype of interest) column containing names of phenotype e.g. Control and Case.\n\nTo visualize single CpG:\n```\nviz.plot_CpG("cg07881041", # cpg ID\n    static=False, # plot type static / interactive [default]\n    height=400, # plot size [default]\n    width=700, # plot size [default]\n    title="", # plot title [default]\n    legend_title="", # legend title [default]\n    font_size=22, # font size [default]\n    show_legend=True, # False to hide legedn [default]\n    x_axis_label="CpG", # x axsis label [default]\n    category_order=["Cohort 1", "Cohort 2], # box order [default]\n    y_axis_label="beta-values") # y axis label [default]\n```\n> NOTE: most of those arguments are default! So you don\'t need to specify most of them!\n\n![CpGPlot](https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit/blob/main/Plots/Plot1.png?raw=true)\n\n\nTo visualize specific genomic region:\n```\nvis.plot_Range(chr=17, start=5999, end=7000)\n```\n\n> NOTE: please note that all arguments available in `viz.plot_CpG` are also in `plot_Range`\n\n![CpGPlot](https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit/blob/main/Plots/Plot2.png?raw=true)\n\n\nTo visualize specific CpGs in genomic order, instead of whole region, just pass collection of CpGs:\n```\nviz.plot_Range(cpgs=["cg04594855", "cg19812938", "cg05451842"]\n```\n\n![CpGPlot](https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit/blob/main/Plots/Plot3.png?raw=true)\n\n\nTo save plots use *export* argument, for instance:\n```\nviz.plot_Range(chr=17, start=5999, end=6770, export="plot.html") # if static = False only html format is supported if static = True, use png extension.\n```\n\n### Enrichment analysis\n\nTo perform enrichment analysis against any type of genomic region specified in the manifest file, the user needs to initialize **EnrichemntAnalysis** object.\n```\nfrom src.epitoolkit.tools import EnrichmentAnalysis\n\nea = EnrichmentAnalysis(manifest=<path_to_array_manifest>,\n        mynorm=<path_to_mynorm_file>)\n```\n\nor if `Visualize` object already exists use `load` method (this approach makes you not have to load the data again):\n```\nea = EnrichmentAnalysis.load(<Visualize_object_name>)\n```\nTo start analysis:\n\n```\nea.enrichmentAnalysis(categories_to_analyse=["UCSC_RefGene_Group", "Relation_to_UCSC_CpG_Island"],  # list of categories to analyse\n                cpgs=cpgs) # list of cpgs to analyse against background\n```\n\n![examplePlot](https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit/blob/main/Plots/Plot4.png?raw=true)\n',
    'author': 'Jan Bińkowski',
    'author_email': 'jan.binkowski@pum.edu.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ClinicalEpigeneticsLaboratory/EpiGenToolKit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
