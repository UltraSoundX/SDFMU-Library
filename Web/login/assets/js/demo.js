/* ============================================================
 * Demo
 * Try various layout options available in Pages
 * For DEMO purposes only.
 * ============================================================ */
(function($) {

    'use strict';

    var rtlSwitch = $('#rtl-switch').get(0);

    // DEMO MODALS SIZE TOGGLER

    $('#btnToggleSlideUpSize').click(function() {
        var size = $('input[name=slideup_toggler]:checked').val()
        var modalElem = $('#modalSlideUp');
        if (size == "mini") {
            $('#modalSlideUpSmall').modal('show')
        } else {
            $('#modalSlideUp').modal('show')
            if (size == "default") {
                modalElem.children('.modal-dialog').removeClass('modal-lg');
            } else if (size == "full") {
                modalElem.children('.modal-dialog').addClass('modal-lg');
            }
        }
    });

    $('#btnStickUpSizeToggler').click(function() {
        var size = $('input[name=stickup_toggler]:checked').val()
        var modalElem = $('#myModal');
        if (size == "mini") {
            $('#modalStickUpSmall').modal('show')
        } else {
            $('#myModal').modal('show')
            if (size == "default") {
                modalElem.children('.modal-dialog').removeClass('modal-lg');
            } else if (size == "full") {
                modalElem.children('.modal-dialog').addClass('modal-lg');
            }
        }
    });

    // Only for fillin modals so that the backdrop action is still there
    $('#modalFillIn').on('show.bs.modal', function(e) {
        $('body').addClass('fill-in-modal');
    })
    $('#modalFillIn').on('hidden.bs.modal', function(e) {
        $('body').removeClass('fill-in-modal');
    })

    //END 

    //Typo Platform
    if ($('#platform').length) {
        var p = $.Pages.getUserPlatform();
        $('#platform').html('<strong>' + $.Pages.getUserPlatform() + '</strong>');
        var fontName;
        if (navigator.appVersion.indexOf("Win") != -1) fontName = "SegeoUI";
        if (navigator.appVersion.indexOf("Mac") != -1) fontName = "Helvetica Neue";
        if (navigator.appVersion.indexOf("X11") != -1) fontName = "Ubuntu";
        if (navigator.appVersion.indexOf("Linux") != -1) fontName = "Ubuntu";
        $('#font_name').text(fontName);
    }

    // START BUILDER


    var resetMenu = function() {
        $('body').removeClass(function(index, css) {
            return (css.match(/(^|\s)menu-\S+/g) || []).join(' ');
        });
    }
    var resetContent = function() {
        $('.page-content-wrapper').removeClass('active');
    }

    var changeTheme = function(name) {
        var rtl = rtlSwitch.checked ? '.rtl' : '';

        if (name == null) {
            $('.main-stylesheet').attr('href', 'pages/css/pages'+rtl+'.css');
            return;
        }
        $('.main-stylesheet').attr('href', 'pages/css/themes/' + name + rtl + '.min.css');
    }
    var layoutOption='1';
    var colorOption='1';
    var contentOption='1';

    $('#btnExport').click(function() {
        $( "#layout" ).val(layoutOption);
        $( "#colors" ).val(colorOption);
        $( "#content" ).val(contentOption);
         $( "#exportForm" ).submit();
    });
    $('.btn-toggle-layout').click(function() {
        $('.btn-toggle-layout').removeClass('active');
        var action = $(this).attr('data-action');
        $(this).addClass('active');
        switch (action) {
            case 'menuDefault':
                resetMenu();
                layoutOption='1';
                break;
            case 'menuPinned':
                resetMenu();
                $('body').addClass('menu-pin');
                layoutOption='2';
                break;
            case 'menuBelow':
                resetMenu();
                $('body').addClass('menu-behind');
                layoutOption='3';
                break;
            case 'menuPinnedBelow':
                resetMenu();
                $('body').addClass('menu-pin menu-behind');
                layoutOption='4';
                break;
        }
    });

    $('.btn-toggle-theme').click(function() {
        $('.btn-toggle-theme').removeClass('active');
        var action = $(this).attr('data-action');
        $(this).addClass('active');
        switch (action) {
            case 'default':
                changeTheme();
                colorOption='1';
                break;
            case 'corporate':
                changeTheme('corporate');
                colorOption='2';
                break;
            case 'retro':
                changeTheme('retro');
                colorOption='3';
                break;
            case 'unlax':
                changeTheme('unlax');
                colorOption='4';
                break;
            case 'vibes':
                changeTheme('vibes');
                colorOption='5';
                break;
            case 'abstract':
                changeTheme('abstract');
                colorOption='6';
                break;
        }
    });

    $('.btn-toggle-content').click(function() {
        $('.btn-toggle-content').removeClass('active');
        $('body').removeClass('horizontal-menu');

        var action = $(this).attr('data-action');
        $(this).addClass('active');
        switch (action) {
            case 'plainContent':
                resetContent();
                contentOption='1';
                $('#plainContent').addClass('active');
                break;
            case 'parallaxCoverpage':
                resetContent();
                contentOption='2';
                $('#parallaxCoverpage').addClass('active');
                break;
            case 'fullheightParallax':
                resetContent();
                contentOption='3';
                $('#fullheightParallax').addClass('active');
                $('#builder').toggleClass('open');
                break;
            case 'titleParallax':
                resetContent();
                contentOption='4';
                $('#titleParallax').addClass('active');
                break;
            case 'columns-3-9':
                resetContent();
                contentOption='5';
                $('#columns-3-9').addClass('active');
                break;
            case 'columns-9-3':
                resetContent();
                contentOption='6';
                $('#columns-9-3').addClass('active');
                $('#builder').toggleClass('open');
                break;
            case 'columns-6-6':
                resetContent();
                contentOption='7';
                $('#columns-6-6').addClass('active');
                $('#builder').toggleClass('open');
                break;
            case 'horizontal-menu':
                resetContent();
                contentOption='8';
                $('#horizontal-menu').addClass('active');
                $('body').addClass('horizontal-menu');
                break;
        }
    });

    if(rtlSwitch !=null){
        rtlSwitch.onchange = function() {
            if(rtlSwitch.checked){
                $('body').addClass('rtl');
                $('.main-stylesheet').attr('href', 'pages/css/themes/modern.rtl.css');
            } else {
                $('body').removeClass('rtl')
                $('.main-stylesheet').attr('href', 'pages/css/themes/modern.css');

            }
        };
    }
    // END BUILDER

})(window.jQuery);