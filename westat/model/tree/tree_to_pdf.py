import os


def tree_to_pdf(file_name, path=''):
    """
    转换决策树到pdf文件

    Args:
        file_name: 决策树文件路径
        path: 目标pdf文件的存放路径

    Returns:
        决策树转换到pdf文件的结果
    """
    # 修改字体为中文
    file_txt = ''
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('helvetica', 'SimHei')
            file_txt = file_txt + line

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(file_txt)

    # 转换决策树到图片 pdf文件
    if path:
        file_path = path
    else:
        file_path = os.path.splitext(file_name)[0] + '.pdf'

    str_exec = 'dot -Tpdf ' + file_name + ' -o ' + file_path  # 决策树转pdf命令
    # print(str_exec)
    result = os.popen(str_exec)
    return result
