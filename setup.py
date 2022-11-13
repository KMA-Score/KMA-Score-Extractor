from cx_Freeze import Executable, setup

executables = [Executable("main.py", target_name="kma_score_dumper")]

options = {
    "build": {
        "excludes": [],
        "zip_include_packages": ["*"],
        "zip_exclude_packages": [],
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
    url="https://github.com/KMA-Score/KMA-Score-Extractor",
    copyright="2022 Dang Hoang Phuc"
)
