"""
contour - Plot contour table data.
"""

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    B="frame",
    S="skip",
    G="label_placement",
    W="pen",
    L="triangular_mesh_pen",
    N="no_clip",
    i="columns",
    l="label",
    C="levels",
    V="verbose",
    X="xshift",
    Y="yshift",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", i="sequence_comma", p="sequence")
def contour(self, x=None, y=None, z=None, data=None, **kwargs):
    """
    Contour table data by direct triangulation.

    Takes a matrix, (x,y,z) pairs, or a file name as input and plots lines,
    polygons, or symbols at those locations on a map.

    Must provide either *data* or *x*, *y*, and *z*.

    [TODO: Insert more documentation]

    Full option list at :gmt-docs:`contour.html`

    {aliases}

    Parameters
    ----------
    x/y/z : 1d arrays
        Arrays of x and y coordinates and values z of the data points.
    data : str or 2d array
        Either a data file name or a 2d numpy array with the tabular data.
    {J}
    {R}
    A : bool or str
        ``'[m|p|x|y]'``
        By default, geographic line segments are drawn as great circle
        arcs. To draw them as straight lines, use *A*.
    {B}
    levels : str
        Contour file or level(s)
    D : str
        Dump contour coordinates
    E : str
        Network information
    label_placement : str
        Placement of labels
    I : bool
        Color the triangles using CPT
    triangular_mesh_pen : str
        Pen to draw the underlying triangulation (default none)
    no_clip : bool
        Do NOT clip contours or image at the boundaries [Default will clip
        to fit inside region].
    Q : float or str
        Do not draw contours with less than cut number of points.
        ``'[cut[unit]][+z]'``
    skip : bool or str
        Skip input points outside region ``'[p|t]'``
    {W}
    label : str
        Add a legend entry for the contour being plotted. Normally, the
        annotated contour is selected for the legend. You can select the
        regular contour instead, or both of them, by considering the label
        to be of the format [*annotcontlabel*][/*contlabel*]. If either
        label contains a slash (/) character then use ``|`` as the
        separator for the two labels instead.
    {V}
    {XY}
    {c}
    {p}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    kind = data_kind(data, x, y, z)
    if kind == "vectors" and z is None:
        raise GMTInvalidInput("Must provided both x, y, and z.")

    with Session() as lib:
        # Choose how data will be passed in to the module
        if kind == "file":
            file_context = dummy_context(data)
        elif kind == "matrix":
            file_context = lib.virtualfile_from_matrix(data)
        elif kind == "vectors":
            file_context = lib.virtualfile_from_vectors(x, y, z)

        with file_context as fname:
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("contour", arg_str)
