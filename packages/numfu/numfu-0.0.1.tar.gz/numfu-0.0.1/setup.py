import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='numfu',
    # packages = ['numfu'],
    version='0.0.1',
    license='MIT',
    description='Master the numpy arts',
    long_description='',
    url='',
    download_url = 'https://github.com/kevinkmcguigan/numfu/archive/refs/tags/0.0.1.tar.gz',
    author='kevin mcguigan',
    author_email='',
    keywords = ['numpy', 'snippits'], 
    install_requires=['numpy'],
    classifiers=['Development Status :: 1 - Planning'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)

# more info:
# https://packaging.python.org/tutorials/packaging-projects/

# better:
#https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56