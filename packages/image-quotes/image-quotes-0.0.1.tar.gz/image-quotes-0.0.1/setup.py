import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages = [ 
  "image_quotes"
]

setuptools.setup(
    name="image-quotes",
    version="0.0.1",
    author="Bruce",
    packages=packages,
    author_email="brucealt69@gmail.com",
    description="A package to get inspirational images for your #MondayMotivation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BruceCodesGithub/img-quotes",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requres= [
      "aiohttp",
      "Pillow"
    ]
)