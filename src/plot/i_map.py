"""
The purpose of this is to visualise the i_metric
on the southern ocean map.
"""
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import src.plot_utils.colors as col
import src.time_wrapper as twr
import src.plot_utils.gen_panels as gp
import src.plot_utils.ko_plot as ko
import src.plot_utils.map as mp
import src.constants as cst


@twr.timeit
def map_imetric(da_i: xr.DataArray, da: xr.DataArray) -> None:
    """
    Plot map i metric clusters.

    Returns void (although matplotlib will be storing the figure).

    Args:
        da_i (xr.DataArray):  xarray.dataarray object.
        da (xr.DataArray): xarray.dataarray object.
    """
    pairs_list: list = []
    width_ratios: list = []
    num_pairs: int = 0
    num_plots: int = 2
    da_i: xr.DataArray = da_i + 1
    map_proj = ccrs.SouthPolarStereo()
    carree = ccrs.PlateCarree()

    for i in range(num_plots):

        if i == 0:

            num_pairs += 1
            pairs = np.asarray([1])
            width_ratios.append(0.5)
            pairs_list.append(pairs)

        elif i == 1:

            width_ratios.append(0.05)
            num_pairs += 1
            pairs = da.coords[cst.P_COORD].values
            cmap_list = col.return_list_of_colormaps(len(pairs), fade_to_white=False)
            pairs_list.append(pairs)

            for width in [1 / num_plots / len(pairs) for x in range(len(pairs))]:
                width_ratios.append(width)

        print(pairs_list)
        print(width_ratios)

    gs = GridSpec(
        nrows=2,
        ncols=len(width_ratios),
        width_ratios=width_ratios,
        height_ratios=[1, 0.05],
        wspace=0.15,
    )

    fig = plt.gcf()
    used_up_columns = 0
    primary_axes_list = []

    for i in range(2):

        if i == 0:
            ax1 = fig.add_subplot(
                gs[0, 0],
                projection=map_proj,
            )
            cbar_ax = fig.add_subplot(gs[1, 0])
            used_up_columns += 2
            mp.southern_ocean_axes_setup(ax1, fig)

        elif i == 1:
            print("used_up_columns", used_up_columns)
            print(
                "used_up_columns + pairs_list[i].shape[0]",
                used_up_columns + pairs_list[i].shape[0],
            )
            ax1 = fig.add_subplot(
                gs[0, used_up_columns : used_up_columns + pairs_list[i].shape[0]],
                projection=map_proj,
            )
            mp.southern_ocean_axes_setup(ax1, fig, add_gridlines=False)
            cbar_axes = [
                fig.add_subplot(gs[1, used_up_columns + j])
                for j in range(len(pairs_list[i]))
            ]
            used_up_columns += pairs_list[i].shape[0] + 1

        number_clusters = 5

        if i == 0:

            print("da_i", da_i)
            print("ax1", ax1)

            im = da_i.plot(
                ax=ax1,
                add_colorbar=False,
                cmap=col.cluster_cmap(number_clusters),
                vmin=0.5,
                vmax=number_clusters + 0.5,
                transform=carree,
                subplot_kws={"projection": map_proj},
                alpha=1,
            )

            plt.colorbar(
                im,
                cax=cbar_ax,
                label="Class Assignment",
                ticks=range(1, number_clusters + 1),
                orientation="horizontal",
            )

            primary_axes_list.append(ax1)
            ax1.set_title("")

        if i == 1:

            fig = plt.gcf()

            for j in range(len(pairs_list[i])):
                # kim orsi fronts.
                im = da.isel(pair=j).plot(
                    cmap=cmap_list[j],
                    vmin=0,
                    vmax=1,
                    ax=ax1,
                    add_colorbar=False,
                    transform=carree,
                    subplot_kws={"projection": map_proj},
                    alpha=1,
                )

                cbar = plt.colorbar(
                    im, cax=cbar_axes[j], orientation="horizontal", ticks=[0, 1]
                )
                cbar.set_label(da.coords[cst.P_COORD].values[j])

            primary_axes_list.append(ax1)
            ax1.set_title("")

            # Add KO plot.
            ko.draw_fronts_kim(ax1)
            leg = ax1.legend(
                bbox_to_anchor=(0.0, -0.1, 0, 0),
                loc="lower right",
                ncol=2,
                mode="expand",
                borderaxespad=0.0,
                frameon=False,
            )

            # set the linewidth of each legend object
            for legobj in leg.legendHandles:
                legobj.set_linewidth(2.0)

    gp.label_subplots(primary_axes_list)
