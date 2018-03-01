import shutil
from os import listdir, mkdir
from os.path import isfile, join
from subprocess import check_output

input_files = [f for f in listdir(".") if isfile(join(".", f)) and ".in" in f]
input_files = ['example.in', 'small.in']

for file in input_files:
    with open(file.replace(".in", ".out"), "w+") as f:
        print(file, "...")
        f.write(check_output(
            ["python", "pizza_answer_example.py", file]).decode("utf-8"))

if os.path.exists("./submit"):
    shutil.rmtree("./submit")

mkdir("./submit")
shutil.copyfile("pizza_answer_example.py", "./submit/pizza.py")
shutil.copyfile("submit.py", "./submit/submit.py")
shutil.make_archive("submit", 'zip', "./submit")
