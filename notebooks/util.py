import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpl_patches
import sklearn

def color_plane_by_prediction(
    model: sklearn.base.ClassifierMixin,
    category_names: list[str],
    colormaps: list[str],
    *,
    threshold: float = 0.5,
    nbins_x: int = 100,
    nbins_y: int = 100,
    xlow: float = 0,
    xhigh: float = 1,
    ylow: float = 0,
    yhigh: float = 1,
    ax: plt.Axes = plt,
) -> list[mpl_patches.Patch]:
    """
    Color the plane with `colormaps` by regions in which `model`'s prediction probabilies exceed `threshold`.

    Returns:
        A list of Matplotlib handle objects for building a legend.

    Args:
        model: a Scikit-Learn classifier model with a `predict_proba` method.
        category_names: names of each category for the legend. (List length must be equal to the number of categories in `model`.)
        colormaps: names of Matplotlib colormaps. (List length must be equal to `category_names`.)
        threshold: cut-off threshold, used as a boundary for the fill color and drawn as a solid line.
        nbins_x: number of bins to sample in the x direction.
        nbins_y: number of bins to sample in the y direction.
        xlow: minimum x to sample.
        xhigh: maximum x to sample.
        ylow: minimum y to sample.
        yhigh: maximum y to sample.
        ax: Matplotlib axis to draw on.
    """

    # compute the three probabilities for every 2D point in the background
    background_x, background_y = np.meshgrid(np.linspace(xlow, xhigh, nbins_x), np.linspace(ylow, yhigh, nbins_y))
    background_2d = np.column_stack([background_x.ravel(), background_y.ravel()])
    probabilities = model.predict_proba(background_2d)
    
    # fill in regions of greater than 50% probability with the appropriate color
    fill_handles = []
    for code, (category, colormap) in enumerate(zip(category_names, colormaps)):
        ax.contourf(
            background_x, background_y, probabilities[:, code].reshape(background_x.shape),
            [threshold, 1],
            cmap=colormap,
        )
        fill_handles.append(mpl_patches.Patch(color=plt.get_cmap(colormap)(0.5), label=category))
    
    # draw contour lines where the probabilities cross the 50% threshold
    for code in range(len(category_names)):
        ax.contour(
            background_x, background_y, probabilities[:, code].reshape(background_x.shape),
            [threshold],
        )

    # for the legend
    return fill_handles