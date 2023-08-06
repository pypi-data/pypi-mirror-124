from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
import subprocess

# command = "sh prepare_env_source.sh"
# process = subprocess.Popen(command, shell=True, cwd=".")


class CustomInstallCommand(install):
    """Custom install setup to help run shell commands (outside shell) before installation"""

    def run(self):
        custom_command = "sh prepare_env_source.sh"
        # custom_process = subprocess.Popen(custom_command, shell=True, cwd=".")
        # custom_process.wait()
        try:
            subprocess.check_call(custom_command, shell=True, cwd=".")
        except subprocess.CalledProcessError:
            print("Not have cmake")
        install.run(self)


class CustomEggInfoCommand(egg_info):
    """Custom install setup to help run shell commands (outside shell) before installation"""

    def run(self):
        egg_info.run(self)
        custom_command = "sh prepare_env_source.sh"
        # custom_process = subprocess.Popen(custom_command, shell=True, cwd=".")
        # custom_process.wait()
        try:
            subprocess.check_call(custom_command, shell=True, cwd=".")
        except subprocess.CalledProcessError:
            print("Not have cmake")


with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    "pandas",
    "numpy",
    "aiosmtplib",
    "python-dateutil",
    "pymongo",
    "redis",
    "pyyaml",
    "motor",
]

extras_require = {
    "full": ["luigi", "scikit-learn", "joblib"],
}


setup(
    name="lightning_fast",
    version="0.0.78",
    author="yingxiongxqs",
    author_email="yingxiongxqs@126.com",
    description="Fast Data Encoders",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xuqiushi/lightning_fast",
    cmdclass={
        "install": CustomInstallCommand,
        # 'develop': CustomDevelopCommand,
        "egg_info": CustomEggInfoCommand,
    },
    # package_dir={"": "lightning_fast"},
    packages=find_packages(exclude=("tests",)),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.7",
    zip_safe=False,
    extras_require=extras_require,
)
