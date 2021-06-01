from typing import Iterable

def writeToFile(content: Iterable[str],
                file_name: str = "extracted",
                file_type: str = "txt",
                file_path: str = "test"):

    print(f'> writing "{file_name}.{file_type}" to path "/{file_path}/"', end = '')

    if isinstance(content, list):
        if not isinstance(content[0], str):
            content = [str(c) for c in content]
    elif not isinstance(content, str):
        content = str(content)

    # Program to show various ways to read and
    # write data in a file.
    file1 = open(f"{file_path}/{file_name}.{file_type}", "w")

    file1.writelines(content)
    file1.close()  # to change file access modes

    print('\t ==> DONE!')


if __name__ == "__main__":
    writeToFile('content', 'writeToFile', 'txt', 'helper')
    # print('done')