// Wishlist functionality for product cards

document.addEventListener('DOMContentLoaded', function() {
    // Get all wishlist buttons
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');

    wishlistButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();

            const productId = this.getAttribute('data-product-id');
            const heartIcon = this.querySelector('i');
            const isInWishlist = heartIcon.classList.contains('fa-solid');

            // Check if user is authenticated first
            const authStatus = await checkAuthStatus();
            if (!authStatus.authenticated) {
                alert('Please login to add items to your wishlist');
                window.location.href = '/login';
                return;
            }

            if (isInWishlist) {
                // Remove from wishlist
                await removeFromWishlist(productId, heartIcon);
            } else {
                // Add to wishlist
                await addToWishlist(productId, heartIcon);
            }
        });
    });

    // Load wishlist state on page load
    loadWishlistState();
});

// Check if user is authenticated
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/status');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error checking auth status:', error);
        return { authenticated: false };
    }
}

// Add product to wishlist
async function addToWishlist(productId, heartIcon) {
    try {
        const response = await fetch('/api/wishlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: parseInt(productId) })
        });

        const data = await response.json();

        if (data.success) {
            // Change heart to filled
            heartIcon.classList.remove('fa-regular');
            heartIcon.classList.add('fa-solid');
            showNotification('Added to wishlist!', 'success');
        } else {
            if (response.status === 409) {
                // Already in wishlist
                heartIcon.classList.remove('fa-regular');
                heartIcon.classList.add('fa-solid');
                showNotification('Already in wishlist', 'info');
            } else {
                showNotification(data.error || 'Failed to add to wishlist', 'error');
            }
        }
    } catch (error) {
        console.error('Error adding to wishlist:', error);
        showNotification('Failed to add to wishlist', 'error');
    }
}

// Remove product from wishlist
async function removeFromWishlist(productId, heartIcon) {
    try {
        const response = await fetch('/api/wishlist', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: parseInt(productId) })
        });

        const data = await response.json();

        if (data.success) {
            // Change heart to outline
            heartIcon.classList.remove('fa-solid');
            heartIcon.classList.add('fa-regular');
            showNotification('Removed from wishlist', 'success');
        } else {
            showNotification(data.error || 'Failed to remove from wishlist', 'error');
        }
    } catch (error) {
        console.error('Error removing from wishlist:', error);
        showNotification('Failed to remove from wishlist', 'error');
    }
}

// Load wishlist state to show which items are already in wishlist
async function loadWishlistState() {
    try {
        const authStatus = await checkAuthStatus();
        if (!authStatus.authenticated) {
            return; // User not logged in, all hearts stay outline
        }

        const response = await fetch('/api/wishlist');
        if (!response.ok) return;

        const data = await response.json();

        if (data.success && data.products) {
            // Get all wishlist product IDs
            const wishlistIds = data.products.map(p => p.id);

            // Update heart icons for wishlisted products
            const wishlistButtons = document.querySelectorAll('.wishlist-btn');
            wishlistButtons.forEach(button => {
                const productId = parseInt(button.getAttribute('data-product-id'));
                if (wishlistIds.includes(productId)) {
                    const heartIcon = button.querySelector('i');
                    heartIcon.classList.remove('fa-regular');
                    heartIcon.classList.add('fa-solid');
                }
            });
        }
    } catch (error) {
        console.error('Error loading wishlist state:', error);
    }
}

// Show notification to user
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Style the notification
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = '15px 20px';
    notification.style.borderRadius = '8px';
    notification.style.zIndex = '10000';
    notification.style.fontWeight = '500';
    notification.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    notification.style.animation = 'slideIn 0.3s ease';

    // Set colors based on type
    if (type === 'success') {
        notification.style.backgroundColor = '#4CAF50';
        notification.style.color = 'white';
    } else if (type === 'error') {
        notification.style.backgroundColor = '#f44336';
        notification.style.color = 'white';
    } else {
        notification.style.backgroundColor = '#2196F3';
        notification.style.color = 'white';
    }

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
