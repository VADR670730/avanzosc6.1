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
from osv import osv, fields
import decimal_precision as dp
import time

from tools.translate import _

class purchase_order(osv.osv):
    _name = 'purchase.order'
    _inherit = 'purchase.order'
    
    def _delete_constraint(self, cr, uid):
#       cr.execute( """ALTER TABLE purchase_order DROP CONSTRAINT purchase_order_name_uniq
#       """)
       return True
    
    _columns = {
              'name': fields.char('Order Reference', size=64, required=True, select=True, help="unique number of the purchase order,computed automatically when the purchase order is created"),
              'type':fields.many2one('purchase.type', 'Type', required=True),
    }
    _defaults = {
                 'name':lambda *a: 'PO/'
    }
   
       

    def select_type(self, cr, uid, ids, context=None):
        vals = {}
        for record in self.browse(cr,uid,ids):
            if record.type and not record.name:
                type_o=self.pool.get('purchase.type').browse(cr,uid,record.type.id)  
                code = type_o.sequence.code
                seq = self.pool.get('ir.sequence').get(cr,uid,code)
                vals.update({'name':seq})
                self.write(cr,uid,[record.id],vals)
        return ids
    
    def wkf_confirm_order(self, cr, uid, ids, context=None):
        res = super(purchase_order, self).wkf_confirm_order(cr,uid,ids,context)
        self.select_type(cr,uid,ids,context)
        return res
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state':'draft',
            'shipped':False,
            'invoiced':False,
            'invoice_ids': [],
            'picking_ids': [],
            'name': 'PO/',
        })
        res = super(osv.osv, self).copy(cr, uid, id, default, context)
        return res
        
        
purchase_order()
