from setuptools import setup, find_packages

setup(
    name='PythonLatexSync',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='A package to synchronize LaTeX files with a server using a simple API.',
    author='Achille Merendino',
    url='https://github.com/prenone/PythonLatexSync'
)

