gsap.registerPlugin(ScrollTrigger);

// 1. Hero Parallax
gsap.to('#hero-bg', {
    yPercent: 30, // Move background down slower than scroll
    ease: 'none',
    scrollTrigger: {
        trigger: '.hero-section',
        start: 'top top',
        end: 'bottom top',
        scrub: true
    }
});

// 2. Intro Text Reveal
const texts = gsap.utils.toArray('.fade-in');
texts.forEach(text => {
    gsap.to(text, {
        opacity: 1,
        y: 0,
        duration: 1,
        scrollTrigger: {
            trigger: text,
            start: 'top 80%', // When top of element hits 80% down viewport
            toggleActions: 'play none none reverse'
        }
    });

    // Set initial state via JS to avoid FOUC if JS fails
    gsap.set(text, { y: 30, opacity: 0 });
});

// 3. Pinned Section: Analytical Engine
// We want to pin the section, keep the image static, and scroll the cards on the right.

// Since CSS flexbox is simpler for layout, we can just pin the whole section 
// and animate the specific cards moving up.
const cards = gsap.utils.toArray('.scroll-card');
const totalScroll = 600; // Pixels to scroll specifically for this section

/* Reset logic for cleaner vertical scroll animation */

// Pin the section, move the text container
const textContainer = document.querySelector('.pin-text');

gsap.to(textContainer, {
    y: '-20%', // Simple shift up to show more content if needed, or we can use the timeline approach
    ease: 'none',
    scrollTrigger: {
        trigger: '.pinned-section',
        start: 'top top',
        end: '+=1500', 
        pin: true,
        scrub: 1
    }
});

// Let's refine the vertical scroll of the cards inside the pinned section
// We want them to slide up into view.
gsap.from(cards, {
    y: 100,
    opacity: 0,
    stagger: 0.5,
    scrollTrigger: {
        trigger: '.pinned-section',
        start: 'top top',
        end: '+=1000',
        scrub: 1
    }
});



// 4. Horizontal Scroll (Legacy)
const timelineContainer = document.querySelector('.timeline-container');

gsap.to(timelineContainer, {
    x: () => -(timelineContainer.scrollWidth - window.innerWidth),
    ease: 'none',
    scrollTrigger: {
        trigger: '.horizontal-scroll-wrapper',
        start: 'top top',
        end: () => `+=${timelineContainer.scrollWidth}`,
        pin: true,
        scrub: 1,
        invalidateOnRefresh: true // Handle resizes
    }
});
