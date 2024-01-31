
def get_value_from_env(file_path, key):
    with open(file_path, "r") as f:
        for line in f:
            # 去除换行符和空格，并以等号分割键值对
            key_value = line.strip().split("=")
            if len(key_value) == 2 and key_value[0] == key:
                return key_value[1]
    return None


def append_data_to_env(key, data_to_append):
    # 读取.env文件内容
    with open(".env", "r") as f:
        lines = f.readlines()

    # 查找包含key的行并在等号后面追加内容
    with open(".env", "w") as f:
        for line in lines:
            if line.strip().startswith(f"{key}="):
                line = f"{key}={line.strip().split('=')[1]}{data_to_append}\n"
            f.write(line)