# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta


class LibraryTransaction(models.Model):
    _name = 'library.transaction'
    _description = 'Library Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Transaction ID",
        default=lambda self: self.env['ir.sequence'].next_by_code('library.transaction'),
        readonly=True
    )

    member_id = fields.Many2one(
        'library.member',
        string="Borrower",
        required=True,
        tracking=True
    )

    book_copy_id = fields.Many2one(
        'library.book.copy',
        string="Book Copy",
        required=True,
        tracking=True
    )

    book_id = fields.Many2one(
        'library.book',
        string="Book Title",
        related='book_copy_id.book_id',
        store=True
    )

    borrow_date = fields.Date(
        string='Borrow Date',
        default=fields.Date.today,
        tracking=True
    )

    expected_return_date = fields.Date(
        string='Expected Return',
        default=lambda self: fields.Date.today() + timedelta(days=7),
        tracking=True
    )

    return_date = fields.Date(string='Return Date')

    status = fields.Selection([
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('late', 'Late'),
    ], default='borrowed', tracking=True)

    late_days = fields.Integer(
        string='Late Days',
        compute='_compute_late_days',
        store=True
    )

    is_overdue = fields.Boolean(
        string='Overdue',
        compute='_compute_late_days',
        store=True
    )

    fine_amount = fields.Float(
        string='Fine Amount',
        compute='_compute_fine_amount',
        store=True
    )

    fine_id = fields.Many2one(
        'library.fine',
        string='Fine Record',
        readonly=True
    )
    
    fine_paid = fields.Boolean(
    string='Fine Paid',
    related='fine_id.paid',
    store=True
)

    @api.depends('expected_return_date', 'return_date', 'status')
    def _compute_late_days(self):
        today = fields.Date.today()
        for rec in self:
            late = 0
            #Đã trả sách
            if rec.status == 'returned' and rec.return_date and rec.expected_return_date:
                diff = (rec.return_date - rec.expected_return_date).days
                late = diff if diff > 0 else 0
            #Chưa trả sách hoắc đã chuyển sang trạng thái trễ
            elif rec.status in ('borrowed', 'late')  and rec.expected_return_date and today > rec.expected_return_date:
                late = (today - rec.expected_return_date).days
            rec.late_days = late
            rec.is_overdue = late > 0

    @api.depends('late_days')
    def _compute_fine_amount(self):
        for rec in self:
            rec.fine_amount = rec.late_days * 3000 if rec.late_days > 0 else 0

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if rec.book_copy_id:
            rec.book_copy_id.status = 'on_loan'
            rec.book_copy_id.current_borrower_id = rec.member_id.id
        return rec

    def action_mark_returned(self):
        for rec in self:
            rec.return_date = fields.Date.today()
            rec.status = 'returned'
            if rec.book_copy_id:
                rec.book_copy_id.status = 'available'
                rec.book_copy_id.current_borrower_id = False
                
            rec._compute_late_days()
            rec._compute_fine_amount()

            if rec.fine_amount > 0:
                if rec.fine_id:
                    rec.fine_id.amount = rec.fine_amount
                else:
                    fine = self.env['library.fine'].create({
                        'transaction_id': rec.id,
                    })
                    rec.fine_id = fine.id
            else:
                rec.fine_id = False

    def action_mark_late(self):
        for rec in self:
            rec.status = 'late'
            if rec.book_copy_id:
                rec.book_copy_id.status = 'on_loan'
                
            rec._compute_late_days()
            rec._compute_fine_amount()

            if rec.fine_amount > 0:
                if rec.fine_id:
                    rec.fine_id.amount = rec.fine_amount
                else:
                    fine = self.env['library.fine'].create({
                        'transaction_id': rec.id,
                    })
                    rec.fine_id = fine.id
            else:
                rec.fine_id = False

    def action_mark_borrowed(self):
        for rec in self:
            rec.status = 'borrowed'
            if rec.book_copy_id:
                rec.book_copy_id.status = 'on_loan'
