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
    "name": "Avanzosc Prevision Tesoreria Extension",
    "version": "1.0",
    "depends": ["base", "l10n_es_prev_tesoreria"],
    "author": "AvanzOSC",
    "category": "Custom Modules",
    "description": """
     Este modulo extiende l10n_es_prev_tesoreria, añade 2 pestañas nuevas, una cobros y pagos de caja,
     y otra pestaña con cobros únicos.
     Además permite exportar a un excel la previsión de tesorería, mediante un botón.
     El desglose de los saldos a parte de por tipo de pago, lo hacer por diferencia entre ingresos y gastos.
    """,
    "init_xml": [],
    'update_xml': ["security/ir.model.access.csv",
                   'wizard/export_csv_wiz.xml',
                   'plantilla_tesoreria.xml',
                   'prev_tesoreria.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}