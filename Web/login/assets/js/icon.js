/* ============================================================
 * Icons
 * Demo page to show icons used in Pages
 * For DEMO purposes only. Extract what you need.
 * ============================================================ */
(function($) {

    'use strict';

    $(document).ready(function() {
        $(".icon-list").sieve({
            searchInput: $('#icon-filter'),
            itemSelector: ".fa-item"
        });

        $('#icon-filter').on('keyup', function() {
            if ($(this).val()) {
                $('#icon-list').removeClass('hidden');
                $('.icon-set-preview').css('opacity', '0');
                $('#icon-list').css('transform', 'translateY(-260px)');
                $("html, body").stop().animate({
                    scrollTop: "250px"
                });
            } else {
                $('#icon-list').css('transform', 'translateY(0)');
                $('.icon-set-preview').css('opacity', '1');
                $('#icon-list').addClass('hidden');
                $("html, body").stop().animate({
                    scrollTop: "0px"
                });
            }
        });
    });

})(window.jQuery);