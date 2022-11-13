from cx_Freeze import Executable, setup
import datetime

executables = [Executable("main.py", target_name="kma_score_dumper", copyright="{} Dang Hoang Phuc".format(datetime.date.today().year))]

options = {
    "build_exe": {
        "excludes": [],
        "zip_include_packages": ["*"],
        "zip_exclude_packages": [],
        "packages": ["fitz", "tqdm", "pdfplumber", "pandas", "loguru", "numpy", "charset_normalizer"]
    },
    "bdist_rpm": {
        "zip_include_packages": ["*"],
        "packages": ["fitz", "tqdm", "pdfplumber", "pandas", "loguru", "numpy", "charset_normalizer"]
    },
    "bdist_mac": {
        "zip_include_packages": ["*"],
        "packages": ["fitz", "tqdm", "pdfplumber", "pandas", "loguru", "numpy", "charset_normalizer"]
    }
}

setup(
    name="kma_score_dumper",
    version="1.0",
    description="KMA Score Dumper",
    executables=executables,
    options=options,
    packages=[],
    author="Dang Hoang Phuc",
    author_email="13364457+phuchptty@users.noreply.github.com",
    url="https://github.com/KMA-Score/KMA-Score-Extractor"
)
