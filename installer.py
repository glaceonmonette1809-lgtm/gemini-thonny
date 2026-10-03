# -*- coding: utf-8 -*-

import os
import platform
import shutil
import tempfile
import zipfile
from pathlib import Path


ZIP_NAME = "thonnycontrib.zip"
PLUGIN_NAME = "thonnycontrib"


def find_thonny_plugins_dir():
    """
    Tự tìm thư mục plugins của Thonny.
    Không hard-code username hoặc Python version.
    """

    home = Path.home()
    system = platform.system()

    if system == "Windows":
        appdata = Path(
            os.environ.get(
                "APPDATA",
                home / "AppData" / "Roaming"
            )
        )

        return appdata / "Thonny" / "plugins"

    elif system == "Darwin":
        return home / "Library" / "Thonny" / "plugins"

    else:
        return home / ".config" / "Thonny" / "plugins"


def install():
    current_dir = Path(__file__).resolve().parent
    zip_file = current_dir / ZIP_NAME

    print("=" * 50)
    print("       GEMINI THONNY INSTALLER")
    print("=" * 50)

    # --------------------------------------------------------
    # Kiểm tra ZIP
    # --------------------------------------------------------

    if not zip_file.exists():
        print()
        print("Không tìm thấy:")
        print(zip_file)
        input("\nNhấn Enter để thoát...")
        return

    # --------------------------------------------------------
    # Tìm thư mục plugin của Thonny
    # --------------------------------------------------------

    plugins_dir = find_thonny_plugins_dir()
    destination = plugins_dir / PLUGIN_NAME

    print()
    print("Thư mục Thonny:")
    print(plugins_dir)

    # --------------------------------------------------------
    # Tạo thư mục plugins
    # --------------------------------------------------------

    try:
        plugins_dir.mkdir(
            parents=True,
            exist_ok=True
        )
    except Exception as e:
        print()
        print("Không thể tạo thư mục plugins:")
        print(e)
        input("\nNhấn Enter để thoát...")
        return

    # --------------------------------------------------------
    # Giải nén ZIP vào thư mục tạm
    # --------------------------------------------------------

    try:
        with tempfile.TemporaryDirectory() as temp_dir:

            temp_dir = Path(temp_dir)

            print()
            print("Đang giải nén thonnycontrib.zip...")

            with zipfile.ZipFile(
                zip_file,
                "r"
            ) as zip_ref:

                zip_ref.extractall(temp_dir)

            # ------------------------------------------------
            # Tìm thư mục thonnycontrib
            # ------------------------------------------------

            extracted = temp_dir / PLUGIN_NAME

            # Trường hợp ZIP có:
            #
            # thonnycontrib/
            # ├── ...
            #
            # thì dùng trực tiếp.
            #
            # Nếu ZIP có thêm một thư mục bao ngoài,
            # tìm tự động.
            # ------------------------------------------------

            if not extracted.is_dir():

                found = None

                for path in temp_dir.rglob(PLUGIN_NAME):

                    if path.is_dir():
                        found = path
                        break

                if found is None:
                    print()
                    print(
                        "Không tìm thấy thư mục "
                        "'thonnycontrib' trong ZIP."
                    )

                    input("\nNhấn Enter để thoát...")
                    return

                extracted = found

            # ------------------------------------------------
            # Xóa plugin cũ
            # ------------------------------------------------

            if destination.exists():

                print()
                print("Đang xóa bản cũ...")

                if destination.is_dir():
                    shutil.rmtree(destination)
                else:
                    destination.unlink()

            # ------------------------------------------------
            # Chép plugin mới
            # ------------------------------------------------

            print()
            print("Đang cài plugin...")

            shutil.copytree(
                extracted,
                destination
            )

        # ----------------------------------------------------
        # Thành công
        # ----------------------------------------------------

        print()
        print("=" * 50)
        print("CÀI ĐẶT THÀNH CÔNG!")
        print("=" * 50)

        print()
        print("Plugin:")
        print(destination)

        print()
        print("Hãy đóng và mở lại Thonny.")

    except zipfile.BadZipFile:
        print()
        print("File thonnycontrib.zip bị lỗi hoặc không phải ZIP hợp lệ.")

    except PermissionError:
        print()
        print("Không có quyền ghi vào thư mục Thonny.")
        print("Hãy đóng Thonny rồi chạy lại installer.")

    except Exception as e:
        print()
        print("Cài đặt thất bại:")
        print(e)

    input("\nNhấn Enter để thoát...")


if __name__ == "__main__":
    install()