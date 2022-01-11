# -*- coding: utf-8 -*-
"""User tables."""
from flask_table import Table, Col


class JobsTable(Table):
    name = Col('Name')
    product_type = Col('Type')
    product_length = Col('Length')
    product_diameter = Col('Diameter')
    product_layers = Col('Layers')

class SpoolsTable(Table):
    id = Col('UID')
    description = Col('Description')
    empty = Col('Empty')