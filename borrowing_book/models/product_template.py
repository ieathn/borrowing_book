# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_library_book = fields.Boolean(
        string='Library Book',
        help='Check this box if this product represents a library book.'
    )
    isbn = fields.Char(string='ISBN')
    author = fields.Char(string='Author')
    publisher = fields.Char(string='Publisher')
    publish_year = fields.Char(string='Publish Year')
