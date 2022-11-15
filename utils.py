import os
import sys

import torch
import torch.nn as nn
import math
import numpy as np
import pandas as pd
from gensim.models import Word2Vec

from gensim.models.word2vec import LineSentence as LS
from torch.ao.sparsity import scheduler
from torch.optim import lr_scheduler
from torch.utils.tensorboard import SummaryWriter
from torchtext.data import BucketIterator, Example, Dataset
from torchtext.vocab import Vectors
from torch.nn import init
import torch
from sklearn.model_selection import train_test_split
from tqdm.asyncio import tqdm

DEVICE = torch.device("cuda" if torch.cuda.is_available() else"cpu")
#torch.device("cuda" if torch.cuda.is_available() else"cpu")

list1 = ['train_merge1/本.txt', 'train_merge1/表面.txt', 'train_merge1/菜.txt', 'train_merge1/补.txt',
         'train_merge1/成立.txt', 'train_merge1/吃.txt', 'train_merge1/出.txt', 'train_merge1/带.txt', 'train_merge1/单位.txt',
         'train_merge1/道.txt',
         'train_merge1/动.txt', 'train_merge1/动摇.txt', 'train_merge1/队伍.txt', 'train_merge1/儿女.txt',
         'train_merge1/发.txt', 'train_merge1/赶.txt',
         'train_merge1/机组.txt', 'train_merge1/叫.txt', 'train_merge1/进.txt', 'train_merge1/镜头.txt',
         'train_merge1/开通.txt', 'train_merge1/看.txt',
         'train_merge1/面.txt', 'train_merge1/牌子.txt', 'train_merge1/平息.txt', 'train_merge1/旗帜.txt',
         'train_merge1/气息.txt', 'train_merge1/气象.txt',
         'train_merge1/日子.txt', 'train_merge1/使.txt', 'train_merge1/说明.txt', 'train_merge1/天地.txt',
         'train_merge1/挑.txt', 'train_merge1/推翻.txt',
         'train_merge1/望.txt', 'train_merge1/想.txt', 'train_merge1/眼光.txt', 'train_merge1/长城.txt',
         'train_merge1/震惊.txt', 'train_merge1/中医.txt']

list2 = ['train_data_csv/本.csv', 'train_data_csv/表面.csv', 'train_data_csv/菜.csv', 'train_data_csv/补.csv',
         'train_data_csv/成立.csv', 'train_data_csv/吃.csv',
         'train_data_csv/出.csv', 'train_data_csv/带.csv', 'train_data_csv/单位.csv', 'train_data_csv/道.csv',
         'train_data_csv/动.csv', 'train_data_csv/动摇.csv',
         'train_data_csv/队伍.csv', 'train_data_csv/儿女.csv', 'train_data_csv/发.csv', 'train_data_csv/赶.csv',
         'train_data_csv/机组.csv', 'train_data_csv/叫.csv',
         'train_data_csv/进.csv', 'train_data_csv/镜头.csv', 'train_data_csv/开通.csv', 'train_data_csv/看.csv',
         'train_data_csv/面.csv', 'train_data_csv/牌子.csv',
         'train_data_csv/平息.csv', 'train_data_csv/旗帜.csv', 'train_data_csv/气息.csv', 'train_data_csv/气象.csv',
         'train_data_csv/日子.csv',
         'train_data_csv/使.csv', 'train_data_csv/说明.csv', 'train_data_csv/天地.csv', 'train_data_csv/挑.csv',
         'train_data_csv/推翻.csv', 'train_data_csv/望.csv', 'train_data_csv/想.csv',
         'train_data_csv/眼光.csv', 'train_data_csv/长城.csv', 'train_data_csv/震惊.csv', 'train_data_csv/中医.csv']

list3 = ['test_merge1/本.txt', 'test_merge1/表面.txt', 'test_merge1/菜.txt', 'test_merge1/补.txt',
         'test_merge1/成立.txt', 'test_merge1/吃.txt', 'test_merge1/出.txt', 'test_merge1/带.txt', 'test_merge1/单位.txt',
         'test_merge1/道.txt',
         'test_merge1/动.txt', 'test_merge1/动摇.txt', 'test_merge1/队伍.txt', 'test_merge1/儿女.txt', 'test_merge1/发.txt',
         'test_merge1/赶.txt',
         'test_merge1/机组.txt', 'test_merge1/叫.txt', 'test_merge1/进.txt', 'test_merge1/镜头.txt', 'test_merge1/开通.txt',
         'test_merge1/看.txt',
         'test_merge1/面.txt', 'test_merge1/牌子.txt', 'test_merge1/平息.txt', 'test_merge1/旗帜.txt', 'test_merge1/气息.txt',
         'test_merge1/气象.txt',
         'test_merge1/日子.txt', 'test_merge1/使.txt', 'test_merge1/说明.txt', 'test_merge1/天地.txt', 'test_merge1/挑.txt',
         'test_merge1/推翻.txt',
         'test_merge1/望.txt', 'test_merge1/想.txt', 'test_merge1/眼光.txt', 'test_merge1/长城.txt', 'test_merge1/震惊.txt',
         'test_merge1/中医.txt']

list4 = ['test_data_csv/本.csv', 'test_data_csv/表面.csv', 'test_data_csv/菜.csv', 'test_data_csv/补.csv',
         'test_data_csv/成立.csv', 'test_data_csv/吃.csv',
         'test_data_csv/出.csv', 'test_data_csv/带.csv', 'test_data_csv/单位.csv', 'test_data_csv/道.csv',
         'test_data_csv/动.csv', 'test_data_csv/动摇.csv',
         'test_data_csv/队伍.csv', 'test_data_csv/儿女.csv', 'test_data_csv/发.csv', 'test_data_csv/赶.csv',
         'test_data_csv/机组.csv', 'test_data_csv/叫.csv',
         'test_data_csv/进.csv', 'test_data_csv/镜头.csv', 'test_data_csv/开通.csv', 'test_data_csv/看.csv',
         'test_data_csv/面.csv', 'test_data_csv/牌子.csv',
         'test_data_csv/平息.csv', 'test_data_csv/旗帜.csv', 'test_data_csv/气息.csv', 'test_data_csv/气象.csv',
         'test_data_csv/日子.csv',
         'test_data_csv/使.csv', 'test_data_csv/说明.csv', 'test_data_csv/天地.csv', 'test_data_csv/挑.csv',
         'test_data_csv/推翻.csv', 'test_data_csv/望.csv', 'test_data_csv/想.csv',
         'test_data_csv/眼光.csv', 'test_data_csv/长城.csv', 'test_data_csv/震惊.csv', 'test_data_csv/中医.csv']


def DATA_tokenize(text):
    return text.split(',')


def get_masks(src, pad_idx=1):
    src_mask = (src == pad_idx)
    return src_mask

def make_data(train_path, test_path, train_wordlist):
    train_lable_path = train_wordlist
    train_lable_path = train_lable_path[:train_lable_path.find('.')] + 'lable.txt'

    with open(train_lable_path, 'r', encoding='utf-8', errors='ignore') as p1:
        lables = '.'.join(p1.readlines()).split(',')
        target_batch = list(map(int, lables))
    target_batch = np.array(target_batch)
    num_classes = np.max(target_batch) + 1

    # 创建DATA字段的Field
    from torchtext import data
    DATA = data.Field(sequential=True, tokenize=DATA_tokenize, batch_first=True, fix_length=60)
    LABEL = data.Field(sequential=False, use_vocab=False)

    # 读取数据
    train_df = pd.read_csv(train_path, sep=',', encoding='utf8', names=['data', 'label'])
    test_df = pd.read_csv(test_path, sep=',', encoding='utf8', names=['data', 'label'])

    # 创建Field的list
    fields = [('data', DATA), ('label', LABEL)]
    examples = []
    test_examples = []

    for data, label in zip(train_df['data'], train_df['label']):
        examples.append(Example.fromlist([data, label], fields))
    for data, label in zip(test_df['data'], test_df['label']):
        test_examples.append(Example.fromlist([data, label], fields))

    # 创建数据集
    data_set = Dataset(examples, fields)
    test_data_set = Dataset(test_examples, fields)
    train_dataset, valid_dataset = data_set.split(0.7)

    #预训练词向量
    # with open(train_wordlist, 'r', encoding='utf-8', errors='ignore') as p1:
    #     sentences = LS(p1)
    #     model = Word2Vec(sentences, vector_size=256, window=4, min_count=1, negative=5, sample=0.001, workers=4,epochs=20)
    #     model.wv.save_word2vec_format('w2c3.txt')



    # 创建词典
    train_word_vectors = Vectors('./word2vec/w2c长城.txt')
    DATA.build_vocab(data_set,test_data_set, vectors=train_word_vectors)
    DATA.vocab.vectors.unk_init = init.xavier_uniform
    vocab_size = len(DATA.vocab)
    print(DATA.vocab.stoi)
    print(DATA.vocab.itos)
    print(vocab_size)

    # Iterator
    train_iter = BucketIterator(dataset=train_dataset, batch_size=16, shuffle=True, device=DEVICE)
    val_iter = BucketIterator(dataset=valid_dataset, batch_size=16,shuffle=True, device=DEVICE)
    test_iter = BucketIterator(dataset=test_data_set, batch_size=16, train=False, sort=False, device=DEVICE)

    return train_iter, val_iter, test_iter, num_classes, vocab_size , train_word_vectors.vectors

def train_one_epoch(model, optimizer, data_loader, device, epoch):
    model.train()
    loss_function = torch.nn.CrossEntropyLoss()
    mean_loss = torch.zeros(1).to(device)
    optimizer.zero_grad()

    data_loader = tqdm(data_loader, file=sys.stdout)

    for step, loader in enumerate(data_loader):
        data ,label= loader
        line ,labels = data
        mask = get_masks(line)
        pred = model(line,mask)
        loss = loss_function(pred, labels.to(device))
        loss.backward()
        mean_loss = (mean_loss * step + loss.detach()) / (step + 1)  # update mean losses

        data_loader.desc = "[epoch {}] mean loss {}".format(epoch, round(mean_loss.item(), 3))

        if not torch.isfinite(loss):
            print('WARNING: non-finite loss, ending training ', loss)
            sys.exit(1)

        optimizer.step()
        optimizer.zero_grad()

    return mean_loss.item()

@torch.no_grad()
def evaluate(model, data_loader, device):
    model.eval()

    # 验证样本总个数
    total_num = len(data_loader.dataset)

    # 用于存储预测正确的样本个数
    sum_num = torch.zeros(1).to(device)

    data_loader = tqdm(data_loader, file=sys.stdout)

    for step, loader in enumerate(data_loader):
        data, label = loader
        line, labels = data
        mask = get_masks(line)
        pred = model(line, mask)
        pred = torch.max(pred, dim=1)[1]
        sum_num += torch.eq(pred, labels.to(device)).sum()

    return sum_num.item() / total_num

if __name__ == '__main__':
    make_data('train_data_csv/长城.csv','test_data_csv/长城.csv','train_merge1/长城.txt')