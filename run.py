import os
import sys

import torch
import torch.nn as nn
import math
from torch.optim import lr_scheduler
from torch.utils.tensorboard import SummaryWriter
import torch
from tqdm.asyncio import tqdm
from module import Config, TextDGCNN
from utils import train_one_epoch, evaluate, make_data, get_masks

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# torch.device("cuda" if torch.cuda.is_available() else"cpu")
train_iter, val_iter, test_iter, num_classes, vocab_size, word_vectors = make_data('train_data_csv/长城.csv',
                                                                                   'test_data_csv/长城.csv',
                                                                                   'train_merge1/长城.txt')
#
# np.random.seed(1)
# torch.manual_seed(1)
# torch.cuda.manual_seed_all(1)
# torch.backends.cudnn.deterministic = True  # 保证每次结果一样
if os.path.exists("./weights") is False:
    os.makedirs("./weights")
config = Config()
config.num_classes = num_classes
config.vocab_size = vocab_size
model = TextDGCNN(config)
model.word_embedding.weight.data.copy_(word_vectors)
model.to(DEVICE)
tb_writer = SummaryWriter()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=0)
lf = lambda x: ((1 + math.cos(x * math.pi / config.num_epochs)) / 2) * (1 - 0.01) + 0.01  # cosine
scheduler = lr_scheduler.LambdaLR(optimizer, lr_lambda=lf)
for epoch in range(config.num_epochs):
    mean_loss = train_one_epoch(model=model,
                                optimizer=optimizer,
                                data_loader=train_iter,
                                device=DEVICE,
                                epoch=epoch)

    scheduler.step()
    # validate
    acc = evaluate(model=model,
                   data_loader=val_iter,
                   device=DEVICE)

    print("[epoch {}] 验证集: {}%".format(epoch, round(acc * 100, 3)))
    tags = ["loss", "accuracy", "learning_rate"]
    tb_writer.add_scalar(tags[0], mean_loss, epoch)
    tb_writer.add_scalar(tags[1], acc, epoch)
    tb_writer.add_scalar(tags[2], optimizer.param_groups[0]["lr"], epoch)
    torch.save(model.state_dict(), "./weights/model-{}.pth".format(epoch))

# create model
test_model = TextDGCNN(config)
test_model.word_embedding.weight.data.copy_(word_vectors.to(DEVICE))
# load model weights
model_weight_path = "./weights/model-89.pth"
test_model.load_state_dict(torch.load(model_weight_path, map_location=DEVICE))
test_model.eval()
test_model.to(DEVICE)

with torch.no_grad():
    total_num = len(test_iter.dataset)
    print(total_num)
    sum_num = torch.zeros(1).to(DEVICE)

    data_loader = tqdm(test_iter, file=sys.stdout)

    for step, loader in enumerate(data_loader):
        data, label = loader
        line, labels = data
        mask = get_masks(line)
        pred = test_model(line, mask)
        pred = torch.max(pred, dim=1)[1]
        sum_num += torch.eq(pred, labels.to(DEVICE)).sum()
    acc = sum_num.item() / total_num
    print('测试集：%.2f%%' % (acc * 100))
