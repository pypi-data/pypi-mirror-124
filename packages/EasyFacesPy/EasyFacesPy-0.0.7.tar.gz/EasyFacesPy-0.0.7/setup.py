from setuptools import setup, find_packages




VERSION = '0.0.7'
DESCRIPTION = 'This library will help you with face recognition in photos.'


# Setting up
setup(
    name="EasyFacesPy",
    version=VERSION,
    author="Nellle",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'Pillow'],
    keywords=['python', 'face', 'opencv'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)