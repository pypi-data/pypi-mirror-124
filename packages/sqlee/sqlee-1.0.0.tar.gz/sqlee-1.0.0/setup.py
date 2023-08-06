import setuptools

long_description = """
# Sqlee
Database Powerd by Gitee.
"""

setuptools.setup(
    name = "sqlee",
    version = "1.0.0",
    author = "Entropy",
    author_email = "fu050409@163.com",
    description = "Database Powerd by Gitee",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitee.com/qu-c/sqlee",
    project_urls = {
        "Bug Tracker": "https://gitee.com/qu-c/sqlee/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license = "MIT",
    scripts = ["sqlee\\sqlee.py"],
    packages = setuptools.find_packages(where="sqlee"),
    package_dir = {"": "sqlee"},
    install_requires = [
        'requests',
        'prompt_toolkit',
        'argparse',
    ],
    python_requires=">=3",
    
)
