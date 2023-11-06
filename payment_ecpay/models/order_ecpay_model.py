# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from datetime import datetime, timedelta

class OrderEcpayModel(models.Model):
    _name = "order.ecpay.model"

    MerchantTradeDate = fields.Char("訂單日期", groups="base.group_user", help="訂單日期")
    ReferenceNo = fields.Char("訂單編號", groups="base.group_user", help="訂單編號")
    MerchantTradeNo = fields.Char("廠商訂單編號", groups="base.group_user", help="廠商訂單編號")
    TradeNo = fields.Char("綠界金流訂單編號", groups="base.group_user", help="綠界金流訂單編號")
    PaymentType = fields.Char("付款方式", groups="base.group_user", help="付款方式")
    PaymentDate = fields.Char("付款日期", groups="base.group_user", help="付款日期")
    card4no = fields.Char("信用卡卡號末4碼", groups="base.group_user", help="信用卡卡號末4碼")
    stage = fields.Char("分期期數", groups="base.group_user", help="分期期數")
    SimulatePaid = fields.Boolean("是否為模擬付款", groups="base.group_user", help="模擬付款")
    RtnCode = fields.Char("付款狀態", groups="base.group_user", help="付款狀態")
    TradeAmt = fields.Char("交易金額", groups="base.group_user", help="交易金額")
    InvoiceMark = fields.Char("電子發票", groups="base.group_user", help="電子發票")
    BankCode = fields.Char("銀行代碼", groups="base.group_user", help="銀行代碼")
    vAccount = fields.Char("虛擬帳號", groups="base.group_user", help="虛擬帳號")
    ExpireDate = fields.Char("繳費期限", groups="base.group_user", help="繳費期限")
    PaymentNo = fields.Char("繳費代碼", groups="base.group_user", help="繳費代碼")
    Barcode1 = fields.Char("繳費條碼1", groups="base.group_user", help="繳費條碼第一段號碼")
    Barcode2 = fields.Char("繳費條碼2", groups="base.group_user", help="繳費條碼第二段號碼")
    Barcode3 = fields.Char("繳費條碼3", groups="base.group_user", help="繳費條碼第三段號碼")
    RtnMsg = fields.Char("交易訊息", groups="base.group_user", help="交易訊息")

    sale_order_id = fields.Many2one("sale.order", "銷售訂單")

    def order_info_record(self, data):
        """
        如果是 ATM、CVS 或 BARCODE, 綠界會將資料送到 _info_notify_url
        # 先撈出 MerchantTradeNo 是否存在在此表裡面，
        # 並找出對應的付款交易單[payment.transaction]來取得對應的銷售單[sales.order]，
        # 並建立與此紀錄關聯
        """
        order = self.search(
            [
                ("MerchantTradeNo", "=", data.get("MerchantTradeNo")),
            ],
            limit=1,
        )

        transaction = self.env["payment.transaction"].search(
            [
                ("reference", "=", data.get("CustomField1")),
            ],
            limit=1,
        )
        Order_date = (transaction.create_date + timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S")
        info_data = {
            "MerchantTradeDate": Order_date if transaction else data.get("TradeDate"),
            "MerchantTradeNo": data.get("MerchantTradeNo"),
            "TradeNo": data.get("TradeNo"),
            "PaymentType": data.get("PaymentType"),
            "RtnCode": data.get("RtnCode"),
            "TradeAmt": data.get("TradeAmt"),
            "BankCode": data.get("BankCode"),
            "vAccount": data.get("vAccount"),
            "ExpireDate": data.get("ExpireDate"),
            "PaymentNo": data.get("PaymentNo"),
            "Barcode1": data.get("Barcode1", ""),
            "Barcode2": data.get("Barcode2", ""),
            "Barcode3": data.get("Barcode3", ""),
            "RtnMsg": data.get("RtnMsg"),
        }



        create_data = False
        for sale_order_id in transaction.sale_order_ids:
            pattern = [(1, order.id, info_data)] if any(order) else [(0, 0, info_data)]
            sale_order_id.ecpay_info_ids = pattern
            create_data = True
        return create_data

    def order_paid_record(self, data):
        # 用此筆交易的 reference 去找尋 sale.order
        transaction = self.env["payment.transaction"].search(
            [
                ("reference", "=", data.get("CustomField1")),
            ],
            limit=1,
        )
        # 使用 transaction 的銷售訂單 id, 去建立銷售訂單的綠界支付資訊
        for sale_order_id in transaction.sale_order_ids:
            paid_data = {
                "MerchantTradeDate": data.get("TradeDate"),
                "MerchantTradeNo": data.get("MerchantTradeNo"),
                "PaymentDate": data.get("PaymentDate"),
                "PaymentType": data.get("PaymentType"),
                "RtnCode": data.get("RtnCode"),
                "RtnMsg": "此為模擬付款" if data.get("SimulatePaid") == "1" else data.get("RtnMsg"),
                "TradeAmt": data.get("TradeAmt"),
                "TradeNo": data.get("TradeNo"),
                "card4no": data.get("card4no"),
                "stage": data.get("stage"),
                "SimulatePaid": True if data.get("SimulatePaid") == "1" else False,
            }
            result = sale_order_id.ecpay_info_ids = [(0, 0, paid_data)]
            print(result)
