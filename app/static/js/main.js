// Shopping Cart Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Update cart count
    function updateCartCount() {
        fetch('/cart/count')
            .then(response => response.json())
            .then(data => {
                document.querySelector('.badge').textContent = data.count;
            });
    }

    // Add to cart
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartCount();
                    // Show success message
                    const alert = document.createElement('div');
                    alert.className = 'alert alert-success alert-dismissible fade show';
                    alert.innerHTML = `
                        ${data.message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    `;
                    document.querySelector('.container').prepend(alert);
                    
                    // Auto dismiss after 3 seconds
                    setTimeout(() => {
                        alert.remove();
                    }, 3000);
                }
            });
        });
    });

    // Remove from cart
    document.querySelectorAll('.remove-from-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            
            fetch(`/cart/remove/${itemId}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartCount();
                    // Remove item row
                    this.closest('tr').remove();
                    
                    // Update total
                    document.querySelector('.cart-total').textContent = `$${data.total.toFixed(2)}`;
                    
                    // If cart is empty, show empty cart message
                    if (data.count === 0) {
                        document.querySelector('.cart-items').innerHTML = '<p>Your cart is empty.</p>';
                        document.querySelector('.checkout-button').style.display = 'none';
                    }
                }
            });
        });
    });

    // Update cart quantity
    document.querySelectorAll('.update-quantity').forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.dataset.itemId;
            const quantity = this.value;
            
            fetch(`/cart/update/${itemId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity: quantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update subtotal
                    this.closest('tr').querySelector('.item-total').textContent = `$${data.subtotal.toFixed(2)}`;
                    // Update total
                    document.querySelector('.cart-total').textContent = `$${data.total.toFixed(2)}`;
                }
            });
        });
    });
}); 