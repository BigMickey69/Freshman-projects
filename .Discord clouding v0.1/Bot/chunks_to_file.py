import os

def reassemble_file(output_filepath, chunk_folder, ori_file_name):
    result_f = open(output_filepath, "wb")
    for file_name in sorted(os.listdir(os.path.join(chunk_folder, ori_file_name))):
        path = os.path.join(chunk_folder, ori_file_name, file_name)
        f = open(path, "rb")
        data = f.read()
        result_f.write(data)
        f.close()
    result_f.close()

if __name__ == "__main__":
    pass
