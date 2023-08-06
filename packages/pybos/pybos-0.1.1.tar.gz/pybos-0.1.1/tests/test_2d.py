#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021 CORIA
"""Demonstration of a BOS script."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from scipy.ndimage import gaussian_filter

from pybos.extraction import idz2n
from pybos.laplacian import solve_BOS
from pybos.physical_laws import polynomial
from pybos.reader import DANTEC_DAT, reader
from pybos.vector_calculus import divergence

pybos_path = test_path = Path(__file__).parent
while pybos_path.name != "tests":
    pybos_path = pybos_path.parent
pybos_path = pybos_path.parent


def filter_(x: float) -> float:
    """Apply a gaussian filter."""
    return gaussian_filter(x, sigma=(2, 2), order=0, mode="nearest")


def read_data() -> xr.Dataset:
    """Read example data."""
    im_datafile = pybos_path / "data/example_data_2d.dat"
    cols = 2, 3, 6, 7  # pix for now
    scale = 1 / (2560 * ((283 - 26) / 319) / 384)  # pix to mm

    data = reader(im_datafile, DANTEC_DAT, usecols=cols, scale=scale, unit="mm")
    data["U"] *= -1
    data["V"] *= -1
    return data


def crop(data: xr.Dataset) -> xr.Dataset:
    """Crop data."""
    pix1, piy1 = 244, 117
    pix2, piy2 = 2321, 2012

    Pix_size = 8

    pix1 = int((pix1 - Pix_size + 0.5) / Pix_size)
    pix2 = int((pix2 - Pix_size + 0.5) / Pix_size)
    piy1 = int((piy1 - Pix_size + 0.5) / Pix_size)
    piy2 = int((piy2 - Pix_size + 0.5) / Pix_size)

    piy1, piy2 = data.dims["y"] - piy2, data.dims["y"] - piy1

    roi = {"x": slice(pix1, pix2), "y": slice(piy1, piy2)}
    cropped_data = data.isel(roi)  # type: ignore
    return cropped_data


def plot(T: xr.DataArray) -> None:
    """Plot the resulting temperature."""
    fig, ax = plt.subplots()
    T.plot.pcolormesh(ax=ax, cmap=plt.cm.jet, vmin=0, vmax=50)
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(pybos_path / "artifacts/Temperature_2d.png", dpi=200)


def check(**res: float) -> None:
    """Check some reference values."""
    ref = pd.Series(
        {
            "divmin": -0.11082972510245184,
            "divmean": 0.0009025630571096038,
            "divmax": 0.1762545837433431,
            "Tmin": 7.173597980756313,
            "Tmean": 26.68481712640316,
            "Tmax": 41.65479086851701,
        }
    )
    pd.testing.assert_series_equal(pd.Series(res).astype(float), ref)


def test_2d() -> None:
    """Run a 2d case."""
    d = 190  # for cube # 0.003 for aquarium # [mm] pattern-tank distance
    w = 400  # [mm] tank width "h" in [Plakina et al 2012]
    n0 = 1.00027  # [] refractive index of the air

    data = read_data()
    cropped_data = crop(data)

    filtered_data = xr.apply_ufunc(filter_, cropped_data, keep_attrs=True)
    filtered_data["divergence"] = divergence(filtered_data)

    n_T, T_n = polynomial()

    T_left = 7.5
    T_right = 39.5

    idz_top = idz_bottom = None
    idz_left = n_T(T_left) * w
    idz_right = n_T(T_right) * w

    idz = solve_BOS(filtered_data.divergence, w, d, n0, idz_top, idz_bottom, idz_left, idz_right)

    # using a 2d hypothesis
    n = idz2n(idz, w, method="2d")

    T = T_n(n)
    plot(T)

    check(
        divmin=filtered_data.divergence.min(),
        divmean=filtered_data.divergence.mean(),
        divmax=filtered_data.divergence.max(),
        Tmin=T.min(),
        Tmean=T.mean(),
        Tmax=T.max(),
    )


if __name__ == "__main__":
    test_2d()
