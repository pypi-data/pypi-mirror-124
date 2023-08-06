from setuptools import setup

setup(
    name="minio_driver",
    version='0.0.1',
    packages=['minio_driver'],
    author="Yubaraj Shrestha",
    author_email="companion.krish@outlook.com",
    install_requires=[
        'masonite',
    ],
    include_package_data=True,
    keywords=["masonite", "storage", "minio", "masonite-storage-driver"]
)
