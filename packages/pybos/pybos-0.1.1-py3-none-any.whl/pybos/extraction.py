#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021 CORIA
"""Radon and Abel transformation."""
from typing import Any, Optional

import numpy as np
import xarray as xr
from pint import UnitRegistry

try:
    from skimage.transform import iradon
except ImportError:
    with_iradon = False
else:
    with_iradon = True

try:
    from abel import Transform
except ImportError:
    with_abel = False
else:
    with_abel = True


def _radon(
    idz: xr.DataArray, angular_resolution: int = 180, filter_name: str = "hamming"
) -> xr.DataArray:
    """Compute the refractive index using a Radon transform."""
    if not with_iradon:
        raise ImportError("Please install scikit-image to access the radon transform.")

    def transform(x: np.ndarray) -> np.ndarray:
        """Compute a radon transform assuming that the signal is constant wrt the angle."""
        II = np.tile(x, (angular_resolution, 1)).T
        res = iradon(II, output_size=x.size, filter_name=filter_name)
        return res

    n = xr.apply_ufunc(
        transform, idz, input_core_dims=[["x"]], output_core_dims=[["z", "x"]], vectorize=True
    )
    n = n.isel({"z": n.z.size // 2})

    return n


def _abel(idz: xr.DataArray, **kwargs: Any) -> xr.DataArray:
    """Compute the refractive index using a Abel transform."""
    if not with_abel:
        raise ImportError("Please install PyAbel to access the abel transform.")

    # defaults values
    kwargs["origin"] = kwargs.get("origin", "image_center")
    kwargs["symmetry_axis"] = kwargs.get("symmetry_axis", 0)
    kwargs["center_options"] = kwargs.get("center_options", {"crop": "maintain_size"})

    def transform(x: np.ndarray) -> np.ndarray:
        """Compute an abel transform."""
        return Transform(x, direction="backward", method="hansenlaw", **kwargs).transform

    n = xr.apply_ufunc(transform, idz)

    return n


def idz2n(
    idz: xr.DataArray,
    w: float,
    n0: float = 1.0,
    method: str = "2d",
    w_unit: Optional[str] = None,
    verbose: bool = False,
    **kwargs: Any,
) -> xr.DataArray:
    """Extract the refractive index from its integral using a 2d or axysimmetric hypothesis."""
    if w_unit is not None:
        if verbose:
            print(f"Scaling w from {w_unit} to {idz.x.units}")
        ureg = UnitRegistry()
        w = (w * ureg(w_unit)).to(ureg(idz.x.units)).magnitude
    elif verbose:
        print("Assuming that w and coords are in the same unit.")

    if method == "2d":
        n = idz / w
    elif method == "radon":
        n = _radon(idz - n0 * w, **kwargs) + n0
    elif method == "abel":
        n = _abel(idz - n0 * w, **kwargs) + n0
    else:
        raise ValueError(f"{method} method unknown")

    n.name = "n"
    n.attrs["units"] = "dimensionless"
    n.attrs["long_name"] = "Refractive index"

    return n
