from setuptools import setup, find_packages

setup(
    name='metabolink',
    version='0.1.0',
    description='A package for metabolic precursor analysis',
    author='Daniel R. Weilandt',
    author_email='daniel.r.weilandt@gmail.com',
    url='https://github.com/yourusername/metabolink',
    packages=find_packages(),
    install_requires=[
        # Add your package dependencies here
        'numpy',
        'pandas',
        'networkx',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)