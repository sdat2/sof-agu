"""map.py by sdat2 - the different maps options.

southern_ocean_axes_setup - SO - up to 30 deg South to 90 degrees south.

"""
import numpy as np
from typing import List
import xarray as xr
from numba import jit
import matplotlib
import matplotlib.path as mpath
import cartopy.crs as ccrs
import src.constants as cst
import src.time_wrapper as twr


@twr.timeit
def southern_ocean_axes_setup(
    ax: matplotlib.axes.Axes,
    fig: matplotlib.figure.Figure,
    add_gridlines: bool = True,
) -> None:
    """
    This function sets up the subplot so that it is a cartopy map of the southern ocean.

    returns void as the ax and figure objects are pointers not data.

    Args:
        ax (matplotlib.axes.Axes): The axis object to add the map to.
        fig (matplotlib.figure.Figure): The figure object for the figure in general.
        add_gridlines (bool): whether or not to add gridlines to the plot.
    """
    carree = ccrs.PlateCarree()
    ax.set_extent([-180, 180, -90, -30], carree)
    fig.subplots_adjust(bottom=0.05, top=0.95, left=0.04, right=0.95, wspace=0.02)

    def plot_boundary() -> None:
        """
        Makes SO plot boundary into a nice circle
        of the right size.
        """
        theta = np.linspace(0, 2 * np.pi, 100)
        center, radius = [0.5, 0.5], 0.45
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)
        ax.set_boundary(circle, transform=ax.transAxes)

    plot_boundary()

    # add coastlines and gridlines
    ax.coastlines(resolution="50m", linewidth=0.3)

    if add_gridlines:
        ax.gridlines(linewidth=0.5)

    # Add 2000m isobath (or whatever the max depth is).

    @jit(cache=True)  # significant performance enhancement.
    def find_isobath(
        tmp_bathymetry: np.ndarray, crit_depth=cst.MAX_DEPTH
    ) -> List[list]:
        """
        Find isobath.

        Args:
            tmp_bathymetry (np.ndarray): Bathymetry np array.
            crit_depth ([type], optional): Critical depth. Defaults to cst.MAX_DEPTH.

        Returns:
            List[list]: List of index pairs.
        """
        isobath_index_list = []
        shape_bathymetry = np.shape(tmp_bathymetry)
        for i in range(0, shape_bathymetry[0] - 1):
            for j in range(0, shape_bathymetry[1] - 1):
                if tmp_bathymetry[i, j] >= crit_depth:
                    if tmp_bathymetry[i - 1, j] < crit_depth:
                        isobath_index_list.append([i, j])
                    if tmp_bathymetry[i, j - 1] < crit_depth:
                        isobath_index_list.append([i, j])
                    if tmp_bathymetry[i + 1, j] < crit_depth:
                        isobath_index_list.append([i, j])
                    if tmp_bathymetry[i, j + 1] < crit_depth:
                        isobath_index_list.append([i, j])
        return isobath_index_list

    i_list = find_isobath(
        xr.open_dataset(cst.SALT_FILE)[cst.DEPTH_NAME].values,
        crit_depth=cst.MAX_DEPTH,
    )

    index_npa: np.ndarray = np.array(i_list)
    lons = xr.open_dataset(cst.SALT_FILE)[cst.X_COORD].values[index_npa[:, 1]]
    lats = xr.open_dataset(cst.SALT_FILE)[cst.Y_COORD].values[index_npa[:, 0]]

    ax.plot(lons, lats, ",", markersize=0.4, color="grey", transform=ccrs.Geodetic())
