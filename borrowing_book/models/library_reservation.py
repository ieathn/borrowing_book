# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError


class LibraryReservation(models.Model):
    _name = 'library.reservation'
    _description = 'Library Reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Reservation Code',
        default=lambda self: self.env['ir.sequence'].next_by_code('library.reservation'),
        readonly=True
    )

    member_id = fields.Many2one(
        'library.member',
        string='Member',
        required=True,
        tracking=True
    )

    book_id = fields.Many2one(
        'library.book',
        string='Book',
        required=True,
        tracking=True
    )

    book_copy_id = fields.Many2one(
        'library.book.copy',
        string='Book Copy',
        tracking=True
    )

    reserve_date = fields.Date(
        string='Reserve Date',
        default=fields.Date.today,
        tracking=True
    )

    expire_date = fields.Date(
        string='Expire Date',
        default=lambda self: fields.Date.today() + timedelta(days=3),
        tracking=True
    )

    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ], default='pending', tracking=True)

    transaction_id = fields.Many2one(
        'library.transaction',
        string='Generated Transaction',
        readonly=True
    )

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        # Optional: auto-select first available copy
        if not rec.book_copy_id and rec.book_id:
            available_copy = rec.book_id.copy_ids.filtered(lambda c: c.status == 'available')[:1]
            if available_copy:
                rec.book_copy_id = available_copy.id
        return rec

    def write(self, vals):
        result = super().write(vals)

        for rec in self:
            if vals.get('status') == 'approved' and not rec.transaction_id:
                if not rec.book_copy_id:
                    raise UserError("Please select a Book Copy before approving.")
                if rec.book_copy_id.status not in ('available', 'reserved'):
                    raise UserError("This copy is not available for borrowing.")

                tx = self.env['library.transaction'].create({
                    'member_id': rec.member_id.id,
                    'book_copy_id': rec.book_copy_id.id,
                    'borrow_date': fields.Date.today(),
                    'expected_return_date': fields.Date.today() + timedelta(days=7),
                    'status': 'borrowed',
                })
                rec.transaction_id = tx.id
                rec.book_copy_id.status = 'on_loan'
                rec.book_copy_id.current_borrower_id = rec.member_id.id

        return result
