import re
import os
import pandas as pd
word_semantic = ''
qiyi_word = ''
UNK, PAD = '<UNK>', '<PAD>'


# 1.去除所有符号
def remove_symbol(list1, list2):
    s = 0
    for i in range(0, 40):
        path1 = list1[i]
        path2 = list2[i]
        if (os.path.exists(path2) == False):
            os.makedirs(path2)
        for file_path in os.listdir(path1):
            read_path = path1 + '/%s'
            write_path = path2 + '/%s.txt'
            with open(read_path % (file_path), mode='r+', encoding='utf-8', errors='igore') as p1:
                lines = p1.readlines()
                for line in lines:
                    symbol = '[《》∶②③‘“’”！，。?？『』「」［］〔〕＜＞·%％：；{}*-+~@#￥%……&（）／=【】、|.．]'  # 中文标点
                    line = re.sub('([《》∶② ③‘’“”！，。?？『』「」［］〔〕＜＞·：；{}*-+~@#￥……&（）=【】、|．]/[a-zA-Z]+)', '', line)
                    line = re.sub('([%％.Ｍ０２３４５７６１８９0-9a-zA-Z]+/[a-zA-Z]+)', '', line)
                    # line=re.sub('([《》∶② ③‘’“”！，。?？『』「」［］〔〕＜＞·%％ ：；{}*-+~@#￥%……&（）=【】、|.．Ｍ０２３４５７６１８９0-9a-zA-Z]/[a-zA-Z]+)','',line)
                    line = re.sub(symbol, '', line)
                    line = re.sub('[Ｍ０２３４５７６１８９0-9]', '', line)
                    line = line.replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ')
                    line = line.lstrip()
                    text = re.split('\n', line)
                    # print(list(text))
                    text = text[0]
                    # print(text)
                    te1 = re.split(' ', text)
                    te2 = te1[:-1]
                    t1 = text.split()
                    text1 = re.sub('[A-Z a-z]', '', text)
                    # print(text1)
                    text1 = text1.replace('/', ' ')
                    text1 = text1.split()
                    # print(len(text1))

                    """text1 为分离词性后的元素，便于在语义库里寻找位子，且下标跟着长度走动"""
                    # for j in t1:
                    #     pass
                    # for j in t1:
                    with open(write_path % (file_path[:file_path.find('.txt')]), "a+", encoding="utf-8",
                              errors='ignore') as P3:
                        for b in te2:
                            a = b.replace('/', ' ')
                            c = a.split(' ')
                            WE1 = c[0] + '/' + c[1] + '/' + '-1' + ' '
                            file = open('./语义表/语义词典.txt', "r", encoding="utf-8")
                            yuyis = file.readlines()

                            for yuyi in yuyis:
                                yuyi = yuyi.replace('\n', '')
                                yuyi = yuyi.split(',')

                                if c[0] == yuyi[0]:
                                    WE = c[0] + '/' + c[1] + '/' + yuyi[1] + ' '
                                    P3.write(WE)
                            if WE.split('/')[0] != c[0]:
                                P3.write(WE1)
                        P3.write('\n')
        s = s + 1
        print('success' + str(s))
    print('end')


# 2.生成语义词典 多词义下，只保留最后一个
def generate_semantic_dictionary():
    read_path = './语义表/语义类型'
    write_path = './语义表/语义词典'
    i = 0
    with open(read_path, "r", encoding="utf-8", errors='ignore') as p1:
        lines = p1.readlines()
        # lines:['#Ｂ超/－网_－波(Bb06)\n'....................................'#鼾睡/醒_入睡_失眠(Ib04)\n']
        print(lines)
        for line in lines:
            # line : #交换机/器具_设备(Ba05) 机器_工具_泵(Bo01)

            # 交换价值/价值_价格(Dj02)

            line = re.split('\n', line)
            # line:['#Ｂ超/－网_－波(Bb06)', '']

            line = line[0]
            line = re.sub('[#]', '', line)
            line = re.sub('[/()]', ' ', line)
            line = line.split()
            # line :['Ｂ超', '－网_－波', 'Bb06']

            cut_line = str(line[-1:]).replace('[', '').replace("'", '').replace(']', '')
            # cut_line:Bb06

            final_line = line[0] + ',' + cut_line
            # final_line:Ｂ超,Bb06

            with open(write_path, "a+", encoding="utf-8", errors='ignore') as p2:
                p2.write(final_line + '\n')
            i = i + 1
            print('success' + str(i))
    print('end')


# 3.添加语义类别
def add_semantic_category(list1, list2):
    global word_semantic
    s = 0
    for i in range(0, 40):
        path1 = list1[i]
        path2 = list2[i]
        semantic_dictionary_path = './语义表/语义词典.txt'
        if (os.path.exists(path2) == False):
            os.makedirs(path2)
        for file_path in os.listdir(path1):
            read_path = path1 + '/%s'
            write_path = path2 + '/%s.txt'
            with open(read_path % (file_path), mode='r+', encoding='utf-8', errors='igore') as p1:
                lines = p1.readlines()
                print(read_path)
                # lines: ['同/d 为/v 郑/nr 先生/n 所/u 编/v 的/u 插图/n 本/n 中国/ns 文学史/n 图文/n 兼备/v 更为/d 读者/ap 欢迎/v 但/c 只/d 限于/v 文学史/n 方面/n \n', '近年/t 很多/m 人/n 想到/v 要/v 编著/v 较/d 大/a 规模/n 的/u 插图/n 本/n 中国/ns 通史/n 并且/c 做/v 了/u 若干/m 尝试/vn \n'....]
                for line in lines:
                    line = line.split('\n')
                    # line: ['同/d 为/v 郑/nr 先生/n 所/u 编/v 的/u 插图/n 本/n 中国/ns 文学史/n 图文/n 兼备/v 更为/d 读者/ap 欢迎/v 但/c 只/d 限于/v 文学史/n 方面/n ', '']

                    line = line[0]
                    line = re.split(' ', line)
                    # line : ['同/d', '为/v', '郑/nr', '先生/n', '所/u', '编/v', '的/u', '插图/n', '本/n', '中国/ns', '文学史/n', '图文/n', '兼备/v', '更为/d', '读者/ap', '欢迎/v', '但/c', '只/d', '限于/v', '文学史/n', '方面/n', '']

                    line = line[:-1]
                    # line : ['同/d', '为/v', '郑/nr', '先生/n', '所/u', '编/v', '的/u', '插图/n', '本/n', '中国/ns', '文学史/n', '图文/n', '兼备/v', '更为/d', '读者/ap', '欢迎/v', '但/c', '只/d', '限于/v', '文学史/n', '方面/n']

                    with open(write_path % (file_path[:file_path.find('.')]), "a+", encoding="utf-8",
                              errors='ignore') as p2:
                        for single_word in line:
                            # single_word:同/d

                            single_word_list = single_word.replace('/', ' ')
                            # single_word_list:同 d

                            single_word_list = single_word_list.split()
                            # sing_word_list:['同', 'd']
                            print(single_word_list)

                            mismatch_word_semantic = single_word_list[0] + '/' + single_word_list[1] + '/' + '-1' + ' '
                            # mismatch_word_semantic:同/d/-1

                            file = open(semantic_dictionary_path, "r", encoding="utf-8")
                            semantic_line = file.readlines()
                            # semantic_line:['滋事,Hj57\n'...]

                            for semantic in semantic_line:
                                semantic = semantic.replace('\n', '')
                                # semantic:滋事,Hj57

                                semantic = semantic.split(',')
                                # semantic['滋事','Hj57']

                                if single_word_list[0] == semantic[0]:
                                    word_semantic = single_word_list[0] + '/' + single_word_list[1] + '/' + semantic[
                                        1] + ' '
                                    p2.write(word_semantic)
                            if word_semantic.split('/')[0] != single_word_list[0]:
                                p2.write(mismatch_word_semantic)
                        p2.write('\n')
                        print('ssss')
        s = s + 1
        print('success' + str(s))
    print('end')


def qiyici(list1, list2):
    global qiyi_word
    ln = 0
    for i in range(0, 40):
        path1 = list1[i]
        path2 = list2[i]
        path3 = list3[i]
        if (os.path.exists(path3) == False):
            os.makedirs(path3)
        qiyi_word = str(path1.split('/')[-1:]).replace('[', '').replace("'", '').replace(']', '')
        # print(qiyi_word)
        for file_path in os.listdir(path1):
            qiyi_path = path1 + '/%s.txt'
            # read_path = path2 + '/%s'
            wtire_path = path3 + '/%s.txt'
            with open(qiyi_path % (file_path[:file_path.find('.txt')]), "r", encoding="utf-8", errors='ignore') as p2:
                lines = p2.readlines()
                # print(lines)
                for line in lines:

                    line = line.replace('\n', '').split(' ')
                    line = line[:-1]
                    # line:['同/d/Jb01', '为/v/Ih01', '郑/nr/Dd15', '先生/n/Al01', '所/u/Di09', '编/v/Hg17', '的/u/Bo29', '插图/n/Dk31', '本/n/Ed61', '中国/ns/Di02', '文学史/n/-1', '图文/n/-1', '兼备/v/Jd04', '更为/d/Ka04', '读者/ap/Aa01', '欢迎/v/Hi05', '但/c/Kc03', '只/d/Dn08', '限于/v/Dd13', '文学史/n/-1', '方面/n/Cb01']
                    # print(line)

                    # 列表解析，枚举line，把存在歧义词的索引i放入index列表中
                    index = [i for i, v in enumerate(line) if v.startswith("%s" % (qiyi_word + "/"))]  # enumerate 枚举函数
                    # index:[8]
                    # print(index)
                    list4 = []
                    n = len(line)
                    # print(n)
                    if len(index):
                        for idx in index:  # 将每一个带有歧义词的位置通过for从列表index中给遍历出来，返回idx
                            list4 = []
                            # idx:8
                            if idx == 0:
                                try:

                                    strR1 = line[idx + 1]
                                    list4.append(','.join(re.split('/', strR1)))

                                    strR2 = line[idx + 2]
                                    list4.append(','.join(re.split('/', strR2)))

                                    strR3 = line[idx + 3]
                                    list4.append(','.join(re.split('/', strR3)))

                                    strR4 = line[idx + 4]
                                    list4.append(','.join(re.split('/', strR4)))

                                except IndexError:
                                    pass
                            elif idx == 1:
                                try:

                                    strL1 = line[idx - 1]
                                    list4.append(','.join(re.split('/', strL1)))

                                    strR1 = line[idx + 1]
                                    list4.append(','.join(re.split('/', strR1)))

                                    strR2 = line[idx + 2]
                                    list4.append(','.join(re.split('/', strR2)))

                                    strR3 = line[idx + 3]
                                    list4.append(','.join(re.split('/', strR3)))

                                    strR4 = line[idx + 4]
                                    list4.append(','.join(re.split('/', strR4)))

                                except IndexError:
                                    pass
                            elif idx == 2:
                                try:

                                    strL1 = line[idx - 2]
                                    list4.append(','.join(re.split('/', strL1)))

                                    strL2 = line[idx - 1]
                                    list4.append(','.join(re.split('/', strL2)))

                                    strR1 = line[idx + 1]
                                    list4.append(','.join(re.split('/', strR1)))

                                    strR2 = line[idx + 2]
                                    list4.append(','.join(re.split('/', strR2)))

                                    strR3 = line[idx + 3]
                                    list4.append(','.join(re.split('/', strR3)))

                                    strR4 = line[idx + 4]
                                    list4.append(','.join(re.split('/', strR4)))

                                except IndexError:
                                    pass

                            elif idx == 3:
                                try:

                                    strL1 = line[idx - 3]
                                    list4.append(','.join(re.split('/', strL1)))

                                    strL2 = line[idx - 2]
                                    list4.append(','.join(re.split('/', strL2)))

                                    strL3 = line[idx - 1]
                                    list4.append(','.join(re.split('/', strL3)))

                                    strR1 = line[idx + 1]
                                    list4.append(','.join(re.split('/', strR1)))

                                    strR2 = line[idx + 2]
                                    list4.append(','.join(re.split('/', strR2)))

                                    strR3 = line[idx + 3]
                                    list4.append(','.join(re.split('/', strR3)))

                                    strR4 = line[idx + 4]
                                    list4.append(','.join(re.split('/', strR4)))

                                except IndexError:
                                    pass

                            elif idx == n - 1:
                                try:
                                    strL1 = line[idx - 4]
                                    list4.append(','.join(re.split('/', strL1)))

                                    strL2 = line[idx - 3]
                                    list4.append(','.join(re.split('/', strL2)))

                                    strL3 = line[idx - 2]
                                    list4.append(','.join(re.split('/', strL3)))

                                    strL4 = line[idx - 1]
                                    list4.append(','.join(re.split('/', strL4)))

                                except IndexError:
                                    pass
                            elif idx == n - 2:
                                try:
                                    strL1 = line[idx - 4]
                                    list4.append(','.join(re.split('/', strL1)))

                                    strL2 = line[idx - 3]
                                    list4.append(','.join(re.split('/', strL2)))

                                    strL3 = line[idx - 2]
                                    list4.append(','.join(re.split('/', strL3)))

                                    strL4 = line[idx - 1]
                                    list4.append(','.join(re.split('/', strL4)))

                                    strR1 = line[idx + 1]
                                    list4.append(','.join(re.split('/', strR1)))

                                except IndexError:
                                    pass

                            elif idx == n - 3:
                                try:
                                    strL1 = line[idx - 4]
                                    list4.append(','.join(re.split('/', strL1)))

                                    strL2 = line[idx - 3]
                                    list4.append(','.join(re.split('/', strL2)))

                                    strL3 = line[idx - 2]
                                    list4.append(','.join(re.split('/', strL3)))

                                    strL4 = line[idx - 1]
                                    list4.append(','.join(re.split('/', strL4)))

                                    strR1 = line[idx + 1]
                                    list4.append(','.join(re.split('/', strR1)))

                                    strR2 = line[idx + 2]
                                    list4.append(','.join(re.split('/', strR2)))

                                except IndexError:
                                    pass

                            elif idx == n - 4:
                                try:
                                    strL1 = line[idx - 4]
                                    list4.append(','.join(re.split('/', strL1)))

                                    strL2 = line[idx - 3]
                                    list4.append(','.join(re.split('/', strL2)))

                                    strL3 = line[idx - 2]
                                    list4.append(','.join(re.split('/', strL3)))

                                    strL4 = line[idx - 1]
                                    list4.append(','.join(re.split('/', strL4)))

                                    strR1 = line[idx + 1]
                                    list4.append(','.join(re.split('/', strR1)))

                                    strR2 = line[idx + 2]
                                    list4.append(','.join(re.split('/', strR2)))

                                    strR3 = line[idx + 3]
                                    list4.append(','.join(re.split('/', strR3)))

                                except IndexError:
                                    pass

                            else:
                                try:
                                    strL1 = line[idx - 4]
                                    list4.append(','.join(re.split('/', strL1)))

                                    strL2 = line[idx - 3]
                                    list4.append(','.join(re.split('/', strL2)))

                                    strL3 = line[idx - 2]
                                    list4.append(','.join(re.split('/', strL3)))

                                    strL4 = line[idx - 1]
                                    list4.append(','.join(re.split('/', strL4)))

                                    strR1 = line[idx + 1]
                                    list4.append(','.join(re.split('/', strR1)))

                                    strR2 = line[idx + 2]
                                    list4.append(','.join(re.split('/', strR2)))

                                    strR3 = line[idx + 3]
                                    list4.append(','.join(re.split('/', strR3)))

                                    strR4 = line[idx + 4]
                                    list4.append(','.join(re.split('/', strR4)))
                                except IndexError:
                                    pass
                            line1 = ','.join(list4)

                            with open(wtire_path % (file_path[:file_path.find('.txt')]), "a+", encoding="utf-8",
                                      errors='ignore') as P3:

                                P3.write(line1 + '\n')
                    else:
                        continue


# 6.添加标签
def add_label(list1, list2):
    for i in range(0, 40):
        path1 = list1[i]
        path2 = list2[i]
        j = 0
        if (os.path.exists(path2) == False):
            os.makedirs(path2)
        for file_path in os.listdir(path1):
            read_path = path1 + '/%s'
            write_path = path2 + '/%s.txt'
            # print(file_path)
            with open(read_path % (file_path), 'r', encoding='utf-8', errors='igore') as p1:
                lines = p1.readlines()
                for line in lines:
                    line = line.replace('\n', '')
                    with open(write_path % (file_path[:file_path.find('.txt')]), "a+", encoding="utf-8",
                              errors='ignore') as P2:
                        P2.write(line + ',' + str(j) + '\n')
                j = j + 1


# 6.5 合并文件
def merge(list1, list2):
    path = list2[0]
    path = path[:path.find('/本')]
    if (os.path.exists(path) == False):
        os.makedirs(path)
    for i in range(0, 40):
        path1 = list1[i]
        path2 = list2[i]
        for file_path in os.listdir(path1):
            read_path = path1 + '/%s'
            write_path = path2
            P1 = open(read_path % (file_path), "r",encoding='utf-8', errors='ignore')
            lines = P1.readlines()
            for line in lines:
                with open(write_path, "a+", encoding="utf-8", errors='ignore') as p1:
                    p1.write(line)

def divid_lable(list1, list2):
    path1 = list2[0]
    path1 = path1[:path1.find('/本')]
    len_list = []
    if (os.path.exists(path1) == False):
        os.makedirs(path1)
    for i in range(0, 40):
        read_path = list1[i]
        write_path = list2[i]
        # print(write_path)
        write_label_path = write_path[:write_path.find('.')] + 'lable.txt'
        label_list = []
        with open(read_path, 'r', encoding='utf-8', errors='ignore') as p1:
            lines = p1.readlines()
            # print(lines)
            for line in lines:
                list3 = line.rstrip('\n').split(',')
                # print(list2)
                len_list3 = len(list3)
                # print(len_list2)
                label_list.append(list3[len_list3 - 1])
                # print(label_list)
                # print(len(label_list))
                data = ' '.join(line.split(',')[:-1])
                # line = line.split(',')
                # len_line = len(line)
                # len_list.append(len_line)
                # a=max(len_list)
                # print(len_list)
                # ['继续', 'v', 'Ig03', '深化', 'v', 'Ih10', '医疗', 'n', 'Hg20', '机构', 'n', 'Di09']
                # print(data)
                with open(write_path, 'a+', encoding='utf-8') as p2:
                    p2.write(data)
                    p2.write('\n')
                p1.close()
            with open(write_label_path, 'a+', encoding='utf-8') as p3:
                p3.write(','.join(label_list))

def make_csv(list1,list2):
    path1 = list2[0]
    path1 = path1[:path1.find('/本')]
    if (os.path.exists(path1) == False):
        os.makedirs(path1)
    for i in range(0, 40):
        list_data = []
        list_label = []
        read_path = list1[i]
        write_path = list2[i]
        with open(read_path, 'r', encoding='utf-8', errors='ignore') as p1:
            lines = p1.read().splitlines()
            for line in lines:
                data_list = line.split(',')
                data = ','.join(data_list[:-1])
                label = ','.join(data_list[len(data_list)-1])
                list_data.append(data)
                list_label.append(label)
            dataframe = pd.DataFrame({'data':list_data,'label':list_label})
            dataframe.to_csv(write_path,index=False,header=False)
    print('success')



list1 = ['./测试语料/本', './测试语料/表面', './测试语料/菜', './测试语料/补', './测试语料/成立', './测试语料/吃',
         './测试语料/出', './测试语料/带', './测试语料/单位', './测试语料/道', './测试语料/动', './测试语料/动摇',
         './测试语料/队伍', './测试语料/儿女', './测试语料/发', './测试语料/赶', './测试语料/机组', './测试语料/叫',
         './测试语料/进', './测试语料/镜头',
         './测试语料/开通', './测试语料/看', './测试语料/面', './测试语料/牌子',
         './测试语料/平息', './测试语料/旗帜', './测试语料/气息', './测试语料/气象', './测试语料/日子', './测试语料/使',
         './测试语料/说明', './测试语料/天地', './测试语料/挑', './测试语料/推翻', './测试语料/望', './测试语料/想',
         './测试语料/眼光', './测试语料/长城', './测试语料/震惊', './测试语料/中医']

list2 = ['./test_remove_symbol/本', './test_remove_symbol/表面', './test_remove_symbol/菜', './test_remove_symbol/补',
         './test_remove_symbol/成立', './test_remove_symbol/吃',
         './test_remove_symbol/出', './test_remove_symbol/带', './test_remove_symbol/单位', './test_remove_symbol/道',
         './test_remove_symbol/动', './test_remove_symbol/动摇',
         './test_remove_symbol/队伍', './test_remove_symbol/儿女', './test_remove_symbol/发', './test_remove_symbol/赶',
         './test_remove_symbol/机组', './test_remove_symbol/叫',
         './test_remove_symbol/进', './test_remove_symbol/镜头',
         './test_remove_symbol/开通', './test_remove_symbol/看', './test_remove_symbol/面', './test_remove_symbol/牌子',
         './test_remove_symbol/平息', './test_remove_symbol/旗帜', './test_remove_symbol/气息', './test_remove_symbol/气象',
         './test_remove_symbol/日子', './test_remove_symbol/使',
         './test_remove_symbol/说明', './test_remove_symbol/天地', './test_remove_symbol/挑', './test_remove_symbol/推翻',
         './test_remove_symbol/望', './test_remove_symbol/想',
         './test_remove_symbol/眼光', './test_remove_symbol/长城', './test_remove_symbol/震惊', './test_remove_symbol/中医']

list3 = ['./test_qiyi/本', './test_qiyi/表面', './test_qiyi/菜', './test_qiyi/补',
         './test_qiyi/成立', './test_qiyi/吃', './test_qiyi/出', './test_qiyi/带',
         './test_qiyi/单位', './test_qiyi/道', './test_qiyi/动', './test_qiyi/动摇',
         './test_qiyi/队伍', './test_qiyi/儿女', './test_qiyi/发',
         './test_qiyi/赶', './test_qiyi/机组', './test_qiyi/叫', './test_qiyi/进',
         './test_qiyi/镜头', './test_qiyi/开通',
         './test_qiyi/看', './test_qiyi/面', './test_qiyi/牌子', './test_qiyi/平息',
         './test_qiyi/旗帜', './test_qiyi/气息',
         './test_qiyi/气象', './test_qiyi/日子', './test_qiyi/使', './test_qiyi/说明',
         './test_qiyi/天地', './test_qiyi/挑',
         './test_qiyi/推翻', './test_qiyi/望', './test_qiyi/想', './test_qiyi/眼光',
         './test_qiyi/长城', './test_qiyi/震惊', './test_qiyi/中医']
list4 = ['./test_addLable/本', './test_addLable/表面', './test_addLable/菜', './test_addLable/补', './test_addLable/成立',
         './test_addLable/吃',
         './test_addLable/出', './test_addLable/带', './test_addLable/单位', './test_addLable/道', './test_addLable/动',
         './test_addLable/动摇',
         './test_addLable/队伍', './test_addLable/儿女', './test_addLable/发', './test_addLable/赶', './test_addLable/机组',
         './test_addLable/叫',
         './test_addLable/进', './test_addLable/镜头',
         './test_addLable/开通', './test_addLable/看', './test_addLable/面', './test_addLable/牌子',
         './test_addLable/平息', './test_addLable/旗帜', './test_addLable/气息', './test_addLable/气象', './test_addLable/日子',
         './test_addLable/使',
         './test_addLable/说明', './test_addLable/天地', './test_addLable/挑', './test_addLable/推翻', './test_addLable/望',
         './test_addLable/想',
         './test_addLable/眼光', './test_addLable/长城', './test_addLable/震惊', './test_addLable/中医']

list5 = ['test_merge/本.txt', 'test_merge/表面.txt', 'test_merge/菜.txt', 'test_merge/补.txt',
         'test_merge/成立.txt',
         'test_merge/吃.txt',
         'test_merge/出.txt', 'test_merge/带.txt', 'test_merge/单位.txt', 'test_merge/道.txt',
         'test_merge/动.txt',
         'test_merge/动摇.txt',
         'test_merge/队伍.txt', 'test_merge/儿女.txt', 'test_merge/发.txt', 'test_merge/赶.txt',
         'test_merge/机组.txt', 'test_merge/叫.txt',
         'test_merge/进.txt', 'test_merge/镜头.txt', 'test_merge/开通.txt', 'test_merge/看.txt',
         'test_merge/面.txt',
         'test_merge/牌子.txt',
         'test_merge/平息.txt', 'test_merge/旗帜.txt', 'test_merge/气息.txt', 'test_merge/气象.txt',
         'test_merge/日子.txt', 'test_merge/使.txt',
         'test_merge/说明.txt', 'test_merge/天地.txt', 'test_merge/挑.txt', 'test_merge/推翻.txt',
         'test_merge/望.txt', 'test_merge/想.txt',
         'test_merge/眼光.txt', 'test_merge/长城.txt', 'test_merge/震惊.txt', 'test_merge/中医.txt']

list6 = ['test_merge1/本.txt', 'test_merge1/表面.txt', 'test_merge1/菜.txt', 'test_merge1/补.txt',
         'test_merge1/成立.txt',
         'test_merge1/吃.txt',
         'test_merge1/出.txt', 'test_merge1/带.txt', 'test_merge1/单位.txt', 'test_merge1/道.txt',
         'test_merge1/动.txt',
         'test_merge1/动摇.txt',
         'test_merge1/队伍.txt', 'test_merge1/儿女.txt', 'test_merge1/发.txt', 'test_merge1/赶.txt',
         'test_merge1/机组.txt', 'test_merge1/叫.txt',
         'test_merge1/进.txt', 'test_merge1/镜头.txt', 'test_merge1/开通.txt', 'test_merge1/看.txt',
         'test_merge1/面.txt',
         'test_merge1/牌子.txt',
         'test_merge1/平息.txt', 'test_merge1/旗帜.txt', 'test_merge1/气息.txt', 'test_merge1/气象.txt',
         'test_merge1/日子.txt', 'test_merge1/使.txt',
         'test_merge1/说明.txt', 'test_merge1/天地.txt', 'test_merge1/挑.txt', 'test_merge1/推翻.txt',
         'test_merge1/望.txt', 'test_merge1/想.txt',
         'test_merge1/眼光.txt', 'test_merge1/长城.txt', 'test_merge1/震惊.txt', 'test_merge1/中医.txt']

list7 = ['test_data_csv/本.csv', 'test_data_csv/表面.csv', 'test_data_csv/菜.csv', 'test_data_csv/补.csv', 'test_data_csv/成立.csv', 'test_data_csv/吃.csv',
         'test_data_csv/出.csv', 'test_data_csv/带.csv', 'test_data_csv/单位.csv', 'test_data_csv/道.csv', 'test_data_csv/动.csv', 'test_data_csv/动摇.csv',
         'test_data_csv/队伍.csv', 'test_data_csv/儿女.csv', 'test_data_csv/发.csv', 'test_data_csv/赶.csv', 'test_data_csv/机组.csv', 'test_data_csv/叫.csv',
         'test_data_csv/进.csv', 'test_data_csv/镜头.csv', 'test_data_csv/开通.csv', 'test_data_csv/看.csv', 'test_data_csv/面.csv', 'test_data_csv/牌子.csv',
         'test_data_csv/平息.csv', 'test_data_csv/旗帜.csv', 'test_data_csv/气息.csv', 'test_data_csv/气象.csv', 'test_data_csv/日子.csv',
         'test_data_csv/使.csv',
         'test_data_csv/说明.csv', 'test_data_csv/天地.csv', 'test_data_csv/挑.csv', 'test_data_csv/推翻.csv', 'test_data_csv/望.csv', 'test_data_csv/想.csv',
         'test_data_csv/眼光.csv', 'test_data_csv/长城.csv', 'test_data_csv/震惊.csv', 'test_data_csv/中医.csv']



if __name__ == '__main__':
    #remove_symbol(list1,list2)
    #add_semantic_category(list2,list3)
    #add_label(list2,list4)
    qiyici(list2,list3)
    add_label(list3,list4)
    merge(list4,list5)
    divid_lable(list5,list6)
    make_csv(list5,list7)



