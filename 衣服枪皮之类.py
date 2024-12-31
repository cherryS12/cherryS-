import sys


# 创建一个函数
def DEC_to_HEX(decimal_number):
    # 将十进制数转换为十六进制并格式化输出
    hex_number = format(int(decimal_number), '08X')  # '08X' 表示输出为8位十六进制数,不足部分用0填充

    # 将十六进制数拆分成数组并反转顺序
    hex_array = [hex_number[i:i + 2] for i in range(0, len(hex_number), 2)]
    reversed_hex_array = hex_array[::-1]  # 反转数组

    # 重新组合反转后的十六进制数并输出
    reversed_hex_number = ''.join(reversed_hex_array)
    print(decimal_number, end='')
    print("转换为：", end='')
    print(reversed_hex_number)
    return reversed_hex_number

def HEX_to_DEC(decimal_hex):
    hex_array = [decimal_hex[i:i + 2] for i in range(0, len(decimal_hex), 2)]
    reversed_hex_array = hex_array[::-1]  # 反转数组
    #print(reversed_hex_array)
    #拼接数组
    reversed_hex_number = ''.join(reversed_hex_array)
    # 将十六进制数转换为十进制并输出
    dec = int(reversed_hex_number,16)
    return dec

# 修改文件十六进制函数
def modify_file_hex(file_path, A, B):
    # 要搜索的十六进制序列
    search_seq1 = bytes.fromhex(A)
    search_seq2 = bytes.fromhex(B)

    # 搜索序列前的偏移量（以字节为单位）
    offset_before_search_seq = 0

    # 读取文件内容
    with open(file_path, "rb") as file:
        file_contents = file.read()

    # 查找第一个和第二个搜索序列的位置
    search_index1 = file_contents.rfind(search_seq1)
    search_index2 = file_contents.rfind(search_seq2)

    # 检查是否找到了两个序列
    if search_index1 == -1 or search_index2 == -1:
        if search_index1 == -1:
            print(HEX_to_DEC(A),end='')
            print("未找到指定的搜索序列。") 
        if search_index2 == -1:
            print(HEX_to_DEC(B),end='')     
            print("未找到指定的搜索序列。")           
    else:
        # 计算需要修改的序列的偏移位置
        replace_index1 = search_index1 - offset_before_search_seq
        replace_index2 = search_index2 - offset_before_search_seq

        # 检查偏移量是否导致替换位置超出文件开始位置
        if replace_index1 < 0 or replace_index2 < 0:
            print("第一个偏移量导致替换位置超出文件开始位置。")
        else:
            # 输出搜索到的序列的偏移位置和偏移后的值
            print(f"第一个搜索的十六进制偏移位置: {hex(search_index1)}")
            # print(f"需要修改的十六进制偏移位置: {hex(replace_index1)}")
            print(f"第一个需要修改的十六进制偏移位置及值 {hex(replace_index1)}: {file_contents[replace_index1:replace_index1 + 4].hex()}")

            print(f"第二个搜索的十六进制偏移位置: {hex(search_index2)}")
            # print(f"第二个需要修改的序列位于文件的十六进制偏移位置: {hex(replace_index2)}")
            print(f"第二个需要修改的十六进制偏移位置及值 {hex(replace_index2)}: {file_contents[replace_index2:replace_index2 + 4].hex()}")

            # 交换两个位置的值
            value_at_replace_index1 = file_contents[replace_index1:replace_index1 + 4]
            value_at_replace_index2 = file_contents[replace_index2:replace_index2 + 4]

            # 创建一个新文件内容的副本,用于修改
            new_contents = bytearray(file_contents)

            # 将value_at_replace_index1的值写入到replace_index2的位置
            new_contents[replace_index2:replace_index2 + 4] = value_at_replace_index1
            # 将value_at_replace_index2的值写入到replace_index1的位置
            new_contents[replace_index1:replace_index1 + 4] = value_at_replace_index2

            # 输出修改后的序列的偏移位置和偏移后的值
            # print(f"第一个修改后的序列位于文件的十六进制偏移位置: {hex(replace_index1)}")
            print(f"第一个修改后的十六进制偏移位置 {hex(replace_index1)}: {new_contents[replace_index1:replace_index1 + 4].hex()}")

            # print(f"第二个修改后的序列位于文件的十六进制偏移位置: {hex(replace_index2)}")
            print(f"第二个修改后的十六进制偏移位置 {hex(replace_index2)}: {new_contents[replace_index2:replace_index2 + 4].hex()}")

            # 将修改后的内容写回文件
            with open(file_path, "wb") as file:
                file.write(new_contents)

            print(f"文件已编辑")


def process_batch(file_path, code_list):
    for original_decimal, new_decimal in code_list:
        modify_file_hex(file_path, DEC_to_HEX(original_decimal), DEC_to_HEX(new_decimal))
        print("------------------------------------------------------")


while True:
    choice = input("请选择操作（1:单个文件修改，2:批量文件修改）：")
    if choice == '1':
        file_path = input("请输入要修改的文件路径（dat）：")
        try:
            original_decimal = int(input("请输入原皮美化代码："))
            new_decimal = int(input("请输入被改的美化代码："))
            modify_file_hex(file_path, DEC_to_HEX(original_decimal), DEC_to_HEX(new_decimal))
        except ValueError:
            print("输入错误，请输入有效的整数。")
    elif choice == '2':
        file_path = input("请输入要修改的文件路径（dat）：")
        txt_file_path = input("请输入包含美化代码的文件路径（txt）：")
        code_list = []
        try:
            with open(txt_file_path, 'r') as f:
                for line in f.readlines():
                    original_decimal, new_decimal = map(int, line.split())
                    code_list.append((original_decimal, new_decimal))
            process_batch(file_path, code_list)
        except ValueError:
            print("文件中的代码格式错误，请输入有效的整数。")
        except FileNotFoundError:
            print("文件未找到，请检查文件路径。")
    else:
        print("无效选项，请重新输入。")

    exit_choice = input("是否继续修改？（继续 Y/返回 n）")
    if exit_choice.lower() == 'n':
        break