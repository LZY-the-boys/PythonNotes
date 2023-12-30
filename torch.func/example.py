import torch
from torch.func import functional_call, jvp

@torch.no_grad()
def ex_func_call():
    # Assume we have a model
    model = torch.nn.Linear(10, 2)

    # new parameters
    # new_parameters = { n:0.1*p for n,p in model.named_parameters()} 
    new_parameters = { n:0.1*p for n,p in model.state_dict().items()} 
    # input data
    input_data = torch.randn(1, 10)

    output0 = model(input_data)
    # Perform functional call: call the model with new parameter, without affecting the original model 
    output1 = functional_call(model, new_parameters, input_data)
    print(output0)
    print(output1)

@torch.no_grad()
def ex_jvp():

    # 实际计算中，我们通常不直接计算Jacobian矩阵，因为存储和计算这个矩阵可能会很昂贵, 
    # 经常对Jacobian矩阵进行向量积 (将输入方向向量（通常是在优化问题中的步长方向向量）左乘到Jacobian矩阵上)

    # for f: R^n -> R^m
    # 在点 x 处的导数（Jacobian 矩阵）通常表示为 J_f(x): J_{ij} = \frac\partial{f_i}\partial{x_j}(x)
    # Jacobian-vector product (jvp): v^T J_f(x)
    # 反向传播操作，这实际上就是计算向量-雅可比乘积 梯度就是Jacobian矩阵和一个全是1的向量的向量-雅可比乘积
    # Vector-Jacobian product (vjp): J_f(x) v

    x = torch.randn([])
    f = lambda x: x * torch.tensor([1., 2., 3])
    # f(x) = [1(x1), 2(x2), 3(x3)], 
    # Jacobian_f = [ df/x1 df/x2 df/x3 ] = [1, 2, 3]
    # Jacobian_f(x) = f(x)
    value, grad = jvp(f, (x,), (torch.tensor(1.),))

    assert torch.allclose(value, f(x))
    assert torch.allclose(grad, torch.tensor([1., 2, 3]))

    x = torch.randn(5)
    y = torch.randn(5)
    f = lambda x, y: (x * y) # * 为逐元素乘法
    # Jacobian_f = [df/x, df/y] = [ df_i/dx_j, df_i/dy_j ] = [diag(y), diag(x)]
    # Jacobian_f(I,I) = yI + xI = x+y 
    _, output = jvp(f, (x, y), (torch.ones(5), torch.ones(5)))
    print(_, output)
    assert torch.allclose(output, x + y)

try:
    ex_jvp()
except:
    import sys,pdb,bdb
    type, value, tb = sys.exc_info()
    if type == bdb.BdbQuit:
        exit()
    print(type,value)
    pdb.post_mortem(tb)