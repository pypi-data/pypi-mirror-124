"""Classiq SDK."""

from classiq.client import configure
from classiq.authentication.authentication import register_device as authenticate
from classiq.async_utils import enable_jupyter_notebook, is_notebook as _is_notebook

if _is_notebook():
    enable_jupyter_notebook()
