// Load user profile data when page loads
document.addEventListener('DOMContentLoaded', async function() {
    try {
        // First, check if user is authenticated
        const authResponse = await fetch('/api/auth/status');
        const authData = await authResponse.json();

        if (!authData.authenticated) {
            // Redirect to login if not authenticated
            window.location.href = '/login';
            return;
        }

        // Get user's full profile data
        const userId = authData.user_id;
        const profileResponse = await fetch(`/api/users/${userId}`);
        const profileData = await profileResponse.json();

        if (profileData.success) {
            // Populate profile fields with user data
            document.getElementById('username').textContent = profileData.user.username;
            document.getElementById('email').textContent = profileData.user.email;
            document.getElementById('created-at').textContent = profileData.user.created_at;

            // Get wishlist count
            const wishlistResponse = await fetch(`/api/wishlist/${userId}`);
            if (wishlistResponse.ok) {
                const wishlistData = await wishlistResponse.json();
                if (wishlistData.success) {
                    document.getElementById('wishlist-count').textContent = wishlistData.items.length;
                } else {
                    document.getElementById('wishlist-count').textContent = '0';
                }
            } else {
                document.getElementById('wishlist-count').textContent = '0';
            }
        } else {
            // Error getting profile data
            alert('Error loading profile: ' + profileData.error);
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        alert('An error occurred while loading your profile.');
        window.location.href = '/';
    }
});
