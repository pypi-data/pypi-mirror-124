from setuptools import setup, find_packages

setup(
    name='sonotoria',
    version='0.1.2',
    description='Jinja expander',
    url='https://gitlab.com/neomyte/sonotoria',
    author='Emmanuel Pluot',
    author_email='emmanuel.pluot@gmail.com',
    license='N/A',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'jinja2'
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows'
    ]
)