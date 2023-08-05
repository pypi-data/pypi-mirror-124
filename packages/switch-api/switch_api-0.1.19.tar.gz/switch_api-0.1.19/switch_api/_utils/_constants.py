# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
A module defining constants referenced by methods and functions defined in  other modules in the package. This module
is not directly referenced by end users.
"""
from typing import Literal
__all__ = ['api_prefix', 'argus_prefix', 'DATETIME_COL_FMT', 'DEPLOY_TYPE', 'EXPECTED_DELIVERY', 'WORK_ORDER_PRIORITY',
           'WORK_ORDER_STATUS', 'WORK_ORDER_CATEGORY', 'ERROR_TYPE', 'MAPPING_ENTITIES', 'QUEUE_NAME', 'QUERY_LANGUAGE',
           'ACCOUNT', 'PROCESS_STATUS']
#api_prefix = "http://localhost:7071/api/SwitchApi/"
api_prefix = "https://pivotstreams.azurewebsites.net/api/SwitchApi/"

# argus_prefix = "http://localhost:7071/api/"
argus_prefix = "https://arguslogicv4b.azurewebsites.net/api/"


DATETIME_COL_FMT = Literal['DateTime', 'Date', 'Time']

# ['DateTime in 1 column',
#  'Date and Time in 2 columns',
#  'Split year and month in 2 columns',
#  'Start and End Date in 2 columns']

EXPECTED_DELIVERY = Literal['15min', 'Hourly', 'Daily', 'Monthly', 'Quarterly']

DEPLOY_TYPE = Literal['ftp', 'email', 'timer']

ACCOUNT = Literal['SwitchStorage', 'SwitchContainer', 'Argus']

QUERY_LANGUAGE = Literal['sql', 'kql']

ERROR_TYPE = Literal['DateTime', 'MissingDevices', 'NonNumeric', 'MissingRequiredField(s)', 'MissingSite(s)',
                     'DuplicateRecords', 'MissingSensors']

PROCESS_STATUS = Literal['ActionRequired', 'Failed']

MAPPING_ENTITIES = Literal['Installations', 'Devices/Sensors', 'Readings', 'Work Orders', 'Signals']

WORK_ORDER_CATEGORY = Literal['Preventative Maintenance', 'Tenant Request']

WORK_ORDER_PRIORITY = Literal['Low', 'Medium', 'High']

WORK_ORDER_STATUS = Literal['Submitted', 'Open',  'In Progress', 'Waiting for 3rd Party', 'Resolved', 'Abandoned',
                            'Closed']

QUEUE_NAME = Literal['task', 'highpriority']
