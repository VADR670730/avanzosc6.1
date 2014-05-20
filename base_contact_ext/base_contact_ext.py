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
from tools.translate import _

class res_partner_address(osv.osv):
    
    _inherit = 'res.partner.address' 
    
    def onchange_contact(self, cr, uid, ids, contact_id, context=None):
        res = {}
        contact_obj = self.pool.get('res.partner.contact')
        if contact_id:
            for contact in contact_obj.browse(cr, uid, [contact_id]):
                res = {
		    		'phone': contact.mobile,
		    		'email': contact.email,
				}
        return {'value': res}
    
res_partner_address()

class res_partner_job(osv.osv):
    
    _inherit = 'res.partner.job' 
    
    def onchange_contact(self, cr, uid, ids, contact_id, context=None):
        res = {}
        contact_obj = self.pool.get('res.partner.contact')
        if contact_id:
            for contact in contact_obj.browse(cr, uid, [contact_id]):
                res = {
                    'phone': contact.mobile,
                    'email': contact.email,
                }
        return {'value': res}
    
res_partner_job()
