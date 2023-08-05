import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dj_audit',
    version='0.0.1',
    author="Tairu Oluwafemi Emmanuel",
    author_email="developer.emmarex@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Emmarex/django-audit",
    download_url="",
    keywords=['Django Audit'],
    packages=setuptools.find_packages(),
    python_requires='~=3.6',
    install_requires=["Django"],
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",
        # "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2"
    ],
)
