# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
A module containing strategies for storing and retrieving credentials.
"""

from .credentials_store import store_credentials, read_credentials, clear_credentials, SwitchCredentials
__all__ = ['store_credentials', 'read_credentials', 'clear_credentials', 'SwitchCredentials']
