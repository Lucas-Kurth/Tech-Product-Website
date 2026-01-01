// Wishlist page functionality

document.addEventListener('DOMContentLoaded', function() {
    loadWishlist();
});

async function loadWishlist() {
    try {
        const response = await fetch('/api/wishlist');

        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to load wishlist');
        }

        const data = await response.json();

        if (data.success) {
            displayWishlistProducts(data.products);
        }
    } catch (error) {
        console.error('Error loading wishlist:', error);
        showError('Failed to load wishlist. Please try again.');
    }
}

function displayWishlistProducts(products) {
    const header = document.querySelector('.header');

    // Create products container if it doesn't exist
    let container = document.querySelector('.wishlist-products-container');
    if (!container) {
        container = document.createElement('main');
        container.className = 'wishlist-products-container';
        header.insertAdjacentElement('afterend', container);
    }

    // Clear existing content
    container.innerHTML = '';

    if (products.length === 0) {
        container.innerHTML = `
            <div class="empty-wishlist">
                <i class="fa-regular fa-heart" style="font-size: 4rem; color: #ccc; margin-bottom: 1rem;"></i>
                <h2>Your wishlist is empty</h2>
                <p>Start adding products you love!</p>
                <a href="/" class="browse-btn">Browse Products</a>
            </div>
        `;
        return;
    }

    // Create wishlist table/list
    const wishlistList = document.createElement('div');
    wishlistList.className = 'wishlist-list';

    // Add header row
    const headerRow = document.createElement('div');
    headerRow.className = 'wishlist-header-row';
    headerRow.innerHTML = `
        <div class="wishlist-header-item">Product</div>
        <div class="wishlist-header-price">Price</div>
        <div class="wishlist-header-actions">Actions</div>
    `;
    wishlistList.appendChild(headerRow);

    // Add product rows
    products.forEach(product => {
        const row = createProductRow(product);
        wishlistList.appendChild(row);
    });

    container.appendChild(wishlistList);
}

function createProductRow(product) {
    const row = document.createElement('div');
    row.className = 'wishlist-row';
    row.innerHTML = `
        <div class="wishlist-item-info">
            <div class="wishlist-item-details">
                <h3 class="wishlist-item-name">${product.name}</h3>
                <p class="wishlist-item-description">${product.description}</p>
                <span class="wishlist-item-category">${product.category || 'Uncategorized'}</span>
            </div>
        </div>
        <div class="wishlist-item-price">
            <span class="price-label">$${product.price.toFixed(2)}</span>
        </div>
        <div class="wishlist-item-actions">
            <a href="${product.external_link}" target="_blank" class="view-product-btn" title="View Product">
                <i class="fa-solid fa-external-link"></i>
            </a>
            <button class="remove-btn" data-product-id="${product.id}" title="Remove from wishlist">
                <i class="fa-solid fa-trash"></i>
            </button>
        </div>
    `;

    // Add remove functionality
    const removeBtn = row.querySelector('.remove-btn');
    removeBtn.addEventListener('click', async function() {
        await removeFromWishlist(product.id, row);
    });

    return row;
}

async function removeFromWishlist(productId, cardElement) {
    try {
        const response = await fetch('/api/wishlist', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: productId })
        });

        const data = await response.json();

        if (data.success) {
            // Animate card removal
            cardElement.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                cardElement.remove();

                // Check if wishlist is now empty
                const cardsWrapper = document.querySelector('.cards-wrapper');
                if (cardsWrapper && cardsWrapper.children.length === 0) {
                    displayWishlistProducts([]);
                }
            }, 300);

            showNotification('Removed from wishlist', 'success');
        } else {
            showNotification(data.error || 'Failed to remove from wishlist', 'error');
        }
    } catch (error) {
        console.error('Error removing from wishlist:', error);
        showNotification('Failed to remove from wishlist', 'error');
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = '15px 20px';
    notification.style.borderRadius = '8px';
    notification.style.zIndex = '10000';
    notification.style.fontWeight = '500';
    notification.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    notification.style.animation = 'slideIn 0.3s ease';

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

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function showError(message) {
    const container = document.querySelector('.wishlist-products-container') || document.querySelector('main');
    if (container) {
        container.innerHTML = `
            <div class="error-message">
                <i class="fa-solid fa-exclamation-circle" style="font-size: 3rem; color: #f44336; margin-bottom: 1rem;"></i>
                <h2>Error</h2>
                <p>${message}</p>
                <button onclick="location.reload()" class="retry-btn">Retry</button>
            </div>
        `;
    }
}

// Add notification animations (these need to be in JS since they're dynamic)
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
