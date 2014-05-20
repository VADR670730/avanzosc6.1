# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "Avanzosc Sale - MRP Workflow",
    "version": "1.0",
    "depends": ["sale",
                "mrp",
                "avanzosc_mrp_product_configurator",
                "account_invoice_analytics",
                "nan_product_pack",
                "avanzosc_crm_call_ext",
                ],
    "author": "AvanzOSC",
    "website" : "http://www.avanzosc.com",
    "category": "Custom Module",
    "description": """
    This module provide :
    * A workflow engine in order to add another step in sale workflow.
    """,
    "init_xml": [],
    'update_xml': [
                   "wizard/pre_order_wizard_view.xml",
                   "sale_mrp_view.xml",
                   "sale_mrp_workflow.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}