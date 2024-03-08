{
    'name': "menyala abangkuh!!",

    'summary': """
        Tutorial OWL""",

    'sequence': -1,

    'description': """
        OWL TUTORIAL
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'OWL',
    'version': '0.1',
    'depends': ['base', 'web', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list.xml',
        'views/res_partner.xml',
        'views/odoo.service.xml',
    ],

    'demo': [
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',

    'assets': {
        'web.assets_backend': [
            'tutorial_owl/static/src/components/*/*.js',
            'tutorial_owl/static/src/components/*/*.xml',
            'tutorial_owl/static/src/components/*/*.scss',
        ],
        'point_of_sale.assets': [
            'tutorial_owl/static/src/pos/**/*.js',
            'tutorial_owl/static/src/pos/**/*.xml',
            'tutorial_owl/static/src/pos/**/*.scss',
           
        ]
    },

}
