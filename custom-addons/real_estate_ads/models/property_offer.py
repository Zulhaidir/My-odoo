from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError

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

    _sql_constraints = [
        ('check_validity', 'check(validity > 0)', 'Tanggal deadline tidak boleh sebelum tanggal creation date')
    ]