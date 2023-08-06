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

import sys as sstm
from pathlib import Path as path_t
from typing import Optional

import imageio as imio
import numpy as nmpy
from PySide2 import QtCore as qtcr
from PySide2 import QtGui as qg_
from PySide2 import QtWidgets as qtwg

import few_colors.few_colors as fwcl
from few_colors.input import ImageFromPath


_WDW: Optional[qtwg.QWidget] = None
_CANVAS: Optional[qtwg.QLabel] = None
_LBL_IMAGE: Optional[nmpy.ndarray] = None
_color_image_g: Optional[nmpy.ndarray] = None
_q_image_g: Optional[qg_.QImage] = None
_new_color_g: Optional[qg_.QColor] = None


def Main():
    """"""
    global _WDW, _CANVAS

    # noinspection PyArgumentList
    app = qtwg.QApplication(sstm.argv)

    if sstm.argv.__len__() > 1:
        lbl_image_path_ = sstm.argv[1]
    else:
        lbl_image_path_ = _ImagePathFromChooser()
        if lbl_image_path_ is None:
            sstm.exit(0)

    if not _LoadLabeledImage(lbl_image_path_):
        sstm.exit(-1)

    _WDW = qtwg.QWidget(parent=None)

    # noinspection PyArgumentList
    open_btn = qtwg.QPushButton("Choose Labeled Image/Array", parent=None)
    # noinspection PyUnresolvedReferences
    open_btn.clicked.connect(_ChooseAndLoadImage)

    # noinspection PyArgumentList
    help_btn = qtwg.QPushButton("?", parent=None)
    # noinspection PyUnresolvedReferences
    help_btn.clicked.connect(_ShowHelp)

    color_image = fwcl.MinimallyColoredFromLabeled(_LBL_IMAGE)
    _CANVAS = qtwg.QLabel(parent=None)
    _CopyImageToCanvas(image=color_image)
    _CANVAS.setScaledContents(True)
    _CANVAS.mousePressEvent = _ChangeObjectColor

    # noinspection PyArgumentList
    save_btn = qtwg.QPushButton("Save", parent=None)
    # noinspection PyUnresolvedReferences
    save_btn.clicked.connect(_SaveImage)

    layout = qtwg.QVBoxLayout()
    top_lyt = qtwg.QHBoxLayout()
    top_lyt.addWidget(open_btn)
    top_lyt.addWidget(help_btn)
    layout.addLayout(top_lyt)
    layout.addWidget(_CANVAS)
    layout.addWidget(save_btn)
    _WDW.setLayout(layout)

    _WDW.show()
    sstm.exit(app.exec_())


def _ChooseAndLoadImage(_: bool = False) -> None:
    #
    lbl_image_path = _ImagePathFromChooser(parent=_WDW)
    if lbl_image_path is None:
        return

    if _LoadLabeledImage(lbl_image_path):
        color_image = fwcl.MinimallyColoredFromLabeled(_LBL_IMAGE)
        _CopyImageToCanvas(image=color_image)


def _ImagePathFromChooser(parent: qtwg.QWidget = None) -> Optional[str]:
    #
    # noinspection PyArgumentList
    path, _ = qtwg.QFileDialog.getOpenFileName(
        parent, "Choose Image/Array", qtcr.QDir.currentPath()
    )

    if path.__len__() == 0:
        return None
    else:
        return path


def _LoadLabeledImage(lbl_image_path: str) -> bool:
    #
    global _LBL_IMAGE

    image, issues = ImageFromPath(path_t(lbl_image_path))
    if image is None:
        # noinspection PyArgumentList
        qtwg.QMessageBox.warning(_WDW, "Loading Error", issues)
        return False

    _LBL_IMAGE = image

    return True


def _CopyImageToCanvas(image: nmpy.ndarray = None) -> None:
    #
    global _color_image_g, _q_image_g

    if image is None:
        image = _color_image_g
    else:
        _color_image_g = image

    # https://github.com/baoboa/pyqt5/blob/master/examples/widgets/imageviewer.py
    #
    # _q_image_g must be kept alive in instance
    # noinspection PyArgumentList
    _q_image_g = qg_.QImage(
        image.data,
        image.shape[1],
        image.shape[0],
        3 * image.shape[1],
        qg_.QImage.Format_RGB888,
    )
    # noinspection PyArgumentList
    p_image = qg_.QPixmap.fromImage(_q_image_g)
    _CANVAS.setPixmap(p_image)


def _ChangeObjectColor(event: qg_.QMouseEvent, *_, **__) -> None:
    #
    pix_x = round(_q_image_g.width() * event.x() / _CANVAS.width())
    pix_y = round(_q_image_g.height() * event.y() / _CANVAS.height())
    mods = int(event.modifiers())

    # noinspection PyArgumentList
    old_color = _q_image_g.pixelColor(pix_x, pix_y)
    color_chooser = qtwg.QColorDialog(old_color, parent=_WDW)
    # noinspection PyUnresolvedReferences
    color_chooser.colorSelected.connect(_StoreNewColorGlobally)
    color_chooser.exec()

    if (_new_color_g is None) or (_new_color_g == old_color):
        return

    if mods == 0:
        old_color_map = _LBL_IMAGE == _LBL_IMAGE[pix_y, pix_x]
    else:
        old_color_map = nmpy.logical_and(
            nmpy.logical_and(
                _color_image_g[:, :, 0] == old_color.red(),
                _color_image_g[:, :, 1] == old_color.green(),
            ),
            _color_image_g[:, :, 2] == old_color.blue(),
        )
    _color_image_g[:, :, 0][old_color_map] = _new_color_g.red()
    _color_image_g[:, :, 1][old_color_map] = _new_color_g.green()
    _color_image_g[:, :, 2][old_color_map] = _new_color_g.blue()

    _CopyImageToCanvas()


def _StoreNewColorGlobally(color: qg_.QColor) -> None:
    #
    global _new_color_g

    _new_color_g = color


def _SaveImage(_: bool = False) -> None:
    #
    # noinspection PyArgumentList
    path, _ = qtwg.QFileDialog.getSaveFileName(
        _WDW, "Saving File", qtcr.QDir.currentPath()
    )

    if path.__len__() == 0:
        return

    # _q_image_g.save(path)
    imio.imwrite(path, _color_image_g)


def _ShowHelp(_: bool = False) -> None:
    #
    # noinspection PyArgumentList
    qtwg.QMessageBox.information(
        _WDW,
        "fewColors Help",
        "<b>How to change the colors</b><br/><br/>"
        "<i>Single object or background.</i><br/>"
        "&bull; Left click an object (or the background).<br/>"
        "&bull; A color chooser window opens.<br/>"
        "&bull; Select a new color and confirm, or cancel.<br/><br/>"
        "<i>All the objects of the same color.</i><br/>"
        '&bull; Left click an object while holding down the "Shift" key.<br/>'
        "&bull; Proceed as for changing the color of a single object.",
    )


if __name__ == "__main__":
    #
    Main()
