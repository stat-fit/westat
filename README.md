

<h1 align="center" style="text-align:center;">
  <img src="./static/logo.png" width = "270" height = "90" alt="westat logo" align=center />
</h1>

<p align="center"> 金融行业信用评分卡模型开发工具  </p>

<p align="center" >
<a href="https://gitee.com/westat/westat"><img  src="https://gitee.com/westat/westat/raw/master/static/gitee.png" width = "25" height = "25"></a>
<a href="https://github.com/stat-fit/westat"><img  src="https://gitee.com/westat/westat/raw/master/static/github.png" width = "25" height = "25"></a>
<a href="https://pypi.org/project/westat/" ><img src="https://gitee.com/westat/westat/raw/master/static/pypi.png" width = "25" height = "25"></a>
<br>
</p>

<h3> 一、描述 </h3>

用于开发信用评分卡模型的python包，包含特征分箱、特征筛选、WOE和IV计算，KS值和AUC计算、模型提升度LIFT、模型稳定性 PSI 计算、决策树绘制、评分卡制作等功能
<br>另外，westat包含常用的金融计算函数，例如等额本息、等额本金等还款方式的计算。

westat基于python3.10进行开发，是开源数据分析处理项目<a href="http://pyminer.com/" >pyminer </a> 的一部分，但是也可以被单独使用。
westat 希望更多朋友能够参与项目，一起维护并提升！


<h3>二、交流</h3>
<ul>
<li>QQ群：945391275 </li>
<li>邮箱：westat@foxmail.com</li>
</ul>

<h3> 三、安装 </h3>

```bash
pip install westat
```

<h3> 四、开发 </h3>

```bash
# 创建环境
conda env create -f environment.yml
# 激活环境
conda activate westat-dev
# 构建
python -m build
# 上传到 pypi
python -m twine upload dist/*
```

<h3> 五、测试 </h3>

```bash
# 创建环境
conda env create -f environment.yml
# 激活环境
conda activate westat-dev
# 测试
jupyter-notebook
# 在jupyter上打开 HereWeGo.ipynb 进行测试
```

<h3> 六、常见操作 </h3>
<h4>查看版本号</h4>

```bash
import westat
westat.version
```

<h4>使用教程</h4>


请查看帮助文档 <a href="https://westat.readthedocs.io" >https://westat.readthedocs.io </a>
<br>


<h3> 决策树分箱 </h3>
<p></p>
<img src="https://gitee.com/westat/westat/raw/master/static/tree_iv.png"  alt="tree_iv" align=center />
<img src="https://gitee.com/westat/westat/raw/master/static/view_woe_iv.png"  alt="view_woe_iv" align=center />

<p></p>

<h3> 等频分箱 </h3>

<p></p>

<img src="https://gitee.com/westat/westat/raw/master/static/qcut_woe_iv.png"  alt="qcut_woe_iv" align=center />

<p></p>
<h3> 个性化分箱 </h3>

<p></p>

<img src="https://gitee.com/westat/westat/raw/master/static/cut_woe_iv.png"  alt="cut_woe_iv" align=center />

<h3> ks和auc计算 </h3>
<p></p>

<img src="https://gitee.com/westat/westat/raw/master/static/auc_ks.png"  alt="auc_ks" align=center />

<p></p>

<h3> ks绘图 </h3>
<p></p>

<img src="https://gitee.com/westat/westat/raw/master/static/plot_ks.png"  alt="plot_ks" align=center />

<p></p>
<h3> 模型提升度 Lift 计算 </h3>

<p></p>

<img src="https://gitee.com/westat/westat/raw/master/static/get_lift.png"  alt="get_lift" align=center />

<p></p>
<h3> 模型稳定度 PSI计算 </h3>
<p></p>

<img src="https://gitee.com/westat/westat/raw/master/static/get_psi.png"  alt="get_psi" align=center />

<p></p>

<h3> 评分卡制作 </h3>
<p></p>

<img src="https://gitee.com/westat/westat/raw/master/static/get_scorecard.png"  alt="get_scorecard" align=center />

<p></p>

<h3> 评分卡分数预测 </h3>
<p></p>

<img src="https://gitee.com/westat/westat/raw/master/static/predict_score.png"  alt="predict_score" align=center />

<p></p>