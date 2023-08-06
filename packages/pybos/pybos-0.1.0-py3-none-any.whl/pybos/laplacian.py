#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021 CORIA
"""Vector operators (mainly divergence)."""

from typing import Optional

import pandas as pd
import xarray as xr
from fipy import CellVariable, DiffusionTerm
from fipy.meshes.uniformGrid2D import UniformGrid2D
from pint import UnitRegistry


def constant(
    w: float,
    d: float,
    n0: float,
    coord_unit: str,
    input_unit: Optional[str] = None,
    w_unit: Optional[str] = None,
    d_unit: Optional[str] = None,
    verbose: bool = False,
) -> float:
    """BOS Vinnishenko et al."""
    if input_unit is not None:
        if verbose and (w_unit, d_unit) != (None, None):
            print(f"ignoring w_unit and d_unit (using input_unit={input_unit})")
        w_unit = d_unit = input_unit
    else:
        if w_unit is None:
            if verbose:
                print(f"assuming w is in {coord_unit} (the same unit as the coords)")
            w_unit = coord_unit
        if d_unit is None:
            if verbose:
                print(f"assuming d is in {coord_unit} (the same unit as the coords)")
            d_unit = coord_unit

    ureg = UnitRegistry()
    d = d * ureg(d_unit)
    w = w * ureg(w_unit)
    output_unit = 1 / ureg(coord_unit)

    cte = 2 * n0 / (2 * d + w)
    cte = cte.to(output_unit)  # type: ignore

    if verbose:
        print(f"The constant is {cte}")

    return cte.magnitude  # type: ignore


def solve_BOS(
    divergence: xr.DataArray,
    w: float,
    d: float,
    n0: float,
    idz_top: Optional[float] = None,
    idz_bottom: Optional[float] = None,
    idz_left: Optional[float] = None,
    idz_right: Optional[float] = None,
    input_unit: Optional[str] = None,
    w_unit: Optional[str] = None,
    d_unit: Optional[str] = None,
    verbose: bool = False,
) -> xr.DataArray:
    """Solve the diffusion equation lap(n)=div."""
    # pylint: disable=too-many-branches
    dx = float(divergence.x[1] - divergence.x[0])
    dy = float(divergence.y[1] - divergence.y[0])
    mesh = UniformGrid2D(
        dx=dx,
        dy=dy,
        nx=divergence.x.size,
        ny=divergence.y.size,
        origin=(divergence.x[0:1] - dx / 2, divergence.y[0:1] - dx / 2),
    )

    Cst = constant(
        w,
        d,
        n0,
        coord_unit=divergence.x.units,
        input_unit=input_unit,
        w_unit=w_unit,
        d_unit=d_unit,
        verbose=verbose,
    )

    idz = CellVariable(name="idz", mesh=mesh)
    B = CellVariable(name="B", mesh=mesh, value=Cst * divergence.to_numpy().ravel())

    eq = DiffusionTerm() == B

    if idz_top is None:
        if verbose:
            print("The top boundary condition is Neuman")
        idz.faceGrad.constrain(((0,), (0,)), where=mesh.facesTop)
    else:
        if verbose:
            print("The top boundary condition is Dirichlet")
        idz.constrain(idz_top, where=mesh.facesTop)

    if idz_bottom is None:
        if verbose:
            print("The bottom boundary condition is Neuman")
        idz.faceGrad.constrain(((0,), (0,)), where=mesh.facesBottom)
    else:
        if verbose:
            print("The bottom boundary condition is Dirichlet")
        idz.constrain(idz_bottom, where=mesh.facesBottom)

    if idz_left is None:
        if verbose:
            print("The left boundary condition is Neuman")
        idz.faceGrad.constrain(((0,), (0,)), where=mesh.facesLeft)
    else:
        if verbose:
            print("The left boundary condition is Dirichlet")
        idz.constrain(idz_left, where=mesh.facesLeft)

    if idz_right is None:
        if verbose:
            print("The right boundary condition is Neuman")
        idz.faceGrad.constrain(((0,), (0,)), where=mesh.facesRight)
    else:
        if verbose:
            print("The right boundary condition is Dirichlet")
        idz.constrain(idz_right, where=mesh.facesRight)

    eq.solve(var=idz)

    df = pd.DataFrame({"x": mesh.x, "y": mesh.y, "idz": idz}).set_index(["y", "x"])
    idz = df.to_xarray().idz
    assert isinstance(idz, xr.DataArray)

    idz.assign_coords(x=divergence.x, y=divergence.y)
    idz.x.attrs = divergence.x.attrs
    idz.y.attrs = divergence.y.attrs

    idz.attrs["units"] = divergence.x.units
    idz.attrs["long_name"] = "Integral of the refractive index"

    return idz
