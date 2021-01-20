# NLP



## 预处理模型

- **word2vec(word to vector)**
  - 实现了低维条件下用稠密向量对词进行表示
  - 仅对词进行单个全局表示，提取浅层文本表征，无法在不同语境下对词的句法和语义特征进行有效表示
- **ELMO（Embeddings frmo Language Models)**
  - 采用双向长短期记忆网络（Long Short-Term Memory， LSTM）对语言模型实现了基于上下文的词嵌入表示，并显著提高了模型在下游任务的性能
- **BERT（Bidirectional Encoder Representations from Transfromers）**和**GPT（Generative PreTraining)**深层次预训练模型
  - Google在Transformer中引入的**注意力机制**是它们的基础



## 文本特征提取技术

- One-Hot编码对词进行符号化处理



### 词级表示

- 词级表示作为一种词的分布式表示方法，通过描述目标
  词与其邻近词之间的关系从而建立模型，从而包含更加丰富
  的语义信



#### N-Gram(N元模型)

- 用于评估一个句子的合理性
- 用于评估两个字符串的差异程度



精确匹配与模糊匹配

- 精确匹配
  - KMP、BM、BMH算法
- 模糊匹配
  - 用于衡量两个字符串之间的“差异”（距离）
  - 基于**编辑距离**的概念
  - Smith-Waterman算法和NeedleMan-Wunsch算法
  -  

