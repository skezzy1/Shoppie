(function($) {
    $(document).ready(function() {
        const sizesField = $('#id_sizes');
        const categoryField = $('#id_product_category');

        categoryField.change(function() {
            const category = parseInt($(this).val());
            let sizes = [];
            if (category === 1) { // Jeans
                sizes = ["28", "30", "32", "34", "36"];
            } else if (category === 2) { // Shirts
                sizes = ["S", "M", "L", "XL", "XXL"];
            } else if (category === 3) { // Trousers
                sizes = ["28", "30", "32", "34", "36"];
            } else if (category === 4) { // Shorts
                sizes = ["28", "30", "32", "34", "36"];
            } else if (category === 5) { // T-shirts
                sizes = ["S", "M", "L", "XL"];
            } else if (category === 6) { // Footwear
                sizes = ["40", "41", "42", "43", "44"];
            } else if (category === 7) { // Jackets
                sizes = ["S", "M", "L", "XL", "XXL"];
            }
            sizesField.val(JSON.stringify(sizes));
        });
    });
})(django.jQuery);

function selectSize(size) {
    const selectedColor = '#28a745'; 
    const selectedTextColor = 'white'; 

    document.getElementById('selected-size').value = size;
    document.querySelectorAll('.size-button').forEach(button => {
        button.classList.remove('selected');
        button.style.backgroundColor = ''; 
        button.style.color = ''; 
    });

    const selectedButton = document.querySelector(`[onclick="selectSize('${size}')"]`);
    selectedButton.classList.add('selected');
    selectedButton.style.backgroundColor = selectedColor;
    selectedButton.style.color = selectedTextColor;
}

function validateSizeSelection() {
    const selectedSize = document.getElementById('selected-size').value;
    if (!selectedSize) {
        alert('Please select a size before adding to cart.');
        return false;
    }
    return true;
}


document.getElementById('add-to-cart-form').addEventListener('submit', function(event) {
    const selectedSize = document.getElementById('selected-size').value;
    if (!selectedSize) {
        alert("Please select a size before adding to cart.");
        event.preventDefault();  
    }
});

