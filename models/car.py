# -*- coding: utf-8 -*-
from odoo import models, fields, api


class car_info(models.Model):
    _name = 'car.car'

    name = fields.Char(string='Name')
    doors_number= fields.Integer(string='Doors Number')
    horse_power = fields.Integer(string='Horse Power')
