#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021 CORIA
"""Demonstration of a BOS script."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from scipy.signal import spline_filter

from pybos.extraction import idz2n
from pybos.laplacian import solve_BOS
from pybos.physical_laws import gladstone_dale, ideal_gaz
from pybos.reader import DANTEC_DAT, reader
from pybos.vector_calculus import divergence

pybos_path = test_path = Path(__file__).parent
while pybos_path.name != "tests":
    pybos_path = pybos_path.parent
pybos_path = pybos_path.parent


def filter_(x: float) -> float:
    """Apply a gaussian filter."""
    return spline_filter(x, lmbda=2)


def read_data() -> xr.Dataset:
    """Read example data."""
    im_datafile = pybos_path / "data/example_data_axi.vect"
    cols = 0, 1, 2, 3  # pix for now
    scale = 1 / 77.0  # pix to mm

    data = reader(
        im_datafile,
        DANTEC_DAT,
        usecols=cols,
        scale=scale,
        unit="mm",
        output_unit="mm",
        skipfooter=0,
    )
    return data


def crop(data: xr.Dataset) -> xr.Dataset:
    """Crop data."""
    roi = {"x": slice(None, None), "y": slice(20, -20)}

    cropped_data = data.isel(roi)  # type: ignore
    return cropped_data


def plot(T: xr.DataArray) -> None:
    """Plot the resulting temperature."""
    fig, ax = plt.subplots()
    T.plot.pcolormesh(ax=ax, cmap=plt.cm.jet, vmin=20, vmax=90)
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(pybos_path / "artifacts/Temperature_axi.png", dpi=200)


def check(**res: float) -> None:
    """Check some reference values."""
    ref = pd.Series(
        {
            "divmin": -0.014772756879968412,
            "divmean": 0.001903474952733359,
            "divmax": 0.02153539914658238,
            "Tmin": 26.74070754311657,
            "Tmean": 52.11628994045219,
            "Tmax": 89.0648083252903,
        }
    )
    pd.testing.assert_series_equal(pd.Series(res).astype(float), ref)


def test_axi() -> None:
    """Run an axi case."""
    d = 55  # [mm] object-pattern distance
    n0 = 1.00027  # [] refractive index of the air
    G = 0.000226  # [m³/Kg] Gladstone constant of air at 20°C and 1 bar
    p = 101_325  # [Pa] = [J/m³] pressure
    M = 28.976 * 1e-3  # [kg/mol] molar mass

    data = read_data()
    cropped_data = crop(data)

    filtered_data = xr.apply_ufunc(filter_, cropped_data, keep_attrs=True)
    filtered_data["divergence"] = divergence(filtered_data)

    w = float(filtered_data.x.max() - filtered_data.x.min())  # [mm] object size

    idz_top = idz_bottom = None
    idz_left = n0 * w
    idz_right = n0 * w

    idz = solve_BOS(filtered_data.divergence, w, d, n0, idz_top, idz_bottom, idz_left, idz_right)

    # using an axisymmetric hypothesis
    n = idz2n(idz, w, n0, method="abel")

    density = gladstone_dale(n, G)
    T = ideal_gaz(density, p, M)

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
    test_axi()
