from cx_Freeze import Executable, setup

executables = [Executable("main.py", target_name="test_bcrypt")]

options = {
    "build_exe": {
        "excludes": [],
        "zip_include_packages": ["*"],
        "zip_exclude_packages": [],
        "packages": ["fitz", "tqdm", "pdfplumber", "pandas", "loguru", "numpy", "charset_normalizer"]
    }
}

setup(
    name="test_bcrypt",
    version="0.1",
    description="cx_Freeze script to test bcrypt",
    executables=executables,
    options=options,
    packages=[],
    author="Marcelo Duarte",
    author_email="marcelotduarte@users.noreply.github.com",
    url="https://github.com/marcelotduarte/cx_Freeze/",
)
