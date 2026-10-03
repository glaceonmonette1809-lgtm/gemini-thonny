import os
import platform
import shutil
import tempfile
import zipfile
from pathlib import Path


def find_plugins_dir():
    home = Path.home()

    if platform.system() == "Windows":
        appdata = Path(
            os.environ.get(
                "APPDATA",
                home / "AppData" / "Roaming"
            )
        )
        return appdata / "Thonny" / "plugins"

    if platform.system() == "Darwin":
        return home / "Library" / "Thonny" / "plugins"

    return home / ".config" / "Thonny" / "plugins"


def main():

    project_dir = Path(__file__).resolve().parent

    zip_file = project_dir / "thonnycontrib.zip"

    if not zip_file.exists():
        raise FileNotFoundError(
            f"Không tìm thấy {zip_file}"
        )

    plugins_dir = find_plugins_dir()
    plugins_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)

        with zipfile.ZipFile(
            zip_file,
            "r"
        ) as z:
            z.extractall(temp)

        source = temp / "thonnycontrib"

        if not source.exists():

            found = next(
                temp.rglob("thonnycontrib"),
                None
            )

            if found is None:
                raise RuntimeError(
                    "Không tìm thấy thonnycontrib trong ZIP."
                )

            source = found

        destination = plugins_dir / "thonnycontrib"

        if destination.exists():
            shutil.rmtree(destination)

        shutil.copytree(
            source,
            destination
        )

    print()
    print("====================================")
    print(" GThonny Updated")
    print("====================================")
    print()
    print(destination)
    print()
    print("Restart Thonny.")


if __name__ == "__main__":
    main()
