# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherits = {'product.template': 'product_tmpl_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product Template',
        required=True,
        ondelete='cascade'
    )

    library_code = fields.Char(string='Library Code', tracking=True)
    shelf_location = fields.Char(string='Shelf Location')
    category = fields.Selection([
        ('novel', 'Novel'),
        ('comic', 'Comic'),
        ('science', 'Science'),
        ('history', 'History'),
        ('academic', 'Academic'),
        ('other', 'Other'),
    ], string='Category', default='novel', tracking=True)

    copy_ids = fields.One2many(
        'library.book.copy',
        'book_id',
        string='Book Copies'
    )

    total_copies = fields.Integer(
        string='Total Copies',
        compute='_compute_copy_counts',
        store=True
    )
    available_copies = fields.Integer(
        string='Available Copies',
        compute='_compute_copy_counts',
        store=True
    )

    @api.depends('copy_ids.status')
    def _compute_copy_counts(self):
        for rec in self:
            rec.total_copies = len(rec.copy_ids)
            rec.available_copies = len(rec.copy_ids.filtered(
                lambda c: c.status == 'available'
            ))
