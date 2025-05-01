from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMaterialRegistry(TransactionCase):

    def setUp(self):
        super().setUp()
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'supplier_rank': 1,
        })

    def test_create_valid_material(self):
        material = self.env['material.registry'].create({
            'code': 'MAT001',
            'name': 'Material A',
            'type': 'fabric',
            'buy_price': 150,
            'supplier_id': self.supplier.id,
        })
        self.assertEqual(material.code, 'MAT001')
        self.assertEqual(material.name, 'Material A')
        self.assertEqual(material.type, 'fabric')
        self.assertEqual(material.buy_price, 150)

    def test_buy_price_validation(self):
        with self.assertRaises(ValidationError) as context:
            self.env['material.registry'].create({
                'code': 'MAT002',
                'name': 'Material B',
                'type': 'jeans',
                'buy_price': 50,
                'supplier_id': self.supplier.id,
            })
        self.assertIn('Material Buy Price must be at least 100.', str(context.exception))

    def test_unique_code_constraint(self):
        self.env['material.registry'].create({
            'code': 'MAT003',
            'name': 'Material C',
            'type': 'cotton',
            'buy_price': 200,
            'supplier_id': self.supplier.id,
        })
        with self.assertRaises(ValidationError) as context:
            self.env['material.registry'].create({
                'code': 'MAT003',
                'name': 'Material D',
                'type': 'cotton',
                'buy_price': 200,
                'supplier_id': self.supplier.id,
            })
        self.assertIn('Material code must be unique.', str(context.exception))