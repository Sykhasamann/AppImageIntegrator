from setuptools import setup, find_packages

setup(
    name="appimage-integrator",
    version="1.0.0",
    description="Intégrateur AppImage CLI & GUI avec extraction, .desktop, icône et désinstallation",
    author="syks",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt5>=5.15.9",
        "watchdog>=3.0.0",
        "Pillow>=9.0.0"
    ],
    entry_points={
        "console_scripts": [
            "appimage-integrator=appimage_integrator:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.7',
)
