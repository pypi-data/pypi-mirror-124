from setuptools import setup, find_packages
import tfdataset

setup(
    name="tfdataset",
    version=".".join(tfdataset.__version__),
    description="Video To Images",
    author="Sang Pil Yoo, Vo Van Tu",
    author_email="ysp9714@gmail.com",
    url="",
    download_url="",
    install_requires=["opencv-python",
                      "tqdm",
                      "numpy",
                      "grpcio",
                      "kazoo",
                      "bs4",
                      "pandas",
                      "tensorflow"],
    entry_points={"console_scripts": [
        "vidal=tfdataset.cutter:main", "actdata=tfdataset.action_recogntion_data:main", "objdata=tfdataset.object_detection_data:main"]},
    packages=find_packages(exclude=["docs", "test*"]),
    package_data={'tfdataset': [
        'autoinjector.json', 'eye_drop.json', 'glucometer.json', 'key.pem', 'star_inhandplus_com.crt']},
    include_package_data=False,
    keywords=["video", "frames"],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
