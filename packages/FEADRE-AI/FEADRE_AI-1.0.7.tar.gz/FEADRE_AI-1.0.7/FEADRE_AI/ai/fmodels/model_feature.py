import torch
from torch import nn
import torch.nn.functional as F

'''
功能层
'''


class Integral(nn.Module):
    '''
    输出最终特图预测值  8 -> 1
    将按 (reg_max+1)*回归个数 的表示,通过期望求出结果
        先将回归值表示成分布概率: softmax
        再离散化: 通过 reg_max 间隙为1离散数组
        求期望: 通过全连接层

    preg = torch.rand(2, 3, 32)
    integral = Integral(7)
    res = integral(preg)
    print(res.shape)
    print(res)
    '''

    def __init__(self, reg_max=16):
        super(Integral, self).__init__()
        self.reg_max = reg_max
        # 7 生成 tensor([0., 1., 2., 3., 4., 5., 6., 7.]) 的区间
        # 这个onnx不支持
        # self.register_buffer('project', torch.linspace(0, self.reg_max, self.reg_max + 1))
        self.interval = torch.linspace(0, self.reg_max, self.reg_max + 1, dtype=torch.float)  # 间隙

    def forward(self, x):
        '''
        设数据最大为7 形成[0., 1., 2., 3., 4., 5., 6., 7.] 分个点

        :param x: (2, 3, 32=4*8)  torch.Size([3, 2100, 32])
        :return:(6,4) 输出为  torch.Size([3, 2100, 4])
        '''
        b, d, c = x.shape
        # (2,3,32) -> (2*3*4,8)=[24, 8] 形成该层24个点的分布图
        x = F.softmax(x.reshape(-1, self.reg_max + 1), dim=-1)
        # [24, 8] ^^ [8,1] -> [24,1] 通过期望求出每个点的具体值   (一个框有4个点)
        # x = F.linear(x, self.project.type_as(x)).reshape(b, d, 4)
        x = F.linear(x, self.interval.to(x)).reshape(b, d, 4)
        return x


if __name__ == '__main__':
    preg = torch.rand(2, 3, 32)
    integral = Integral(7)
    res = integral(preg)
    print(res.shape)
    print(res)
