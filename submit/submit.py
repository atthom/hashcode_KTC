import shutil
from os import listdir, mkdir
from os.path import isfile, join, exists
from subprocess import check_output

input_files = [f for f in listdir(".") if isfile(join(".", f)) and ".in" in f]

for file in input_files:
    with open(file.replace(".in", ".out"), "w+") as f:
        print(file, "...")
        f.write(check_output(
            ["python", "googlecar.py", file]).decode("utf-8"))

if exists("./submit"):
    shutil.rmtree("./submit")

mkdir("./submit")
shutil.copyfile("googlecar.py", "./submit/googlecar.py")
shutil.copyfile("submit.py", "./submit/submit.py")
shutil.make_archive("submit", 'zip', "./submit")
