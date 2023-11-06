# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo.addons.payment.controllers import portal as payment_portal

_logger = logging.getLogger(__name__)


class PaymentPortal(payment_portal.PaymentPortal):
    def _create_transaction(
            self, payment_option_id, reference_prefix, amount, currency_id, partner_id, flow,
            tokenization_requested, landing_route, is_validation=False,
            custom_create_values=None, **kwargs
    ):
        """ Override addons 'payment' controller method"""
        tx_sudo = super()._create_transaction(
            payment_option_id=payment_option_id,
            reference_prefix=reference_prefix,
            amount=amount,
            currency_id=currency_id,
            partner_id=partner_id,
            flow=flow,
            tokenization_requested=tokenization_requested,
            landing_route=landing_route,
            is_validation=is_validation,
            custom_create_values=custom_create_values,
            **kwargs
        )

        payment_type = kwargs.get('payment_type')
        if payment_type and tx_sudo.provider_code == 'ECPay':
            tx_sudo.payment_method = payment_type

        return tx_sudo
