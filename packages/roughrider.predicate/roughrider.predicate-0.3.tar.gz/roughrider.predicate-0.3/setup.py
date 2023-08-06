import os
from setuptools import setup, find_packages
from Cython.Build import cythonize

version = "0.3"

install_requires = [
]

test_requires = [
    'pytest',
]


setup(
    name='roughrider.predicate',
    version=version,
    author='Souheil CHELFOUH',
    author_email='trollfot@gmail.com',
    url='http://gitweb.dolmen-project.org',
    download_url='http://pypi.python.org/pypi/roughrider.predicate',
    description='Pure python predicate/guard/validation system.',
    long_description=(open("README.rst").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.rst")).read()),
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['roughrider',],
    include_package_data=True,
    zip_safe=False,
    ext_modules = cythonize([
        "src/roughrider/predicate/errors.pyx",
        "src/roughrider/predicate/utils.pyx",
    ]),
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
    },
)
