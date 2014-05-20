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
    "name": "Avanzosc Agreement fixed price",
    "version": "1.0",
    "depends": [
                "account_invoice_analytics",
    ],
    "author": "AvanzOSC",
    "website" : "http://www.avanzosc.com",
    "category": "Custom Module",
    "description": """
        This module adds new fields:
            * fixed price, in invoice agreement.
            * ref field in the analytic search view 
            * product field in the analytic tree view    
            
            MOD - Dani
            Wizard to generate the analytic entry lines to Specific date
            Create Invoice Wizard from hr_timesheet_invoice module disabled """,
    "init_xml": [],
    'update_xml': [
                   "agreement_view.xml",
                   "account_analytic_account_view.xml",
                   "account_analytic_line_view_inh.xml",
                   "wizard/analytic_wiz_run_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
