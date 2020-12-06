# @jit(nopython=True)
def go_through_with_numba(cart_prod, i_metric, sorted_version, threshold):
    if True:
        pair_i_metric_list = []

        pair_list = []

        for pair in cart_prod:
            print("pair", pair)
            """pair [0 1] pair [0 2] pair [0 3]
               pair [1 2] pair [1 3] pair [2 3]"""
            temp_list = for_loops_with_numba(pair, i_metric, sorted_version, threshold)
            if temp_list[2] == True:
                pair_list.append(temp_list[0])
                pair_i_metric_list.append(temp_list[1])
            # time, YC, XC
            # shape (60, 2, 588, 2160)
    print("pair_list", pair_list)

    return pair_i_metric_list, pair_list


# @jit(nopython=True)
def for_loops_with_numba(pair, i_metric, sorted_version, threshold):
    shape = np.shape(sorted_version)
    print("shape", shape)
    # shape (60, 2, 588, 2160)
    at_least_one_point = False
    # float32 changed from np.zeros
    pair_i_metric = np.zeros([shape[0], shape[2], shape[3]])  # , dtype='float64'
    pair_i_metric[:, :, :] = np.nan
    for i in range(shape[0]):  # 60
        for j in range(shape[2]):  # 588
            for k in range(shape[3]):  # 2160
                if np.array_equal(pair, sorted_version[i, :, j, k]):
                    # sorted_version (60, 2, 588, 2160)
                    if i_metric[i, j, k] >= threshold:
                        # i_metric (60, 588, 2160)
                        pair_i_metric[i, j, k] = i_metric[i, j, k]
                        at_least_one_point = True
    return [pair, pair_i_metric, at_least_one_point]


def pair_i_metric(ds, threshold=0.05):

    print("ds.A_B.values.shape", ds.A_B.values.shape)

    sorted_version = np.sort(ds.A_B.values, axis=1)
    print("sorted_version.shape", sorted_version.shape)
    # sorted_version (60, 2, 588, 2160)

    i_metric = ds.IMETRIC.isel(Imetric=0).values

    print("i_metric", i_metric.shape)
    # i_metric (60, 588, 2160)

    list_no = [i for i in range(int(np.nanmax(sorted_version)) + 1)]

    print("list_no", list_no)

    # list_no [0, 1, 2, 3]

    cart_prod = [
        np.array([a, b]) for a in list_no for b in list_no if a <= b and a != b
    ]
    # [array([0, 1]), array([0, 2]), array([0, 3]), array([1, 2]), array([1, 3]), array([2, 3])]

    print("cart_prod", cart_prod)

    pair_i_metric_list, pair_list = go_through_with_numba(
        cart_prod, i_metric, sorted_version, threshold
    )

    print("pair_i_metric_list", pair_i_metric_list)
    print("pair_i_metric_list len", len(pair_i_metric_list))
    print("pair_list", pair_list)
    print("pair_list len", len(pair_list))

    shape = np.shape(sorted_version)
    # shape (60, 2, 588, 2160)

    pair_i_metric_array = np.zeros(
        [len(pair_i_metric_list), shape[0], shape[2], shape[3]]
    )

    for i in range(len(pair_i_metric_list)):

        pair_i_metric_array[i, :, :, :] = pair_i_metric_list[i][:, :, :]

    pair_str_list = []

    for i in range(len(pair_list)):
        pair_str_list.append(
            str(pair_list[i][0] + 1) + " to " + str(pair_list[i][1] + 1)
        )

    da = xr.DataArray(
        pair_i_metric_array,
        dims=["pair", "time", "YC", "XC"],
        coords={
            "XC": ds.coords["XC"].values,
            "YC": ds.coords["YC"].values,
            "time": ds.coords["time"].values,
            "pair": pair_str_list,
        },
    )

    return da
