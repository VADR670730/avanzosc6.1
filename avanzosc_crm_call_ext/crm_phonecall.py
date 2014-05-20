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

from crm import crm
from osv import fields, osv

from datetime import datetime
import time
from tools.translate import _

class crm_phonecall(crm.crm_case, osv.osv):
    _inherit = ['crm.phonecall','mail.thread']
    _name = "crm.phonecall"
        
    _columns = {
        'credit': fields.float('Total Receivable'),
        'invoice2pay': fields.integer('Invoices to pay'),
        'last_invoice': fields.date('Last Invoice'),
        'last_payment': fields.date('Last Payment'),
        'lead_id' : fields.many2one('crm.lead', 'Lead'),
        'helpdesk_id' : fields.many2one('crm.helpdesk', 'Help Desk'),
        'claim_id' : fields.many2one('crm.claim', 'Claim'),
        'canal_id': fields.many2one('crm.case.channel','Canal'),
        'message_ids': fields.one2many('mail.message', 'res_id', 'Messages', domain=[('model','=',_name)]),

    }
    
    def onchange_partner_id(self, cr, uid, ids, part, email=False):
        invoice_obj = self.pool.get('account.invoice')
        voucher_obj = self.pool.get('account.voucher')
        res = super(crm_phonecall, self).onchange_partner_id(cr, uid, ids, part, email)
        if part:
            partner = self.pool.get('res.partner').browse(cr, uid, part)
            unpaid_invoice_ids = invoice_obj.search(cr, uid, [('partner_id', '=', part), ('state', '=', 'open')])
            invoice_ids = invoice_obj.search(cr, uid, [('partner_id', '=', part)])
            voucher_ids = voucher_obj.search(cr, uid, [('partner_id', '=', part)])
            if invoice_ids:
                last_invoice = invoice_obj.browse(cr, uid, invoice_ids[0])
                for invoice in invoice_obj.browse(cr, uid, invoice_ids):
                    if invoice.date_invoice > last_invoice.date_invoice and invoice.date_invoice != False:
                        last_invoice = invoice
                    elif last_invoice.date_invoice == False:
                        last_invoice = invoice
                res['value'].update({
                       'last_invoice': last_invoice.date_invoice,
                })  
            if voucher_ids:
                last_voucher = voucher_obj.browse(cr, uid, voucher_ids[0])
                for voucher in voucher_obj.browse(cr, uid, voucher_ids):
                    if voucher.date > last_voucher.date and voucher.date != False:
                        last_voucher = voucher
                    elif last_voucher.date == False:
                        last_voucher = voucher
                res['value'].update({
                       'last_payment': last_voucher.date,
                })
            if unpaid_invoice_ids:
                res['value'].update({
                    'invoice2pay': int(len(unpaid_invoice_ids)),
                })          
            res['value'].update({
                'credit': partner.credit,
            })
        return res
    
    def case_close(self, cr, uid, ids, *args):
        """Overrides close for crm_case for setting close date
        """
        res = True
        for phone in self.browse(cr, uid, ids):
            phone_id = phone.id
            data = {'date_closed': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'state':'done'}
            self.write(cr, uid, ids, {'duration': 0.0, 'state':'open'})
            if phone.duration <=0:
                duration = datetime.now() - datetime.strptime(phone.date, '%Y-%m-%d %H:%M:%S')
                data.update({'duration': duration.seconds/float(60)})
            #res = super(crm_phonecall, self).case_close(cr, uid, [phone_id], args)
            self.write(cr, uid, [phone_id], data)
        return res
    
    def action_make_meeting(self, cr, uid, ids, context=None):
        """
        This opens Meeting's calendar view to schedule meeting on current Phonecall
        @return : Dictionary value for created Meeting view
        """
        value = {}
        for phonecall in self.browse(cr, uid, ids, context=context):
            data_obj = self.pool.get('ir.model.data')

            # Get meeting views
            result = data_obj._get_id(cr, uid, 'crm', 'view_crm_case_meetings_filter')
            res = data_obj.read(cr, uid, result, ['res_id'])
            id1 = data_obj._get_id(cr, uid, 'crm', 'crm_case_calendar_view_meet')
            id2 = data_obj._get_id(cr, uid, 'crm', 'crm_case_form_view_meet')
            id3 = data_obj._get_id(cr, uid, 'crm', 'crm_case_tree_view_meet')
            if id1:
                id1 = data_obj.browse(cr, uid, id1, context=context).res_id
            if id2:
                id2 = data_obj.browse(cr, uid, id2, context=context).res_id
            if id3:
                id3 = data_obj.browse(cr, uid, id3, context=context).res_id

            context = {
                        'default_phonecall_id': phonecall.id,
                        'default_partner_id': phonecall.partner_id and phonecall.partner_id.id or False,
                        'default_email': phonecall.email_from ,
                        'default_name': phonecall.name
                    }

            value = {
                'name': _('Meetings'),
                'domain' : "[('user_id','=',%s)]" % (uid),
                'context': context,
                'view_type': 'form',
                'view_mode': 'calendar,form,tree',
                'res_model': 'crm.meeting',
                'view_id': False,
                'views': [(id1, 'calendar'), (id2, 'form'), (id3, 'tree')],
                'type': 'ir.actions.act_window',
                'search_view_id': res['res_id'],
                'nodestroy': True
                }

        return value
    
    
crm_phonecall()