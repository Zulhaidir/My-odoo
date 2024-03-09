from odoo import fields, models, api
from datetime import timedelta

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

    @api.onchange('validity', 'creation_date')
    def _onchange_deadline(self):
        if self.creation_date and self.validity:
            self.deadline = self.creation_date + timedelta(days=self.validity)
        else:
            self.deadline = False

    def _inverse_deadline(self):
            self.validity = (self.deadline - self.creation_date).days

    @api.model
    def _set_creation_date(self):
        return fields.Date.today()

    creation_date = fields.Date(string="Create Date", default=_set_creation_date)
    

    