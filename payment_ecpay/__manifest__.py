# -*- coding: utf-8 -*-

{
    'name': 'ECPay 綠界第三方金流模組',
    'category': 'Accounting',
    'summary': 'Payment Acquirer: ECPay 綠界第三方金流模組',
    'version': '1.3',
    'description': """ECPay 綠界付款模組""",
    'author' : '元植顧問',
    'website' : 'https://www.yuanchih-consult.com/',
    'depends': ['payment'],
    'data': [
        'security/payment_ecpay_access_rule.xml',
        'security/ir.model.access.csv',
        'views/payment_views.xml',
        'views/payment_ecpay_templates.xml',
        'views/payment_ecpay_order_templates.xml',
        'views/payment_ecpay_order_views.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,
}
