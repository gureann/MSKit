import typing

import matplotlib.pyplot as plt
import numpy as np


def init_container(container=None, **fig_args):
    if container is None:
        container = plt.figure(*fig_args)
    if isinstance(container, plt.Figure):
        new_ax_method = container.add_axes
    elif isinstance(container, plt.Axes):
        new_ax_method = container.inset_axes
    else:
        raise ValueError(f'container should be `Figure` or `Axes` or `None`, now {type(container)}')
    return container, new_ax_method


def init_isometric_axes(
        left_init=0.05, bottom_init=0.05, right_end=0.9, top_end=0.9,
        ax_col_gap=0.1, ax_row_gap=0.1,
        row_num=2, col_num=5,
        total_num=None,
        container=None,
        **fig_args
):  # TODO support new ax args
    container, new_ax_method = init_container(container=container, **fig_args)

    if isinstance(ax_col_gap, (float, int)):
        ax_col_gap = [ax_col_gap] * (col_num - 1)
    if isinstance(ax_row_gap, (float, int)):
        ax_row_gap = [ax_row_gap] * (row_num - 1)
    else:
        ax_row_gap = ax_row_gap[::-1]
    if not total_num:
        total_num = row_num * col_num

    fig_length = right_end - left_init
    fig_height = top_end - bottom_init

    row_height = (fig_height - sum(ax_row_gap)) / row_num
    col_length = (fig_length - sum(ax_col_gap)) / col_num

    ax_x = [left_init + sum(ax_col_gap[:i]) + col_length * i for i in range(col_num)]
    ax_y = [top_end - sum(ax_row_gap[:i]) - row_height * (i + 1) for i in range(row_num)]

    ax_num = 0
    axes_list = []
    for row_index, y in enumerate(ax_y):
        for col_index, x in enumerate(ax_x):
            if ax_num == total_num:
                break
            ax = new_ax_method([x, y, col_length, row_height])
            axes_list.append(ax)
            ax_num += 1

    return container, axes_list


def init_weighted_axes(
        x_start=0.05,
        x_end=0.9,
        y_start=0.05,
        y_end=0.9,

        col_gap: typing.Union[float, int, list, tuple, np.ndarray] = 0.1,
        row_gap: typing.Union[float, int, list, tuple, np.ndarray] = 0.1,

        row_num=None,
        col_num=None,
        width_weights=None,
        height_weights=None,

        return_type='array',  # array / dict
        axes_names=None,  # list of names for all generated axes (row * col), or two tuples in list to boardcast to a matrix

        container=None,
        **fig_args,
):
    """

    :param left_start:
    :param bottom_start:
    :param right_end:
    :param top_end:

    :param ax_col_gap:
    :param ax_row_gap:
    :param row_num:
    :param col_num:
    :param ax_width_weights:
    :param ax_height_weights:
    :param return_type:
    :param row_axes_names:
    :param col_axes_names:
    :param container: figure or ax
        If not defined, will init a figure
    :param ax_args:
        will be passed to function for init new ax (fig.add_axes or ax.inset_axes)

    sharex: 'all', 'col', `[(1, 3, 5), (0, 2)]`, `2/2-2/4;3/1-3/3;2/0-2/1`


    :return:
    """
    container, new_ax_method = init_container(container=container, **fig_args)


    ax_x_start = 0.12
    ax_x_end = 0.99
    ax_x_gap = 0.025
    ax_x_group_gap = 0.0
    ax_width_weights = [4, 4, 4]
    ax_x_width = (
            (ax_x_end - ax_x_start - ax_x_group_gap - ax_x_gap * (len(ax_width_weights) - 1))
            / sum(ax_width_weights)
            * np.asarray(ax_width_weights))

    ax_y_start = 0.12
    ax_y_end = 0.8
    ax_y_gap = 0.05
    ax_y_group_gap = 0.0
    ax_y_height_weights = [3, 4]
    ax_y_height = (
            (ax_y_end - ax_y_start - ax_y_group_gap - ax_y_gap * (len(ax_y_height_weights) - 1))
            / sum(ax_y_height_weights)
            * np.asarray(ax_y_height_weights))


    ax_x = ax_x_start + sum(ax_x_width[:st_idx]) + ax_x_gap * st_idx

    _ax_y = ax_y_end - sum(ax_y_height[:1]) - ax_y_gap * 0
    if st_idx == 0:
        ax_count = f.add_axes([ax_x, _ax_y, ax_x_width[st_idx], ax_y_height[0]])
    else:
        ax_count = f.add_axes([ax_x, _ax_y, ax_x_width[st_idx], ax_y_height[0]], sharey=axes_count[0])
    axes_count.append(ax_count)

    _ax_y = ax_y_end - sum(ax_y_height[:2]) - ax_y_gap * 1
    if st_idx == 0:
        ax_error = f.add_axes([ax_x, _ax_y, ax_x_width[st_idx], ax_y_height[1]], sharex=ax_count)
    else:
        ax_error = f.add_axes([ax_x, _ax_y, ax_x_width[st_idx], ax_y_height[1]], sharex=ax_count, sharey=axes_error[0])
    axes_error.append(ax_error)
