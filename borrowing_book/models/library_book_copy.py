# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LibraryBookCopy(models.Model):
    _name = 'library.book.copy'
    _description = 'Physical Book Copy'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # name = fields.Char(
    #     string='Copy Code',
    #     default=lambda self: self.env['ir.sequence'].next_by_code('library.book.copy'),
    #     tracking=True
    # )
    
    name = fields.Char(
        string='Copy Code',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('library.book.copy'),
        tracking=True,
        readonly=False,
    )

    book_id = fields.Many2one(
        'library.book',
        string='Book',
        required=True,
        tracking=True
    )

    status = fields.Selection([
        ('available', 'Available'),
        ('on_loan', 'On Loan'),
        ('reserved', 'Reserved'),
        ('lost', 'Lost'),
    ], string='Status', default='available', tracking=True)

    current_borrower_id = fields.Many2one(
        'library.member',
        string='Current Borrower',
        compute='_compute_current_borrower',
        store=True
    )

    transaction_ids = fields.One2many(
        'library.transaction',
        'book_copy_id',
        string='Transactions'
    )

    borrow_count = fields.Integer(
        string='Times Borrowed',
        compute='_compute_borrow_stats',
        store=True
    )

    borrower_history_ids = fields.Many2many(
        'library.member',
        string='Borrower History',
        compute='_compute_borrow_stats',
        store=False
    )

    @api.depends('transaction_ids.status', 'transaction_ids.borrow_date')
    def _compute_current_borrower(self):
        for rec in self:
            active_tx = rec.transaction_ids.filtered(
                lambda t: t.status in ('borrowed', 'late')
            ).sorted(key=lambda t: t.borrow_date or fields.Date.today(), reverse=True)
            rec.current_borrower_id = active_tx[0].member_id.id if active_tx else False

            if active_tx:
                rec.status = 'on_loan'
            else:
                if rec.status == 'on_loan':
                    rec.status = 'available'

    @api.depends('transaction_ids.member_id')
    def _compute_borrow_stats(self):
        for rec in self:
            rec.borrow_count = len(rec.transaction_ids)
            rec.borrower_history_ids = rec.transaction_ids.mapped('member_id')
