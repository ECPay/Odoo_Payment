'use strict';
odoo.define('payment_ecpay.create_order', function (require) {
  var ajax = require('web.ajax');

  function chose_payment_type() {
    //  取得被選擇項目的值
    var payment_type = $("#ecpay_payment_method").find(":selected").val();
    ajax.jsonRpc('/payment/ecpay/save_payment_type', 'call', {
      payment_type: payment_type
    }).then(function () {
    });
  }

  $(window).on("load", function() {
    // 將 selection 隱藏起來
    $('#ecpay_payment_method').hide();

    // 如果 selection 有任何改變, 呼叫 function
    $('#ecpay_payment_method').change( function() {
      // 記錄起來
      chose_payment_type();
    });

    // 前端會根據後端的 payment method 來顯示有哪些付款方式
    $('input[type=radio][name=pm_id]').change(function() {
      if (this.dataset.provider === 'ecpay') {
        $('#ecpay_payment_method').fadeIn();
        chose_payment_type();
      } else {
        $('#ecpay_payment_method').fadeOut();
      }
    });
  });
});