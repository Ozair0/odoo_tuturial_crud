from odoo import http
from odoo.http import request
from odoo.http import route
from odoo.addons.portal.controllers.portal import CustomerPortal

# This way we can inherit a controller
class CustomerPortalInherit(CustomerPortal):
    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        print("Controller inherited")
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                for field in set(['country_id', 'state_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

class Cars(http.Controller):
    @http.route('/cars', auth='public', type="http", website=True)
    def display_car(self, **kw):
        cars = request.env['car.car'].search([])
        vals = {
            'cars':cars
        }
        return request.render('theme_learnecom.display_cars', vals)
    
    @http.route('/cars/create', auth='public', type="http", website=True)
    def create_car_page(self, **kw):
        return request.render('theme_learnecom.create_car')
    
    @http.route('/cars/create', auth='public', type="http", website=True, methods=['POST'])
    def create_car(self, **kw):
        print(kw)
        if(kw.get('doors_number') == '' or kw.get('horse_power') == '' or kw.get('name') == ''):
            print('Empty Error')
            return request.redirect('/cars/create/')
        if(int(kw.get('doors_number')) < 1 or int(kw.get('horse_power')) < 1 or kw.get('name') == ''):
            print('0 erro')
            return request.redirect('/cars/create/')
        request.env['car.car'].create({
            'name': kw.get('name'),
            'doors_number': kw.get('doors_number'),
            'horse_power': kw.get('horse_power')
        })
        return request.redirect('/cars')
    
    @http.route('/cars/update', auth='public', type="http", website=True)
    def update_car_page(self, **kw):
        car = request.env['car.car'].search([('id','=',kw.get('id'))])
        vals = {
            'car': car
        }
        return request.render('theme_learnecom.update_car', vals)
    
    @http.route('/cars/update', auth='public', type="http", website=True, methods=['POST'])
    def update_car(self, **kw):
        print(kw)
        if(kw.get('doors_number') == '' or kw.get('horse_power') == '' or kw.get('name') == ''):
            print('Empty Error')
            return request.redirect('/cars/update/?id='+kw.get('id'))
        if(int(kw.get('doors_number')) < 1 or int(kw.get('horse_power')) < 1 or kw.get('name') == ''):
            print('0 erro')
            return request.redirect('/cars/update/?id='+kw.get('id'))
        request.env['car.car'].search([('id', '=', kw.get('id'))]).write({
            'name': kw.get('name'),
            'doors_number': kw.get('doors_number'),
            'horse_power': kw.get('horse_power')
        })
        return request.redirect('/cars')
    
    @http.route('/cars/delete', auth='public', type="http", website=True)
    def delete_car_page(self, **kw):
        if(kw.get('id') == ''):
            return request.redirect('/cars')
        if(int(kw.get('id')) < 0):
            return request.redirect('/cars')
        request.env['car.car'].search([('id','=',kw.get('id'))]).unlink()
        
        return request.redirect('/cars')
