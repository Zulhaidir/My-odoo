from odoo import fields, models, api

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([
        ('new', 'New'), 
        ('received', 'Offer Received'), 
        ('accepted', 'Offer Accepted'), 
        ('sold', 'Sold'),
        ('cancel', 'Cancelled'),
    ], default='new', string="Status")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    data_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], 
        string="Garden Orientation", default='north')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesman")
    buyer_id = fields.Many2one('res.partner', string="Buyer", domain=[('is_company', '=', True)])
    total_area = fields.Integer(string="Total Area")
    phone = fields.Char(string="Phone", related="buyer_id.phone")
    offer_count = fields.Integer(string="Offers", compute="_compute_offer_count")

    def action_property_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - Offers",
            'domain': [('property_id', '=', self.id)],
            'view_mode': 'tree',
            'res_model': 'estate.property.offer'
        }

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped("price"))
            else:
                rec.best_offer = 0

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    @api.onchange('living_area', 'garden_area')
    def _onchange_total_area(self):
        self.total_area = self.living_area + self.garden_area

    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    