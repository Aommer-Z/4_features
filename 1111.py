import re



qiyi_word = '本'
line = ['大字/n/Dk05', '本/n/Ed61', '在/p/Jd02', '拼音/n/Dk05', '检/v/-1', '字/n/Bg07', '之外/f/Cb05', '还/d/Hi27', '增加/v/Ih05', '了/u/Ig01', '四角号码/n/-1', '检字表/n/Dk18', '以/c/Di02', '适应/v/Jc01', '方言/n/Dk06', '地区/n/Cb08', '的/u/Bo29', '需要/n/Jc05']
index = [i for i, v in enumerate(line) if v.startswith("%s" % (qiyi_word + "/"))]  # enumerate 枚举函数
n = len(line)
if len(index):
    for idx in index:  # 将每一个带有歧义词的位置通过for从列表index中给遍历出来，返回idx
        list4 = []
        # idx:8
        print(idx)
        if idx == 0:
            try:

                list4.append('null')
                list4.append('null')
                list4.append('null')
                list4.append('null')
                list4.append('null')
                list4.append('null')

                strW = line[idx]
                list4.append(re.split('/', strW)[0])

                strR1 = line[idx + 1]
                list4.append(','.join(re.split('/', strR1)))

                strR2 = line[idx + 2]
                list4.append(','.join(re.split('/', strR2)))
            except IndexError:
                pass
        elif (idx == 1):
            try:
                list4.append('null')
                list4.append('null')
                list4.append('null')

                strL1 = line[idx - 1]
                list4.append(','.join(re.split('/', strL1)))

                strW = line[idx]
                list4.append(re.split('/', strW)[0])

                strR1 = line[idx + 1]
                list4.append(','.join(re.split('/', strR1)))

                strR2 = line[idx + 2]
                list4.append(','.join(re.split('/', strR2)))

            except IndexError:
                pass
        elif idx == n - 1:
            try:
                strL1 = line[idx - 2]
                list4.append(','.join(re.split('/', strL1)))

                strL2 = line[idx - 1]
                list4.append(','.join(re.split('/', strL2)))

                strW = line[idx]
                list4.append(re.split('/', strW)[0])

                list4.append('null')
                list4.append('null')
                list4.append('null')
                list4.append('null')
                list4.append('null')
                list4.append('null')
                list4.append('sdkoaskdosad')

            except IndexError:
                pass
        elif idx == n - 2:
            try:
                strL1 = line[idx - 2]
                list4.append(','.join(re.split('/', strL1)))

                strL2 = line[idx - 1]
                list4.append(','.join(re.split('/', strL2)))

                strW = line[idx]
                list4.append(re.split('/', strW)[0])

                strR1 = line[idx + 1]
                list4.append(','.join(re.split('/', strR1)))

                list4.append('null')
                list4.append('null')
                list4.append('null')

            except IndexError:
                pass

        else:
            try:
                strL1 = line[idx - 2]
                list4.append(','.join(re.split('/', strL1)))

                strL2 = line[idx - 1]
                list4.append(','.join(re.split('/', strL2)))

                strW = line[idx]
                list4.append(re.split('/', strW)[0])

                strR1 = line[idx + 1]
                list4.append(','.join(re.split('/', strR1)))

                strR2 = line[idx + 2]
                list4.append(','.join(re.split('/', strR2)))
            except IndexError:
                pass
print(list4)

if len(index):
    for idx in index:  # 将每一个带有歧义词的位置通过for从列表index中给遍历出来，返回idx
        # idx:8
        # print(idx)
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
        if idx == 1:
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
        if idx == 2:
            try:
                strL1 = line[idx - 1]
                list4.append(','.join(re.split('/', strL1)))

                strL2 = line[idx - 2]
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
        if idx == 3:
            try:
                strL1 = line[idx - 1]
                list4.append(','.join(re.split('/', strL1)))

                strL2 = line[idx - 2]
                list4.append(','.join(re.split('/', strL2)))

                strL3 = line[idx - 3]
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
        if idx == n - 1:
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
        if idx == n - 2:
            try:
                strR1 = line[idx + 1]
                list4.append(','.join(re.split('/', strR1)))

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
        if idx == n - 3:
            try:
                strR1 = line[idx + 1]
                list4.append(','.join(re.split('/', strR1)))

                strR2 = line[idx + 2]
                list4.append(','.join(re.split('/', strR2)))

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