from odoo import fields, models

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string="Name", required=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    data_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price")
    best_offer = fields.Float(string="Best Offer")
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Total Area(sqm)")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], 
        string="Garden Orientation", default='north')


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string="Name", required=True)

    