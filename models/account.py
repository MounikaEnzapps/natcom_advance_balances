from odoo import fields, models,api
from odoo.exceptions import UserError

from uuid import uuid4
import qrcode
import base64
import logging

from lxml import etree

from odoo import fields, models
import requests
import json
from datetime import datetime,date
import convert_numbers


class AccountMove(models.Model):
    _inherit = 'account.move'
    _order = 'invoice_date_time desc'


    net_amount_jan = fields.Float(compute='_net_amount_jan')
    net_amount_jan = fields.Float(compute='_net_amount_jan')
    discount_comma = fields.Float(compute='_compute_discount_comma')
    advance_comma = fields.Float(compute='_compute_advance_comma')
    net_amount_jan_arabic = fields.Float(compute='_net_amount_jan_ar')
    vat_amount_comma = fields.Float(compute='_vat_amount_comma')
    net_amount_with_comma = fields.Float(compute='_net_amount_with_vat_comma')


    def _compute_discount_comma(self):
        for each in self:
            if each.discount_value:
                each.discount_comma = float(each.discount_value)
            else:
                each.discount_comma = float(0)
    def _compute_advance_comma(self):
        for each in self:
            if each.advance:
                each.advance_comma = float(each.advance)
            else:
                each.advance_comma = float(0)
    def _vat_amount_comma(self):
        for each in self:
            if each.state == 'posted':
                tax_amount = each.amount_untaxed - float(each.advance) - float(each.discount_value)
                each.vat_amount_comma = tax_amount * 0.15
            else:
                each.vat_amount_comma = 0
    def _net_amount_with_vat_comma(self):
        for each in self:
            if each.state == 'posted':
                tax_amount =  each.amount_untaxed - float(each.advance) - float(each.discount_value)
                value = tax_amount * 0.15
                each.net_amount_with_comma = tax_amount+value
            else:
                each.net_amount_with_comma = 0





    def _net_amount_jan(self):
        for each in self:
            if each.state == 'posted':
               each.net_amount_jan = float(each.amount_untaxed - float(each.advance) - float(each.discount_value))
            else:
                each.net_amount_jan = 0
         # return self.net_amount_jan
    def _net_amount_jan_ar(self):
        for each in self:
            if each.state == 'posted':
               net_amount = each.net_amount_jan = float(each.amount_untaxed - float(each.advance) - float(each.discount_value))
               each.net_amount_jan_arabic = convert_numbers.english_to_arabic(int(net_amount))
            else:
                each.net_amount_jan_arabic = convert_numbers.english_to_arabic(int(0))
         # return self.net_amount_jan



    def amount_tax_per(self):
        tax_amount =  self.amount_untaxed - float(self.advance) - float(self.discount_value)
        value = tax_amount * 0.15
        return value
    def amount_net_amount(self):
        net_amount = self.amount_untaxed - float(self.advance) - float(self.discount_value)
        return convert_numbers.english_to_arabic(int(net_amount))

    def amount_tax_per_arabic(self):
        m= self.amount_untaxed - float(self.advance) - float(self.discount_value)
        value = m * 0.15
        before, after = str(value).split('.')
        before_int = int(before)
        after_int = int(after)
        before_ar = convert_numbers.english_to_arabic(before_int)
        after_ar = convert_numbers.english_to_arabic(after_int)
        ar_total_tax_amount = before_ar + '.' + after_ar
        return before_ar + '.' + after_ar

    def net_amount_with_vat(self):
        tax_amount =  self.amount_untaxed - float(self.advance) - float(self.discount_value)
        value = tax_amount * 0.15
        return tax_amount+value
    def ar_net_amount_with_vat(self):
        tax_amount = self.amount_untaxed - float(self.advance) - float(self.discount_value)
        value = tax_amount * 0.15
        with_vat = tax_amount + value
        return convert_numbers.english_to_arabic(int(with_vat))

