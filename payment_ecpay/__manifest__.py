# -*- coding: utf-8 -*-

{
    "name": "ECPay 綠界第三方金流模組",
    "category": "Accounting",
    "summary": "Payment Acquirer: ECPay 綠界第三方金流模組",
    "version": "16.0.1.0",
    "description": """ECPay 綠界第三方金流模組""",
    'author': 'ECPAY',
    'website': 'http://www.ecpay.com.tw',
    "depends": ["l10n_tw", "payment", "payment_custom", "sale", "sale_management", "web", "website_sale"],
    "data": [
        "security/payment_ecpay_access_rule.xml",
        "security/ir.model.access.csv",
        "views/payment_views.xml",
        "views/payment_ecpay_templates.xml",
        "views/payment_ecpay_order_templates.xml",
        "views/payment_ecpay_order_views.xml",
        "views/sale_order.xml",
        "data/payment_provider_data.xml",
        "data/ecpay_credit_limit.xml",
    ],
    "installable": True,
    'application': True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "assets": {
        'web.assets_frontend': [
            "payment_ecpay/static/src/js/selection.js",
        ],
    },
}
