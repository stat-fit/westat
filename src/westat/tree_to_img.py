def tree_to_img(file_name, path='', dtype='svg'):
    """
    转换决策树到图片

    Args:
        file_name: 决策树文件路径
        path: 目标图片的存放路径
        dtype: 图片格式

    Returns:
        决策树转换到图片的结果
    """
    # 修改字体为中文
    file_txt = ''
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('helvetica', 'SimHei')
            file_txt = file_txt + line

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(file_txt)

    # 转换决策树到图片
    if path:
        file_path = path
    else:
        file_path = os.path.splitext(file_name)[0] + '.' + dtype

    str_exec = 'dot -T' + dtype + ' ' + file_name + ' -o ' + file_path  # 决策树转图片命令
    print(str_exec)
    result = os.popen(str_exec)
    return result