import shutil
from pathlib import Path
import re
import sys
import threading
from multiprocessing import cpu_count, Process


class FileSorter:
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a",
        "b",
        "v",
        "g",
        "d",
        "e",
        "e",
        "j",
        "z",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "r",
        "s",
        "t",
        "u",
        "f",
        "h",
        "ts",
        "ch",
        "sh",
        "sch",
        "",
        "y",
        "",
        "e",
        "yu",
        "u",
        "ja",
        "je",
        "ji",
        "g",
    )

    MAP = {}

    for cirilic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        MAP[ord(cirilic)] = latin
        MAP[ord(cirilic.upper())] = latin.upper()

    def __init__(self, source_folder):
        self.source_folder = source_folder

        self.JPEG_IMAGES = []
        self.JPG_IMAGES = []
        self.PNG_IMAGES = []
        self.SVG_IMAGES = []
        self.MP3_AUDIO = []
        self.OGG_AUDIO = []
        self.WAV_AUDIO = []
        self.AMR_AUDIO = []
        self.AVI_VIDEO = []
        self.MP4_VIDEO = []
        self.MOV_VIDEO = []
        self.MKV_VIDEO = []
        self.DOC_DOCUMENTS = []
        self.DOCX_DOCUMENTS = []
        self.TXT_DOCUMENTS = []
        self.PDF_DOCUMENTS = []
        self.XLSX_DOCUMENTS = []
        self.PPTX_DOCUMENTS = []
        self.OTHERS = []
        self.ZIP_ARCHIVES = []
        self.GZ_ARCHIVES = []
        self.TAR_ARCHIVES = []
        self.FOLDERS = []
        self.EXTENSIONS = set()
        self.UNKNOWN = set()

        self.REGISTER_EXTENSION = {
            "JPEG": self.JPEG_IMAGES,
            "JPG": self.JPG_IMAGES,
            "PNG": self.PNG_IMAGES,
            "SVG": self.SVG_IMAGES,
            "MP3": self.MP3_AUDIO,
            "OGG": self.OGG_AUDIO,
            "WAV": self.WAV_AUDIO,
            "AMR": self.AMR_AUDIO,
            "AVI": self.AVI_VIDEO,
            "MP4": self.MP4_VIDEO,
            "MOV": self.MOV_VIDEO,
            "MKV": self.MKV_VIDEO,
            "DOC": self.DOC_DOCUMENTS,
            "DOCX": self.DOCX_DOCUMENTS,
            "TXT": self.TXT_DOCUMENTS,
            "PDF": self.PDF_DOCUMENTS,
            "XLSX": self.XLSX_DOCUMENTS,
            "PPTX": self.PPTX_DOCUMENTS,
            "ZIP": self.ZIP_ARCHIVES,
            "GZ": self.GZ_ARCHIVES,
            "TAR": self.TAR_ARCHIVES,
        }

    def get_extension(self, name):
        return Path(name).suffix[1:].upper()

    def scan(self, folder):
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in (
                    "archives",
                    "video",
                    "audio",
                    "documents",
                    "images",
                    "OTHERS",
                ):
                    self.FOLDERS.append(item)
                    self.scan(item)
                continue

            ext = self.get_extension(item.name)
            full_name = folder / item.name
            if not ext:
                self.OTHERS.append(full_name)
            else:
                try:
                    ext_register = self.REGISTER_EXTENSION[ext]
                    ext_register.append(full_name)
                    self.EXTENSIONS.add(ext)
                except KeyError:
                    self.UNKNOWN.add(ext)
                    self.OTHERS.append(full_name)

    def normalize(self, name):
        string = name.translate(self.MAP)
        translated_name = re.sub(r"[^a-zA-Z.0-9_]", "_", string)
        return translated_name

    def handle_image(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        new_file_path = target_folder / self.normalize(file_name.name)
        shutil.move(str(file_name), str(new_file_path))
        return new_file_path

    def handle_audio(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        new_file_path = target_folder / self.normalize(file_name.name)
        shutil.move(str(file_name), str(new_file_path))
        return new_file_path

    def handle_video(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        new_file_path = target_folder / self.normalize(file_name.name)
        shutil.move(str(file_name), str(new_file_path))
        return new_file_path

    def handle_documents(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        new_file_path = target_folder / self.normalize(file_name.name)
        shutil.move(str(file_name), str(new_file_path))
        return new_file_path

    def handle_archive(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / self.normalize(
            file_name.name.replace(file_name.suffix, "")
        )
        folder_for_file.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(
                str(file_name.absolute()), str(folder_for_file.absolute())
            )
        except shutil.ReadError:
            print(f"Error extracting {file_name}")
            return
        else:
            file_name.unlink()
            return folder_for_file

    def core(self):
        # self.scan(self.source_folder)
        processes = []
        pr = Process(
            target=self.scan(self.source_folder),
        )
        pr.start()
        processes.append(pr)

        for file in self.JPEG_IMAGES:
            threading.Thread(
                target=self.handle_image,
                args=(file, self.source_folder / "images"),
                daemon=True,
            ).start()
        for file in self.JPG_IMAGES:
            threading.Thread(
                target=self.handle_image,
                args=(file, self.source_folder / "images"),
                daemon=True,
            ).start()
        for file in self.PNG_IMAGES:
            threading.Thread(
                target=self.handle_image,
                args=(file, self.source_folder / "images"),
                daemon=True,
            ).start()
        for file in self.SVG_IMAGES:
            self.handle_image(file, self.source_folder / "images")
        for file in self.MP3_AUDIO:
            threading.Thread(
                target=self.handle_audio,
                args=(file, self.source_folder / "audio"),
                daemon=True,
            ).start()
        for file in self.OGG_AUDIO:
            self.handle_audio(file, self.source_folder / "audio")
        for file in self.WAV_AUDIO:
            threading.Thread(
                target=self.handle_audio,
                args=(file, self.source_folder / "audio"),
                daemon=True,
            ).start()
        for file in self.AMR_AUDIO:
            threading.Thread(
                target=self.handle_audio,
                args=(file, self.source_folder / "audio"),
                daemon=True,
            ).start()

        for file in self.AVI_VIDEO:
            threading.Thread(
                target=self.handle_video,
                args=(file, self.source_folder / "video"),
                daemon=True,
            ).start()
        for file in self.MP4_VIDEO:
            threading.Thread(
                target=self.handle_video,
                args=(file, self.source_folder / "video"),
                daemon=True,
            ).start()
        for file in self.MOV_VIDEO:
            threading.Thread(
                target=self.handle_video,
                args=(file, self.source_folder / "video"),
                daemon=True,
            ).start()
        for file in self.MKV_VIDEO:
            self.handle_video(file, self.source_folder / "video")

        for file in self.DOC_DOCUMENTS:
            threading.Thread(
                target=self.handle_documents,
                args=(file, self.source_folder / "documents"),
                daemon=True,
            ).start()
        for file in self.DOCX_DOCUMENTS:
            threading.Thread(
                target=self.handle_documents,
                args=(file, self.source_folder / "documents"),
                daemon=True,
            ).start()
        for file in self.TXT_DOCUMENTS:
            threading.Thread(
                target=self.handle_documents,
                args=(file, self.source_folder / "documents"),
                daemon=True,
            ).start()
        for file in self.PDF_DOCUMENTS:
            threading.Thread(
                target=self.handle_documents,
                args=(file, self.source_folder / "documents"),
                daemon=True,
            ).start()
        for file in self.XLSX_DOCUMENTS:
            threading.Thread(
                target=self.handle_documents,
                args=(file, self.source_folder / "documents"),
                daemon=True,
            ).start()
        for file in self.PPTX_DOCUMENTS:
            self.handle_documents(file, self.source_folder / "documents")

        for file in self.OTHERS:
            self.handle_image(file, self.source_folder / "others")

        for file in self.ZIP_ARCHIVES:
            p = Process(
                target=self.handle_archive,
                args=(file, self.source_folder / "archives"),
            )
            p.start()
            processes.append(p)
        for file in self.GZ_ARCHIVES:
            p = Process(
                target=self.handle_archive,
                args=(file, self.source_folder / "archives"),
            )
            p.start()
            processes.append(p)
        for file in self.TAR_ARCHIVES:
            p = Process(
                target=self.handle_archive,
                args=(file, self.source_folder / "archives"),
            )
            p.start()
            processes.append(p)

        for folder in self.FOLDERS[::-1]:
            try:
                folder.rmdir()
            except OSError:
                print(f"Error during remove folder {folder}")


def start():
    if len(sys.argv) > 1:
        folder_process = Path(sys.argv[1])
        file_sorter = FileSorter(folder_process)
        file_sorter.core()


def factorize(*numbers):
    result = []
    for number in numbers:
        result.append([i for i in range(1, number + 1) if number % i == 0])
    print(result)
    return tuple(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("To sort files use: python script.py <folder_path>")
        numbers = input("Enter numbers to factorize (divided by coma): ")
        numbers = [int(num) for num in numbers.split(",")]
        threading.Thread(target=factorize, args=numbers, daemon=True).start()
        sys.exit(1)

    start()
    numbers = input("Enter numbers to factorize (divided by coma): ")
    numbers = [int(num) for num in numbers.split(",")]
    threading.Thread(target=factorize, args=numbers, daemon=True).start()
    print(cpu_count())
