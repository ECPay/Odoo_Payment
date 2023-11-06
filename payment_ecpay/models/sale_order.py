# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    ecpay_info_ids = fields.One2many("order.ecpay.model", "sale_order_id", "綠界支付資訊")
