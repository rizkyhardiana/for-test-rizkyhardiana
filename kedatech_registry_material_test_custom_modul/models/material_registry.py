from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MaterialRegistry(models.Model):
    _name = 'material.registry'
    _description = 'Material Registry'
    _order = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(string='Material Code', readonly=True, copy=False)
    name = fields.Char(string="Material Name", required=True, tracking=True, index=True)
    type = fields.Selection(
        [('fabric', 'Fabric'), ('jeans', 'Jeans'), ('cotton', 'Cotton')],
        string='Material Type',
        required=True
    )
    buy_price = fields.Float(string='Material Buy Price', required=True)
    supplier_id = fields.Many2one('res.partner', string='Related Supplier', domain=[('supplier_rank', '>', 0)], required=True)
    detail_line_ids = fields.One2many('material.registry.line', 'material_id', string='Detail Lines')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id.id)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Material code must be unique.')
    ]

    @api.onchange('type')
    def _onchange_type_generate_code(self):
        for rec in self:
            if not rec.code and rec.type:
                rec.code = rec._generate_code_from_type(rec.type)

    def _generate_code_from_type(self, material_type):
        prefix_map = {
            'fabric': 'FAB',
            'cotton': 'COT',
            'jeans': 'JNS',
        }
        prefix = prefix_map.get(material_type)
        domain = [('code', 'like', f'{prefix}-%')]
        existing = self.search(domain, order='code desc', limit=1)
        if existing and existing.code:
            try:
                last_number = int(existing.code.split('-')[-1])
            except ValueError:
                last_number = 0
        else:
            last_number = 0
        next_number = str(last_number + 1).zfill(3)
        return f"{prefix}-{next_number}"

    @api.model
    def create(self, vals):
        if not vals.get('code') and vals.get('type'):
            vals['code'] = self._generate_code_from_type(vals['type'])
        return super().create(vals)

    def write(self, vals):
        for rec in self:
            new_type = vals.get('type')
            if new_type and new_type != rec.type:
                new_code = rec._generate_code_from_type(new_type)
                vals['code'] = new_code
        return super().write(vals)

    @api.constrains('buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError('Material Buy Price must be at least 100.')

class MaterialRegistryLine(models.Model):
    _name = 'material.registry.line'
    _description = 'Material Registry Line'

    material_id = fields.Many2one('material.registry', string='Material', ondelete='cascade', required=True)
    color = fields.Char(string='Color', required=True)
    size = fields.Char(string='Size', required=True)
    quantity = fields.Integer(string='Quantity', required=True)

