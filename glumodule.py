import torch.nn as nn
import math
import torch
import matplotlib.pyplot as plt



class GateLinearUnit(nn.Module):
    def __init__(self, embedding_size, num_filers, kernel_size, vocab_size, bias=True, batch_norm=True, activation=nn.Tanh()):
        super(GateLinearUnit, self).__init__()
        self.batch_norm = batch_norm
        self.activation = activation
        self.embedding = nn.Embedding(vocab_size, embedding_size)
        self.conv_layer1 = nn.Conv1d(256, num_filers, kernel_size, padding=1)
        self.conv_layer2 = nn.Conv1d(256, num_filers, kernel_size, padding=1)
        self.batch_norm = nn.LayerNorm(num_filers)
        self.sigmoid = nn.Sigmoid()

        nn.init.kaiming_uniform_(self.conv_layer1.weight)
        nn.init.kaiming_uniform_(self.conv_layer2.weight)

    def gate(self, inputs):
        """门控机制"""
        return self.sigmoid(inputs)

    def forward(self, inputs):
        #embed = self.embedding(inputs)
        #print(embed.size())
        #embed = embed.unsqueeze(1)
        output = self.conv_layer1(inputs)
        output = output.permute(0,2,1)
        print(output.size())
        gate_output = self.conv_layer2(inputs)
        gate_output = gate_output.permute(0, 2, 1)
        print(gate_output.size())
        # Gate Operation
        inputs = inputs.permute(0,2,1)
        output = inputs+output * self.gate(gate_output)
        return output


if __name__=="__main__":
    x = torch.Tensor(16,256,60)
    glu = GateLinearUnit(embedding_size=256, num_filers=256, kernel_size=3, vocab_size=400)
    out = glu(x)
    print(out.size())