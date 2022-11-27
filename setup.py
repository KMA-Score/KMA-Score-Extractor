from cx_Freeze import Executable, setup
import datetime
import os

executables = [Executable("main.py", target_name="kma_score_dumper",
                          copyright="{} Dang Hoang Phuc".format(datetime.date.today().year))]

include_files = [
    os.path.abspath(os.path.join("data", "baseStructure.sql")),
    os.path.abspath(os.path.join("data", "subjectNameMapping.csv"))
]

options = {
    "build_exe": {
        "excludes": [],
        "zip_include_packages": ["*"],
        "zip_exclude_packages": [],
        "packages": ["fitz", "tqdm", "pdfplumber", "pandas", "loguru", "numpy", "charset_normalizer"],
        "include_files": include_files
    },
    "bdist_rpm": {
        # "packages": ["fitz", "tqdm", "pdfplumber", "pandas", "loguru", "numpy", "charset_normalizer"],
        # "include_files": include_files
    },
    "bdist_mac": {
        "zip_include_packages": ["*"],
        "packages": ["fitz", "tqdm", "pdfplumber", "pandas", "loguru", "numpy", "charset_normalizer"],
        "include_files": include_files
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
