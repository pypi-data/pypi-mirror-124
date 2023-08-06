import json
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy.sparse.csgraph import connected_components
from scipy.stats import chi2 as chisq


def bucket_column(df: pd.DataFrame,
                  col: str,
                  n_buckets: int=5,
                  label_col: str='label',
                  return_splits: bool=False,
                  drop: bool=False,
                  **kwargs):
    """Turn a column of ordinal values (or possibly continuous, though untested (bin first?))
    into a n_buckets binary columns.
    Combines buckets iteratively based on chi-squared value of adjacent buckets.

    Args:
        df: the data
        col: column name to bucketize
        n_buckets: number of buckets to create
        label_col: column of binary data target
        v: verbosity of merging functions
        method: 'iterative' or 'heirarchical'

    Returns:
        df: data without col, with buckets
    """
    # massage data
    feat_vec = df[[col, label_col]]
    x = get_label_counts(feat_vec, col, label_col=label_col)
    # get cuts
    cuts = chi_merge_fixed(x, n_buckets, **kwargs)
    # make bin edges for cutting
    cuts_array = [x.index[0]]
    cuts_array += [cuts[i] for i in range(len(cuts))]
    cuts_array.append(x.index[-1] + 1)
    cuts_array = np.array(cuts_array)
    # add new columns directly onto df
    df = apply_cuts(df, col, cuts_array)
    # return df without the original column
    if return_splits:
        if drop:
            return df.drop([col], axis=1), cuts_array
        else:
            return df, cuts_array
    if drop:
        return df.drop([col], axis=1)
    else:
        return df


def apply_cuts(df, col, cuts_array):
    for i in range(len(cuts_array) - 1):
        # cut = x.index.values[(x.index.values >= cuts_array[i]) & (x.index.values < cuts_array[i + 1])]
        # print(cut)
        new_name = col + str(cuts_array[i]) + "-" + str(cuts_array[i + 1])
        # print(new_name)
        df[new_name] = ((df[col].values >= cuts_array[i]) & (df[col].values < cuts_array[i + 1])) * 1.0
    return df


def bucket_column_nominal(df: pd.DataFrame,
                          col: str,
                          n_buckets: int=5,
                          label_col: str='label',
                          return_splits: bool=False,
                          drop: bool=False,
                          **kwargs):
    """Turn a column of nominal values into a n_buckets binary columns.
    Combines buckets iteratively based on chi-squared value between all buckets.

    Args:
        df: the data
        col: column name to bucketize
        n_buckets: number of buckets to create
        label_col: column of binary data target
        v: verbosity of merging functions
        method: 'iterative' or 'heirarchical'

    Returns:
        df: data without col, with buckets
    """
    # massage data
    feat_vec = df[[col, label_col]]
    x = get_label_counts(feat_vec, col, label_col=label_col)
    # get cuts
    buckets = chi_merge_fixed_nominal(x, n_buckets, **kwargs)
    print(buckets)
    bucket_values = [[x.index[i] for i in bucket] for bucket in buckets]
    print(bucket_values)
    # add new columns directly onto df
    df = apply_cuts_nominal(df, col, bucket_values)
    # return df without the original column
    if return_splits:
        if drop:
            return df.drop([col], axis=1), bucket_values
        else:
            return df, bucket_values
    if drop:
        return df.drop([col], axis=1)
    else:
        return df


def apply_cuts_nominal(df, col, buckets):
    for bucket in buckets:
        # cut = x.index.values[(x.index.values >= cuts_array[i]) & (x.index.values < cuts_array[i + 1])]
        # print(cut)
        new_name = col + "_" + "_".join(list(map(str, bucket)))
        # print(new_name)
        df[new_name] = df[col].isin(bucket) * 1.0
    return df


def chi_merge_fixed(x, n_buckets, v=False, method='iterative'):
    """ Perform chi merge algorithm on a column.
    Merge buckets until only n_buckets remain.

    The step is adjusted adapatively, until exactly n_buckets are left.
    With method='iterative', will merge all buckets under threshold (potentially
    merging more than one bucket at once).
    With method='heirarchical', will only merge once per step.

    Inputs:
        x: DataFrame with [n_values x n_classes]

    Outputs:
        dictionary of cuts {0: cut[0], 1: cut[1]}
        (could just be an array)
    """
    step = 1.0
    m = 2
    cutoff = 0.0
    max_iter = 1000

    printv(x, v)
    printv(x.shape, v)
    buckets = x.shape[0]
    num_label_classes = x.shape[1]  # df = num_label_classes - 1
    consective_adds = 0
    n_iter = 0
    while buckets > n_buckets:
        n_iter += 1
        if n_iter > max_iter or step < 0.000001:
            print("Hit max num iterations...")
            break
        cutoff += step
        printv(cutoff, v)
        all_chisq = get_chisquare_array(x, num_label_classes, m)
        printv(all_chisq, v)
        printv(all_chisq.shape, v)
        to_merge = (np.arange(x.shape[0] - m + 1) + m)[all_chisq < cutoff]
        printv(to_merge, v)
        # speed up
        if len(to_merge) == 0:
            consective_adds += 1
            if consective_adds > 20:
                step = step * 2
                consective_adds = 0
        else:
            consective_adds = 0
        # slow down
        if buckets - to_merge.shape[0] < n_buckets and method != 'heirarchical':
            cutoff -= step
            step = step / 2.0
            continue
        if method == 'iterative':
            to_merge = to_merge
        elif method == 'heirarchical':
            to_merge = np.array([np.argmin(all_chisq) + m])
        # do the merging
        # reverse the order so that we don't mess up indexing
        for i in np.flipud(to_merge):
            for j in range(m - 1):
                printv('merging..' + str(x.index[[i - (j + 1)]]), v)
                # sum # observations for each label class, writing them into the
                # lowest index
                x.iloc[i - m] += x.iloc[i - (j + 1)]
                # delete the rows that are not the lowest index
                x = x.drop(x.index[[i - (j + 1)]])
        buckets = x.shape[0]
    return {i - 1: x.index[i] for i in range(1, len(x))}


def chi_merge_fixed_nominal(x, n_buckets, v=False, method='iterative'):
    """ Perform chi merge algorithm on a column.
    Merge buckets until only n_buckets remain.

    The step is adjusted adapatively, until exactly n_buckets are left.
    With method='iterative', will merge all buckets under threshold (potentially
    merging more than one bucket at once).
    With method='heirarchical', will only merge once per step.

    Inputs:
        x: DataFrame with [n_values x n_classes]

    Outputs:
        dictionary of cuts {0: cut[0], 1: cut[1]}
        (could just be an array)
    """
    step = 1
    cutoff = 0.0
    max_iter = 1000

    printv(method, v)
    printv(x, v)
    printv(x.shape, v)
    buckets = x.shape[0]
    num_label_classes = x.shape[1]  # df = num_label_classes - 1
    consective_adds = 0
    final_buckets = [[i] for i in range(buckets)]
    n_iter = 0
    while buckets > n_buckets:
        cutoff += step
        n_iter += 1
        if n_iter > max_iter or step < 0.000001:
            print("Hit max num iterations...")
            break
        printv(cutoff, v)
        all_chisq = get_chisquare_matrix(x, num_label_classes)
        printv(all_chisq, v)
        printv(all_chisq.shape, v)
        # build the join groups
        # we can think of this as a matrix and join the connected components
        n_components, labels = connected_components(
            ((all_chisq < cutoff) & (all_chisq != 0)) * 1.0,
            directed=False,
            return_labels=True)
        printv(labels, v)
        components = [np.arange(x.shape[0])[labels == i] for i in range(n_components)]
        non_singleton_components = [components[i] for i in range(n_components) if components[i].shape[0] > 1]
        printv(non_singleton_components, v)
        # speed up
        if len(non_singleton_components) == 0:
            consective_adds += 1
            if consective_adds > 20:
                step = step * 2
                consective_adds = 0
        else:
            consective_adds = 0
        # slow down
        if buckets - len(non_singleton_components) < n_buckets and method != 'heirarchical':
            cutoff -= step
            step = step / 2
            continue
        if method == 'heirarchical':
            all_chisq[all_chisq == 0] = all_chisq.max()
            non_singleton_components = [np.array(np.unravel_index(np.argmin(all_chisq), all_chisq.shape))]
        # make an array of the merge-to for each of the components
        merge = []
        merge_to = []
        for c in non_singleton_components:
            c.sort()
            for i in range(1, c.shape[0]):
                merge.append(c[i])
                merge_to.append(c[0])
        printv(merge, v)
        printv(merge_to, v)
        merge = np.array(merge)
        merge_to = np.array(merge_to)
        s = np.argsort(merge)
        merge = merge[s]
        merge_to = merge_to[s]
        printv(merge, v)
        printv(merge_to, v)
        # do the merging
        for i in np.flipud(np.arange(merge.shape[0])):
            printv('merging..' + str(x.index[merge[i]]) + " into " + str(x.index[merge_to[i]]), v)
            # sum # observations for each label class, writing them into the
            # lowest index
            x.iloc[merge_to[i]] += x.iloc[merge[i]]
            # delete the rows that are not the lowest index
            x = x.drop(x.index[merge[i]])
            final_buckets[merge_to[i]] += final_buckets[merge[i]]
            final_buckets[merge[i]] = []
            final_buckets = [bucket for bucket in final_buckets if len(bucket) != 0]
        buckets = x.shape[0]
    return final_buckets


def chi_merge(x, m=2, alpha=0.05):
    """ Perform chi merge algorithm on a column.
    Iterate through the buckets and merge adjacent buckets if chisq value
    less than cutoff.

    inputs:
    x: matrix of dato chimerge
    m: how many rows to merge at one time
    alpha: 1 - desired significance level

    output: dictionary of {percentiles:max values}
    """
    # determine cut off value -- if significance level is 0.95, it's the 95th
    # percentile of chi squared distrib
    num_label_classes = x.shape[1]  # df = num_label_classes - 1
    # alpha = 0.05 # significance = 1.0 - alpha
    cutoff = chisq.ppf(1 - alpha, num_label_classes - 1)
    algo_finished = False
    while algo_finished is False:
        x, merged = merge_buckets(x, cutoff, num_label_classes, m)
        algo_finished = False if merged else True
        print('algo finished:', algo_finished)
    return {i - 1: x.index[i] for i in range(1, len(x))}


def get_label_counts(feat_vec, feat_name, label_col='label'):
    """ return a table where row/index = unique values of feature vector
    and columns contain counts of each value for each label class """
    feat_vec = feat_vec.sort_values(feat_name, na_position='first')
    return feat_vec.pivot_table(index=feat_name, columns=label_col, aggfunc=np.count_nonzero, fill_value=0)


def merge_buckets(x, cutoff, k, m):
    """ starting with the lowest value of the feature vector, merge bins """
    merged = False
    i = m - 1
    while i < len(x) - 1:
        i += 1
        X2 = get_chisquare(x.iloc[i - m:i], k, m)
        if X2 < cutoff:
            merged = True
            for j in range(m - 1):
                print('merging..', x.index[[i - (j + 1)]])
                # sum # observations for each label class, writing them into the
                # lowest index
                x.iloc[i - m] += x.iloc[i - (j + 1)]
                # delete the rows that are not the lowest index
                x = x.drop(x.index[[i - (j + 1)]])
    return x, merged


def get_chisquare_array(x, k, m):
    """ get the array of chisq values """
    i = m - 1
    results = np.zeros(len(x) - m + 1)
    while i < len(x):
        i += 1
        # print(i - m)
        X2 = get_chisquare(x.iloc[i - m:i], k, m)
        results[i - m] = X2
    return results


def get_chisquare_matrix(x, k):
    """get the matrix of chisq values
    don't consider the order of things in x to be meaninful
    i.e., this will work for nominal datatypes.

    will return an upper triangular matrix.
    """
    i = 0
    results = np.zeros((len(x), len(x)))
    while i < len(x):
        j = i + 1
        while j < len(x):
            X2 = get_chisquare(x.iloc[[i, j]], k, 2)
            results[i, j] = X2
            j += 1
        i += 1
    return results


def get_chisquare(x, k, m):
    """return the chisquare value of a row and its adjacent row

    inputs:
    x: row aka 'interval' <class 'pandas.core.series.Series'>
    k: # of label classes
    m: # of rows to get chisquare value for (default 2)
    Ri: # observations in ith interval across all k label classes
    Cj: # observations in jth label class across all m intervals
    Aij: # observations in ith interval for label class j
    N: # observations across all k label classes, m intervals

    output: chi square value
    """
    Ri = X2 = 0
    N = np.sum(np.sum(x))
    for i in range(m):
        Ri = sum(x.iloc[i])
        for j in range(k):
            Cj = sum(x[x.columns[j]])
            Aij = x[x.columns[j]].iloc[i]
            Eij = Ri * Cj / float(N)
            try:
                X2 += (math.pow((Aij - float(Eij)), 2) / float(Eij))
            except ZeroDivisionError:
                pass
    return X2
