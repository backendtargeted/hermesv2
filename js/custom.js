// Custom JavaScript for bababebi site
jQuery(document).ready(function($) {
    // Initialize Drupal behaviors
    if (typeof Drupal !== 'undefined') {
        Drupal.attachBehaviors(document);
    }
    
    // Custom menu handling (simplified version of original)
    var imageSrcDir = "/sites/all/themes/bababebi/images/menu/";
    var menuItems = [];
    
    // Handle menu items if they exist
    $.each($("#main-menu").children('li'), function(i, item) {
        var menuAnchorElement = $(item).children();
        var ultimoIndice = menuAnchorElement.attr('href').lastIndexOf("/");
        var linkName = menuAnchorElement.attr('href').substr(ultimoIndice+1);
        
        console.log("Processing menu item:", linkName);
        
        // Add hover effects for menu items
        menuAnchorElement.hover(
            function() {
                $(this).addClass('hover');
            },
            function() {
                $(this).removeClass('hover');
            }
        );
        
        menuItems.push(menuAnchorElement);
    });
    
    // Smooth scrolling for anchor links
    $('a[href*="#"]').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top - 100
                }, 1000);
                return false;
            }
        }
    });
    
    // Image lightbox functionality
    $('.views-field img').click(function() {
        var src = $(this).attr('src');
        var alt = $(this).attr('alt') || '';
        
        // Create lightbox overlay
        var lightbox = $('<div class="lightbox-overlay">' +
            '<div class="lightbox-content">' +
                '<span class="lightbox-close">&times;</span>' +
                '<img src="' + src + '" alt="' + alt + '">' +
            '</div>' +
        '</div>');
        
        $('body').append(lightbox);
        $('body').addClass('lightbox-open');
        
        // Close lightbox
        $('.lightbox-close, .lightbox-overlay').click(function() {
            lightbox.remove();
            $('body').removeClass('lightbox-open');
        });
        
        // Close on escape key
        $(document).keyup(function(e) {
            if (e.keyCode == 27) { // Escape key
                lightbox.remove();
                $('body').removeClass('lightbox-open');
            }
        });
    });
    
    // Add loading animation
    $(window).on('load', function() {
        $('body').addClass('loaded');
    });
    
    // Print functionality
    $('.print-button').click(function() {
        window.print();
    });
    
    // Social media link tracking (if analytics is needed)
    $('.view-footer a').click(function() {
        var platform = $(this).find('img').attr('alt');
        console.log('Social media click:', platform);
        // Add analytics tracking here if needed
    });
});

// Lightbox CSS (injected via JavaScript)
jQuery(document).ready(function($) {
    var lightboxCSS = `
        <style>
        .lightbox-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .lightbox-content {
            position: relative;
            max-width: 90%;
            max-height: 90%;
        }
        
        .lightbox-content img {
            max-width: 100%;
            max-height: 100%;
            border-radius: 5px;
        }
        
        .lightbox-close {
            position: absolute;
            top: -40px;
            right: 0;
            color: white;
            font-size: 30px;
            cursor: pointer;
            background-color: rgba(0, 0, 0, 0.5);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .lightbox-close:hover {
            background-color: rgba(0, 0, 0, 0.8);
        }
        
        .lightbox-open {
            overflow: hidden;
        }
        
        body.loaded {
            opacity: 1;
        }
        
        body {
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        </style>
    `;
    
    $('head').append(lightboxCSS);
});
