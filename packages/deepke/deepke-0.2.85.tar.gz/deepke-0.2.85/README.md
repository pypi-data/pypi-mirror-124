<p align="center">
    <a href="https://github.com/zjunlp/deepke"> <img src="pics/logo.png" width="400"/></a>
<p>
<p align="center">  
    <a href="https://deepke.openkg.cn">
        <img alt="Documentation" src="https://img.shields.io/badge/DeepKE-website-green">
    </a>
    <a href="https://pypi.org/project/deepke/#files">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/deepke">
    </a>
    <a href="https://github.com/zjunlp/DeepKE/blob/master/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/zjunlp/deepke">
    </a>
</p>
<p align="center">
    <b>简体中文 | <a href="https://github.com/zjunlp/DeepKE/blob/test_new_deepke/README_ENGLISH.md">English</a></b>
</p>

<h1 align="center">
    <p>基于深度学习的开源中文知识图谱抽取框架</p>
</h1>


DeepKE 是一个支持**低资源、长篇章**的知识抽取工具，可以基于pytorch实现命名实体识别、关系抽取和属性抽取功能。

<br>

## 在线演示

在线演示 [demo](https://deepke.openkg.cn)

### 进行预测
下面使用一个demo展示预测过程
<img src="pics/demo.gif" width="636" height="494" align=center>

<br>

## 模型架构

Deepke的架构图如下所示

<h3 align="center">
    <img src="pics/architectures.png">
</h3>

DeepKE包括了三个模块，可以进行关系抽取、实体命名识别以及属性抽取的任务，在各个模块下包括各自的子模块。其中关系抽取模块就有常规模块、文档级抽取模块以及低资源少样本模块。在每一个子模块中，分为分词、预处理等的一个工具集合，以及编码和训练预测部分。

<br>

## 快速上手

DeepKE支持pip安装使用，以常规全监督设定关系抽取为例

1、下载代码 ```git clone https://github.com/zjunlp/DeepKE.git```（别忘记star和fork哈！！！）

2、创建虚拟环境 ```conda create -n deepke python=3.8```

3、进入虚拟环境 ```conda activate deepke```

4、pip安装需要的依赖包，如果直接使用，```pip install deepke```；如需修改源码使用，首先```python setup.py install```,修改完后，```python setup.py develop```

5、进入使用位置 ```cd DeepKE/example/re/standard```

6、进行训练 ```python run.py```,训练用到的参数可在conf文件夹内修改

7、进行预测```python predict.py```,预测用到的参数可在conf文件夹内修改

### 环境依赖

> python == 3.8

- torch == 1.5
- hydra-core == 1.0.6
- tensorboard == 2.4.1
- matplotlib == 3.4.1
- transformers == 3.4.0
- jieba == 0.42.1
- scikit-learn == 0.24.1
- pytorch-transformers == 1.2.0
- seqeval == 1.2.2
- tqdm == 4.60.0
- opt-einsum==3.3.0
- ujson

1. **命名实体识别NER**

   数据为txt文件，样式范例为：
   |                           Sentence                           |           Person           |    Location    |          Organization          |
   | :----------------------------------------------------------: | :------------------------: | :------------: | :----------------------------: |
   | 本报北京9月4日讯记者杨涌报道：部分省区人民日报宣传发行工作座谈会9月3日在4日在京举行。 |            杨涌            |      北京      |            人民日报            |
   | 《红楼梦》是中央电视台和中国电视剧制作中心根据中国古典文学名著《红楼梦》摄制于1987年的一部古装连续剧，由王扶林导演，周汝昌、王蒙、周岭等多位红学家参与制作。 | 王扶林，周汝昌，王蒙，周岭 |      中国      | 中央电视台，中国电视剧制作中心 |
   | 秦始皇兵马俑位于陕西省西安市，1961年被国务院公布为第一批全国重点文物保护单位，是世界八大奇迹之一。 |           秦始皇           | 陕西省，西安市 |             国务院             |

   具体流程请进入详细的README中：

   **[常规全监督STANDARD](https://github.com/zjunlp/deepke/blob/test_new_deepke/example/ner/standard)** ：
    常规模块为预训练模型，可进入其目录，修改数据集以及conf文件夹下的目录，```python run.py```即可训练，```python predict.py```即可预测。

    **[少样本FEW-SHOT](https://github.com/zjunlp/DeepKE/tree/test_new_deepke/example/ner/few-shot)** ：
      少样本模块，可进入其目录，模型加载和保存位置以及配置可以在shell脚本中修改```python run.py```训练conll2003,```python run.py +train=few_shot```直接进行few-shot训练,若要加载模型，修改few_shot.yaml中的load_path,```python predict.py```即可预测。

2. **关系抽取RE**

   关系抽取是从非结构化的文本中抽取出实体之间的关系，以下为几个样式范例，数据为csv文件：

   |                        Sentence                        | Relation |    Head    | Head_offset |    Tail    | Tail_offset |
   | :----------------------------------------------------: | :------: | :--------: | :---------: | :--------: | :---------: |
   | 《岳父也是爹》是王军执导的电视剧，由马恩然、范明主演。 |   导演   | 岳父也是爹 |      1      |    王军    |      8      |
   |  《九玄珠》是在纵横中文网连载的一部小说，作者是龙马。  | 连载网站 |   九玄珠   |      1      | 纵横中文网 |      7      |
   |     提起杭州的美景，西湖总是第一个映入脑海的词语。     | 所在城市 |    西湖    |      8      |    杭州    |      2      |

   具体流程请进入详细的README中，RE包括了以下三个子功能

   **[常规全监督STANDARD](https://github.com/zjunlp/deepke/blob/test_new_deepke/example/re/standard)** ： 
   常规模块为常用的深度学习模型，有CNN、RNN、Capsule、GCN、Transforemer以及预训练模型，可进入其目录，修改数据集以及conf文件夹下的目录，```python run.py```即可训练，```python predict.py```即可预测。

   **[少样本FEW-SHOT](https://github.com/zjunlp/deepke/blob/test_new_deepke/example/re/few-shot)** :
   进入其目录，修改数据集以及conf文件夹下的目录，```python run.py```即可训练，如需从上次训练的模型开始训练：设置.yaml中的train_from_saved_model为上次保存模型的路径，每次训练的日志保存路径默认保存在根目录，可以通过.yaml中的log_dir来配置```python predict.py```即可预测。

   **[文档级DOCUMENT](https://github.com/zjunlp/deepke/blob/test_new_deepke/example/re/document)** :
   ```train_distant.json```由于文件太大，请自行从Google Drive上下载到data/目录下.进入其目录，修改数据集以及conf文件夹下的目录，```python run.py```即可训练，如需从上次训练的模型开始训练：设置.yaml中的train_from_saved_model为上次保存模型的路径，每次训练的日志保存路径默认保存在根目录，可以通过.yaml中的log_dir来配置```python predict.py```即可预测。

3. **属性抽取AE**

   数据为csv文件，样式范例为：

   |                           Sentence                           |   Att    |   Ent    | Ent_offset |      Val      | Val_offset |
   | :----------------------------------------------------------: | :------: | :------: | :--------: | :-----------: | :--------: |
   |          张冬梅，女，汉族，1968年2月生，河南淇县人           |   民族   |  张冬梅  |     0      |     汉族      |     6      |
   | 杨缨，字绵公，号钓溪，松溪县人，祖籍将乐，是北宋理学家杨时的七世孙 |   朝代   |   杨缨   |     0      |     北宋      |     22     |
   |        2014年10月1日许鞍华执导的电影《黄金时代》上映         | 上映时间 | 黄金时代 |     19     | 2014年10月1日 |     0      |

   具体流程请进入详细的README中:

   **[常规全监督STANDARD](https://github.com/zjunlp/deepke/blob/test_new_deepke/example/ae/standard)** ：
    常规模块为常用的深度学习模型，有CNN、RNN、Capsule、GCN、Transforemer以及预训练模型，可进入其目录，修改数据集以及conf文件夹下的目录，```python run.py```即可训练，```python predict.py```即可预测。

<br>

## 备注（常见问题）
1. 使用 Anaconda 时，建议添加国内镜像，下载速度更快。如[清华镜像](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)。

1. 使用 pip 时，建议使用国内镜像，下载速度更快，如阿里云镜像。

1. 安装后提示 `ModuleNotFoundError: No module named 'past'`，输入命令 `pip install future` 即可解决。

1. 使用语言预训练模型时，在线安装下载模型比较慢，更建议提前下载好，存放到 pretrained 文件夹内。具体存放文件要求见文件夹内的 readme.md。

<br>

## 项目成员

张宁豫、陶联宽、余海洋、陈想、田玺、李磊、黎洲波、徐欣、邓淑敏、姚云志、叶宏彬、谢辛、郑国轴、陈华钧等

