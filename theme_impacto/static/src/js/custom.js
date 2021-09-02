
/*************************
      Predefined Variables
*************************/ 
var COMERCIO = {};

 (function($){
  "use strict"; 
/*************************
      Predefined Variables
*************************/ 
 
  var $window = $(window),
  $document = $(document),
  $body = $('body'),
  $bar = $('.bar'),
  $header = $('header');


 /*************************
        Check if function exists
*************************/ 
     $.fn.exists = function () {
        return this.length > 0;
    };


 /*************************
       counter
*************************/  
 COMERCIO.counters = function () {
     var $counter = $('.counter-box');
          if ($counter.exists()) {
              $counter.each(function () {
                  var $elem = $(this);
                       $elem.appear(function () {                       
                          $elem.find('.timer').countTo();
                       });   
              });
          }
  };


/*************************
       owl-carousel 
*************************/
 COMERCIO.carousel = function () {
    $(".owl-carousel").each(function () {
        var $this = $(this),
            $items = ($this.data('items')) ? $this.data('items') : 1,
            $loop = ($this.attr('data-loop')) ? $this.data('loop') : true,
            $navdots = ($this.data('nav-dots')) ? $this.data('nav-dots') : false,
            $navarrow = ($this.data('nav-arrow')) ? $this.data('nav-arrow') : false,
            $autoplay = ($this.attr('data-autoplay')) ? $this.data('autoplay') : true,
            $space = ($this.attr('data-space')) ? $this.data('space') : 30;       
           
            $(this).owlCarousel({
                loop: false,
                mouseDrag: false,
                touchDrag: false,
                pullDrag: false,
                items: $items,
                responsive: {
                  0:{items: $this.data('xx-items') ? $this.data('xx-items') : 1},
                  499:{items: $this.data('xs-items') ? $this.data('xs-items') : 1},
                  768:{items: $this.data('sm-items') ? $this.data('sm-items') : 2},
                  980:{items: $this.data('md-items') ? $this.data('md-items') : 3},
                  1200:{items: $items}
                },

                dots: $navdots,
                margin:$space,
                nav: $navarrow,
                navText:["<i class='fa fa-angle-left fa-2x'></i>","<i class='fa fa-angle-right fa-2x'></i>"],
                autoplay: false,
                autoplayHoverPause: true   
           });           
    });
}

/*************************
       Magnific Popup
************************/
COMERCIO.mediaPopups = function () {
    if ($(".popup-img").exists()) {
          $('.popup-img').magnificPopup({
              type: 'image',
              tLoading: 'Loading image #%curr%...',
              mainClass: 'mfp-img-mobile',
              gallery: {
                  enabled: true,
                  navigateByImgClick: true,
                  preload: [0,1] // Will preload 0 - before current, and 1 after the current image
              },
              image: {
                  tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
                  titleSrc: function(item) {
                      return item.el.attr('title') + '<small>by Marsel Van Oosten</small>';
                  }
             }
         }); 
      }
      if ($(".popup-youtube, .popup-vimeo, .popup-gmaps").exists()) {
           $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
                disableOn: 700,
                type: 'iframe',
                mainClass: 'mfp-fade',
                removalDelay: 160,
                preloader: false,
                fixedContentPos: false
          });
      }
  }

/*************************
       Progressbar
*************************/  
// COMERCIO.progressBar = function () {
//    var $progressBar = $('.progress-bar');
//     if ($progressBar.exists()) {
//         $progressBar.each(function (i, elem) {
//             var $elem = $(this),
//                 percent = $elem.attr('data-percent') || "100",
//                 delay = $elem.attr('data-delay') || "100",
//                 type = $elem.attr('data-type') || "%";
//             if (!$elem.hasClass('progress-animated')) {
//                 $elem.css({
//                     'width': '0%'
//                 });
//             }
//         var progressBarRun = function () {
//             $elem.animate({
//                 'width': percent + '%'
//             }, 'easeInOutCirc').addClass('progress-animated');
//              $elem.delay(delay).append('<span class="progress-type animated fadeIn">' + type + '</span><span class="progress-number animated fadeIn">' + percent + '</span>');
//         };
//         $(elem).appear(function () {
//                 setTimeout(function () {
//                     progressBarRun();
//                 }, delay);
//             });
//         });
//       }
// };

 

/*************************
         Product Details
*************************/
COMERCIO.product_details = function () {
     $("#pro_detail_zoom.owl-carousel").owlCarousel({
            items: 1,
            margin: 30,
            navigation: true,
            pagination: false
    })
    $("#o-carousel-product .carousel-indicators").mCustomScrollbar();
    $('.menu-filter').click(function() {
      $("#products_grid_before").css({
          "width": "300px",
          "transition": "0.5s"
      });
      $("#wrapwrap").css({
          "margin-left": "300px",
          "transition": "0.5s"
      });
     $('body').css("overflow-x", "hidden"); 
     $('.popup-overlay').addClass('active');
  });
    $('.popup-overlay').click(function() {
       $(this).removeClass('active');
         $("#products_grid_before").css({
            "width": "0",
            "transition": "0.5s"
        });
         $("#wrapwrap").css({
          "margin-left": "0",
          "transition": "0.5s"
      });
    });

  $('.mobile-view-filter-close-btn').click(function() {
      $("#products_grid_before").css({
          "width": "0px",
          "transition": "0.5s"
      });
      $("#wrapwrap").css({
          "margin-left": "0px",
          "transition": "0.5s"
      });
      $(".main-header-maxW").removeClass("transparent");
  });


}


/*************************
  Search Box
*************************/
COMERCIO.searchbox = function (e) {
    $('a[href="#search-but"]').on("click", function(event) {
      event.preventDefault();
      $("#search-box").addClass("open");
      $('#search-box > form > input.search-input').focus();
    });
  $("#search-box, #search-box button.close").on("click keyup", function(event) {
    if (
      event.target == this ||
      event.target.className == "close" ||
      event.keyCode == 27
    ) {
      $(this).removeClass("open");
    }
  });
  $("#search-box form").submit(function(event) {
      $("#search-box").removeClass("open");
   // return false;
  });
}


/*************************
  Search Box
*************************/
COMERCIO.shoppageview = function () {
    $(".new-filter .shift_list_view").click(function(e) {
        $(".new-filter button").removeClass('active');
        $(this).addClass('active');
        $('#products_grid').removeClass("list-view-box").removeClass("grid-view-box");
        $('#products_grid').addClass("list-view-box");        
        localStorage.setItem("product_view", "list");

    });
    $(".new-filter .shift_grid_view").click(function(e) {
       $(".new-filter button").removeClass('active');
        $(this).addClass('active')
        $('#products_grid').removeClass("list-view-box").removeClass("grid-view-box");
        localStorage.setItem("product_view", "grid");
    });

     $(".new-filter .shift_grid_view2").click(function(e) {
        $(".new-filter button").removeClass('active');
        $(this).addClass('active')
        $('#products_grid').removeClass("list-view-box").removeClass("grid-view-box");
        $('#products_grid').addClass("grid-view-box");
        localStorage.setItem("product_view2", "grid2");
    });

    if (localStorage.getItem("product_view") == 'list') {
       $(".new-filter button").removeClass('active');
        $(".new-filter .shift_list_view").addClass('active')
        $('#products_grid').addClass("list-view-box");
    }
    if (localStorage.getItem("product_view") == 'grid') {
        $(".new-filter button").removeClass('active');
        $(".new-filter .shift_grid_view").addClass('active')
        $('#products_grid').removeClass("list-view-box");
    }   
}


/*************************
  Pallaraxbanner
*************************/
COMERCIO.pallaraxbanner = function () {
    var lFollowX = 0,
    lFollowY = 0,
    x = 0,
    y = 0,
    friction = 1 / 30;

    function moveBackground() {
      x += (lFollowX - x) * friction;
      y += (lFollowY - y) * friction;

     var translate = 'translate(' + x + 'px, ' + y + 'px) scale(1.1)';

      $('.pallarax-move').css({
        '-webit-transform': translate,
        '-moz-transform': translate,
        'transform': translate
      });

      window.requestAnimationFrame(moveBackground);
    }

    $("#carousel-1").mousemove(function(e){
        var lMouseX = Math.max(-100, Math.min(100, $(window).width() / 2 - e.clientX));
        var lMouseY = Math.max(-100, Math.min(100, $(window).height() / 2 - e.clientY));
        lFollowX = (20 * lMouseX) / 100; // 100 : 12 = lMouxeX : lFollow
        lFollowY = (10 * lMouseY) / 100;
    });

    moveBackground();
}


/*************************
  Pallaraxbanner
*************************/
COMERCIO.megamenu_countdown = function () {

  //Mobile menu
  $(".mm-mega-menu > a").click(function(event) {
     event.preventDefault();
     $(this).parent().toggleClass("open-mob-menu");
     $(this).toggleClass("mob-menu-open");
  });


  $('.countdown').countdown({
      zeroCallback: function(options) {
        $('.countdown').fadeOut();
      }
    });
}


$(window).scroll(function() {
    if ($(window).scrollTop() >= 250) {
        $('body').addClass('sticky-header');
    } else {
        $('body').removeClass('sticky-header');
    }
});



/****************************************************
     COMERCIO Window load and functions
****************************************************/
  

 //Document ready functions
    $document.ready(function () {   
		COMERCIO.carousel();	
        COMERCIO.counters(), 
        COMERCIO.mediaPopups(),
        COMERCIO.searchbox(),
        COMERCIO.product_details(),
        COMERCIO.pallaraxbanner(),
        COMERCIO.megamenu_countdown(),
        COMERCIO.shoppageview();
        
        $('#menu-trigger').click(function(){
			      $(this).toggleClass('open');
			      $('#overlay-menu').toggleClass('menu-open');
		    });
        $('#ad-carousel-product .owl-thumbs').remove();
        
        
        if($("header").hasClass("head-left"))
        {
             $("body").addClass("header-left");
        }
        
        $("header .search_expand, .search_expand, .affixed search_expand").on("click", function(event){
            $(".search_expand").toggleClass("ct-search-expand");
            event.stopPropagation();
        });
        
        $('body').on('click', '#search_close', function() {
       
            $(".search_expand").removeClass("ct-search-expand");
            
        });
        
        
        if($( "header" ).children().hasClass("header-li"))
        {
            $( "header" ).addClass("header site-header header-light");
        }
        
        $("body").on('click',".js-copy", function() {
    			var target_id = $(this).attr("data-content-target");
    			var target_html = $('#' + target_id).html();
    			$("#html_data").val(target_html);
    			$("#sub_data").click();
		  });
		  $("body").on("click", ".builder a.nav-link", function(){
    			var x = $(this).attr("href");
    			x = x.replace("#", "");
    			$(".tab-content .tab-pane").each(function(){
    				var y = $(this).attr("id");
    				if (x == y) $(this).addClass("active show");
    				else $(this).removeClass("active show");
    			});
      });
    });
    
 
    
    

    /* Variables */
    var $verticalCollapsibleMenu = $('#hamburger-menu'),
        $verticalCollapsibleSubMenu = $verticalCollapsibleMenu.find('.submenu');
    
    /* Close Off Canvas Sub Menu */
    $verticalCollapsibleSubMenu.slideUp();

    /* Category Sub Menu Toggle */
    $verticalCollapsibleMenu.on('click', 'li a', function(e) {
        var $this = $(this);
        if ( $this.siblings('.submenu').length) {
            e.preventDefault();
            if ($this.siblings('ul:visible').length){
                $this.siblings('ul').slideUp();
            }else {
                $this.closest('li').siblings('li').find('ul:visible').slideUp();
                $this.siblings('ul').slideDown();
            }
        }
	  });
})(jQuery);



