import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "src/main.py",
        "--name=lithium",
        "-F",
        "--clean",
        "--hidden-import=sklearn.utils.typedefs",
        "--hidden-import=sklearn.utils._typedefs",
        "--hidden-import=sklearn.neighbors.typedefs",
    ]
)
