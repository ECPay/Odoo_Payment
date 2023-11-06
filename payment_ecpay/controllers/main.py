# -*- coding: utf-8 -*-
import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ECPayController(http.Controller):
    _notify_url = "/payment/ecpay/result_notify"
    _return_url = "/payment/ecpay/website_return"
    _info_notify_url = "/payment/ecpay/info_notify"
    _payment_process_url = "/payment/ecpay/website_return"

    @http.route(
        "/payment/ecpay/result_notify",
        type="http",
        methods=["POST"],
        auth="public",
        website=True,
        csrf=False,
    )
    def ecpay_notify(self, **post):
        """
        當消費者付款完成後，綠界會將付款結果參數以 Server POST 回傳到該網址。
        1. 請勿設定與 Client 端接收付款結果網址 OrderResultURL 相同位置，避免程式判斷錯誤。
        2. 請在收到 Server 端付款結果通知後，請正確回應 1|OK 給綠界。
        """
        _logger.info("綠界回傳[付款資訊] %s", pprint.pformat(post))
        #  計算驗證 CheckMacValue 是否相符
        result = request.env["payment.transaction"].sudo().ecpay_check_mac_value(post)
        if result:
            # 若為 1 時，代表此交易為模擬付款，請勿出貨。
            # 若為 0 時，代表此交易非模擬付款。
            if post.get("SimulatePaid", "1") == "0" and post.get("RtnCode", "1") == "0" or result == "test":
                # 執行 odoo 內建交易內容
                request.env["payment.transaction"].sudo()._handle_notification_data(
                    "ECPay", post
                )
                # 執行綠界交易內容(付款結果)
                request.env["order.ecpay.model"].sudo().order_paid_record(post)
            return "1|OK"
        else:
            return "0|error"

    @http.route(
        "/payment/ecpay/info_notify",
        type="http",
        methods=["POST"],
        auth="public",
        website=True,
        csrf=False,
    )
    def ecpay_info(self, **post):
        """
        使用 ATM/CVS/BARCODE 付款方式建立訂單完成後，以下參數會以
        Server POST 方式傳送至訂單資料設定的回傳付款網址 [PaymentInfoURL]
        1. 綠界: 以 ServerPost 方式傳送取號結果訊息至特店的 Server 網址 [PaymentInfoURL]
        2. 特店: 收到綠界的取號結果訊息，並判斷檢查碼是否相符
        3. 特店: 檢查碼相符後，於網頁端回應 1|OK
        """
        _logger.info("綠界回傳[取號結果] %s", pprint.pformat(post))
        #  計算驗證 CheckMacValue 是否相符
        if request.env["payment.transaction"].sudo().ecpay_check_mac_value(post):
            # 執行 odoo 內建交易內容
            request.env["payment.transaction"].sudo()._handle_notification_data(
                "ECPay", post
            )
            # 執行綠界交易內容(付款資訊)
            request.env["order.ecpay.model"].sudo().order_info_record(post)
            return "1|OK"
        else:
            return "0|error"

    @http.route(
        "/payment/ecpay/website_return",
        type="http",
        methods=["GET", "POST"],
        auth="public",
        website=True,
        csrf=False,
        save_session=False,
    )
    def ecpay_return(self, **post):
        """
        消費者點選此按鈕後，會將頁面導回到此設定的網址
        導回時不會帶付款結果到此網址，只是將頁面導回而已。
        設定此參數，綠界會在付款完成或取號完成頁面上顯示[返回商店]的按鈕。
        """
        _logger.info("綠界[返回商店]")
        if post:
            request.env["payment.transaction"].sudo()._handle_notification_data("ECPay", dict(post))
        return request.redirect("/payment/status")
