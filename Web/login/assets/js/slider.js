/* ============================================================
 * Sliders
 * Sliders using Ion Slider and noUiSlider jQuery Plugins
 * For DEMO purposes only. Extract what you need.
 * ============================================================ */
(function($) {

    'use strict';

    $(document).ready(function() {
        $(".ion_slider").ionRangeSlider({
            min: 0,
            max: 5000,
            type: 'double',
            prefix: "$",
            maxPostfix: "+",
            prettify_enabled: false,
            grid: true
        });
        $("#example_1").ionRangeSlider({
            min: 0,
            max: 5000,
            type: 'double',
            prefix: "$",
            maxPostfix: "+",
            prettify_enabled: false,
            grid: true
        });

        $("#example_2").ionRangeSlider({
            min: 1000,
            max: 100000,
            from: 30000,
            to: 90000,
            type: 'double',
            step: 500,
            postfix: " €",
            grid: true
        });

        $("#example_3").ionRangeSlider({
            min: 0,
            max: 10,
            type: 'single',
            step: 0.1,
            postfix: " carats",
            prettify_enabled: false,
            grid: true
        });

        $("#example_4").ionRangeSlider({
            min: -50,
            max: 50,
            from: 0,
            postfix: "°",
            prettify_enabled: false,
            grid: true
        });

        $("#example_5").ionRangeSlider({
            values: [
                "January", "February",
                "March", "April",
                "May", "June",
                "July", "August",
                "September", "October",
                "November", "December"
            ],
            type: 'single',
            grid: true
        });

        $("#example_6").ionRangeSlider({
            min: 10000,
            max: 100000,
            step: 1000,
            postfix: " miles",
            from: 55000,
            hideMinMax: false,
            hideFromTo: true
        });

    });

    //NOUI SLIDER //

    $(document).ready(function() {
        //Just for RTL purposes
        var direction = ($("body").hasClass("rtl")) ? "rtl": "ltr";

        $(".nouislider_element").each(function(index) {
            var val = $(this).attr('data-value');
            if (val == null)
                val = 0
            $(this).noUiSlider({
                direction:direction,
                start: val,
                connect: "lower",
                range: {
                    'min': 0,
                    'max': 100
                }
            });
        });

        $("#slider-margin").noUiSlider({
            start: [20, 80],
            margin: 30,
            connect: true,
            range: {
                'min': 0,
                'max': 100
            }
        });
        $("#slider-limit").noUiSlider({
            start: [10, 120],
            limit: 40,
            behaviour: 'drag',
            connect: true,
            range: {
                'min': 0,
                'max': 100
            }
        })
        $("#slider-limit").Link('lower').to($('#slider-limit-value-min'))
        $("#slider-limit").Link('upper').to($('#slider-limit-value-max'));

        $("#slider-step").noUiSlider({
            start: [20, 80],
            step: 10,
            connect: true,
            range: {
                'min': 0,
                'max': 100
            }
        });

        $("#slider-vertical").noUiSlider({
            start: [20, 80],
            step: 10,
            margin: 20,
            connect: true,
            direction: 'rtl',
            orientation: 'vertical',
            range: {
                'min': 0,
                'max': 100
            }
        });

        $("#slider-tooltips").noUiSlider({
            start: 40,
            connect: "lower",
            range: {
                'min': 0,
                'max': 100
            }
        });

        $("#slider-tooltips").Link('lower').to('-inline-<div class="tooltip fade top in" style="top: -33px;left: -14px;opacity: 0.7;"></div>', function(value) {
            // The tooltip HTML is 'this', so additional
            // markup can be inserted here.
            $(this).html(
                '<div class="tooltip-inner">' +
                '<span>' + value + '</span>' +
                '</div>'
            );
        });

    });

})(window.jQuery);