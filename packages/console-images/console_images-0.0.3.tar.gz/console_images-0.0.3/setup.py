import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

requirements = ["colorama", "typing", "pillow"]

setuptools.setup(
	name="console_images",
	version="0.0.3",
    author="LedinecMing",
	author_email="loliamalexxaxa@gmail.com",
	description="Colored console images and gifs",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	install_requires=requirements,
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)

