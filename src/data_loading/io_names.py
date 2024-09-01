"""Defaults for naming files."""
import os
import xarray as xr
import src.constants as cst
import src.time_wrapper as twr
import src.models.make_pair_metric as tpi


@twr.timeit
def return_pair_i_metric(
    k_clusters: int = cst.K_CLUSTERS,
    pca: int = cst.D_PCS,
    save_nc: bool = True,
    t_index: int = cst.EXAMPLE_TIME_INDEX,
) -> xr.DataArray:
    """Return pair i metric.

    Args:
        k_clusters (int, optional): Number of
               clusters. Defaults to cst.K_CLUSTERS.
        pca (int, optional): Number of principal components. Defaults to cst.D_PCS.
        save_nc (bool, optional): Whether or not to save the resulting dataset.
            Defaults to True.
        t_index (int, optional): Time index cst.EXAMPLE_TIME_INDEX.

    Returns:
        xr.DataArray: pair i metric.
    """
    link_to_netcdf = return_name(k_clusters, pca) + ".nc"
    ds = xr.open_dataset(link_to_netcdf)
    print(ds.__str__())
    batch_size = 2
    for i in range(t_index, t_index + batch_size, batch_size):
        print("running", i)
        if save_nc:
            da = tpi.pair_i_metric(
                ds.isel(time=slice(i, i + batch_size)), threshold=0.05
            )
            print("not saving")
        else:
            da = (
                xr.open_dataset(_return_pair_name(k_clusters, pca) + ".nc")
                .to_array()
                .isel(time=slice(i, i + batch_size))
            )

    return da


def return_name(k_clusters: int, pca_components: int) -> str:
    """Return name.

    Args:
        k_clusters (int): The number of classes.
        pca_components (int): The number of pcas.

    Returns:
        str: file names.
    """
    return (
        str(cst.GEN_ROOT)
        + "/nc/i-metric-joint-k-"
        + str(k_clusters)
        + "-d-"
        + str(pca_components)
    )


def return_plot_folder(k_clusters: int, pca_components: int) -> str:
    """Return plot folder name.

    Args:
        k_clusters (int): The number of classes.
        pca_components (int): The number of pcas.

    Returns:
        str: file names.
    """
    folder = (
        "../FBSO-Report/"
        + "images/i-metric-joint-k-"
        + str(k_clusters)
        + "-d-"
        + str(pca_components)
        + "/"
    )
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def return_folder(k_clusters: int, pca_components: int) -> str:
    """Return return folder name.

    Args:
        k_clusters (int): The number of classes.
        pca_components (int): The number of pcas.

    Returns:
        str: file names.

    """
    folder = return_name(k_clusters, pca_components) + "/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def _return_pair_name(k_clusters: int, pca_components: int) -> str:
    """Return pair name.

    Args:
        k_clusters (int): The number of classes.
        pca_components (int): The number of pcas.

    Returns:
        str: file names.

    """
    return (
        str(cst.GEN_ROOT)
        + "nc/pair-i-metric-k-"
        + str(k_clusters)
        + "-d-"
        + str(pca_components)
    )


def _return_pair_folder(k_clusters: int, pca_components: int) -> str:
    """Return pair folder name.

    Args:
        k_clusters (int): The number of classes.
        pca_components (int): The number of pcas.

    Returns:
        str: file names.

    """
    folder = (
        str(cst.GEN_ROOT)
        + "/nc/pair-i-metric-k-"
        + str(k_clusters)
        + "-d-"
        + str(pca_components)
        + "/"
    )
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder
