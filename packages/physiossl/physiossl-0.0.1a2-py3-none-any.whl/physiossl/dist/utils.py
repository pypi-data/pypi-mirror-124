"""
@Time    : 2021/10/13 23:13
@File    : utils.py
@Software: PyCharm
@Desc    : 
"""
import torch
import torch.distributed as dist


def is_distributed_enabled():
    return (
            torch.distributed.is_available() and
            torch.distributed.is_initialized() and
            torch.distributed.get_world_size() > 1
    )


class SyncAllGather(torch.autograd.Function):
    @staticmethod
    def forward(ctx, tensor):
        ctx.batch_size = tensor.shape[0]

        gathered_tensor = [torch.zeros_like(tensor) for _ in range(torch.distributed.get_world_size())]

        torch.distributed.all_gather(gathered_tensor, tensor)
        gathered_tensor = torch.cat(gathered_tensor, 0)

        return gathered_tensor

    @staticmethod
    def backward(ctx, grad_output):
        grad_input = grad_output.clone()
        torch.distributed.all_reduce(grad_input, op=dist.ReduceOp.SUM, async_op=False)

        idx_from = torch.distributed.get_rank() * ctx.batch_size
        idx_to = (torch.distributed.get_rank() + 1) * ctx.batch_size
        return grad_input[idx_from:idx_to]


def gather_tensor_sync(tensors: torch.Tensor):
    assert is_distributed_enabled()
    tensors_gathered = SyncAllGather.apply(tensors)

    return tensors_gathered
