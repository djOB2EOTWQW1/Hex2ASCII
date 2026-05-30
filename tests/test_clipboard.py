from unittest import mock
from PIL import Image
from core import clipboard

def test_grab_image_returns_pil_image_from_imagegrab():
    fake = Image.new("RGB", (2, 2), "white")
    with mock.patch("core.clipboard.ImageGrab") as ig:
        ig.grabclipboard.return_value = fake
        assert clipboard.grab_image() is fake

def test_grab_image_returns_none_when_empty():
    with mock.patch("core.clipboard.ImageGrab") as ig:
        ig.grabclipboard.return_value = None
        with mock.patch("core.clipboard._grab_wayland", return_value=None):
            assert clipboard.grab_image() is None
