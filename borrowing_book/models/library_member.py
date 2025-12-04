# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Member_id',
        required=True,
        tracking=True
    )

    student_code = fields.Char(related='partner_id.student_code', store=True, readonly=False)
    class_name = fields.Char(related='partner_id.class_name', store=True, readonly=False)
    faculty = fields.Char(related='partner_id.faculty', store=True, readonly=False)

    phone = fields.Char(related='partner_id.phone', store=True, readonly=False)
    email = fields.Char(related='partner_id.email', store=True, readonly=False)
    address = fields.Char(string='Address')

    active = fields.Boolean(default=True)

    transaction_ids = fields.One2many(
        'library.transaction', 'member_id', string='Transactions'
    )
    transaction_count = fields.Integer(
        string='Transaction Count',
        compute='_compute_transaction_count',
        store=True
    )

    @api.depends('transaction_ids')
    def _compute_transaction_count(self):
        for rec in self:
            rec.transaction_count = len(rec.transaction_ids)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for rec in self:
            if rec.partner_id:
                rec.name = rec.partner_id.name
