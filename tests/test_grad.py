# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NVIDIA-License
#
# Authors: Guojin Chen (work done during internship at NVIDIA), Haoyu Yang
#
# Project: DiffOPC — Differentiable OPC
# Paper:   https://dl.acm.org/doi/10.1145/3676536.3676764
#
# NVIDIA CORPORATION and its affiliates retain all intellectual property and
# proprietary rights in and to this software and related documentation. Any
# use, reproduction, or distribution is subject to the terms of the NVIDIA
# License (see LICENSE in the project root). The work may be used only for
# non-commercial research or evaluation, except by NVIDIA Corporation and
# its affiliates.

import torch
from torch.autograd import Function, gradcheck


class CustomFunction(Function):
    @staticmethod
    def forward(ctx, *inputs):
        ctx.save_for_backward(*inputs)
        return tuple(x * 2 for x in inputs)

    @staticmethod
    def backward(ctx, *grad_outputs):
        return tuple(g * 2 for g in grad_outputs)


def test_custom_function():
    input_values = (
        torch.tensor(1.0, dtype=torch.float64, requires_grad=True),
        torch.tensor(2.0, dtype=torch.float64, requires_grad=True),
    )
    test_passed = gradcheck(CustomFunction.apply, input_values, eps=1e-6, atol=1e-4)
    assert test_passed


if __name__ == "__main__":
    test_custom_function()
    print("Gradcheck passed!")
