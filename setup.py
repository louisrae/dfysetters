from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="dfysetters",
    version="2.0.8.3",
    description="Back end code base for a sales-as-a-service business",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/louisrae/dfysetters",
    author="Louis-Rae",
    author_email="louisrae@settersandspecialists.com",
    keywords="tracking, email, onboarding",
    packages=find_packages(),
    python_requires=">=3.6, <4",
    install_requires=["pandas", "gspread", "gcsa", "slackclient"],
)
