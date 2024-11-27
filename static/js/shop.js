function addToCart(productId) {
    fetch(`/add_to_cart/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ productId: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            updateCartCount(data.total_items);
            updateCartDisplay(data.cart_items);
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}


function removeFromCart(productId) {
    fetch(`/remove_from_cart/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ productId: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            updateCartCount(data.total_items);
            updateCartDisplay(data.cart_items);
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

function deleteFromCart(productId) {
    fetch(`/delete_from_cart/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ productId: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            updateCartCount(data.total_items);
            updateCartDisplay(data.cart_items);
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateCartCount(totalItems) {
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        cartCount.textContent = totalItems;
    }
}

function updateCartDisplay(cartItems) {
    const cartContainer = document.getElementById('cart-container');
    if (cartContainer) {
        cartContainer.innerHTML = '';
        if (cartItems.length > 0) {
            cartItems.forEach(item => {
                const cartItemHTML = `
                    <div class="cart-item">
                        <p>${item.name} (${item.quantity}) - $${item.total_price}</p>
                        <button onclick="addToCart(${item.id})">+</button>
                        <button onclick="removeFromCart(${item.id})">-</button>
                        <button onclick="deleteFromCart(${item.id})">Remove</button>
                    </div>
                `;
                cartContainer.innerHTML += cartItemHTML;
            });
        } else {
            cartContainer.innerHTML = '<p>Your cart is empty.</p>';
        }
    }
}

function getCSRFToken() {
    const cookieValue = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '{{ csrf_token }}';
}
document.addEventListener('DOMContentLoaded', () => {
    const quantityControls = document.querySelectorAll('.quantity-controls');

    quantityControls.forEach(control => {
        control.addEventListener('click', (event) => {
            const target = event.target;
            const productId = target.dataset.productId;
            let url = '';

            if (target.classList.contains('increase')) {
                url = `/increase_quantity/${productId}/`;
            } else if (target.classList.contains('decrease')) {
                url = `/decrease_quantity/${productId}/`;
            }

            if (url) {
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken') // Отримуємо токен CSRF
                    }
                })
                .then(response => {
                    if (response.ok) {
                        return response.text();
                    }
                    throw new Error('Network response was not ok.');
                })
                .then(() => {
                    window.location.reload(); // Перезавантаження сторінки
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
