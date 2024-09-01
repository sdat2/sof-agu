"""Xarray values."""
import numpy as np
import xarray as xr
import collections


def order_indexes(dataarray: xr.DataArray, index_list: list) -> np.ndarray:
    """Order indices.

    Goes from a datarray to a numpy array, ideally guaranteeing that
    the ordering of the numpy array is the same as would be expected.

    Args:
        dataarray (xr.DataArray): [description]
        index_list (list): [description]

    Returns:
        np.ndarray: the numpy array which has been correctly ordered.
    """

    dim_list = list(dataarray.dims)
    print("index_list", index_list)
    print("list(dataaray.dims)", dim_list)
    init_list = []

    for dim in dim_list:
        init_list.append(index_list.index(dim))

    print("init_list", init_list)
    fin_list = list(range(len(dim_list)))
    dataarray_values = np.moveaxis(dataarray.values, init_list, fin_list)

    return dataarray_values


def _old_order_indexes(dataarray: xr.DataArray, index_list: list) -> np.ndarray:
    """Old order indexes.

    Args:
        dataarray (xr.DataArray): dataarray to reorder.
        index_list (list): index list to odre by.

    Returns:
        np.ndarray: dataarray_values.
    """

    coords_list = []
    for item in index_list:
        coords_list.append((item, dataarray.coords[item].values.shape[0]))

    coords_d = collections.OrderedDict(coords_list)

    print("coords_d", coords_d)

    init_position_d = []

    shape = np.shape(dataarray.values)

    for key in coords_d:
        init_position_d.append((key, shape.index(coords_d[key])))

    init_position_d = collections.OrderedDict(init_position_d)

    print("init_position_d", init_position_d)

    init_list = list(init_position_d.values())
    fin_list = list(range(len(coords_d.values())))

    dataarray_values = np.moveaxis(dataarray.values, init_list, fin_list)

    print(index_list, np.shape(dataarray_values))

    return dataarray_values
