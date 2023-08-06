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

from collections import defaultdict as default_dict_t
from pathlib import Path as path_t
from typing import Optional, Tuple

import imageio as mgio
import numpy as nmpy


array_t = nmpy.ndarray


# See at the end of module
LOADING_FOR_EXTENSION = default_dict_t(lambda: _ImageFromImagePath)
MESSAGE_FOR_EXTENSION = default_dict_t(lambda: "image or unreadable by imageio")
MESSAGE_FOR_EXTENSION |= {
    ".npy": "Numpy file or unreadable",
    ".npz": "Numpy file or unreadable",
}


def ImageFromPath(path: path_t, /) -> Tuple[Optional[array_t], Optional[str]]:
    """"""
    extension = path.suffix.lower()
    LoadingFunction = LOADING_FOR_EXTENSION[extension]

    try:
        image = LoadingFunction(path)
        image = _AsOneGrayChannelOrAsIs(image)

        is_valid, issues = _LabeledImageIsValid(image)
        if not is_valid:
            issues = f"{path}: Incorrectly labeled image:\n    {issues}"
            image = None
    except BaseException as exc:
        message = MESSAGE_FOR_EXTENSION[extension]
        issues = f"{path}: Not a valid {message}\n({exc})"
        image = None

    return image, issues


def _ImageFromImagePath(path: path_t, /) -> array_t:
    """"""
    return mgio.imread(str(path))


def _ImageFromNumpyPath(path: path_t, /) -> array_t:
    """"""
    output = nmpy.load(str(path))

    if hasattr(output, "keys"):
        first_key = tuple(output.keys())[0]
        output = output[first_key]

    return output


def _AsOneGrayChannelOrAsIs(image: array_t, /) -> array_t:
    """"""
    if (
        (image.ndim == 3)
        and (3 <= image.shape[2] <= 4)
        and nmpy.array_equal(image[..., 0], image[..., 1])
        and nmpy.array_equal(image[..., 0], image[..., 2])
    ):
        if (image.shape[2] == 3) or nmpy.all(image[..., 3] == image[0, 0, 3]):
            return image[..., 0]

    return image


def _LabeledImageIsValid(image: array_t, /) -> Tuple[bool, Optional[str]]:
    """"""
    has_valid_dimension = image.ndim == 2
    unique_values = nmpy.unique(image)
    expected_values = range(nmpy.amax(image) + 1)

    is_valid = (
        has_valid_dimension
        and (unique_values.__len__() > 1)
        and nmpy.array_equal(unique_values, expected_values)
    )

    if is_valid:
        issues = None
    elif unique_values.__len__() == 1:
        issues = [
            f"Only one value present in image: {unique_values[0]}; Expected=at least 0 and 1"
        ]
    else:
        if unique_values[0] > 0:
            issues = ["0?"]  # Zero is missing
        else:
            issues = [str(unique_values[0])]
        for v_m_1_idx, label in enumerate(unique_values[1:]):
            previous = unique_values[v_m_1_idx]
            label_as_str = str(label)
            if label == previous:
                issues.append("=" + label_as_str)
            elif label > previous + 1:
                issues.extend(("...?", label_as_str))
            else:
                issues.append(label_as_str)
    if issues is not None:
        if not has_valid_dimension:
            issues.append(f"{image.ndim}: Invalid image dimension; Expected=2")
        issues = ", ".join(issues)

    return is_valid, issues


LOADING_FOR_EXTENSION |= {".npy": _ImageFromNumpyPath, ".npz": _ImageFromNumpyPath}
