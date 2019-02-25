# coding: utf-8
import logging
from odoo import api, fields, models, _
from odoo.addons.payment_ecpay.controllers.ecpay_payment_sdk import *

_logger = logging.getLogger(__name__)


class OrderEcpayModel(models.Model):
    _name = 'order.ecpay.model'

    name = fields.Char(
        '綠界金流訂單名稱')
    MerchantTradeDate = fields.Char(
        '訂單日期',
        groups='base.group_user',
        help='訂單日期')
    ReferenceNo = fields.Char(
        string='訂單編號',
        groups='base.group_user',
        help='訂單編號')
    sale_order_id = fields.Many2one(
        "sale.order",
        string='訂單編號',
        groups='base.group_user',
        help='訂單編號')
    MerchantTradeNo = fields.Char(
        '廠商訂單編號',
        groups='base.group_user',
        help='廠商訂單編號')
    TradeNo = fields.Char(
        '綠界金流訂單編號',
        groups='base.group_user',
        help='綠界金流訂單編號')
    PaymentType = fields.Char(
        '付款方式',
        groups='base.group_user',
        help='付款方式')
    PaymentDate = fields.Char(
        '付款日期',
        groups='base.group_user',
        help='付款日期')
    card4no = fields.Char(
        '信用卡卡號末4碼',
        groups='base.group_user',
        help='信用卡卡號末4碼')
    stage = fields.Char(
        '分期期數',
        groups='base.group_user',
        help='分期期數')
    RtnCode = fields.Char(
        '付款狀態',
        groups='base.group_user',
        help='付款狀態')
    TradeAmt = fields.Char(
        '交易金額',
        groups='base.group_user',
        help='交易金額')
    InvoiceMark = fields.Char(
        '電子發票',
        groups='base.group_user',
        help='電子發票')
    BankCode = fields.Char(
        '銀行代碼',
        groups='base.group_user',
        help='銀行代碼')
    vAccount = fields.Char(
        '虛擬帳號',
        groups='base.group_user',
        help='虛擬帳號')
    ExpireDate = fields.Char(
        '繳費期限',
        groups='base.group_user',
        help='繳費期限')
    PaymentNo = fields.Char(
        '繳費代碼',
        groups='base.group_user',
        help='繳費代碼')
    Barcode1 = fields.Char(
        '繳費條碼1',
        groups='base.group_user',
        help='繳費條碼第一段號碼')
    Barcode2 = fields.Char(
        '繳費條碼2',
        groups='base.group_user',
        help='繳費條碼第二段號碼')
    Barcode3 = fields.Char(
        '繳費條碼3',
        groups='base.group_user',
        help='繳費條碼第三段號碼')
    RtnMsg = fields.Char(
        '交易訊息',
        groups='base.group_user',
        help='交易訊息')

    @api.multi
    def order_info_record(self, data):
        """
        如果是 ATM、CVS 或 BARCODE, 綠界會將資料送到 _info_notify_url
        """
        # 先撈出 MerchantTradeNo 是否在資料庫裏面
        order = self.search(
            [('MerchantTradeNo', '=', data.get('MerchantTradeNo')), ], limit=1)
        info_data = {
            'MerchantTradeDate': data.get('TradeDate'),
            'TradeNo': data.get('TradeNo'),
            'PaymentType': ReplyPaymentType[data.get('PaymentType')],
            'RtnCode': data.get('RtnCode'),
            'TradeAmt': data.get('TradeAmt'),
            'BankCode': data.get('BankCode'),
            'vAccount': data.get('vAccount'),
            'ExpireDate': data.get('ExpireDate'),
            'PaymentNo': data.get('PaymentNo'),
            'Barcode1': data.get('Barcode1', ''),
            'Barcode2': data.get('Barcode2', ''),
            'Barcode3': data.get('Barcode3', ''),
            'RtnMsg': data.get('RtnMsg'),
        }
        # 先看有無這筆訂單
        if order:  # 有-寫入此筆訂單資訊
            return order.write(info_data)
        else:  # 無-建立此筆訂單資訊
            info_data.update({
                'MerchantTradeNo': data.get('MerchantTradeNo'),
            })
            return self.create(info_data)

    @api.multi
    def order_record(self, data):
        # 先撈出 MerchantTradeNo 是否在資料庫裏面
        order = self.search(
            [('MerchantTradeNo', '=', data.get('MerchantTradeNo')), ])
        order_data = {
            'MerchantTradeDate': data.get('MerchantTradeDate'),
            'ReferenceNo': data.get('CustomField1'),
            'PaymentType': data.get('ChoosePayment'),
            'TradeAmt': data.get('TotalAmount'),
        }
        if order:
            return order.write(order_data)
        else:
            order_data.update({
                'MerchantTradeNo': data.get('MerchantTradeNo'),
            })
            return self.create(order_data)

    @api.multi
    def order_paid_record(self, data):
        """
        如果付款完成, 綠界會將資料送到 _notify_url
        """
        # 先撈出 MerchantTradeNo 是否在資料庫裏面
        order = self.search(
            [('MerchantTradeNo', '=', data.get('MerchantTradeNo')), ])
        paid_data = {
            'PaymentDate': data.get('PaymentDate'),
            'PaymentType': ReplyPaymentType[data.get('PaymentType')],
            'RtnCode': data.get('RtnCode'),
            'RtnMsg': data.get('RtnMsg'),
            'TradeAmt': data.get('TradeAmt'),
            'TradeNo': data.get('TradeNo'),
            'card4no': data.get('card4no'),
            'stage': data.get('stage'),
        }
        sale_order = self.env['sale.order'].search(
            [('name', '=', data.get('CustomField1')),])
        if sale_order and (paid_data['RtnCode'] == '1'):
            paid_data.update(
                {'name': data.get('MerchantTradeNo'),
                'sale_order_id': sale_order.id,
                'ReferenceNo': False,})

        # 先看有無這筆訂單
        if order:  # 有-寫入此筆訂單資訊
            order.write(paid_data)
            if paid_data['RtnCode'] == '1':
                sale_order.write({'ecpay_trade_no_id': order.id})
        else:  # 無-建立此筆訂單資訊
            paid_data.update({
                'MerchantTradeNo': data.get('MerchantTradeNo'),
            })
            res = self.create(paid_data)
            if paid_data['RtnCode'] == '1':
                sale_order.write({'ecpay_trade_no_id': res.id})

class SaleOrder(models.Model):
    _inherit = "sale.order"

    ecpay_trade_no_id = fields.Many2one(
        'order.ecpay.model',
        string='綠界金流訂單編號',
        help='綠界金流訂單編號')