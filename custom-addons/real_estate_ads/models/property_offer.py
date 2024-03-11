from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class TransientOffers(models.TransientModel):
    _name = 'transient.model.offers'
    _description = 'Transient Offers'

    @api.autovacuum
    def _transient_vacuum(self):
        pass

    partner_email = fields.Char(string="Email")
    partner_phone = fields.Char(string="Phone")

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _inherit = ['transient.model.offers']
    _description = 'Estate Properties Offer'

    name = fields.Char(string="Description", compute="_compute_name")
    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')], 
        string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity", default=7)
    deadline = fields.Date(string="Deadline", inverse="_inverse_deadline")

    @api.model
    def _set_create_date(self):
        return fields.Date.today()

    creation_date = fields.Date(string="Create Date", default=_set_create_date)

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False

    @api.onchange('validity', 'creation_date')
    def _onchange_deadline(self):
        if self.creation_date and self.validity:
            self.deadline = self.creation_date + timedelta(days=self.validity)
        else:
            self.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline == rec.creation_date:
                raise ValidationError("Tanggal deadline tidak boleh sama dengan tanggal creation date")
            if rec.deadline < rec.creation_date:
                raise ValidationError("Tanggal deadline tidak boleh sebelum tanggal creation date")

    def _validate_accepted_offer(self):
        offer_ids = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
        ])
        if offer_ids:
            raise ValidationError("Hanya boleh satu Penawaran yang diterima")
            
    def action_accept_offer(self):
        self._validate_accepted_offer()
        if self.property_id:
            self.property_id.write({
                'selling_price': self.price,
                'state': 'accepted',
            })
        self.status = 'accepted'
    
    def action_decline_offer(self):
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received',
            })
        self.status = 'refused'
        

    def write(self, vals):
        _logger.info(f"ini adalah vals ===> {vals}")
        _logger.info(f"ini adalah self ===> {self}")
        _logger.info(f"ini adalah self.env.cr ===> {self.env.cr}")
        _logger.info(f"ini adalah self.env.uid ===> {self.env.uid}")
        _logger.info(f"ini adalah self.env.context ===> {self.env.context}")

        res_partner_ids = self.env['res.partner'].search_count([
            ('is_company', '=', True),
        ])
        _logger.info(f"ini adalah search count ===> {res_partner_ids}")

        res_partner_ids_2 = self.env['res.partner'].search([
            ('is_company', '=', True),
        ], limit=1)
        _logger.info(f"ini adalah search limit=1 ===> {res_partner_ids_2}")

        res_partner_ids_3 = self.env['res.partner'].search([
            ('is_company', '=', True),
        ]).mapped('phone')
        _logger.info(f"ini adalah search mapped phone ===> {res_partner_ids_3}")

        res_partner_ids_4 = self.env['res.partner'].search([
            ('is_company', '=', True),
        ]).filtered(lambda x: x.phone == '(828)-316-0593')
        _logger.info(f"ini adalah search filtered phone ===> {res_partner_ids_4}")

        return super(PropertyOffer, self).write(vals)