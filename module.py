import torch.nn as nn
import math
import torch
import matplotlib.pyplot as plt

class Config(object):

    def __init__(self):
        self.max_len = 60  # pad后的统一长度
        self.embedding_size = 256  # 字向量维度
        self.vocab_size = 0
        self.device = torch.device('cpu')  # 设备
        self.num_epochs = 90  # epoch数
        self.batch_size = 8  # mini-batch大小
        self.learning_rate = 0.0001  # 学习率
        self.n_heads = 4

        self.filter_sizes = (2, 3, 4)  # 卷积核尺寸
        self.cnn_conf_list = [(3, 1), (3, 2), (3, 4), (3, 1)]  # 卷积核数量(channels数)

        self.max_size = 10000
        self.min_freq = 1
        self.dtype = torch.FloatTensor
        self.device = torch.device("cpu")

        self.padding_index = 0
        self.keep_dropout = 0.1

        self.out_channels = 3
        self.k_size = 3
        self.l2_reg_lambda = 0.0001
        self.dilation_rate = 3
        self.dropout = 0.1

        self.num_classes = 0
        self.word_size = 0
        self.padding_idx = 1




class GluLayer(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        # 第一个线性层
        self.fc1 = nn.Linear(input_size, output_size)
        # 第二个线性层
        self.fc2 = nn.Linear(input_size, output_size)
        # pytorch的GLU层
        self.glu = nn.GLU()

    def forward(self, x):
        # 先计算第一个线性层结果
        a = self.fc1(x)
        # 再计算第二个线性层结果
        b = self.fc2(x)
        # 拼接a和b，水平扩展的方式拼接
        # 然后把拼接的结果传给glu
        return self.glu(torch.cat((a, b), dim=2))

class PositionalEncoding(nn.Module):
    def __init__(self, config, dropout=0.1):
        super(PositionalEncoding, self).__init__()

        ## 位置编码的实现其实很简单，直接对照着公式去敲代码就可以，下面这个代码只是其中一种实现方式；
        ## 从理解来讲，需要注意的就是偶数和奇数在公式上有一个共同部分，我们使用log函数把次方拿下来，方便计算；
        ## pos代表的是单词在句子中的索引，这点需要注意；比如max_len是128个，那么索引就是从0，1，2，...,127
        ##假设我的demodel是512，2i那个符号中i从0取到了255，那么2i对应取值就是0,2,4...510
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(config.max_len, config.embedding_size)
        position = torch.arange(0, config.max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, config.embedding_size, 2).float() * (-math.log(10000.0) / config.embedding_size))
        pe[:, 0::2] = torch.sin(position * div_term)## 这里需要注意的是pe[:, 0::2]这个用法，就是从0开始到最后面，补长为2，其实代表的就是偶数位置
        pe[:, 1::2] = torch.cos(position * div_term)##这里需要注意的是pe[:, 1::2]这个用法，就是从1开始到最后面，补长为2，其实代表的就是奇数位置
        ## 上面代码获取之后得到的pe:[max_len*d_model]

        ## 下面这个代码之后，我们得到的pe形状是：[max_len*1*d_model]
        pe = pe.unsqueeze(0).transpose(0, 1)

        self.register_buffer('pe', pe)  ## 定一个缓冲区，其实简单理解为这个参数不更新就可以

    def forward(self, x):
        """
        x: [seq_len, batch_size, d_model]
        """

        x = x + self.pe[:x.size(0), :]

        return self.dropout(x)


class DGCNNLayer(nn.Module):

    def __init__(self, in_channels, out_channels, k_size=3, dilation_rate=2 , dropout=0.1):
        super(DGCNNLayer, self).__init__()
        self.k_size = k_size
        self.dilation_rate = dilation_rate
        self.pad_size = int(self.dilation_rate * (self.k_size - 1) / 2)
        # print(self.k_size)
        # print(self.dilation_rate)
        self.dropout_layer = nn.Dropout(dropout)
        # self.liner_layer = nn.Linear(int(out_channels / 2), out_channels)
        self.glu_layer = nn.GLU()
        self.relu_layer = nn.ReLU()
        self.conv_layer = nn.Conv1d(in_channels, out_channels * 2, kernel_size=k_size, dilation=dilation_rate,
                                    padding=(self.pad_size,))
        self.layer_normal = nn.LayerNorm(in_channels)
        self.init_parameters()


    def init_parameters(self):
        for m in self.modules():
            if isinstance(m, nn.Conv1d):
                nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        '''

        :param x: shape: [batch_size, seq_length, channels(embeddings)]
        :return:
        '''
        x = x.permute(0, 2, 1)
        x = self.conv_layer(x)
        #plt.hist(self.conv_layer.weight.data.numpy().reshape(-1, 1), bins=30)
        #plt.show()
        x = self.relu_layer(x)
        x = x.permute(0, 2, 1)
        x = self.glu_layer(x)

        return self.layer_normal(x)


class TextDGCNN(nn.Module):

    def __init__(self, config):
        super(TextDGCNN, self).__init__()

        self.word_embedding = nn.Embedding(config.vocab_size, config.embedding_size, config.padding_idx)
        self.word_position_embedding = PositionalEncoding(config)
        # 膨胀卷积列表
        self.dgcnn_list = DGCNNLayer(config.embedding_size, config.embedding_size, dropout=config.keep_dropout)

        # 自注意力层
        self.attention = nn.MultiheadAttention(embed_dim=config.embedding_size, num_heads=8,
                                               dropout=0,
                                               batch_first=True)
        # 全连接层
        self.GAP_layer = nn.AdaptiveAvgPool1d(config.num_classes)
        self.relu_layer = nn.ReLU()


    def forward(self, x, mask):
        word_inputs = self.word_embedding(x)
        #word_position_inputs = self.word_position_embedding(word_inputs.transpose(0, 1)).transpose(0, 1)
        dgcnn_output = self.dgcnn_list(word_inputs)
        attn_output, attn_output_weights = self.attention(query=dgcnn_output, key=dgcnn_output, value=dgcnn_output,
                                                          key_padding_mask=mask)
        x = attn_output
        batch_size = x.size(0)
        x = x.reshape(batch_size, -1)
        x = self.GAP_layer(x)

        return x
