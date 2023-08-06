import setuptools

with open("README.md", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="converterpy",
    version="0.0.2",
    author="Bilal Ekrem Harmansa",
    author_email="bilalekremharmansa@gmail.com",
    description="customizable converter tool to convert <source> to <target>",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bilalekremharmansa/converterpy",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'convert = converterpy.main.convert:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
