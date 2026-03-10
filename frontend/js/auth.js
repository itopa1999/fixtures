/* ========================================
   AUTH PAGE - Form Handler
   ======================================== */

(function() {
    // ---------- login form handler ----------
    const form = document.getElementById('loginForm');
    const loginBtn = form.querySelector('.login-btn');
    let isSubmitting = false; // Prevent multiple submissions
    
    loginBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        
        // Prevent multiple submissions
        if (isSubmitting) return;
        isSubmitting = true;
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        
        // Show preloader
        preloader.show();

        if (username === '' || password === '') {
            preloader.hide();
            showError('Please enter both username and password.', 'Validation Error');
            isSubmitting = false;
            return;
        }

        try {
            // Send credentials via POST request body to backend
            const response = await fetch(`${window.ADMIN_URL}auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
            });

            preloader.hide();

            if (response.ok) {
                const data = await response.json();
                isSubmitting = false; // Reset flag for success
                // Redirect silently to index
                window.location.href = 'index.html';
            } else {
                isSubmitting = false; // Reset flag for error
                const errorData = await response.json().catch(() => ({ message: 'Login failed' }));
                showError(errorData.message || 'Login failed. Please check your credentials.', 'Login Error');
            }
        } catch (error) {
            preloader.hide();
            console.error('Login error:', error);
            showError('An error occurred during login. Please try again.', 'Network Error');
            isSubmitting = false;
        }
    });

    // subtle autofocus (optional)
    document.getElementById('username').focus();
})();
