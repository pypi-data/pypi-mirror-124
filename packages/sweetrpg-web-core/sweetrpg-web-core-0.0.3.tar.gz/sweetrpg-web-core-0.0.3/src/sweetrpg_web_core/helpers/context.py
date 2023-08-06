# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""context.py
Context helper functions.
"""

from flask import current_app
import os


def get_context() -> dict:
    return {
        'user': {}, # TODO current_app.session['user']???
        'base_path': os.environ.get('APPLICATION_BASE_PATH') or ""
    }
