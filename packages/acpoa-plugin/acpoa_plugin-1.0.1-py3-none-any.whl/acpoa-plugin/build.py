import glob
import os
import re


def build(args):
    def update_datalist():
        files = []
        for d in os.listdir("src"):
            if not os.path.isdir(d):
                pass
            sub_path = os.path.join("src", d)
            sub_files = glob.glob(os.path.join(sub_path, "**", "*"), recursive=True)
            sub_files = [os.path.relpath(sub_file, sub_path) for sub_file in sub_files]
            files += sub_files

        with open('setup.py', 'r') as file:
            text = file.read()
        text = re.sub(r"(files = ).*", rf"\1{files}", text)
        with open('setup.py', 'w') as file:
            file.write(text)

    original_path = os.getcwd()
    os.chdir(args.path)
    if args.data_detection: update_datalist()
    os.system("python3 -m build")
    os.chdir(original_path)
