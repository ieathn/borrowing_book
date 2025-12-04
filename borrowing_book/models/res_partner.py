# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_library_member = fields.Boolean(
        string='Library Member',
        help='Check this if this contact is also a library member.'
    )
    student_code = fields.Char(string='Student Code')
    class_name = fields.Char(string='Class')
    faculty = fields.Char(string='Faculty')
