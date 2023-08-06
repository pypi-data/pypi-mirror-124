
import numpy as np
from scipy.spatial.distance import pdist, cdist, squareform

import matplotlib.pyplot as plt
import matplotlib as mpl

import leidenalg as louvain
import igraph as ig
from sklearn.neighbors import NearestNeighbors

mpl.rcParams['figure.dpi'] = 100


def numpy_mad(mtx):
    medians = []
    for column in mtx.T:
        medians.append(np.median(column[column != 0]))
    median_distances = np.abs(
        mtx - np.tile(np.array(medians), (mtx.shape[0], 1)))
    mads = []
    for (i, column) in enumerate(median_distances.T):
        mads.append(np.median(column[mtx[:, i] != 0]))
    return np.array(mads)


def ssme(mtx, axis=None):
    medians = np.median(mtx, axis=0)
    median_distances = mtx - np.tile(np.array(medians), (mtx.shape[0], 1))
    ssme = np.sum(np.power(median_distances, 2), axis=axis)
    return ssme


def hacked_louvain(knn, resolution=1):

    g = ig.Graph()
    g.add_vertices(knn.shape[0])  # this adds adjacency.shape[0] vertices
    edges = [(s, t) for s in range(knn.shape[0]) for t in knn[s]]

    g.add_edges(edges)



    if g.vcount() != knn.shape[0]:
        logging.warning(
            f'The constructed graph has only {g.vcount()} nodes. '
            'Your adjacency matrix contained redundant nodes.'
        )

    print("Searching for partition")
    part = louvain.find_partition(
        g, partition_type=louvain.RBConfigurationVertexPartition, resolution_parameter=resolution)
    clustering = np.zeros(knn.shape[0], dtype=int)
    for i in range(len(part)):
        clustering[part[i]] = i
    print("Louvain: {}".format(clustering.shape))
    return clustering


def weighted_correlation(x, weights):

    weighted_covariance = np.cov(x, fweights=weights)
    diagonal = np.diag(weighted_covariance)
    normalization = np.sqrt(np.abs(np.outer(diagonal, diagonal)))
    correlations = weighted_covariance / normalization
    correlations[normalization == 0] = 0
    correlations[np.identity(correlations.shape[0], dtype=bool)] = 1.

    return correlations

def stack_dictionaries(dictionaries):
    stacked = {}
    for dictionary in dictionaries:
        for key, value in dictionary.items():
            if key not in stacked:
                stacked[key] = []
            stacked[key].append(value)
    return stacked


def partition_mutual_information(p1, p2):
    p1 = p1.astype(dtype=float)
    p2 = p2.astype(dtype=float)
    population = p1.shape[1]
    intersections = np.dot(p1, p2.T)
    partition_size_products = np.outer(np.sum(p1, axis=1), np.sum(p2, axis=1))
    log_term = np.log(intersections) - \
        np.log(partition_size_products) + np.log(population)
    log_term[np.logical_not(np.isfinite(log_term))] = 0
    mutual_information_matrix = (intersections / population) * log_term
    return mutual_information_matrix


def count_list_elements(elements):
    dict = {}
    for element in elements:
        if element not in dict:
            dict[element] = 0
        dict[element] += 1
    return dict


def generate_feature_value_html(features, values, normalization=None, cmap=None):

    col_header = ["Features", "Values"]
    values = np.around(list(values), decimals=3)

    mtx = np.array([[str(f) for f in features], [str(v) for v in values]]).T

    html = generate_html_table(mtx, col_header=col_header)

    return html


def generate_html_table(mtx, row_header=None, col_header=None, colors=None):

    header = []
    rows = []

    if col_header is not None:
        if row_header is not None:
            header.append(f"<th></th>")
        for header_element in col_header:
            header.append(f'<th scope="col">{header_element}</th>')

    if row_header is None:
        row_header = ["", ] * mtx.shape[0]
    else:
        row_header = [f'<th scope="row">{str(rh)}</th>' for rh in row_header]

    if colors is None:
        colors = np.zeros((*mtx.shape, 4))

    for row, row_colors, rh in zip(mtx, colors, row_header):
        row_inner = []
        for element, c_val in zip(row, row_colors):
            r, g, b, a = c_val * 100
            a /= 3
            color_tag = f'style="background-color:rgba({r}%,{g}%,{b}%,{a}%);"'
            row_inner.append(f"<td {color_tag}>{element}</td>")
        row_str = "".join(["<tr>", f"{rh}", *row_inner, "</tr>"])
        rows.append(row_str)

    html_elements = [
        '<table>',
        "<style>",
        "th,td {padding:5px; min-width:30px;max-width:30px;}",
        "td {width=30px;}"
        "th {border-bottom:2px solid black;border-right:2px solid black;}"
        "</style>",
        "<tr>",
        *header,
        "</tr>",
        *rows,
        "</table>",
    ]

    return "".join(html_elements)


def generate_cross_reference_table(mtx, features):

    # Generate color values

    cmap = mpl.cm.get_cmap("bwr")
    colors = cmap(mtx)

    html = generate_html_table(
        mtx, row_header=features, col_header=features, colors=colors)

    return html


def js_wrap(name, content):
    return f"<script> let {name} = {content};</script>"


def fast_knn(elements, k, neighborhood_fraction=.01, metric='euclidean'):


    """
    Finds the indices of k nearest neighbors for each sample in a matrix, using any of the standard scipy distance metrics.

    Arguments:
    Elements: NxM matrix of N elements, M features. This is the thing we are giving you k-nearest-neighbors of.
    k: uint < N. The number of nearest neighbors to find.
    Neighborhood fraction: don't worry about it. (The number of fragments that the input is divided into to evaluate the triangle inequality. For REALLY huge inputs try setting it lower, like .001)

    What's so special about this function? Isn't there a builtin that does this? Yes. This function is special because it does not have to compute the entire pairwise distance matrix between each element in elements and each other element. For large numbers of elements this saves time and space.

    This is only guaranteed correct when used with a TRUE METRIC THAT OBEYS THE TRIANGLE INEQUALITY

    (but realistically it works sort of ok even if that's not true)

    """

    nearest_neighbors = np.zeros((elements.shape[0], k), dtype=int)
    complete = np.zeros(elements.shape[0], dtype=bool)

    neighborhood_size = max(
        k * 3, int(elements.shape[0] * neighborhood_fraction))
    anchor_loops = 0

    while np.sum(complete) < complete.shape[0]:

        anchor_loops += 1

        available = np.arange(complete.shape[0])[~complete]
        np.random.shuffle(available)
        anchors = available[:int(complete.shape[0] / neighborhood_size) * 3]

        for anchor in anchors:
            print(f"Complete:{np.sum(complete)}\r", end='')

            if metric == "sister":
                anchor_distances = sister_distance(
                    elements[anchor].reshape(1, -1), elements)[0]
            else:
                anchor_distances = cdist(elements[anchor].reshape(
                    1, -1), elements, metric=metric)[0]

            neighborhood = np.argpartition(anchor_distances, neighborhood_size)[
                :neighborhood_size]
            anchor_local = np.where(neighborhood == anchor)[0]

            if metric == "sister":
                local_distances = sister_distance(elements[neighborhood])
            else:
                local_distances = squareform(
                    pdist(elements[neighborhood], metric=metric))

            anchor_to_worst = np.max(local_distances[anchor_local])

            for i, sample in enumerate(neighborhood):
                if not complete[sample]:

                    # First select the indices in the neighborhood that are knn
                    best_neighbors_local = np.argpartition(
                        local_distances[i], k + 1)

                    # Next find the worst neighbor among the knn observed
                    best_worst_local = best_neighbors_local[np.argmax(
                        local_distances[i][best_neighbors_local[:k + 1]])]
                    # And store the worst distance among the local knn
                    best_worst_distance = local_distances[i, best_worst_local]
                    # Find the distance of the anchor to the central element
                    anchor_distance = local_distances[anchor_local, i]

                    # By the triangle inequality the closest any element outside the neighborhood
                    # can be to element we are examining is the criterion distance:
                    criterion_distance = anchor_to_worst - anchor_distance

                    # Therefore if the criterion distance is greater than the best worst distance, the local knn
                    # is also the best global knn

                    if best_worst_distance >= criterion_distance:
                        continue
                    else:
                        # Before we conclude we must exclude the sample itself from its
                        # k nearest neighbors
                        best_neighbors_local = [
                            bn for bn in best_neighbors_local[:k + 1] if bn != i]
                        # Finally translate the local best knn to the global indices
                        best_neighbors = neighborhood[best_neighbors_local]

                        nearest_neighbors[sample] = best_neighbors
                        complete[sample] = True
    print("\n")

    return nearest_neighbors


def double_fast_knn(elements1, elements2, k, neighborhood_fraction=.01, metric='cosine'):

    """
    See also fast_knn

    This is fast_knn where we have two sets of elements. The elements are matched (for nodes each element in set 2 is a sister of the node in set 1). We use it when we wish to find a KNN where the average of the two sets of distances is used. This is useful for incorporating the relatives of nodes when computing a KNNfor node clustering. Why not simply find the average of the two matrices?

    Same rationale as fast_knn: We don't have to compute the whole distance matrix, only small chunks of it.
    """

    if elements1.shape != elements2.shape:
        raise Exception("Average metric knn inputs must be same size")

    nearest_neighbors = np.zeros((elements1.shape[0], k), dtype=int)
    complete = np.zeros(elements1.shape[0], dtype=bool)

    neighborhood_size = max(
        k * 3, int(elements1.shape[0] * neighborhood_fraction))
    anchor_loops = 0

    while np.sum(complete) < complete.shape[0]:

        anchor_loops += 1

        available = np.arange(complete.shape[0])[~complete]
        np.random.shuffle(available)
        anchors = available[:int(complete.shape[0] / neighborhood_size) * 3]

        for anchor in anchors:
            print(f"Complete:{np.sum(complete)}\r", end='')

            ad_1 = cdist(elements1[anchor].reshape(
                1, -1), elements1, metric=metric)[0]
            ad_2 = cdist(elements2[anchor].reshape(
                1, -1), elements2, metric=metric)[0]
            anchor_distances = (ad_1 + ad_2) / 2

    #         print(f"anchor:{anchor}")

            neighborhood = np.argpartition(anchor_distances, neighborhood_size)[
                :neighborhood_size]
            anchor_local = np.where(neighborhood == anchor)[0]

    #         print(neighborhood)

            ld_1 = squareform(pdist(elements1[neighborhood], metric=metric))
            ld_2 = squareform(pdist(elements2[neighborhood], metric=metric))
            local_distances = (ld_1 + ld_2) / 2

            anchor_to_worst = np.max(local_distances[anchor_local])

            for i, sample in enumerate(neighborhood):
                if not complete[sample]:

                    # First select the indices in the neighborhood that are knn
                    best_neighbors_local = np.argpartition(
                        local_distances[i], k + 1)

                    # Next find the worst neighbor among the knn observed
                    best_worst_local = best_neighbors_local[np.argmax(
                        local_distances[i][best_neighbors_local[:k + 1]])]
                    # And store the worst distance among the local knn
                    best_worst_distance = local_distances[i, best_worst_local]
                    # Find the distance of the anchor to the central element
                    anchor_distance = local_distances[anchor_local, i]

                    # By the triangle inequality the closest any element outside the neighborhood
                    # can be to element we are examining is the criterion distance:
                    criterion_distance = anchor_to_worst - anchor_distance

                    # Therefore if the criterion distance is greater than the best worst distance, the local knn
                    # is also the best global knn

                    if best_worst_distance >= criterion_distance:
                        continue
                    else:
                        # Before we conclude we must exclude the sample itself from its
                        # k nearest neighbors
                        best_neighbors_local = [
                            bn for bn in best_neighbors_local[:k + 1] if bn != i]
                        # Finally translate the local best knn to the global indices
                        best_neighbors = neighborhood[best_neighbors_local]

                        nearest_neighbors[sample] = best_neighbors
                        complete[sample] = True
    print("\n")

    return nearest_neighbors

def sister_distance(sisters_1, sisters_2=None):
    if sisters_2 is None:
        sisters_2 = sisters_1.copy()

    # Compute distances of samples to others using the sister encoding
    product = np.dot(sisters_1, sisters_2.T)
    populations_1 = np.sum((sisters_1 != 0).astype(dtype=int), axis=1)
    populations_2 = np.sum((sisters_2 != 0).astype(dtype=int), axis=1)
    dot_min = np.zeros((sisters_1.shape[0], sisters_2.shape[0]))
    dot_max = np.zeros((sisters_1.shape[0], sisters_2.shape[0]))

    for i in range(sisters_1.shape[0]):
        dot_min[i] = populations_2
        dot_max[i] = populations_2
        dot_min[i][populations_2 > populations_1[i]] = populations_1[i]
        dot_max[i][populations_2 < populations_1[i]] = populations_1[i]

    product = product + dot_min

    return 1 -(product  / (2*dot_max))


def jackknife_variance(values):
    squared_values = np.power(values, 2)
    n = squared_values.shape[0]
    sum = np.sum(squared_values, axis=0)
    excluded_sum = sum - squared_values
    excluded_mse = excluded_sum / (n - 1)
    jackknifed = np.var(
        excluded_mse, axis=0) * (n - 1)

    return jackknifed
