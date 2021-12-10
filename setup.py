import setuptools
from pathlib import Path
from snowman import __sm

with open(Path("./README.md")) as file:
	descr = file.read()

setuptools.setup(
	name=__sm.APPNAME,
	version=__sm.version_tuple_to_str(__sm.VERSION),
	author=__sm.__authour__,
	author_email=__sm.__email__,
	description="API testing library",
	long_description=descr,
	long_description_content_type="text/markdown",
	url="https://github.com/rubbieKelvin/snowman",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.0',
	license="MIT"
)