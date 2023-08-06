"""This module gathers all plotting functions.

All those functions use `matplotlib <https://matplotlib.org/>`_.

.. todo::
    * add somewhere high level functions to draw specific mcda data types
"""
from typing import Any, List, Union, cast

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path as MPath
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

from ..core.aliases import NumericValue


def piecewise_linear_colormap(
    colors: Any, name: str = "cmap"
) -> mcolors.LinearSegmentedColormap:
    """Create piecewise linear colormap.

    :param colors: list of any type of color accepted by :mod:`matplotlib`
    :param name: name of the created colormap
    :return: piecewise linear colormap
    """
    return mcolors.LinearSegmentedColormap.from_list(name, colors)


def plot_linespoints(
    ax: Any,
    x: Union[List[str], List[NumericValue]],
    y: Union[List[str], List[NumericValue]],
    xticklabels: List[str] = None,
    yticklabels: List[str] = None,
    xtick_labels_options: dict = None,
    ytick_labels_options: dict = None,
    stem: bool = False,
    plot_options: dict = None,
):
    """Plot one serie of points.

    (`xticklabels`, `xtick_labels_options`) and (`yticklabels`,
    `ytick_labels_options`) are only used when `x` (respectively `y`) are
    :class:`str` values.

    `xticklabels` (respectively `yticklabels`) are used to order the `x` values
    (respectively `y`) on their axis.

    `plot_options` must be different depending on `stem` value:

    * ``True``:
        `plot_options` can contain up to 3 options that will fed to
        intended target function:

        * 'baseline':
            :class:`dict` which values set the stem baseline
            using :func:`matplotlib.pyplot.setp`

        * 'markerline':
            :class:`dict` which values set the stem markerline
            using :func:`matplotlib.pyplot.setp`

        * 'stemlines':
            :class:`dict` which values set the stem stemlines
            using :func:`matplotlib.pyplot.setp`

    * ``False``: `plot_options` contains options fed to `plot` function

    :param ax: axis on which to draw plot
    :param x: abscissa
    :param y: ordinates
    :param xticklabels: ordered list of abscissa labels
    :param yticklabels: ordered list of ordinate labels
    :param xtick_labels_options: options used when setting `xticklabels`
    :param ytick_labels_options: options used when setting `yticklabels`
    :param stem: if ``True`` use stem plot, otherwise regular `plot`
    :param plot_options: options fed to the chosen plotting method
    """
    xtick_labels_options = (
        {} if xtick_labels_options is None else xtick_labels_options
    )
    ytick_labels_options = (
        {} if ytick_labels_options is None else ytick_labels_options
    )
    plot_options = {} if plot_options is None else plot_options

    xx = x
    yy = y
    xticks = None
    yticks = None
    if isinstance(x[0], str):
        x = cast(List[str], x)
        if xticklabels is None:
            xticklabels = [*set(xxx for xxx in x)]
        xx = cast(List[NumericValue], [xticklabels.index(xxx) for xxx in x])
        xticks = np.arange(len(xticklabels))
    if isinstance(y[0], str):
        y = cast(List[str], y)
        if yticklabels is None:
            yticklabels = [*set(yyy for yyy in y)]
        yy = cast(List[NumericValue], [yticklabels.index(yyy) for yyy in y])
        yticks = np.arange(len(yticklabels))

    if stem:
        # Discrete plot
        markerline, stemlines, baseline = ax.stem(xx, yy)
        if "markerline" in plot_options:
            for k, v in plot_options["markerline"]:
                plt.setp(markerline, k, v)
        if "stemlines" in plot_options:
            for k, v in plot_options["stemlines"]:
                plt.setp(stemlines, k, v)
        if "baseline" in plot_options:
            for k, v in plot_options["baseline"]:
                plt.setp(baseline, k, v)
    else:
        # Regular plot
        ax.plot(xx, yy, **plot_options)

    if type(x[0]) is str:
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, **xtick_labels_options)
    if type(y[0]) is str:
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels, **ytick_labels_options)


def plot_barchart(
    ax: Any,
    x: List[str],
    y: Union[List[str], List[NumericValue]],
    yticklabels: List[str] = None,
    plot_options: dict = None,
    xtick_labels_options: dict = None,
    ytick_labels_options: dict = None,
):
    """Plot barchart.

    (`yticklabels`, `ytick_labels_options`) are only used when `y` are
    :class:`str` values.

    `yticklabels` are used to order the `y` values on their axis.

    :param ax: axis on which to draw plot
    :param x: labels used for abscissa
    :param y: labels or numeric values used for ordinates
    :param yticklabels: ordered list of ordinate labels
    :param plot_options: options fed to `bar` function
    :param xtick_labels_options: options used when setting `xticklabels`
    :param ytick_labels_options: options used when setting `yticklabels`
    """
    plot_options = {} if plot_options is None else plot_options
    xtick_labels_options = (
        {} if xtick_labels_options is None else xtick_labels_options
    )
    ytick_labels_options = (
        {} if ytick_labels_options is None else ytick_labels_options
    )
    xx = np.arange(len(x))
    yy = y
    yticks = None
    if isinstance(y[0], str):
        y = cast(List[str], y)
        if yticklabels is None:
            yticklabels = [*set(yyy for yyy in y)]
        yy = cast(List[NumericValue], [yticklabels.index(yyy) for yyy in y])
        yticks = np.arange(len(yticklabels))
    ax.bar(xx, yy, **plot_options)
    ax.set_xticks(xx)
    ax.set_xticklabels(x, **xtick_labels_options)
    if yticklabels is not None:
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels, **ytick_labels_options)


def plot_piechart(
    ax: Any,
    x: List[str],
    y: List[NumericValue],
    plot_options: dict = None,
    axis: str = None,
    strict: bool = True,
):
    """Plot pie chart.

    :param ax: axis on which to draw plot
    :param x: labels used for abscissa
    :param y: numeric values used for ordinates
    :param plot_options: options fed to `pie` function
    :param axis: option fed to `axis` function (ex: 'equal')
    :param strict:
        if ``False``, it allows to represent negative values by partial
        normalization
    """
    yy = y if strict or min(y) >= 0 else [yyy - min(y) for yyy in y]
    plot_options = {} if plot_options is None else plot_options
    ax.pie(yy, labels=x, **plot_options)
    if axis is not None:
        ax.axis(axis)


def create_radar_projection(num_vars: int, frame: str = "circle"):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    :param num_vars: number of variables for radar chart
    :param frame: shape of frame surrounding axes ('circle' or 'polygon')

    .. note::
        it is necessary to call this function before plotting star plots with
        :func:`plot_star_chart` (with the same amount of variables)
    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = "radar"
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location("N")

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == "circle":
                return Circle((0.5, 0.5), 0.5)
            elif frame == "polygon":
                return RegularPolygon(
                    (0.5, 0.5), num_vars, radius=0.5, edgecolor="k"
                )
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == "circle":
                return super()._gen_axes_spines()
            elif frame == "polygon":
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(
                    axes=self,
                    spine_type="circle",
                    path=MPath.unit_regular_polygon(num_vars),
                )
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(
                    Affine2D().scale(0.5).translate(0.5, 0.5) + self.transAxes
                )
                return {"polar": spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)


def plot_star_chart(
    ax: Any,
    x: List[str],
    y: List[NumericValue],
    rgrids: List[NumericValue] = None,
    y_lim: List[NumericValue] = None,
    alpha: NumericValue = None,
    plot_options: dict = None,
):
    """Plot star chart.

    :param ax: axis on which to draw plot
    :param x: labels used for abscissa
    :param y: numeric values used for ordinates
    :param rgrids: radial ticks to set for the plot
    :param y_lim: radial limits to set for the plot
    :param alpha:
        if set, surface of under the plotted values will be filled with color
        provided in `plot_options` with this value as the `alpha` channel
        (transparency)
    :param plot_options: options fed to star chart `plot` function
    """
    plot_options = {} if plot_options is None else plot_options

    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, len(x), endpoint=False)
    if rgrids is not None:
        ax.set_rgrids(rgrids)
    if y_lim is not None:
        ax.set_ylim(*y_lim)
    ax.plot(theta, y, **plot_options)
    if alpha is not None:
        if "color" in plot_options:
            ax.fill(theta, y, facecolor=plot_options["color"], alpha=alpha)
        else:
            ax.fill(theta, y, alpha=alpha)
    ax.set_varlabels(x)


def plot_chart(
    ax: Any,
    x: List = None,
    y: List = None,
    chart_type: str = "default",
    **kwargs: Any,
):
    """Plot a chart.

    :param ax: axis on which to draw plot
    :param x: abscissas
    :param y: ordinates
    :param chart_type: type of chart to draw:

        * 'bar': :func:`plot_barchart`
        * 'pie': :func:`plot_piechart`
        * 'star': :func:`plot_star_chart`
        * 'points`: :func:`plot_points`

    :param kwargs: other parameters fed to chosen plot function
    """
    x = [] if x is None else x
    y = [] if y is None else y
    if chart_type == "bar":
        plot_barchart(ax, x, y, **kwargs)
    elif chart_type == "pie":
        plot_piechart(ax, x, y, **kwargs)
    elif chart_type == "star":
        plot_star_chart(ax, x, y, **kwargs)
    else:
        plot_linespoints(ax, x, y, **kwargs)


def plot_subplot_chart(
    ax: Any,
    plots: List[dict],
    xlabel: str = None,
    ylabel: str = None,
    title: str = None,
    chart_type: str = "default",
):
    """Plot superposed charts and their axis labels and title.

    :param ax: axis on which to draw plot
    :param plots: list of parameters fed to chosen plot function for each plot
    :param xlabel: label for x axis
    :param ylabel: label for y axis
    :param title: title of subplot being plotted
    :param chart_type: type of chart to draw (see: :func:`plot_chart` for list)
    """
    for plot in plots:
        plot_chart(ax, chart_type=chart_type, **plot)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)


def plot_subplots(
    plots: List[dict],
    ncols: int = 0,
    nrows: int = 0,
    first_axis: int = 0,
    fig: Any = None,
    fig_options: dict = None,
) -> Any:
    """Plot a figure with subplots.

    :param plots:
        list of options for each subplot being plotted, each fed to
        :func:`plot_subplot_chart`
    :param ncols: desired number of columns for subplot layout
    :param nrows: desired number of rows for subplot layout
    :param first_axis: plotting layout order:

        * ``0``: columns-first
        * ``1``: rows-first

    :param fig: figure on which to draw (created if not provided)
    :param fig_options: options fed to :func:`matplotlib.pyplot.subplots`
    :return: drawn figure
    """
    fig_options = {} if fig_options is None else fig_options
    if ncols == 0 and nrows == 0:
        ncols = 1
        nrows = len(plots)
    elif nrows == 0:
        nrows = int(np.ceil(len(plots) / ncols))
    elif ncols == 0:
        ncols = int(np.ceil(len(plots) / nrows))

    if fig is None:
        fig, axes = plt.subplots(ncols=ncols, nrows=nrows, **fig_options)
    else:
        axes = fig.axes

    if nrows > 1 and ncols > 1:
        if first_axis == 0:
            axes = [axes[i, j] for i in range(nrows) for j in range(ncols)]
        else:
            axes = [axes[i, j] for j in range(ncols) for i in range(nrows)]
    if len(plots) > 1:
        for i in range(len(plots), len(axes)):
            axes[i].remove()
    else:
        axes = cast(List[Any], [axes])

    for plot, ax in zip(plots, axes):
        plot_subplot_chart(ax, **plot)
    return fig


def plot_superposed_values(
    plots: List[dict],
    chart_type: str = "default",
    fig: Any = None,
    fig_options: dict = None,
    ax_options: dict = None,
    subplot_options: dict = None,
) -> Any:
    """Plot charts superposed on one axis.

    :param plots: list of parameters fed to chosen plot function for each plot
    :param chart_type: type of chart to draw (see: :func:`plot_chart` for list)
    :param fig: figure on which to draw (created if not provided)
    :param fig_options: options fed to :func:`matplotlib.pyplot.figure`
    :param ax_options:
        options fed to :func:`plot_subplot_chart` but not passed further
    :param subplot_options: options fed to `fig.add_subplot`
    :return: drawn figure
    """
    ax_options = {} if ax_options is None else ax_options
    fig_options = {} if fig_options is None else fig_options
    subplot_options = {} if subplot_options is None else subplot_options
    if fig is None:
        fig = plt.figure(**fig_options)
    ax = fig.add_subplot(**subplot_options)
    plot_subplot_chart(ax=ax, plots=plots, chart_type=chart_type, **ax_options)
    return fig


def plot_labelled_values(
    labels: Any,
    values: Any,
    chart_type: str = "default",
    fig: Any = None,
    fig_options: dict = None,
    ax_options: dict = None,
    subplot_options: dict = None,
    **kwargs: Any,
) -> Any:
    """Plot one chart on one figure.

    :param labels: abscissa
    :param values: ordinates
    :param chart_type: type of chart to draw (see: :func:`plot_chart` for list)
    :param fig: figure on which to draw (created if not provided)
    :param fig_options: options fed to :func:`matplotlib.pyplot.figure`
    :param ax_options:
        options fed to :func:`plot_subplot_chart` but not passed further
    :param subplot_options: options fed to `fig.add_subplot`
    :param kwargs:
        options fed to chosen plotting function (see :func:`plot_chart` for
        list)
    :return: drawn figure
    """
    ax_options = {} if ax_options is None else ax_options
    fig_options = {} if fig_options is None else fig_options
    subplot_options = {} if subplot_options is None else subplot_options
    if fig is None:
        fig = plt.figure(**fig_options)
    ax = fig.add_subplot(**subplot_options)
    plots = {"x": labels, "y": values}
    plot_subplot_chart(
        ax=ax, plots=[{**plots, **kwargs}], chart_type=chart_type, **ax_options
    )
    return fig
