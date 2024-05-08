import os

CODE = 9709

for file in os.listdir(fr"dir\{CODE}-Converted"):
    filename = os.fsdecode(file)

    if not filename.startswith("I"):
        with open(fr"dir\{CODE}-Converted\{filename}", "r+") as f:
            content = f.read()
            f.seek(0, 0)
            f.write("Combined Component Code, Paper Combinations, A*, A, B, C, D, E".rstrip(
                '\r\n') + '\n' + content)
