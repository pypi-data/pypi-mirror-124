from setuptools import setup, find_packages


setup(
    name='tweets_cleaner',
    version='0.1',
    license='MIT',
    long_description_content_type="text/x-rst",
    author="Rizki Maulana",
    author_email='rizkimaulana348@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/rizki4106/tweets_cleaner',
    keywords='twitter tweets data data-science machine-learning data-trasformation data-preprocessing',
)