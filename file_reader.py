def raw_read(filename, mode="list"):
    if filename.endswith(".txt"):
        pass
    elif filename == "":
        filename = "test.txt"
    else:
        filename += ".txt"
    with open(filename, "r") as file:
        text = file.readlines()
    if mode == "list":
        return text
    elif mode == "pure_raw":
        pure_text = ""
        for line in text:
            pure_text += " " + line
        return pure_text
