from setuptools import setup, find_packages


VERSION = '0.0.3'
DESCRIPTION = 'A basic helper package for students of AusBi Datademy'
LONG_DESCRIPTION = 'A package that allows new python user/learner to insteract with the code conveniently, without the hastle of handling error or database connection'

# Setting up
setup(
    name="datademy-helper",
    version=VERSION,
    author="HaPhan Tran (AusBi Datademy)",
    author_email="<haphantran@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'learner', 'helper',
              'input', 'get_int', 'get_string'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
