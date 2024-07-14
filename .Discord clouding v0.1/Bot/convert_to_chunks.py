import os

BYTE_LIMIT = 26_108_800
#BYTE_LIMIT = 45000  #for testing 


def read_in_chunks(file):
    global BYTE_LIMIT
    while True:
        data = file.read(BYTE_LIMIT)
        if not data:
            break
        yield data

def write_file_in_chunks(f, PATH_TO_TEMP, file_name, file_path):
    total_chunk_num = int(os.path.getsize(file_path)/BYTE_LIMIT) + 1
    i = 1
    path = os.path.join(PATH_TO_TEMP, file_name)
    if not os.path.exists(path):
        os.makedirs(path)

    for chunk in read_in_chunks(f):
        header_num = "{:04}".format(i)
        f2 = open(os.path.join(path,f"{header_num}.json"), "wb")
        f2.write(chunk)
        f2.close()
        i+=1
    f.close()
    return total_chunk_num






    