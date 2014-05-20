# -*- encoding: utf-8 -*-
##############################################################################
#
#    7 i TRIA
#    Copyright (C) 2011 - 2012 7 i TRIA <http://www.7itria.cat>
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

from osv import osv, fields         #siempre se ha de poner
from datetime import date
import base64
import time
import netsvc

class setitria_mods_import_dev_c19_wizard(osv.osv_memory):
    
    
    def _process_record_51(self, cr, uid, st_data, line, context=None):
       
       
        #
        # Add a new group to the statement groups
        #
        st_group = {}
        st_data['groups'] = st_data.get('groups', [])
        st_data['groups'].append(st_group)


        #
        # Set the group values
        #        
        st_group .update({
                'nif_empresa'   : line[4:13],
                'sufijo'        : line[13:16],
                'fecha_fich'    : time.strftime('%Y-%m-%d', time.strptime(line[16:22], '%d%m%y')),
                'cliente'       : line[28:68].strip(),
                'entidad'       : line[88:92],
                'oficina'       : line[92:96],
                'nom_entitat'   : line[108:148].strip(),
                '_num_records'  : 1,
                'num_records'   : 0,
                '_num_dev'      : 0,
                'num_dev'       : 0,
                'import'        : 0,
                'groups'        : []
            })
        
        
        return st_group;
    
    def _process_record_53(self, cr, uid, st_data, line, context=None):
       
        super53 = st_data['groups'][-1]
        
        #
        # Add a new group to the statement groups
        #
        st_group = {}
        super53['groups'] = super53.get('groups', [])
        super53['groups'].append(st_group)
        
        st_group.update({
                    'nif'           : line[4:13],
                    'sufijo'        : line[13:16],
                    'fecha'         : time.strftime('%Y-%m-%d', time.strptime(line[22:28], '%d%m%y')),
                    'nombrecl'      : line[28:68].strip(),
                    'entidad'       : line[68:72],
                    'oficina'       : line[72:76],
                    'dc'            : line[76:78],
                    'ncc'           : line[78:88],
                    '_num_records'  : 1,
                    'num_records'   : 0,
                    '_num_dev'      : 0,
                    'num_dev'       : 0,
                    'import'        : 0,
                    'lineas'         : []
            })
        
        return st_group 
   
   
    def _process_record_56(self, cr, uid, st_data, line, context=None):
        super56 = st_data['groups'][-1]
        super2 = super56['groups'][-1]
        
        
        #
        # Add a new line to the statement lines
        #
        st_line = {}
        super2['lineas'] = super2.get('lineas', [])
        super2['lineas'].append(st_line)

        #
        # Set the line values
        #
        st_line.update({
            'nif'           : line[4:13],
            'sufijo'        : line[13:16],
            'codi_ref'      : line[16:28].strip(),
            'nombre_titular': line[28:68].strip(),
            'entidad'       : line[68:72],
            'oficina'       : line[72:76],
            'dc'            : line[76:78],
            'ncc'           : line[78:88],
            'importe'       : float(line[88:96]) + (float(line[96:98]) / 100),
            'codi_dev'      : line[98:104].strip(),
            'codi_ref_int'  : line[104:114].strip(),
            'line_ref'      : line[114:121].strip(),
            'concepto'      : line[114:154].strip(),
            'motivo_dev'    : line[154:155].strip()
        })

        super2['_num_records'] += 1
        super2['_num_dev'] += 1
        super2['import'] += st_line['importe']
        
        return st_line
    
    def _process_record_58(self, cr, uid, st_data, line, context=None):
        super58 = st_data['groups'][-1]
        super2 = super58['groups'][-1]
        
        super2['_num_records'] += 1
        
        print line[104:114]
        devolucions = float(line[104:114])
        registres = float(line[114:124])
        importe = float(line[88:96]) + (float(line[96:98]) / 100)
        
        
        
        ################################################
        ##   CHECKS A NIVEL DE GRUP
        ################################################
        if devolucions != super2['_num_dev'] :
            raise osv.except_osv('Error in C19 file', 'El numero de devolucions no coincideix amb el definit al grup. (linea: %s)' % (super['_num_records'] + super2['_num_records']))
        if registres != super2['_num_records']:
            raise osv.except_osv('Error in C19 file', 'El numero de registres no coincideix amb el definit al grup. (linea: %s)' % (super['_num_records'] + super2['_num_records']))
        if abs(importe - super2['import']) > 0.005:
            raise osv.except_osv('Error in C19 file', "L'import dels registres no coincideix amb el definit al grup. (linea: %s)" % (super['_num_records'] + super2['_num_records']))
        
        
        
        super2['num_dev'] = devolucions
        super2['import'] = importe
        super2['num_records'] = registres
        
        super58['_num_records'] += super2['num_records']
        super58['import'] += importe
        super58['_num_dev'] += devolucions
        
        return super2
    
    
    def _process_record_59(self, cr, uid, st_data, line, context):
        super59 = st_data['groups'][-1]
        
        super59['_num_records'] += 1
        
        devolucions = float(line[104:114])
        registres = float(line[114:124])
        importe = float(line[88:96]) + (float(line[96:98]) / 100)
        
        
        ################################################
        ##   CHECKS A NIVEL DE CAPÇALERA SUPERIOR
        ################################################
        if devolucions != super59['_num_dev'] :
            raise osv.except_osv('Error in C19 file', 'El numero de devolucions no coincideix amb el definit al total. (linea: %s)' % (super['_num_records']))
        if registres != super59['_num_records']:
            raise osv.except_osv('Error in C19 file', 'El numero de registres no coincideix amb el definit al total. (linea: %s)' % (super['_num_records']))
        if abs(importe - super59['import']) > 0.005:
            raise osv.except_osv('Error in C19 file', "L'import dels registres no coincideix amb el deffecha_fichinit al total. (linea: %s)" % (super['_num_records']))
        
        
        super59['num_dev'] = devolucions
        super59['import'] = importe
        super59['num_records'] = registres
        
        
        return super
    
    
    
    def _load_c19_file(self, cr, uid, file_contents, context=None):
        if context is None:
            context = {}
        
        st_data = {
                'groups' : []
            }
        
        #
        # Read the C19 file
        #
        decoded_file_contents = base64.decodestring(file_contents)
        try:
            unicode(decoded_file_contents, 'utf8')
        except Exception: # Si no puede convertir a UTF-8 es que debe estar en ISO-8859-1: Lo convertimos
            #hem quitat l'ultim
            decoded_file_contents = unicode(decoded_file_contents, 'iso-8859-1')#.encode('utf-8')    
        
        #
        # Process the file lines
        #
        for line in decoded_file_contents.split("\n"):
            if len(line) == 0:
                continue
            if not (line[2:4] == '90'):
                raise osv.except_osv('Error in C19 file', 'data code %s is not valid.' % line[2:4])
            if line[0:2] == '51': # Registro cabecera de cuenta (obligatorio)
                self._process_record_51(cr, uid, st_data, line, context)
            elif line[0:2] == '53': # Registro cabecera de ordenante (obligatorio)
                self._process_record_53(cr, uid, st_data, line, context)
            elif line[0:2] == '56': # Registros individual obligatorio
                self._process_record_56(cr, uid, st_data, line, context)
            elif line[0:2] == '58': # Registro total de ordenante
                self._process_record_58(cr, uid, st_data, line, context)
            elif line[0:2] == '59': # Registro total general
                self._process_record_59(cr, uid, st_data, line, context)
            elif ord(line[0]) == 26: # CTRL-Z (^Z), is often used as an end-of-file marker in DOS
                pass
            else:
                raise osv.except_osv('Error in C19 file', 'Record type %s is not valid.' % line[0:2])

        return st_data
    
    def _attach_file_to_fitxer(self, cr, uid, file_contents, file_name, fitxer_id, context=None):
        """
        Attachs a file to the given fitxer de rebuts retornats
        """
        if context is None:
            context = {}
        attachment_facade = self.pool.get('ir.attachment')
        attachment_name = 'Fitxer Rebuts Retornat'

        #
        # Remove the previous statement file attachment (if any)
        #
        ids = attachment_facade.search(cr, uid, [
                    ('res_id', '=', fitxer_id),
                    ('res_model', '=', 'setitria.fitxerretornat'),
                    ('name', '=', attachment_name),
                ], context=context)
        if ids:
            attachment_facade.unlink(cr, uid, ids, context)

        #
        # Create the new attachment
        #
        res = attachment_facade.create(cr, uid, {
                    'name': attachment_name,
                    'datas': file_contents,
                    'datas_fname': file_name,
                    'res_model': 'setitria.fitxerretornat',
                    'res_id': fitxer_id,
                }, context=context)
        
        return res
    
    _name = 'setitria.mods.import.dev.c19.wizard'
    _columns = {
        'file': fields.binary('Arxiu de retornats del Banc', required=True, filename='file_name'),
        'file_name': fields.char('Arxiu de retornats del Banc', size=64),
        'journal_id':fields.many2one('account.journal', 'Journal', required=True)
        }
    
    def import_action(self, cr, uid, ids, context=None):
        """
        Imports the C19 file selected by the user on the wizard form
        """
        filename = self.browse(cr, uid, ids[0]).file_name
        msg = "\n\n****** INICIO CARGA DEVOLUCIONES: " + filename + " ******\n\n"
        f = open('/var/log/openerp/openerp-server.log', 'a')
        f.write(msg)
        f.close()
        if context is None:
            context = {}
        sumk = 0
        factura = self.pool.get('account.invoice')
        banc = self.pool.get('res.bank')
        apunt = self.pool.get('account.move.line')
        fitxer = self.pool.get('setitria.fitxerretornat')
        lineafit = self.pool.get('setitria.fitxerretornat.line')
        pay_line = self.pool.get('payment.line')      
        partner_obj = self.pool.get('res.partner')
        for c19_wizard in self.browse(cr, uid, ids, context):
            # Load the file data into the st_data dictionary
            st_data = self._load_c19_file(cr, uid, c19_wizard.file, context=context)
            journal = c19_wizard.journal_id.id
            for grupoTotal in st_data['groups']:    # per cada grup gran (en principi un per fitxer, pero aixó no es pot control-lar)
                banc_id = False
                banc_id = banc.search(cr, uid, [('code', '=', grupoTotal['entidad'])])
                if not banc_id:
                    raise osv.except_osv('Error tractant el fitxer', "El codi del banc indicat al fitxer no existeix")
                else:
                    banc_id = banc_id[0]
                values = {
                            'date'      : grupoTotal['fecha_fich'],
                            'date_imp'  : date.today().isoformat(),
                            'name'      : c19_wizard.file_name,
                            'banc_id'   : banc_id
                          }
                domain = [('date', '=', grupoTotal['fecha_fich'],), ('name', '=', c19_wizard.file_name), ('banc_id', '=', banc_id)]
                fitxer_id = False
                fitx_ids = fitxer.search(cr, uid, domain)
                if fitx_ids:
                    fitxer_id = fitx_ids[0]
                else:
                    fitxer_id = fitxer.create(cr, uid, values, context=context)
                
                for grupo in grupoTotal['groups']:  # per cada grup (agrupacio de rebuts per dia)
                    for linea in grupo['lineas']:   # per cada rebut
                        sumk += 1
                        msg = str(sumk) + '\n'
                        f = open('/var/log/openerp/openerp-server.log', 'a')
                        f.write(msg)
                        f.close()
                        created = False                        
                        ids = factura.search(cr, uid, [('number', '=', linea['codi_ref'])])
                        if not ids:
                            ids = factura.search(cr, uid, [('internal_number', '=', linea['codi_ref'])])
                            if not ids:
                                ids = factura.search(cr, uid, [('name', '=', linea['codi_ref'])])
                                if not ids:
                                    ids = factura.search(cr, uid, [('reference', '=', linea['codi_ref'])])
                        
                        print 'Sufijo: ' + str(linea['sufijo'])
                        print 'codi_ref: ' + str(linea['codi_ref']).lstrip('0')
                        print 'nombre_titular: ' + str(linea['nombre_titular'])
                        print 'entidad: ' + str(linea['entidad'])
                        print 'oficina: ' + str(linea['oficina'])
                        print 'dc: ' + str(linea['dc'])
                        print 'ncc: ' + str(linea['ncc'])
                        print 'importe: ' + str(linea['importe'])
                        print 'codi_dev: ' + str(linea['codi_dev'])
                        print 'codi_ref_int: ' + str(linea['codi_ref_int'])
                        print 'concepto: ' + str(linea['concepto'])
                        print 'motivo_dev: ' + str(linea['motivo_dev'])
                        line_ref = str(linea['sufijo']) + str(linea['codi_ref']).lstrip('0') + str(linea['nombre_titular']) + str(linea['entidad']) + str(linea['oficina']) + str(linea['dc']) + str(linea['ncc']) + str(linea['importe']) + str(linea['codi_dev']) + str(linea['codi_ref_int']) + str(linea['concepto']) + str(linea['motivo_dev'])
                        line_list = lineafit.search(cr, uid, [('line_ref', '=', line_ref), ('fitxer_id', '=', fitxer_id), ('state', '=', 'incomplete')])
                        line_list2 = lineafit.search(cr, uid, [('line_ref', '=', line_ref), ('fitxer_id', '=', fitxer_id), ('state', '=', 'valid')])
                        line_list3 = lineafit.search(cr, uid, [('line_ref', '=', False), ('fitxer_id', '=', fitxer_id), ('state', '=', 'incomplete')])			
                        if line_list:
                            msg = line_ref + "\n"
                            f = open('/var/log/openerp/openerp-server.log', 'a')
                            f.write(msg)
                            f.close()
                            lineafit.unlink(cr, uid, line_list)
                        if line_list2:
                            continue
                        if line_list3:
                            lineafit.unlink(cr, uid, line_list3)
                        codi_dev = linea['codi_dev']
                        importe = linea['importe']
                        fecha_dev = grupoTotal['fecha_fich']
                        partner = False
                        partner = partner_obj.search(cr, uid, [('ref', '=', linea['codi_ref'])])
                        if partner:
                            part = partner_obj.browse(cr, uid, partner[0])
                            id_compte_430 = part.property_account_receivable.id
                        else:
                            if linea['codi_ref'].isdigit():
                                partner = partner_obj.search(cr, uid, [('id', '=', linea['codi_ref']), ('name', 'like', linea['nombre_titular'])])
                                if partner:
                                    part = partner_obj.browse(cr, uid, partner[0])
                                    id_compte_430 = part.property_account_receivable.id
                                else:
                                    partner = partner_obj.search(cr, uid, [('id', '=', linea['codi_ref'])])
                                    if partner:
                                        part = partner_obj.browse(cr, uid, partner[0])
                                        id_compte_430 = part.property_account_receivable.id
                        if not partner:
                            partner = partner_obj.search(cr, uid, [('ref', '=', linea['codi_ref'][3:])])
                            if partner:
                                part = partner_obj.browse(cr, uid, partner[0])
                                id_compte_430 = part.property_account_receivable.id
                            else:
                                partner = partner_obj.search(cr, uid, [('ref', '=', linea['codi_ref'].lstrip('0'))])
                                if partner:
                                    part = partner_obj.browse(cr, uid, partner[0])
                                    id_compte_430 = part.property_account_receivable.id
                                else:
                                    raise osv.except_osv('Error', 'Partner not found containing %s Reference number.' % linea['codi_ref'].lstrip('0'))
                        partner = partner[0]
                        ids = False
                        pline = False
#                        pline_ids=[]
                        if codi_dev:  
                            pline_ids = pay_line.search(cr, uid, [('ml_inv_ref', '=', int(codi_dev))])
                            for line in pline_ids:
                                pline = pay_line.browse(cr, uid, line)
                                if pline.id == int(linea['codi_ref_int']):
                                    break
                                else:
                                    pline = False
                        
                        if pline and pline.ml_inv_ref:
                            if pline.ml_inv_ref.id == int(codi_dev):
                                ids = pline.ml_inv_ref.id
                        if linea['line_ref']:
                            msg = linea['line_ref'] + "\n"
                            f = open('/var/log/openerp/openerp-server.log', 'a')
                            f.write(msg)
                            f.close()
                            pline_ids = pay_line.search(cr, uid, [('name', '=', linea['line_ref'])])
                            msg = str(pline_ids) + "\n\n"
                            f = open('/var/log/openerp/openerp-server.log', 'a')
                            f.write(msg)
                            f.close()
                            for line in pline_ids:
                                pline = pay_line.browse(cr, uid, line)
                            #if pline.partner_id.ref == linea['codi_ref']:
                                ids = pline.ml_inv_ref.id
                                partner = pline.partner_id.id
                                part = pline.partner_id
                                id_compte_430 = part.property_account_receivable.id
                                pay_line_id = pline
                                msg = '----  ' + str(ids) + '  ----  ' + str(partner) + '  ----  ' + str(pay_line_id) + "\n"
                                f = open('/var/log/openerp/openerp-server.log', 'a')
                                f.write(msg)
                                f.close()
                                if ids == False:
                                    inv_list = factura.search(cr, uid, [('partner_id', '=', part.id), ('state', '=', 'paid'), ('amount_total', '=', importe)])  
                                    if inv_list:
                                        ids = inv_list[0] 
                                        inv = factura.browse(cr, uid, ids)
                                        pline_ids = inv.payment_ids
                                        if pline_ids:
                                            pay_line_id = pline_ids[0] 
                                if ids:
                                    line_list = lineafit.search(cr, uid, [('line_ref', '=', False), ('fitxer_id', '=', fitxer_id), ('state', '=', 'valid'), ('invoice_id', '=', ids), ('date', '=', fecha_dev)])
                                    if line_list:
                                        continue
                            values = {
                                      'fitxer_id'   : fitxer_id,
                                      'invoice_id'  : ids,
                                      'date'        : fecha_dev,
                                      'motiu_dev'   : linea['motivo_dev'],
                                      'dev_amount'  : linea['importe'],
                                      'partner_id'  : partner,
                                      'line_ref' : line_ref,
                                    }
                            
                            fact_obj = factura.browse(cr, uid, ids)
                            id_linea = apunt.search(cr, uid, [
                                         ('account_id', '=', id_compte_430),
                                         ('debit', '=', fact_obj.amount_total),
                                                        ])
                            msg = str(id_linea) + "\n"
                            f = open('/var/log/openerp/openerp-server.log', 'a')
                            f.write(msg)
                            f.close()
                            if id_linea:
                                for linea in id_linea:
                                    apunt_lines = []
                                    line_obj = apunt.browse(cr, uid, linea)
                                    invoice_id = line_obj.invoice.id
                                    if invoice_id == ids:
                                        recon_id = False
                                        inv_o = factura.browse(cr, uid, ids)
                                        reference = 'DEV FACT %s' % inv_o.name
                                        if pline:
                                            if pline.payment_move_id:
                                                cp_move = pline.payment_move_id.id
                                            else:
                                                values['notes'] = "The payment is not complete."
                                                lineafit.create(cr, uid, values, context=context) 
                                                created = True                                                
                                                break
                                        else:
                                            cp_move = pay_line_id.move_id.id 
                                        period = self.pool.get('account.period').find(cr, uid, fecha_dev, context)[0]
                                        msg = str(cp_move) + "\n"
                                        f = open('/var/log/openerp/openerp-server.log', 'a')
                                        f.write(msg)
                                        f.close()
                                        account_move = self.pool.get('account.move').copy(cr, uid, cp_move, {'ref':reference, 'date':fecha_dev, 'period_id':period, 'journal_id':journal})
                                        account_move_o = self.pool.get('account.move').browse(cr, uid, account_move)
                                        lines = account_move_o.line_id
                                        kont = 0
            
                                        for move_line in lines:
                                            recon = False
                                            amount = 0.0
                                            move_line_o = apunt.browse(cr, uid, move_line.id)
                                            for inv_move_line in inv_o.move_id.line_id:
                                                inv_line_o = apunt.browse(cr, uid, inv_move_line)
                                                if inv_line_o.reconcile_id:
                                                    recon = inv_line_o.reconcile_id.id
                                                    break
    
                                            if(recon != move_line_o.reconcile_id.id):
                                                continue                           
                                            if move_line_o.debit == 0.0:
                                                amount = move_line_o.credit
                                            else:
                                                amount = move_line_o.debit
                                            if ((lines.__len__() < 3) or (kont < 2 and move_line_o.partner_id.id == part.id and amount == inv_o.amount_total and not pline) or ((kont < 2) and move_line_o.partner_id.id == part.id and amount == inv_o.amount_total and pline and inv_o.name == move_line_o.name)):
                                                debit = 0.0
                                                credit = 0.0
                                                if move_line_o.debit > 0.0:
                                                    credit = importe
                                                if move_line_o.credit > 0.0:
                                                    debit = importe
                                                    apunt_lines.append(move_line_o.id)
                                                res = {'move_id':int(account_move), 'credit':credit, 'debit':debit, 'state':'draft', 'reconcile_id':False, 'date':fecha_dev, 'journal_id':journal, 'period_id':period}
                                                apunt.write(cr, uid, [move_line_o.id], res)
                                                if line_obj.reconcile_id:
                                                    recon_id = line_obj.reconcile_id.id
                                                    apunt_lines.append(line_obj.id)
                                                kont = kont + 1
                                            else:
                                                apunt.unlink(cr, uid, [move_line_o.id])
                                        for payline in fact_obj.payment_ids:
                                            if payline.reconcile_id and payline.reconcile_id.id == recon_id:
                                                apunt_lines.append(payline.id)
                                        #self.pool.get('account.move').button_validate(cr, uid, [account_move])
                                        self.pool.get('account.move.reconcile').unlink(cr, uid, recon_id, context=context)
                                        #apunt.write(cr,uid,apunt_lines,{'company_id':company})
                                        apunt.reconcile_partial(cr, uid, apunt_lines)
                                        wf_service = netsvc.LocalService("workflow")
                                        wf_service.trg_validate(uid, 'account.invoice', ids, 'open_test2', cr)
                                        try:
                                            self.pool.get('account.move').button_validate(cr, uid, [account_move])
                                        except:
                                            break
                                values['state'] = 'valid' 
                            else:                              
                                values['notes'] = "No s'ha trobat el apunt de contraprestació de la factura"
                        else:
                            line_list = lineafit.search(cr, uid, [('line_ref', '=', line_ref), ('fitxer_id', '=', fitxer_id)])
                            if line_list:
                                created = True
                                msg = "Sip\n"
                                f = open('/var/log/openerp/openerp-server.log', 'a')
                                f.write(msg)
                                f.close()
                        values = {
                                      'fitxer_id'   : fitxer_id,
                                      'line_ref'    : line_ref,
                                      'date'        : fecha_dev,
                                      'motiu_dev'   : linea['motivo_dev'],
                                      'dev_amount'  : linea['importe'],
                                      'notes'       : "Invoice not found."
                                    }
                        if not created:
                            lineafit.create(cr, uid, values, context=context)  
                cr.commit()
                self._attach_file_to_fitxer(cr, uid, c19_wizard.file, c19_wizard.file_name, fitxer_id)          
        msg = "\n\n****** FINAL CARGA DEVOLUCIONES: " + filename + " ******\n\n"
        f = open('/var/log/openerp/openerp-server.log', 'a')
        f.write(msg)
        f.close()
        return {}

    
setitria_mods_import_dev_c19_wizard()


class setitria_fitxerretornat(osv.osv):
    _name = "setitria.fitxerretornat"
    _description = 'Fitxer Rebuts Retornats'
    
    
    def _get_rebuts(self, cr, uid, ids, context=None):
        list_fitxer = [ l.fitxer_id.id for l in  self.pool.get('setitria.fitxerretornat.line').browse(cr, uid, ids, context=context)]
        return list_fitxer
    
    def _calcul_state(self, cr, uid, ids, name, arg, context=None):
        if not ids: return {}
        res = {}
        for line_id in ids:
            res[line_id] = ['incomplete']
            
        cr.execute('''
            SELECT
                a.id,
               COALESCE(max(b.state),'incomplete')
            FROM
                     setitria_fitxerretornat a
                LEFT OUTER JOIN
                    setitria_fitxerretornat_line b
                        ON
                            a.id=b.fitxer_id
            WHERE
                a.id IN %s 
            GROUP BY 
                a.id
            ''', (tuple(ids),))
        
        for oid, state in cr.fetchall():
            res[oid] = state
                        
        return res
        
    _columns = {
        'date'      : fields.date('Return date'),
        'banc_id'   : fields.many2one('res.bank', 'Origin bank'),
        'name'      : fields.char("File name", size=64, required=True),
        'date_imp'  : fields.date("File import date" ),
        'lines_id'  : fields.one2many('setitria.fitxerretornat.line', 'fitxer_id'),
        'notes'     : fields.text('Notes'),
        'state'     : fields.function(_calcul_state, method=True,
                            string='State', type='selection', 
                            selection=[
                                       ('incomplete', 'Incompleta'),
                                       ('valid', 'Valida')
                                       ],
                            store={
                                   'setitria.fitxerretornat.line': (_get_rebuts, ['state'], 10),
                                   }
                                      ),
        'journal_id':fields.many2one('account.journal', 'Journal', 
                                     required=True)
                }



        
    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        attachment_facade = self.pool.get('ir.attachment')
        
        attachment_name = 'Fitxer Rebuts Retornat'
        
        for line_id in ids:
            #
            # Remove the previous statement file attachment (if any)
            #
            id_at = attachment_facade.search(cr, uid, [
                        ('res_id', '=', line_id),
                        ('res_model', '=', 'setitria.fitxerretornat'),
                        ('name', '=', attachment_name),
                    ], context=context)
            if id_at:
                attachment_facade.unlink(cr, uid, id_at, context)
        
        ret = super(setitria_fitxerretornat, self).unlink(cr, uid, ids, context=context)
        return ret;
    
    def process_lines (self, cr, uid, ids, context=None):
#        res = {}
        if context is None:
            context = {}

        factura = self.pool.get('account.invoice')
#        banc = self.pool.get('res.bank')
        apunt = self.pool.get('account.move.line')
#        reconc = self.pool.get('account.move.reconcile')
#        fitxer = self.pool.get('setitria.fitxerretornat')
        lineafit = self.pool.get('setitria.fitxerretornat.line')
#        pay_line = self.pool.get('payment.line')      
#        account_obj = self.pool.get('account.account')
        move_obj = self.pool.get('account.move')
        period_obj = self.pool.get('account.period')
#        partner_obj = self.pool.get('res.partner')
        reconcile_obj = self.pool.get('account.move.reconcile')
#        company = self.pool.get('res.company').search(cr,uid,[])[0]
        fitx = self.browse(cr, uid, ids, context)[0]
#        banc_id = fitx.banc_id
        journal = fitx.journal_id.id
#        fitxer_id = fitx.id
        fecha_dev = fitx.date
        for linea_reg in fitx.lines_id:
            if linea_reg.state == 'valid':
                continue
            # por cada linea
#            created = False
            partner = linea_reg.partner_id
#            importe = linea_reg.dev_amount
            amount = linea_reg.dev_amount
            id_compte_430 = partner.property_account_receivable.id
            fact = False # Buscamos factura
            if linea_reg.invoice_id:
                fact = linea_reg.invoice_id.id
            else:               
                fact_lst = factura.search(cr, uid,[
                                            ('partner_id', '=', partner.id),
                                            ('amount_total', '=', amount),
                                            ('reconciled','=', True),
                                            ('state','=', 'paid')
                                             ])
                if fact_lst != []:
                    fact_lst.reverse()
                    fact= fact_lst[0]
            if fact:
                if not linea_reg.invoice_id:
                    lineafit.write(cr,uid,linea_reg.id,{'invoice_id':fact})
                fact_obj = factura.browse(cr, uid, fact)
                id_linea = []
                if fact_obj.amount_total >= 0:
                    id_linea = apunt.search(cr, uid,[
                                        ('account_id', '=', id_compte_430),
                                        ('debit', '=', fact_obj.amount_total),
                                        ('move_id', '=', fact_obj.move_id.id),
                                        ('reconcile_id', '!=', False)
                                            ])
                else:
                    id_linea = apunt.search(cr, uid,[
                                ('account_id', '=', id_compte_430),
                                ('credit', '=', (fact_obj.amount_total * -1)),
                                ('move_id', '=', fact_obj.move_id.id),
                                ('reconcile_id', '!=', False)
                                    ])
                if id_linea:
                    for linea in id_linea:
                        apunt_lines = []
                        line_obj = apunt.browse(cr, uid, linea)
#                        pline_lst = []
#                        if fact_obj.amount_total >= 0:
#                            pline_lst = apunt.search(cr, uid, [
#                                ('account_id', '=', id_compte_430),
#                                ('credit', '=', fact_obj.amount_total),
#                                ('reconcile_id','=',line_obj.reconcile_id.id)
#                                         ])
#                        else:
#                            pline_lst = apunt.search(cr, uid, [
#                                ('account_id', '=', id_compte_430),
#                                ('debit', '=', (fact_obj.amount_total * -1)),
#                                ('reconcile_id','=',line_obj.reconcile_id.id)
#                                         ])
#                        if pline_lst:
#                            pline = pline_lst[0]
#                        else:
#                            pline = False
                        invoice_id = line_obj.invoice.id
                        if invoice_id == fact:
                            recon_o = line_obj.reconcile_id
                            recon_id = recon_o.id
                            for rec_line in recon_o.line_id:
                                apunt_lines.append(rec_line.id)
                            inv_o = factura.browse(cr, uid, fact)
                            reference = 'DEV FACT: %s' % inv_o.number
                            period = period_obj.find(cr, uid, fecha_dev, 
                                                     context)[0]
                            account_move = move_obj.create(cr, uid, 
                                    {'ref':reference, 'date':fecha_dev, 
                                    'period_id':period, 'journal_id':journal})
                            account_move_o=move_obj.read(cr,uid,account_move,
                                            ['name','id'],context)
                            move_name = account_move_o['name']
                            dev_line_vals = {
                                 'period_id':period,
                                 'ref':reference,
                                 'journal_id':journal,
                                 'date':fecha_dev,
                                 'partner_id':inv_o.partner_id.id,
                                 'debit':inv_o.amount_total,
                                 'credit':0.0,
                                 'account_id':id_compte_430,
                                 'move_id':account_move,
                                 'name':move_name,
                                 'currency_id':inv_o.currency_id.id,
                                }
                            journal_o = fitx.journal_id
                            dev_bank_line_vals = {
                                'account_id':journal_o.default_credit_account_id.id,
                                'period_id':period,
                                'ref':reference,
                                'journal_id':journal,
                                'date':fecha_dev,
                                'partner_id':inv_o.partner_id.id,
                                'credit':inv_o.amount_total,
                                'debit':0.0,
                                'move_id':account_move,
                                'name':move_name,
                                'currency_id':inv_o.currency_id.id,
                                }
                            if inv_o.amount_total < 0:
                                dev_line_vals.update({
                                 'debit':0.0,
                                 'credit':(inv_o.amount_total * -1)
                                 })
                                dev_bank_line_vals.update({
                                 'account_id':journal_o.default_debit_account_id.id,
                                 'credit':0.0,
                                 'debit':(inv_o.amount_total * -1)
                                 })
                            dev_line_id = apunt.create(cr,uid,dev_line_vals)
                            apunt_lines.append(dev_line_id)
                            apunt.create(cr,uid,dev_bank_line_vals)
                            reconcile_obj.unlink(cr, uid, recon_id, context)
                            apunt.reconcile_partial(cr, uid, apunt_lines)
                            wf_service = netsvc.LocalService("workflow")
                            wf_service.trg_validate(uid,'account.invoice',fact,
                                                    'open_test2', cr)
                            factura.button_reset_taxes(cr,uid,[fact],context)
                            try:
                                move_obj.button_validate(cr,uid,[account_move])
                            except:
                                break
                            lineafit.write(cr,uid,[linea_reg.id],
                                           {'state':'valid'}) 
                        else:                              
                            lineafit.write(cr,uid,[linea_reg.id],{
                                       'state' : 'incomplete',
                                       'info' : 'Apunte de pago no encontrado'
                                       })  
            else:
                lineafit.write(cr,uid,[linea_reg.id],{
                                           'state' : 'incomplete',
                                           'info' : 'Factura no encontrada'
                                           })                              
        return True
    
    
setitria_fitxerretornat()

class setitria_fitxerretornat_line(osv.osv):
    _name = "setitria.fitxerretornat.line"
    _description = 'Lineas Fitxers Rebuts Retornats'
    
    _columns = {
        'fitxer_id' : fields.many2one('setitria.fitxerretornat', 'Return file', ondelete='cascade'),
        'motiu_dev' : fields.selection([
                                            ('0', "Amount to zero"),
                                            ('1', "Noncurrent"),
                                            ('2', "Non domiciled or account cancelled"),
                                            ('3', "Domiciled office not exists"),
                                            ('4', "Aplicación R.D. 338/90, sobre el NIF"),
                                            ('5', "By customer's request: error or domiciliation decline."),
                                            ('6', "By customer's request: amount disagreement."),
                                            ('7', "Duplicate, inappropriate, wrong or missing data."),
                                            ('8', "Unused")
                                        ], 'Return type'),
        'invoice_id': fields.many2one('account.invoice', 'Invoice', domain="[('type','=','in_invoice')]"),
        'date'      : fields.date('Return date'),
        'state'     : fields.selection([
                                            ('incomplete', 'Error'),
                                            ('valid', 'Complet'),
                                            ('no_process', 'No processed')
                                        ], 'State'),
        'notes'     : fields.text('Notes'),
        'partner_id': fields.many2one('res.partner', 'Customer'),
        'dev_amount': fields.float('Amount', digits=(13, 2)),
        'line_ref'  : fields.text('Ref'),
        'info': fields.char('Load log', size=128)
    }
    
    def onchange_invoice(self, cr, uid, ids, invoice, context=None):
        if not context:
            context = {}
            
        value = {}
        
        invoice_obj = self.pool['account.invoice']
        if invoice:
            invoice_o = invoice_obj.browse(cr,uid,invoice)
            value.update({
                          'partner_id':invoice_o.partner_id.id,
                          'dev_amount': invoice_o.amount_total,
                          })
        return {'value':value}
    
    _defaults = {
        'state'  : 'no_process',
        'date':lambda self,cr,uid,c: c.get('dev_date',False),
    }
    
setitria_fitxerretornat_line()
