// Check authentication status and update navbar accordingly
async function updateNavbar() {
    try {
        const response = await fetch('/api/auth/status');
        const data = await response.json();

        const navActions = document.querySelector('.nav-actions');

        if (data.authenticated) {
            // User is logged in - show personalized navbar
            navActions.innerHTML = `
                <a href="/profile" class="nav-icon" title="Profile">
                    <i class="fa-regular fa-user"></i>
                </a>
                <span class="nav-username">Welcome, ${data.username}!</span>
                <a href="/wishlist" class="nav-btn nav-btn-wishlist">Wishlist</a>
                <button id="logoutBtn" class="nav-btn nav-btn-logout">Logout</button>
            `;

            // Add logout functionality
            const logoutBtn = document.getElementById('logoutBtn');
            logoutBtn.addEventListener('click', async () => {
                try {
                    const logoutResponse = await fetch('/api/logout', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    const logoutData = await logoutResponse.json();

                    if (logoutData.success) {
                        // Redirect to home and reload to show logged-out navbar
                        window.location.href = '/';
                    } else {
                        alert('Logout failed. Please try again.');
                    }
                } catch (error) {
                    console.error('Logout error:', error);
                    alert('An error occurred during logout.');
                }
            });

        } else {
            // User is NOT logged in - show login/register buttons
            navActions.innerHTML = `
                <a href="/wishlist" class="nav-btn nav-btn-wishlist">Wishlist</a>
                <a href="/login" class="nav-btn nav-btn-login">Login</a>
                <a href="/register" class="nav-btn nav-btn-register">Register</a>
            `;
        }
    } catch (error) {
        console.error('Error checking auth status:', error);
    }
}

// Run when page loads
document.addEventListener('DOMContentLoaded', updateNavbar);
