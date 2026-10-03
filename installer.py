import os
import platform
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path


PROJECT_ZIP = (
    "https://github.com/"
    "glaceonmonette1809-lgtm/"
    "gemini-thonny/"
    "archive/refs/heads/main.zip"
)


def find_thonny_plugins():
    home = Path.home()

    if platform.system() == "Windows":
        appdata = Path(
            os.environ.get(
                "APPDATA",
                home / "AppData" / "Roaming"
            )
        )

        thonny = appdata / "Thonny"

        # Tìm Pythonxxx/site-packages
        matches = list(
            thonny.glob(
                "plugins/Python*/site-packages"
            )
        )

        if matches:
            return matches[0]

        # Nếu chưa có thì tạo vị trí mặc định.
        return thonny / "plugins"

    if platform.system() == "Darwin":
        return (
            home
            / "Library"
            / "Thonny"
            / "plugins"
        )

    return (
        home
        / ".config"
        / "Thonny"
        / "plugins"
    )


def main():
    print("Installing Gemini Thonny...")

    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)

        project_zip = temp / "project.zip"

        print("Downloading...")

        urllib.request.urlretrieve(
            PROJECT_ZIP,
            project_zip
        )

        print("Extracting...")

        with zipfile.ZipFile(
            project_zip,
            "r"
        ) as z:
            z.extractall(temp)

        project_dir = (
            temp
            / "gemini-thonny-main"
        )

        plugin_zip = (
            project_dir
            / "thonnycontrib.zip"
        )

        if not plugin_zip.exists():
            raise RuntimeError(
                "Không tìm thấy thonnycontrib.zip."
            )

        plugin_temp = temp / "plugin"

        with zipfile.ZipFile(
            plugin_zip,
            "r"
        ) as z:
            z.extractall(plugin_temp)

        source = plugin_temp / "thonnycontrib"

        if not source.exists():
            found = next(
                plugin_temp.rglob("thonnycontrib"),
                None
            )

            if found is None:
                raise RuntimeError(
                    "Không tìm thấy thư mục "
                    "thonnycontrib."
                )

            source = found

        destination_dir = find_thonny_plugins()

        destination_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        destination = (
            destination_dir
            / "thonnycontrib"
        )

        if destination.exists():
            shutil.rmtree(destination)

        shutil.copytree(
            source,
            destination
        )

    print()
    print("Gemini Thonny installed successfully!")
    print(f"Installed to: {destination}")
    print()
    print("Restart Thonny.")


if __name__ == "__main__":
    main()
