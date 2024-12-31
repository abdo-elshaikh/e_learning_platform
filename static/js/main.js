

// Show or hide the menu when the button is clicked
const menuToggle = document.getElementById('menu-toggle');
const sidebar = document.getElementById('sidebar');
// Mobile Navigation Toggle
const toggleBtn = document.getElementById('toggle-btn');
const toggleMenu = document.getElementById('toggle-menu');
toggleBtn.addEventListener('click', () => {
    toggleMenu.classList.toggle('hidden');
});



// Close Snackbar
document.querySelectorAll('.close-snack-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        this.parentElement.remove();
    });
});

// Scroll to Categories Section
const categoryBtn = document.getElementById('category-btn');
const categoriesSection = document.getElementById('categories');

// Scroll to the categories section when the button is clicked
if (categoryBtn && categoriesSection) {
    categoryBtn.addEventListener('click', () => {
        categoriesSection.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
        });
    });
}

// Scroll to Top Button
const backToTopBtn = document.querySelector('.back-to-top');

// Show or hide the back-to-top button based on scroll position
if (backToTopBtn) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopBtn.classList.remove('hidden');
        } else {
            backToTopBtn.classList.add('hidden');
        }
    });
}

// Custom scroll-to-top function with slower animation
function scrollToTop() {
    const scrollDuration = 900;
    const start = window.scrollY;
    const startTime = performance.now();

    function scrollStep(currentTime) {
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / scrollDuration, 1);
        const easeInOutQuad = progress < 0.5
            ? 2 * progress * progress
            : -1 + (4 - 2 * progress) * progress;

        window.scrollTo(0, start * (1 - easeInOutQuad));

        if (progress < 1) {
            requestAnimationFrame(scrollStep);
        }
    }

    requestAnimationFrame(scrollStep);
}

// Attach the custom scroll-to-top function to the button
if (backToTopBtn) {
    backToTopBtn.addEventListener('click', scrollToTop);
}


// Swiper slider
document.addEventListener('DOMContentLoaded', () => {
    const swiper = new Swiper('.swiper-container', {
        loop: true,
        spaceBetween: 30,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        autoplay: {
            delay: 4000,
            disableOnInteraction: false,
        },
        breakpoints: {
            640: {
                slidesPerView: 1,
            },
            1024: {
                slidesPerView: 2,
            }
        },
    });
});

const swiper = new Swiper('.swiper-container', {
    loop: true,
    autoplay: {
        delay: 5000,
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        640: {
            slidesPerView: 1,
            spaceBetween: 20,
        }
    }
});

