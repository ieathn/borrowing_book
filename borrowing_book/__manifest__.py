{
    'name': 'Borrowing Book Management',
    'version': '1.0.0',
    'summary': 'Library book borrowing & reservation management',
    'category': 'Services/Library',          # DÒNG QUAN TRỌNG
    'sequence': -100,                        # hiện lên đầu
    'author': 'Team5',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'contacts', 'product'],
    'data': [
        'security/borrowing_book_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/actions.xml',
        
        'views/book_view.xml',
        'views/book_copy_view.xml',
        'views/member_view.xml',
        'views/reservation_view.xml',
        'views/transaction_view.xml',
        'views/fine_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],
}