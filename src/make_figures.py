"""
Make figures: run through all the paper figures and make them.

Takes roughly 5 minutes the first time it is run.
"""
import os
from typing import Tuple
import numpy as np
import numpy.ma as ma
import xarray as xr
import matplotlib.pyplot as plt
import logging
import src.constants as cst
import src.plot_utils.latex_style as lsty
import src.plot_utils.xarray_panels as xp
import src.models.train_pyxpcm as tim
import src.plot.clust_3d as c3d
import src.plot.i_map as imap
import src.plot.profiles as prof
import src.plot.preprocessing_profiles as prep
import src.data_loading.io_names as io
from src.models.sobel import sobel_np
import src.time_wrapper as twr


@twr.timeit
def make_all_figures() -> None:
    """
    Make all the figures in the paper in a sequence.

    Takes roughly 15 minutes  on jasmin.
    """
    # fig_list = [1, 2, 3, 4, 5, 6, 7, 8, "A1", "A2", "A3", "A4", "B1", "B2"]
    fig_list = [4]  # ["B1", "B2"]

    fig_prefix = os.path.join(cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME)
    data_prefix = os.path.join(cst.DATA_PATH, "RUN_" + cst.RUN_NAME)

    # Create or get the logger
    logger = logging.getLogger(__name__)
    # set log level
    logger.setLevel(logging.INFO)

    # pylint: disable=logging-not-lazy
    logger.info("Starting make_all_figures, " + " should take about about 8 minutes.")
    print(
        "settings:\n",
        "cst.EXAMPLE_TIME_INDEX",
        cst.EXAMPLE_TIME_INDEX,
        "cst.SEED",
        cst.SEED,
    )

    # Initialise mpl params.
    lsty.mpl_params()

    # FIGURE 1: pc maps.
    if 1 in fig_list:
        logger.info("Making pc maps.")

        ds = xr.open_dataset(cst.DEFAULT_NC)

        da_temp = ds.PCA_VALUES.isel(time=cst.EXAMPLE_TIME_INDEX)
        xp.sep_plots(
            [da_temp.isel(pca=0), da_temp.isel(pca=1), da_temp.isel(pca=2)],
            ["PC1", "PC2", "PC3"],
        )
        plt.savefig(fig_prefix + "_pc_map" + cst.FIGURE_TYPE)
        plt.clf()

    if np.any([x in fig_list for x in [2, 5, "B1", "B2"]]):
        ## make profiles.
        logger.info("Making profiles.")

        lsty.mpl_params()

        # train pcm on a year of data.
        pcm, ds = tim.train_on_interpolated_year(
            time_i=cst.EXAMPLE_TIME_INDEX,
            k_clusters=cst.K_CLUSTERS,
            maxvar=cst.D_PCS,
            min_depth=cst.MIN_DEPTH,
            max_depth=cst.MAX_DEPTH,
            remove_init_var=False,
        )

        # new prefixes for saving gmm cluster profiles etc.

        temp_name = data_prefix + "_temp.nc"
        profiles_name = data_prefix + "_profiles_temp.nc"
        ds.to_netcdf(path=temp_name)

        # MAKE/PLOT PROFILES
        ds = xr.open_dataset(temp_name)
        profile_ds = prof.make_profiles(ds)
        profile_ds.to_netcdf(path=profiles_name)
        profile_ds = xr.open_dataset(profiles_name)

        print(profile_ds)

    if 5 in fig_list:
        # Figure 5: plot profiles.
        prof.plot_profiles(profile_ds)
        lsty.set_dim(plt.gcf())
        plt.savefig(fig_prefix + "_profiles" + cst.FIGURE_TYPE)
        plt.clf()

    if 2 in fig_list:
        # FIGURE 2: Plot 3d clusters.
        logger.info("2: Plot 3d clusters.")

        lsty.mpl_params()

        c3d.comp_3d(
            # pylint: disable=protected-access
            pcm._classifier.weights_,
            # pylint: disable=protected-access
            pcm._classifier.means_,
            # pylint: disable=protected-access
            pcm._classifier.covariances_,
            ds,
        )

        lsty.set_dim(plt.gcf())
        plt.savefig(fig_prefix + "_s3d_clusters" + cst.FIGURE_TYPE)
        plt.clf()

    if 3 in fig_list:
        # FIGURE 3: I metric viridis colormap.
        logger.info("3: I metric geographical map with viridis colormap.")

        lsty.mpl_params()
        ds = xr.open_dataset(cst.DEFAULT_NC)
        xp.sep_plots(
            [
                ds.IMETRIC.isel(Imetric=0, time=cst.EXAMPLE_TIME_INDEX),
                ds.IMETRIC.isel(Imetric=0).mean(dim=cst.T_COORD, skipna=True),
            ],
            [r"$\mathcal{I}$-metric ", r"$\mathcal{I}$-metric"],
            [[0.0, 1.0], [0.0, 1.0]],
            ["viridis", "viridis"],
        )
        plt.savefig(fig_prefix + "_i_metric_dual" + cst.FIGURE_TYPE)
        plt.clf()
        lsty.mpl_params()

    if "X" in fig_list:
        # FIGURE X: single multi color.
        logger.info("X: Example multi colour i metric plot for K=5.")

        da = io.return_pair_i_metric(k_clusters=cst.K_CLUSTERS)
        xp.plot_single_i_metric(da.isel(time=0))
        plt.savefig(fig_prefix + "_i_metric_single" + cst.FIGURE_TYPE)
        plt.clf()

    if 4 in fig_list:

        # FIGURE 4: Plot clusters and i metrics on maps.
        logger.info("4: Plot cluster/imetric on map.")

        lsty.mpl_params()
        da = io.return_pair_i_metric(k_clusters=cst.K_CLUSTERS).isel(time=0)
        da_i = xr.open_dataset(cst.DEFAULT_NC).A_B.isel(
            rank=0, time=cst.EXAMPLE_TIME_INDEX
        )
        imap.map_imetric(da_i, da)
        plt.savefig(fig_prefix + "_map_i_comp" + cst.FIGURE_TYPE)
        plt.clf()

    if 7 in fig_list:

        # FIGURE 7: Plot different k_clusters cluster multi colour plots.
        logger.info("7: compare K=2, K=4.")

        lsty.mpl_params()
        xp.plot_several_pair_i_metrics(
            [
                io.return_pair_i_metric(k_clusters=2).isel(time=0),
                io.return_pair_i_metric(k_clusters=4).isel(time=0),
            ]
        )
        plt.tight_layout()
        plt.savefig(fig_prefix + "_i_metric_comp" + cst.FIGURE_TYPE)
        plt.clf()

    # FIGURE 6: PC1 y grads

    if np.any([x in fig_list for x in [6, "A1", "A2", "A3", "A4"]]):

        ds = xr.open_dataset(cst.DEFAULT_NC)

        lsty.mpl_params()

        ds = xr.open_dataset(cst.DEFAULT_NC)
        da_temp = ds.PCA_VALUES.isel(time=cst.EXAMPLE_TIME_INDEX)

        def get_y_sobel(
            pc_da_temp: xr.DataArray,
        ) -> Tuple[xr.DataArray, xr.DataArray, xr.DataArray]:
            pc1_y: xr.DataArray = pc_da_temp.isel(pca=0)
            pc1_y.values = sobel_np(pc1_y.values)[1]
            pc2_y: xr.DataArray = pc_da_temp.isel(pca=1)
            pc2_y.values = sobel_np(pc2_y.values)[1]
            pc3_y: xr.DataArray = pc_da_temp.isel(pca=2)
            pc3_y.values = sobel_np(pc3_y.values)[1]
            return pc1_y, pc2_y, pc3_y

        pc1_y, pc2_y, pc3_y = get_y_sobel(da_temp)

        xp.sep_plots(
            [pc1_y, pc2_y, pc3_y],
            ["$G_y$ * PC1", "$G_y$ * PC2", "$G_y$ * PC3"],
            [[-40, 40], [-40, 40], [-40, 40]],
        )

        plt.savefig(fig_prefix + "_y_sobel" + cst.FIGURE_TYPE)
        plt.clf()

        da_y = ds.PCA_VALUES.isel(time=cst.EXAMPLE_TIME_INDEX).differentiate(
            cst.Y_COORD
        )
        for pc, grad, sobel in [
            [1, da_y.isel(pca=0), pc1_y],
            [2, da_y.isel(pca=1), pc2_y],
            [3, da_y.isel(pca=2), pc3_y],
        ]:
            cor = ma.corrcoef(
                ma.masked_invalid(grad.values.ravel()),
                ma.masked_invalid(sobel.values.ravel()),
            )
            print("$G_y$, Y grad comparison", "pc" + str(pc), cor)

        # sobel x grad.

        lsty.mpl_params()

        def get_x_sobel(
            pc_da_temp: xr.DataArray,
        ) -> Tuple[xr.DataArray, xr.DataArray, xr.DataArray]:
            pc1_x: xr.DataArray = pc_da_temp.isel(pca=0)
            pc1_x.values = sobel_np(pc1_x.values)[0]
            pc2_x: xr.DataArray = pc_da_temp.isel(pca=1)
            pc2_x.values = sobel_np(pc2_x.values)[0]
            pc3_x: xr.DataArray = pc_da_temp.isel(pca=2)
            pc3_x.values = sobel_np(pc3_x.values)[0]
            return pc1_x, pc2_x, pc3_x

        pc1_x, pc2_x, pc3_x = get_x_sobel(da_temp)

        xp.sep_plots(
            [pc1_x, pc2_x, pc3_x],
            ["$G_x$ * PC1", "$G_x$ * PC2", "$G_x$ * PC3"],
            [[-40, 40], [-40, 40], [-40, 40]],
        )

        plt.savefig(fig_prefix + "_x_sobel" + cst.FIGURE_TYPE)
        plt.clf()

        da_x = ds.PCA_VALUES.isel(time=cst.EXAMPLE_TIME_INDEX).differentiate(
            cst.X_COORD
        )
        for pc, grad, sobel in [
            [1, da_x.isel(pca=0), pc1_x],
            [2, da_x.isel(pca=1), pc2_x],
            [3, da_x.isel(pca=2), pc3_x],
        ]:
            cor = ma.corrcoef(
                ma.masked_invalid(grad.values.ravel()),
                ma.masked_invalid(sobel.values.ravel()),
            )
            print("$G_x$, X grad comparison", "pc" + str(pc), cor)

        # Appendix
        logger.info("A: Appendix figures.")

        # uvel, pca1 y grad for example.
        logger.info("A: uvel/ y grad for example.")

        lsty.mpl_params()

        uvel_ds = xr.open_dataset(cst.UVEL_FILE).isel(Z=cst.EXAMPLE_Z_INDEX)

        # make mean
        pc1_y, pc2_y, pc3_y = get_y_sobel(da_temp)

        tot_y = pc1_x.values
        tot_y[:] = 0.0

        for i in range(len(uvel_ds.coords[cst.T_COORD].values)):
            pc1_y, _, _ = get_y_sobel(ds.PCA_VALUES.isel(time=i))
            tot_y += pc1_y.values

        mean_y = tot_y / len(uvel_ds.coords[cst.T_COORD].values)

        pc2_y.values = mean_y

        pc1_y, _, _ = get_y_sobel(ds.PCA_VALUES.isel(time=i))

        ds = xr.open_dataset(cst.DEFAULT_NC)
        xp.sep_plots(
            [
                pc1_y,
                uvel_ds.UVEL.isel(time=cst.EXAMPLE_TIME_INDEX),
                pc2_y,
                uvel_ds.UVEL.mean(dim=cst.T_COORD, skipna=True),
            ],
            ["$G_y$ * PC1", r"$U$ (m s$^{-1}$)", "$G_y$ * PC1", r"$U$ (m s$^{-1}$)"],
        )
        plt.savefig(fig_prefix + "_pc_y_sobel_comp" + cst.FIGURE_TYPE)
        plt.clf()

        pc1_y, pc2_y, pc3_y = get_y_sobel(da_temp)
        uvel_da = uvel_ds.UVEL.isel(time=cst.EXAMPLE_TIME_INDEX)

        for pc, pc_da in [[1, pc1_y], [2, pc2_y], [3, pc3_y]]:
            cor = ma.corrcoef(
                ma.masked_invalid(pc_da.values.ravel()),
                ma.masked_invalid(uvel_da.values.ravel()),
            )
            print("$G_y$ * PC" + str(pc), "UVEL", cor)

        # uvel, pca1 y grad over time.
        logger.info("A: uvel / y grad overtime.")

        lsty.mpl_params()

        uvel_ds = xr.open_dataset(cst.UVEL_FILE).isel(Z=cst.EXAMPLE_Z_INDEX)
        pca_ds = xr.open_dataset(cst.DEFAULT_NC).isel(pca=0).differentiate(cst.Y_COORD)

        cor_list = list()

        for time_i in range(len(uvel_ds.coords[cst.T_COORD].values)):
            pc1_y, _, _ = get_y_sobel(
                xr.open_dataset(cst.DEFAULT_NC).PCA_VALUES.isel(time=time_i)
            )
            cor = ma.corrcoef(
                ma.masked_invalid(uvel_ds.isel(time=time_i).UVEL.values.ravel()),
                ma.masked_invalid(pc1_y.values.ravel()),
            )
            cor_list.append(cor[1, 0])

        plt.plot(uvel_ds.coords[cst.T_COORD].values, cor_list)
        plt.xlabel("Time")
        plt.ylabel("Correlation coefficient")

        plt.xlim(
            [
                uvel_ds.coords[cst.T_COORD].values[0],
                uvel_ds.coords[cst.T_COORD].values[
                    len(uvel_ds.coords[cst.T_COORD].values) - 1
                ],
            ]
        )
        plt.title(r"Correlation between $G_{y}$ * PC1 and $U$")
        plt.savefig(fig_prefix + "_pc_y_sobel_corr" + cst.FIGURE_TYPE)
        plt.clf()

        #  compare correlations and make correlation graph.
        logger.info("A: vvel / y grad over time.")

        cor = ma.corrcoef(
            ma.masked_invalid(
                uvel_ds.mean(dim=cst.T_COORD, skipna=True).UVEL.values.ravel()
            ),
            ma.masked_invalid(
                pca_ds.mean(dim=cst.T_COORD, skipna=True).PCA_VALUES.values.ravel()
            ),
        )
        print("Correlate U, mean", cor)

        logger.info("A: vvel / y grad in pc1 over time.")

        vvel_ds = xr.open_dataset(cst.VVEL_FILE).isel(Z=cst.EXAMPLE_Z_INDEX)

        cor_list = list()

        for time_i in range(len(uvel_ds.coords[cst.T_COORD].values)):
            pc1_x, _, _ = get_x_sobel(
                xr.open_dataset(cst.DEFAULT_NC).isel(time=time_i).PCA_VALUES
            )

            cor = ma.corrcoef(
                ma.masked_invalid(vvel_ds.isel(time=time_i).VVEL.values.ravel()),
                ma.masked_invalid(pc1_x.values.ravel()),
            )
            cor_list.append(cor[1, 0])

        lsty.mpl_params()

        plt.plot(uvel_ds.coords[cst.T_COORD].values, cor_list)
        plt.xlabel("Time")
        plt.ylabel("Correlation coefficient")
        plt.xlim(
            [
                uvel_ds.coords[cst.T_COORD].values[0],
                uvel_ds.coords[cst.T_COORD].values[
                    len(uvel_ds.coords[cst.T_COORD].values) - 1
                ],
            ]
        )
        plt.title(r"Correlation between $G_{x}$ * PC1 and $V$")
        plt.savefig(fig_prefix + "_pc_x_sobel_corr" + cst.FIGURE_TYPE)
        plt.clf()

        # compare meridional velocity to gradient.
        logger.info("A: vvel/ y grad in pc1 at one time point.")

        vvel_ds = xr.open_dataset(cst.VVEL_FILE).isel(Z=cst.EXAMPLE_Z_INDEX)

        lsty.mpl_params()

        # make mean

        pc1_x, pc2_x, pc3_x = get_x_sobel(da_temp)

        tot_x = pc1_x.values
        tot_x[:] = 0.0

        # get mean

        for i in range(len(uvel_ds.coords[cst.T_COORD].values)):
            pc1_x, _, _ = get_x_sobel(ds.PCA_VALUES.isel(time=i))
            tot_x += pc1_x.values

        mean_x = tot_x / len(uvel_ds.coords[cst.T_COORD].values)

        pc2_x.values = mean_x

        pc1_x, _, _ = get_x_sobel(ds.PCA_VALUES.isel(time=i))

        xp.sep_plots(
            [
                pc1_x,
                vvel_ds.VVEL.isel(time=cst.EXAMPLE_TIME_INDEX),
                pc2_x,
                vvel_ds.VVEL.mean(dim=cst.T_COORD, skipna=True),
            ],
            ["$G_x$ * PC1", r"$V$ (m s$^{-1}$)", "$G_x$ * PC1", r"$V$ (m s$^{-1}$)"],
        )
        plt.savefig(fig_prefix + "_pc_x_sobel_comp" + cst.FIGURE_TYPE)
        plt.clf()

        logger.info("A: finished.")

        pc1_x, pc2_x, pc3_x = get_x_sobel(da_temp)
        vvel_da = vvel_ds.VVEL.isel(time=cst.EXAMPLE_TIME_INDEX)

        for pc, pc_da in [[1, pc1_x], [2, pc2_x], [3, pc3_x]]:
            cor = ma.corrcoef(
                ma.masked_invalid(pc_da.values.ravel()),
                ma.masked_invalid(vvel_da.values.ravel()),
            )
            print("$G_x$ * PC" + str(pc), "UVEL", cor)

    # Make figures B1 and B2:
    if "B1" in fig_list:
        # Figure B1: mean/std of profiles for salinity
        prep.mean_std_plot(pcm)
        plt.savefig(fig_prefix + "_mean_plot" + cst.FIGURE_TYPE, bbox_inches="tight")
        plt.clf()

        lsty.mpl_params()

    if "B2" in fig_list:

        # Figure B2: effect of pca on profiles (mirrors Figure 4 in Pauthenet et al. 2017)
        prep.pauth17_pca_profiles(pcm)
        plt.savefig(
            fig_prefix + "_pca_real_space_plot" + cst.FIGURE_TYPE, bbox_inches="tight"
        )
        plt.clf()

        lsty.mpl_params()
