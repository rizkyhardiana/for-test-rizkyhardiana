# -*- coding: utf-8 -*-
{
    'name': 'Material Registry Kedatech Test',
    'version': '1.0',
    'summary': 'Module for registering materials',
    'description': 'This module allows users to register materials, set prices, link to suppliers, and manage materials (create, update, delete, filter).',
    'category': 'Inventory',
    'author': 'Rizky H',
    'depends': ['base', 'stock', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/material_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

