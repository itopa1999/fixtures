/* ========================================
   AUTH PAGE - Background Animation & Form Handler
   ======================================== */

(function() {
    const shape1 = document.getElementById('shape1');
    const shape2 = document.getElementById('shape2');

    // remove any CSS animation (just to be sure, override style)
    shape1.style.animation = 'none';
    shape2.style.animation = 'none';

    let mouseX = 0.5, mouseY = 0.5; // default center
    let targetMouseX = 0.5, targetMouseY = 0.5;
    const WINDOW_WIDTH = window.innerWidth;
    const WINDOW_HEIGHT = window.innerHeight;

    // update mouse target
    window.addEventListener('mousemove', (e) => {
        targetMouseX = e.clientX / window.innerWidth;
        targetMouseY = e.clientY / window.innerHeight;
    });

    // also reset on window resize
    window.addEventListener('resize', () => {
        // keep proportions, no extra action
    });

    // animation loop for smooth drift & mouse follow
    const MAX_SHIFT = 28; // max translation in px
    let time = 0;

    function animateShapes() {
        time += 0.005; // slow oscillation

        // smooth mouse follow (easing)
        mouseX += (targetMouseX - mouseX) * 0.05;
        mouseY += (targetMouseY - mouseY) * 0.05;

        // center-based: range -1..1
        const mX = (mouseX - 0.5) * 2;
        const mY = (mouseY - 0.5) * 2;

        // idle sinusoidal drift (gentle) – separate for each shape
        const idleX1 = Math.sin(time * 0.8) * 8;
        const idleY1 = Math.cos(time * 0.6) * 6;
        const idleX2 = Math.sin(time * 0.5 + 2) * 10;
        const idleY2 = Math.cos(time * 0.7 + 1) * 9;

        // mouse contribution (different intensity per shape)
        const mouseX1 = mX * MAX_SHIFT * 0.8;
        const mouseY1 = mY * MAX_SHIFT * 0.6;
        const mouseX2 = mX * MAX_SHIFT * -0.5; // opposite direction
        const mouseY2 = mY * MAX_SHIFT * -0.7;

        // combine idle + mouse
        const translateX1 = idleX1 + mouseX1;
        const translateY1 = idleY1 + mouseY1;
        const translateX2 = idleX2 + mouseX2;
        const translateY2 = idleY2 + mouseY2;

        shape1.style.transform = `translate(${translateX1}px, ${translateY1}px)`;
        shape2.style.transform = `translate(${translateX2}px, ${translateY2}px)`;

        requestAnimationFrame(animateShapes);
    }

    animateShapes();

    // ---------- login form handler using modals ----------
    const form = document.getElementById('loginForm');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        
        // Show preloader
        preloader.show();

        // Simulate API call
        setTimeout(() => {
            preloader.hide();
            
            if (username === '' || password === '') {
                showError('Please enter both username and password.', 'Validation Error');
            } else {
                // Show success dialog before redirecting
                showConfirm(
                    `Welcome back, ${username}!\n\nRedirecting to dashboard...`,
                    () => {
                        // Redirect or perform other actions
                        console.log('User authenticated:', username);
                    },
                    {
                        title: 'Login Successful',
                        confirmText: 'Continue',
                        isDangerous: false
                    }
                );
            }
        }, 1500);
    });

    // subtle autofocus (optional)
    document.getElementById('username').focus();
})();
