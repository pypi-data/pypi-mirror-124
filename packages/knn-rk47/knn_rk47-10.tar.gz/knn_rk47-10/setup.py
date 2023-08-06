from setuptools import setup

setup(
    name='knn_rk47',
    version='10',
    install_requires=[
        'hnswlib',
    ],
    packages=['knn'],
    package_dir={
        "": "src"
        },
    package_data={
        "knn": ["index.bl"]
    },
    include_package_data=True
)

