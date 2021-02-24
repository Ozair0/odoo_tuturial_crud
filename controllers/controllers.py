from odoo import http
from odoo.http import request

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
