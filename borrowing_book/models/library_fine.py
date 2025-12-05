from odoo import models, fields, api
class LibraryFine(models.Model):
    _name = 'library.fine'
    _description = 'Library Fine'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Fine Code',
        default=lambda self: self.env['ir.sequence'].next_by_code('library.fine'),
        readonly=True)

    transaction_id = fields.Many2one(
        'library.transaction',
        string='Transaction',
        required=True,
        tracking=True,
        ondelete='cascade',  )

    member_id = fields.Many2one(
        'library.member',
        string='Member',
        related='transaction_id.member_id',
        store=True)

    book_copy_id = fields.Many2one(
        'library.book.copy',
        string='Book Copy',
        related='transaction_id.book_copy_id',
        store=True)

    amount = fields.Float(
        string='Amount',
        related='transaction_id.fine_amount',
        store=True,
        readonly=False,   
        tracking=True)

    paid = fields.Boolean(string='Paid', default=False)

