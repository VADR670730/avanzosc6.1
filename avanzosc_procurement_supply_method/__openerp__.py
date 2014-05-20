# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2008-2014 AvanzOSC S.L. (Oihane) All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "AvanzOsc - Supply Method in Procurement Orders",
    "version": "1.0",
    "depends": ["procurement"],
    "author": "AvanzOSC",
    "category": "Custom Module",
    "website": "http://www.avanzosc.es",
    "complexity": "normal",
    "description": """
    This module provide :
       * New field 'supply_method' in procurement.order model, automatically
         filed with product.template supply method       
    """,
    "init_xml": [],
    "update_xml": ["procurement_view.xml"],
    "demo_xml": [],
    "installable": True,
    "active": False,
#    "certificate": 'certificate',
}