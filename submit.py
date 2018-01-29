import os
import shutil
from os import listdir
from os.path import isfile, join
from subprocess import check_output


input_files = [f for f in listdir(".") if isfile(join(".", f)) and ".in" in f]

for file in input_files:
    with open(file.replace(".in", ".out"), "w+") as f:
        f.write(check_output(["python", "pizza.py", file]).decode("utf-8"))


if os.path.exists("./submit"):
    shutil.rmtree("./submit")

os.mkdir("./submit")
shutil.copyfile("pizza.py", "./submit/pizza.py")
shutil.copyfile("submit.py", "./submit/submit.py")

shutil.make_archive("submit", 'zip', "./submit")
