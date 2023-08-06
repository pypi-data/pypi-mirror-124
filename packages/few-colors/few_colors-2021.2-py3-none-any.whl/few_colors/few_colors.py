# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2019)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import networkx.algorithms.coloring as nxcl
import numpy as nmpy
import scipy.ndimage as spim
import skimage.color as sicl
import skimage.future.graph as sigh


array_t = nmpy.ndarray


def MinimallyColoredFromLabeled(image: array_t) -> array_t:
    """"""
    output = nmpy.zeros((*image.shape, 3), dtype=nmpy.float64)

    labels = nmpy.unique(image)
    if labels[0] == 0:
        labels = labels[1:]

    dilated = nmpy.full_like(image, labels[0])
    distance_map = spim.distance_transform_edt(image != labels[0])

    for label in labels[1:]:
        current_map = spim.distance_transform_edt(image != label)
        closer_bmap = current_map < distance_map
        distance_map[closer_bmap] = current_map[closer_bmap]
        dilated[closer_bmap] = label

    gray_as_rgb = nmpy.dstack(3 * (dilated,))
    rag = sigh.rag_mean_color(gray_as_rgb, dilated)
    re_indexing = nxcl.greedy_color(rag)
    max_new_idx = max(re_indexing.values())
    for old, new in re_indexing.items():
        old_bmap = image == old
        output[..., 0][old_bmap] = new / max_new_idx  # Hue
        output[..., 1:][old_bmap] = 1.0  # Saturation and value

    output = sicl.hsv2rgb(output)
    output = nmpy.around(255.0 * output).astype(nmpy.uint8)

    return output
