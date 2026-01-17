// Register ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

// 1. Basic Animation (Hero)
gsap.from('.title', {
    y: -50,
    opacity: 0,
    duration: 1,
    ease: 'power3.out'
});

gsap.from('.subtitle', {
    y: 50,
    opacity: 0,
    duration: 1,
    delay: 0.3,
    ease: 'power3.out'
});

gsap.to('.box-hero', {
    rotation: 360,
    duration: 2,
    repeat: -1,
    ease: 'linear'
});

// 2. ScrollTrigger Scrub
gsap.to('.box-scrub', {
    x: 500,
    rotation: 360,
    backgroundColor: '#00b894',
    scrollTrigger: {
        trigger: '.trigger-section',
        start: 'top center',
        end: 'bottom center',
        scrub: 1, // Smooth scrubbing
        // markers: true // Uncomment for debug markers
    }
});

// 3. Pinned Section
gsap.to('.box-pin', {
    scale: 3,
    rotation: 45,
    scrollTrigger: {
        trigger: '.pin-section',
        start: 'top top',
        end: '+=800', // Pin for 800px of scrolling
        pin: true,
        scrub: true
    }
});

// 4. Timeline
const tl = gsap.timeline({ paused: true });

tl.to('.box-a', { x: 100, rotation: 90, duration: 0.5 })
  .to('.box-b', { x: 100, rotation: -90, duration: 0.5 })
  .to('.box-c', { x: 100, rotation: 180, duration: 0.5 })
  .to('.timeline-container', { backgroundColor: '#dfe6e9', duration: 0.2 });

document.getElementById('play-timeline').addEventListener('click', () => {
    tl.restart();
});

// Trigger timeline on scroll just for fun
gsap.to('.timeline-section', {
    scrollTrigger: {
        trigger: '.timeline-section',
        start: 'top 80%',
        onEnter: () => tl.play()
    }
});
