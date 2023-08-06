from setuptools import setup

setup(
    name="minio_driver",
    version='0.0.6',
    packages=['minio_driver'],
    author="Yubaraj Shrestha",
    author_email="companion.krish@outlook.com",
    install_requires=[
        'masonite',
    ],
    description="Minio Storage Driver for Masonite",
    license="MIT",
    include_package_data=True,
    keywords=["masonite", "storage", "minio", "masonite-storage-driver"]
)
