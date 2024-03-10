from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Properties Offer'

    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')], 
        string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity")
    deadline = fields.Date(string="Deadline", inverse="_inverse_deadline")

    @api.model
    def _set_create_date(self):
        return fields.Date.today()

    creation_date = fields.Date(string="Create Date", default=_set_create_date)

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

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('creation_date'):
                rec['creation_date'] = fields.Date.today()
        return super(PropertyOffer, self).create(vals)

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