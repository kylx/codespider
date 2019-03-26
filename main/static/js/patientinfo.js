(function($) {
    "use strict";
    $('.info_input').each(function() {
        $(this).on('blur', function() {
            if ($(this).val().trim() != "") {
                $(this).addClass('has-val')
            } else {
                $(this).removeClass('has-val')
            }
        })
    })
    var name = $('.validate-input input[name="name"]');
    var email = $('.validate-input input[name="email"]');
    var message = $('.validate-input textarea[name="message"]');
    $('.validate-form').on('submit', function() {
        var check = !0;
        if ($(name).val().trim() == '') {
            showValidate(name);
            check = !1
        }
        if ($(email).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
            showValidate(email);
            check = !1
        }
        if ($(message).val().trim() == '') {
            showValidate(message);
            check = !1
        }
        return check
    });
    $('.validate-form .info_input').each(function() {
        $(this).focus(function() {
            hideValidate(this)
        })
    });

    function showValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).addClass('alert-validate')
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate')
    }
})(jQuery)