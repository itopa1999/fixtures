/* ========================================
   DASHBOARD PAGE - Background Animation & Main Handler
   ======================================== */

(function() {
    const shape1 = document.getElementById('shape1');
    const shape2 = document.getElementById('shape2');

    // remove any CSS animation (just to be sure, override style)
    if (shape1) shape1.style.animation = 'none';
    if (shape2) shape2.style.animation = 'none';

    let mouseX = 0.5, mouseY = 0.5; // default center
    let targetMouseX = 0.5, targetMouseY = 0.5;
    const WINDOW_WIDTH = window.innerWidth;
    const WINDOW_HEIGHT = window.innerHeight;

    // update mouse target
    window.addEventListener('mousemove', (e) => {
        targetMouseX = e.clientX / window.innerWidth;
        targetMouseY = e.clientY / window.innerHeight;
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

        if (shape1) shape1.style.transform = `translate(${translateX1}px, ${translateY1}px)`;
        if (shape2) shape2.style.transform = `translate(${translateX2}px, ${translateY2}px)`;

        requestAnimationFrame(animateShapes);
    }

    animateShapes();

    // ---------- Dashboard handler ----------
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Show confirm dialog
            showConfirm(
                'Are you sure you want to log out?',
                () => {
                    // Clear cookies
                    document.cookie = 'access=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
                    document.cookie = 'refresh=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
                    document.cookie = 'email=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
                    document.cookie = 'name=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
                    document.cookie = 'group=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
                    
                    // Redirect to login
                    window.location.href = 'auth.html';
                },
                {
                    title: 'Logout',
                    confirmText: 'Yes, Logout',
                    isDangerous: true
                }
            );
        });
    }

    // Load user data from cookies
    const userName = window.userName || 'User';
    const userEmail = window.userEmail || '';
    
    // Update header with user info
    const userNameElem = document.getElementById('userName');
    const userEmailElem = document.getElementById('userEmail');
    if (userNameElem) userNameElem.textContent = userName;
    if (userEmailElem) userEmailElem.textContent = userEmail;
})();
