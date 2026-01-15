from setuptools import setup, find_packages

setup(
    name="gpu-usage-menubar",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyobjc-framework-Cocoa>=10.0",
        "Pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "gpu-usage-menubar=gpu_usage_menubar.app:main",
        ],
    },
)
