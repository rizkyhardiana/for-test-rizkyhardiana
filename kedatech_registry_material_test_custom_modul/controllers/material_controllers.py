import json
import requests
from odoo.tests import api
from werkzeug.wrappers import Response
from odoo import http, _, exceptions
from odoo.http import request

class MaterialController(http.Controller):

    @http.route('/api/materials_test', type='http', auth='public', methods=['GET'], csrf=False)
    def get_materials_rest_api(self, **params):
        try:
            #For test by id
            #example http://localhost:8096/api/materials_test/?id=21
            get_id = params.get('id')
            domain = []
            if get_id:
                domain.append(('id', '=', int(get_id)))

            materials = request.env['material.registry'].sudo().search_read(
                domain,
                ['code', 'name', 'type', 'buy_price', 'supplier_id']
            )
            #For test all datas
            # materials = request.env['material.registry'].sudo().search_read([], ['code', 'name', 'type', 'buy_price', 'supplier_id'])
            data = []
            for m in materials:
                data.append({
                    'code': m.get('code'),
                    'name': m.get('name'),
                    'type': m.get('type'),
                    'buy_price': m.get('buy_price'),
                    'supplier_id': m.get('supplier_id')[0] if m.get('supplier_id') else None,
                    'supplier_name': m.get('supplier_id')[1] if m.get('supplier_id') else None,
                })

            response = {
                'status': 200,
                'message': 'Success',
                'results': data,
            }
            return Response(
                json.dumps(response),
                content_type='application/json',
                status=200
            )

        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'Bad Request',
                'details': str(e),
            }
            return Response(
                json.dumps(error_response),
                content_type='application/json',
                status=400
            )

    @http.route('/api/materials_test', type='http', auth='public', methods=['POST'], csrf=False)
    def create_material_rest_api(self, **post):
        #example http://localhost:8096/api/materials_test/
        #method : POST
        #headers: Content-Type: application/json
        #body :
        # {
        #   "name": "Baju Baru",
        #   "type": "cotton",
        #   "buy_price": 70000,
        #   "supplier_id": 1
        # }

        try:
            params = json.loads(request.httprequest.data)

            required_fields = ['name', 'type', 'buy_price', 'supplier_id']
            missing = [f for f in required_fields if f not in params]
            if missing:
                raise Exception(f'Missing fields: {", ".join(missing)}')

            if params.get('buy_price', 0) < 100:
                raise Exception('Material Buy Price must be ≥ 100.')

            material = request.env['material.registry'].sudo().create(params)

            response = {
                'status': 201,
                'message': 'Material created successfully',
                'id': material.id,
                'code': material.code,
                'name': material.name,
                'type': material.type,
            }
            return Response(json.dumps(response), content_type='application/json', status=201)

        except Exception as e:
            return Response(
                json.dumps({'status': 400, 'error': str(e)}),
                content_type='application/json',
                status=400
            )

    @http.route('/api/materials_test/<int:material_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_material_rest_api(self, material_id, **post):
        # example http://localhost:8096/api/materials_test/<material_id>
        # method : PUT
        # headers: Content-Type: application/json
        # body :
        # {
        #   "name": "Baju Update",
        #   "type": "fabric",
        #   "buy_price": 80000,
        #   "supplier_id": 2
        # }
        try:
            params = json.loads(request.httprequest.data)

            material = request.env['material.registry'].sudo().browse(material_id)
            if not material.exists():
                raise Exception('Material not found.')

            if 'buy_price' in params and params['buy_price'] < 100:
                raise Exception('Material Buy Price must be ≥ 100.')

            material.write(params)

            response = {
                'status': 200,
                'message': 'Material updated successfully',
                'id': material.id,
                'code': material.code,
                'name': material.name,
                'type': material.type,
            }
            return Response(json.dumps(response), content_type='application/json', status=200)

        except Exception as e:
            return Response(
                json.dumps({'status': 400, 'error': str(e)}),
                content_type='application/json',
                status=400
            )

    @http.route('/api/materials_test/<int:material_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_material_rest_api(self, material_id):
        try:
            material = request.env['material.registry'].sudo().browse(material_id)
            if not material.exists():
                raise Exception('Material not found.')

            material_name = material.name
            material.unlink()

            response = {
                'status': 200,
                'name': material_name,
                'message': 'Material deleted successfully'
            }
            return Response(json.dumps(response), content_type='application/json', status=200)

        except Exception as e:
            return Response(
                json.dumps({'status': 400, 'error': str(e)}),
                content_type='application/json',
                status=400
            )