odoo.define('payment_ecpay.create_order', require => {
    'use strict';

    const checkoutForm = require('payment.checkout_form');
    var session = require('web.session');

    checkoutForm.include({
        events: Object.assign({}, checkoutForm.prototype.events, {
            'click .card-body.o_payment_option_card': '_payment_acquirer_select',
        }),

        init: function () {
            this._super(...arguments);
            if ($('input[name="o_payment_radio"]').length > 1) {
                $('input[name="o_payment_radio"]').prop('checked', false);
            }
            this._payment_acquirer_select();
        },

        _payment_acquirer_select: function (ev) {
            const self = this;
            // 如果變更支付方式,則判斷是否為 ecpay 以顯示下拉選單
            const acquirer_input = $('form[name="o_payment_checkout"]').find('input[name="o_payment_radio"]');
            const selector = $('form[name="o_payment_checkout"]').find('div.ecpay_payment_method');
            acquirer_input.each((index, element) => {
                if ($(element).data('provider') == 'ecpay' && $(element).prop('checked') == true) {
                    $(selector).removeClass('d-none');
                } else {
                    $(selector).addClass('d-none');
                }
            })
        },

        // _prepareTransactionRouteParams: function (provider, paymentOptionId, flow) {
        //     const transactionRouteParams = this._super(...arguments);
        //     // console.log($('#ecpay_payment_type').length); // 输出#ecpay_payment_method元素的数量
        //     // console.log($('#ecpay_payment_type').find(":selected").length); // 输出选中的option元素的数量
        //
        //     const payment_type = $('#ecpay_payment_type').find(":selected").val().trim();
        //     // console.log(payment_type); // 输出选中的值
        //     return {
        //         ...transactionRouteParams,
        //         payment_type: payment_type,
        //     };
        // },
        _prepareTransactionRouteParams: function (provider, paymentOptionId, flow) {
            const transactionRouteParams = this._super(...arguments);

            let payment_type = 'Credit'; // Default value
            const ecpayPaymentTypeElement = $('#ecpay_payment_type');

            if (ecpayPaymentTypeElement.length > 0) {
                const selectedOption = ecpayPaymentTypeElement.find(":selected");
                if (selectedOption.length > 0) {
                    payment_type = selectedOption.val().trim();
                }
            }

            return {
                ...transactionRouteParams,
                payment_type: payment_type,
            };
        },

    });
});