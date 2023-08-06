import torch
'''
start
t_init 开始
是否pytorch GPU 0
返回GPU的数量 5
torch.__version__ 版本 1.10.0+cu113
返回Ture GPU安装成功 True
可用gpu数量 5
索引：0，gpu名字：NVIDIA GeForce RTX 3090
索引：1，gpu名字：NVIDIA GeForce RTX 2080
索引：2，gpu名字：NVIDIA GeForce GTX 1660 Ti
索引：3，gpu名字：NVIDIA P106-100
索引：4，gpu名字：NVIDIA GeForce GTX 1060 6GB
'''

def t_init():
    print('t_init 开始')
    print('是否pytorch GPU', torch.cuda.current_device())
    print('返回GPU的数量', torch.cuda.device_count())
    # 必须单独操作
    print('torch.__version__ 版本', torch.__version__)
    print('返回Ture GPU安装成功', torch.cuda.is_available())
    num_gpu = torch.cuda.device_count()
    print('可用gpu数量', num_gpu)
    for i in range(num_gpu):
        print('索引：%s，gpu名字：%s' % (i, torch.cuda.get_device_name(i)))


def t_calc():
    from torchvision import models
    print('t_calc 开始')
    # 切换gpu
    select_gpu = 0
    device = torch.device("cuda:%s" % select_gpu if torch.cuda.is_available() else "cpu")
    torch.cuda.set_device(select_gpu)
    print('当前gpu名字', torch.cuda.get_device_name(select_gpu))
    print('返回当前设备索引', torch.cuda.current_device())
    print('返回当前空存使用量', torch.cuda.max_memory_allocated() / (1024.0 * 1024.0))
    batch = 3
    size = [416, 416]
    a = torch.rand(batch, 3, *size).to(device)
    b = torch.rand(batch, 3, *size).to(device)
    model = models.wide_resnet50_2(pretrained=False)
    model = model.to(device)
    print('输出结果 ---')
    # net = torch.nn.DataParallel(model, device_ids=[0])
    print(a * b)
    print('返回当前空存使用量', torch.cuda.max_memory_allocated() / (1024.0 * 1024.0))
    print(model(a))


if __name__ == '__main__':
    print('start')
    t_init()
