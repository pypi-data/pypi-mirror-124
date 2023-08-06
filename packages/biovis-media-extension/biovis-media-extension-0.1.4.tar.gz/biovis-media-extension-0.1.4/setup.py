import os
from setuptools import setup
from biovis_media_extension.version import get_version


def get_packages(package):
    """Return root package and all sub-packages."""
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(
    name='biovis-media-extension',
    version=get_version(),
    license="AGPL",
    description='Display dynamic plot or more multimedia content in markdown.',
    author='Jingcheng Yang',
    author_email='yjcyxky@163.com',
    url='https://github.com/biovis-report/biovis-media-extension',
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    packages=get_packages("biovis_media_extension"),
    keywords='markdown, dynamic plot, multimedia',
    install_requires=[
        'plotly>=3.6.1',
        'bokeh>=1.0.4',
        'Jinja2>=2.10',
        'Markdown>=3.0.1',
        'pyparsing>=2.3.1',
        'requests>=2.21.0',
        'multiqc>=1.7',
        'sqlalchemy>=1.2.18',
        'psutil>=5.5.1'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'markdown.extensions': [
            'biovis_media_extension = biovis_media_extension.extension:BioVisPluginExtension'
        ]
    }
)
