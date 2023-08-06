#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021 CORIA
"""Vector operators (mainly divergence)."""

import xarray as xr


def divergence(
    data: xr.Dataset,
    edge_order: int = 0,
    mask: bool = True,
    U: str = "U",
    V: str = "V",
    verbose: bool = False,
) -> xr.DataArray:
    """Compute the divergence of a 2D vector field."""
    edge_order_ = max(edge_order, 1)
    grad_x = data[U].differentiate("x", edge_order=edge_order_)
    grad_y = data[V].differentiate("y", edge_order=edge_order_)

    if not edge_order:
        grad_x[{"x": [0, -1]}] = 0
        grad_y[{"y": [0, -1]}] = 0

    div = grad_x + grad_y

    if mask:
        div = div.where(abs(data[U]) > 1e-30, 0.0)

    div.name = "div"
    div.attrs["units"] = "dimensionless"
    div.attrs["long_name"] = "Displacement divergence"

    if verbose:
        print(f"The divergence is computed as : div = d({U})/dx + d({V})/dx")
        print(f"Using a {edge_order}-th order accurate differences at the boundaries.")
        if not edge_order:
            print(" (the normal derivative is taken to be 0 at the boundaries)")

        if mask:
            print(f"A mask is applied to remove the values where |{U}|<=1e-30")

        print(f"mean(divergence)={float(div.mean())}")

    return div


def amplitude(data: xr.Dataset, U: str = "U", V: str = "V", verbose: bool = False) -> xr.DataArray:
    """Compute the amplitude of a 2D vector field."""
    norm = xr.ufuncs.hypot(data[U], data[V])  # type: ignore # pylint: disable=no-member
    assert isinstance(norm, xr.DataArray)

    norm.name = "norm"
    norm.attrs["units"] = data[U].units
    norm.attrs["long_name"] = "Displacement amplitude"

    if verbose:
        print(f"mean(amplitude)={float(norm.mean())}")

    return norm
