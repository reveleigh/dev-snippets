// Helper to log to the onscreen console in hooks.html
function logToScreen(message) {
    const consoleOutput = document.getElementById('console-log');
    if (consoleOutput) {
        const p = document.createElement('p');
        p.className = 'log-entry';
        p.textContent = `> ${message}`;
        consoleOutput.appendChild(p);
        consoleOutput.scrollTop = consoleOutput.scrollHeight;
    } else {
        console.log(message);
    }
}

// Visualize steps in hooks.html
function highlightStep(stepId) {
    const step = document.getElementById(stepId);
    if (step) {
        gsap.to(step, { scale: 1.2, backgroundColor: '#00b894', color: '#fff', duration: 0.2, yoyo: true, repeat: 1 });
    }
}

// Initialize Barba
barba.init({
    sync: true,
    debug: true,
    
    // Global Hooks
    hooks: {
        before(data) {
            logToScreen(`Before: ${data.trigger.href}`);
        },
        leave(data) {
            logToScreen('Leaving...');
            highlightStep('step-leave');
        },
        enter(data) {
            logToScreen('Entering...');
            highlightStep('step-enter');
        },
        after(data) {
            logToScreen('After transition complete.');
            // Update active nav link
            document.querySelectorAll('nav a').forEach(link => {
                link.classList.toggle('active', link.getAttribute('href') === data.next.url.path.replace(/^\//,'')); // simple check
            });
        }
    },

    transitions: [
        // 1. Transition TO 'transitions' namespace (Slide Effect)
        {
            name: 'slide-transition',
            to: {
                namespace: ['transitions']
            },
            async leave(data) {
                const done = this.async();
                
                // Slide blue panel in from right
                await gsap.to('.slide-transition-panel', {
                    x: '0%',
                    duration: 0.4,
                    ease: 'power2.inOut'
                });
                
                done();
            },
            enter(data) {
                // Scroll top
                window.scrollTo(0, 0);

                // Slide blue panel away to left
                gsap.set('.slide-transition-panel', { x: '0%' });
                gsap.to('.slide-transition-panel', {
                    x: '-100%',
                    duration: 0.4,
                    ease: 'power2.inOut',
                    clearProps: 'all'
                });

                // Animate content inside
                gsap.from(data.next.container, {
                    opacity: 0,
                    x: 50,
                    duration: 0.5,
                    delay: 0.2
                });
            }
        },
        
        // 2. Default Transition (Fade with Green Mask)
        {
            name: 'default-transition',
            // Default rules (applies if no other rule matches)
            
            async leave(data) {
                const done = this.async();
                
                // Animate the mask up
                await gsap.to('.transition-mask', {
                    y: '0%',
                    duration: 0.5,
                    ease: 'power2.inOut'
                });

                // Fade out current
                await gsap.to(data.current.container, {
                    opacity: 0,
                    duration: 0.2
                });

                done();
            },

            async enter(data) {
                window.scrollTo(0, 0);

                // Animate mask down
                gsap.to('.transition-mask', {
                    y: '-100%',
                    duration: 0.5,
                    ease: 'power2.inOut',
                    clearProps: 'all'
                });

                // Fade in new
                gsap.from(data.next.container, {
                    opacity: 0,
                    y: 20,
                    duration: 0.5,
                    delay: 0.2,
                    ease: 'power2.out'
                });
            }
        }
    ]
});
