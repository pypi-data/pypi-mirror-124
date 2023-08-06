#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021 CORIA
"""Read displacement data from Davis or Dantec."""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import pandas as pd
import xarray as xr
from pint import UnitRegistry

DAVIS_CSV = {"sep": ";", "usecols": (0, 1, 4, 5), "names": ("x", "y", "U", "V"), "header": 0}
DANTEC_CSV = {
    "sep": ",",
    "usecols": (2, 3, 6, 7),
    "names": ("x", "y", "U", "V"),
    "header": 0,
    "skiprows": 5,
}
DAVIS_DAT = {"sep": " ", "usecols": (0, 1, 4, 5), "names": ("x", "y", "U", "V"), "skiprows": 3}
DANTEC_DAT = {
    "sep": None,
    "usecols": (4, 5, 8, 9),
    "names": ("x", "y", "U", "V"),
    "skiprows": 3,
    "skipfooter": 3,
    "engine": "python",
}


def validate_template(
    template: Dict[str, Any],
    x_col: Optional[int] = None,
    y_col: Optional[int] = None,
    u_col: Optional[int] = None,
    v_col: Optional[int] = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Make sure that we have enough information in the template to read the data."""
    template = template.copy()
    default_names = "x", "y", "U", "V"
    default_cols = 0, 1, 2, 3
    assert len(default_names) == len(default_cols)
    warning = False

    if "names" not in template:
        print('You should provide the "names" argument providing the order of columns')
        template["names"] = default_names
        warning = True

    if sorted(template["names"]) != sorted(default_names):
        raise ValueError(f"The colomn names must be exactly {default_names} in any order")

    if "usecols" not in template and None in (x_col, y_col, u_col, v_col):
        print("You should specify which columns to use")
        template["usecols"] = 0, 1, 2, 3
        warning = True

    if len(template["usecols"]) != len(default_cols):
        raise ValueError(
            f"The usecols argument must have {len(default_cols)} values"
            f' corresponding to {template["names"]}'
        )

    if (x_col, y_col, u_col, v_col) != (None, None, None, None):
        cols = list(template["usecols"])
        if x_col is not None:
            cols[template["names"].index("x")] = x_col
        if y_col is not None:
            cols[template["names"].index("y")] = y_col
        if u_col is not None:
            cols[template["names"].index("U")] = u_col
        if v_col is not None:
            cols[template["names"].index("V")] = v_col
        template["usecols"] = tuple(cols)

    if warning:
        print(f'Assuming names={template["names"]} and usecols={template["usecols"]}, i.e. ')

    if warning or verbose:
        for name, col in zip(template["names"], template["usecols"]):
            print(f"The data for {name} is expected to be in columns {col}")

    return template


def validate_scale(
    scale: float = 1.0,
    coord_scale: float = 1.0,
    displacement_scale: float = 1.0,
    unit: Optional[str] = None,
    coord_unit: Optional[str] = None,
    displacement_unit: Optional[str] = None,
    output_unit: Optional[str] = None,
    verbose: bool = False,
) -> Tuple[float, float, str]:
    """Make sure that we have enough information in the template to read the data."""
    if unit is not None:
        if verbose and (coord_unit, displacement_unit) != (None, None):
            print(f"ignoring coord_unit and displacement_unit (using unit={unit})")
        coord_unit = displacement_unit = unit
    elif None in (coord_unit, displacement_unit):
        raise ValueError("You must provide the unit of the input data (after the rescaling)")

    if output_unit is None:
        if verbose:
            print(f"The output unit is chosen to be the same as the coord unit ({coord_unit})")
        output_unit = coord_unit
    assert isinstance(output_unit, str)

    if scale is not None:
        if verbose and (coord_scale, displacement_scale) != (None, None):
            print(f"ignoring coord_scale and displacement_scale (using scale={scale})")
        coord_scale = displacement_scale = scale

    ureg = UnitRegistry()
    output_unit_ = ureg(output_unit)
    coord_unit_ = ureg(coord_unit)
    displacement_unit_ = ureg(displacement_unit)

    coord_scale *= coord_unit_.to(output_unit_).magnitude
    displacement_scale *= displacement_unit_.to(output_unit_).magnitude

    if verbose:
        print(
            f"The input data will be scaled to {output_unit_.units}"
            f"with the following scaling factor: "
        )
        print(f"  coord_scale={coord_scale}")
        print(f"  displacement_scale={displacement_scale}")

    return coord_scale, displacement_scale, output_unit


def reader(
    filename: Union[str, Path],
    template: Dict[str, Any],
    scale: float = 1.0,
    coord_scale: float = 1.0,
    displacement_scale: float = 1.0,
    x_col: Optional[int] = None,
    y_col: Optional[int] = None,
    u_col: Optional[int] = None,
    v_col: Optional[int] = None,
    output_unit: Optional[str] = None,
    unit: Optional[str] = None,
    coord_unit: Optional[str] = None,
    displacement_unit: Optional[str] = None,
    verbose: bool = False,
    **kwargs: Any,
) -> xr.Dataset:
    """Read a csv file from Dantec or Davis."""
    filename = Path(filename)
    template = validate_template({**template, **kwargs}, x_col, y_col, u_col, v_col, verbose)
    coord_scale, displacement_scale, unit = validate_scale(
        scale,
        coord_scale,
        displacement_scale,
        unit,
        coord_unit,
        displacement_unit,
        output_unit,
        verbose,
    )

    dataframe = pd.read_csv(filename, **template)

    dataframe.x *= coord_scale
    dataframe.y *= coord_scale

    dataframe.U *= displacement_scale
    dataframe.V *= displacement_scale

    dataframe = dataframe.set_index(["y", "x"])
    dataset = dataframe.to_xarray()
    assert isinstance(dataset, xr.Dataset)

    dataset.x.attrs["units"] = unit
    dataset.y.attrs["units"] = unit
    dataset.U.attrs["units"] = unit
    dataset.V.attrs["units"] = unit
    dataset.U.attrs["long_name"] = "Displacement along x"
    dataset.V.attrs["long_name"] = "Displacement along y"

    return dataset


if __name__ == "__main__":
    data = reader(
        "BOS_tanguy_15092021/test1_Iminsta0_cube_eau_2607_PIV_Imref0_9Im_.6o5xcjgo.000000.dat",
        template=DANTEC_DAT,
        scale=2,
        unit="mm",
        output_unit="m",
        verbose=True,
    )
    print(data)
