PATH = '../sample.xml'  # Path for the Sample File


def read_file(FilePath=PATH) -> list:
    """
    input: take the path name for the xml file
    return: list contains each line in the file
    """
    data = None
    with open(FilePath, 'r') as File:
        data = File.readlines()
    data_list = []
    for line in data:
        data_list.append(str(line).strip())
    return data_list


if __name__ == '__main__':
    pass
