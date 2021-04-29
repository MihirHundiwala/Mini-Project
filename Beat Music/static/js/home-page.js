$(document).ready(function() {

    $(".btn").click(function() {
        $("input[type='text']").toggleClass("active");
    });

    var slider = $('#categories');

    slider.owlCarousel({
        margin: 10,
        items: 3,
        center: true,
        stagePadding: 30,
        loop: true,
        autoHeight: true,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 2
            },
            768: {
                items: 3
            },
        }
    });

    slider.on('mousewheel', '.owl-stage', function(e) {
        if (e.originalEvent.wheelDelta > 0) {
            slider.trigger('prev.owl');
        } else {
            slider.trigger('next.owl');
        }
        e.preventDefault();
    });

    var soul = $('#soul');
    soul.owlCarousel({
        margin: 10,
        stagePadding: 30,
        dots: false,
        nav: true,
        navText: ["<div class='nav-button owl-prev'>‹</div>", "<div class='nav-button owl-next'>›</div>"],
        responsive: {
            0: {
                items: 3
            },
            576: {
                items: 4
            },
            768: {
                items: 5
            },
            992: {
                items: 7,
            },
        }
    });

    soul.on('mousewheel', '.owl-stage', function(e) {
        if (e.originalEvent.wheelDelta > 0) {
            soul.trigger('prev.owl');
        } else {
            soul.trigger('next.owl');
        }
        e.preventDefault();
    });

    var romance = $('#romance');
    romance.owlCarousel({
        margin: 10,
        stagePadding: 30,
        dots: false,
        nav: true,
        navText: ["<div class='nav-button owl-prev'>‹</div>", "<div class='nav-button owl-next'>›</div>"],

        responsive: {
            0: {
                items: 3
            },
            576: {
                items: 4
            },
            768: {
                items: 5
            },
            992: {
                items: 7,
            },
        }
    });

    romance.on('mousewheel', '.owl-stage', function(e) {
        if (e.originalEvent.wheelDelta > 0) {
            romance.trigger('prev.owl');
        } else {
            romance.trigger('next.owl');
        }
        e.preventDefault();
    });

    var pop = $('#pop');
    pop.owlCarousel({
        margin: 10,
        stagePadding: 30,
        dots: false,
        nav: true,
        navText: ["<div class='nav-button owl-prev'>‹</div>", "<div class='nav-button owl-next'>›</div>"],

        responsive: {
            0: {
                items: 3
            },
            576: {
                items: 4
            },
            768: {
                items: 5
            },
            992: {
                items: 7,
            },
        }
    });

    pop.on('mousewheel', '.owl-stage', function(e) {
        if (e.originalEvent.wheelDelta > 0) {
            pop.trigger('prev.owl');
        } else {
            pop.trigger('next.owl');
        }
        e.preventDefault();
    });

    var bollywoodparty = $('#bollywoodparty');
    bollywoodparty.owlCarousel({
        margin: 10,
        stagePadding: 30,
        dots: false,
        nav: true,
        navText: ["<div class='nav-button owl-prev'>‹</div>", "<div class='nav-button owl-next'>›</div>"],

        responsive: {
            0: {
                items: 3
            },
            576: {
                items: 4
            },
            768: {
                items: 5
            },
            992: {
                items: 7,
            },
        }
    });

    bollywoodparty.on('mousewheel', '.owl-stage', function(e) {
        if (e.originalEvent.wheelDelta > 0) {
            bollywoodparty.trigger('prev.owl');
        } else {
            bollywoodparty.trigger('next.owl');
        }
        e.preventDefault();
    });

    var hiphop = $('#hiphop');
    hiphop.owlCarousel({
        margin: 10,
        stagePadding: 30,
        dots: false,
        nav: true,
        navText: ["<div class='nav-button owl-prev'>‹</div>", "<div class='nav-button owl-next'>›</div>"],

        responsive: {
            0: {
                items: 3
            },
            576: {
                items: 4
            },
            768: {
                items: 5
            },
            992: {
                items: 7,
            },
        }
    });

    hiphop.on('mousewheel', '.owl-stage', function(e) {
        if (e.originalEvent.wheelDelta > 0) {
            hiphop.trigger('prev.owl');
        } else {
            hiphop.trigger('next.owl');
        }
        e.preventDefault();
    });

    var oldsongs = $('#oldsongs');
    oldsongs.owlCarousel({
        margin: 10,
        stagePadding: 30,
        dots: false,
        nav: true,
        navText: ["<div class='nav-button owl-prev'>‹</div>", "<div class='nav-button owl-next'>›</div>"],

        responsive: {
            0: {
                items: 3
            },
            576: {
                items: 4
            },
            768: {
                items: 5
            },
            992: {
                items: 7,
            },
        }
    });

    oldsongs.on('mousewheel', '.owl-stage', function(e) {
        if (e.originalEvent.wheelDelta > 0) {
            oldsongs.trigger('prev.owl');
        } else {
            oldsongs.trigger('next.owl');
        }
        e.preventDefault();
    });
});