import os
import pandas as pd
from sklearn import tree

from . import graphviz
from .tree_to_img import tree_to_img
from .tree_to_pdf import tree_to_pdf


def plot_tree(data: pd.DataFrame,
              out_file: str = None,
              criterion: str = 'gini',
              splitter: str = 'best',
              max_depth: int = 3,
              min_samples_split=50,
              min_samples_leaf=0.05,
              max_features=None,
              random_state=None,
              max_leaf_nodes=None,
              target='y',
              class_names=None,
              ):
    """
    根据给定的数据集，绘制决策树
    Args:
        data:目标数据集
        out_file:str,输出文件路径和名称
        criterion:衡量分组质量的标准，可选“gini”, “entropy”, “log_loss”
        splitter:str,sklearn拆分节点的方法
        max_depth: int,树的深度
        min_samples_split:int,拆分内部节点所需的最小样本数
        min_samples_leaf: float,叶子节点样本数量最小占比,默认为0.05
        max_features:寻找最佳分割时需要考虑的特征数量，int, float 或 {“auto”, “sqrt”, “log2”}
        random_state:随机种子,默认为None
        max_leaf_nodes: int,最大叶子节点数,默认为 4
        target:str,目标变量名称，默认为'y'
        class_names:str,分类
    Returns:

    """
    clf = tree.DecisionTreeClassifier(criterion=criterion,
                                      splitter=splitter,
                                      max_depth=max_depth,
                                      min_samples_split=min_samples_split,
                                      min_samples_leaf=min_samples_leaf,
                                      random_state=random_state,
                                      max_features=max_features,
                                      max_leaf_nodes=max_leaf_nodes,
                                      )
    col = [i for i in data.columns if i != target]
    x = data[col].values.reshape(-1, 1)
    y = data[target].values

    clf.fit(x, y)

    from westat.utils import current_path
    file_path = os.path.join(current_path, '../../plugins/win/Graphviz/bin')
    os.environ['WORK_HOME'] = file_path

    if out_file is None:
        dot_data = tree.export_graphviz(clf,
                                        out_file=None,
                                        feature_names=col,
                                        class_names=class_names,
                                        filled=True,
                                        rounded=True)
        graph = graphviz.Source(dot_data)
        return graph
    else:
        file_ext = os.path.splitext(out_file)[-1]  # 获取输出文件的扩展名

        # 随机生成一个临时的dot文件名
        import random
        random_name = random.randint(1, 99999)
        temp_dot = str(random_name) + '.dot'

        # 如果已经存在决策树临时文件，则需要先进行删除
        if os.path.exists(temp_dot):
            os.remove(temp_dot)

        # 生成决策树临时文件
        tree.export_graphviz(clf,
                             out_file=temp_dot,
                             feature_names=col,
                             class_names=class_names,
                             filled=True,
                             rounded=True)

        # 根据决策树临时文件，转换为目标文件格式
        if file_ext == '.pdf':
            tree_to_pdf(temp_dot, path=out_file)
        elif file_ext in ('.svg', '.png', '.jpg'):
            tree_to_img(temp_dot, path=out_file, dtype=file_ext[1:])
        else:
            print('{0} 包含不支持的文件格式'.format(out_file))

        # 如果已经生成文件，则删除临时决策树文件
        import time
        time.sleep(1)
        if os.path.exists(out_file):
            os.remove(temp_dot)

        return 0
