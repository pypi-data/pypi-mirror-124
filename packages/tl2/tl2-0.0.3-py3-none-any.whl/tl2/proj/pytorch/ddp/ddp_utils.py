import numpy as np
import os
import argparse
import torch
import torch.distributed as dist

from . import d2_comm


def gather_tensor_of_master(tensor):

  tensor_list = d2_comm.all_gather(tensor)
  tensor = tensor_list[0].to(tensor.device)
  return tensor


def all_gather_to_same_device(data):

  data_list = d2_comm.all_gather(data=data)

  ret_list = []
  for tensor in data_list:
    ret_list.append(tensor.to(data.device))

  return ret_list


def gather_to_same_device(data):

  data_list = d2_comm.gather(data=data)

  ret_list = []
  for tensor in data_list:
    ret_list.append(tensor.to(data.device))

  return ret_list


def parser_local_rank():
  parser = argparse.ArgumentParser()
  parser.add_argument("--local_rank", type=int, default=0)
  args, _ = parser.parse_known_args()
  return args.local_rank


def is_distributed():
  n_gpu = int(os.environ["WORLD_SIZE"]) if "WORLD_SIZE" in os.environ else 1
  distributed = n_gpu > 1
  return distributed


def ddp_init(seed=0):
  """
  use config_cfgnode
  """

  rank = parser_local_rank()
  distributed = is_distributed()

  torch.manual_seed(seed)
  torch.cuda.set_device(rank)

  if distributed:
    torch.distributed.init_process_group(backend="nccl", init_method="env://")
    # important: use different random seed for different process
    torch.manual_seed(seed + dist.get_rank())
    torch.cuda.set_device(rank)
    dist.barrier()

  world_size = d2_comm.get_world_size()

  return rank, world_size



