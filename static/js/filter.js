function filterProducts() {
    let searchValue = document.getElementById("search").value.toLowerCase();
    let productCards = document.querySelectorAll(".product-card");
    
    productCards.forEach(card => {
        let productTitle = card.querySelector(".product-title").textContent.toLowerCase();
        if (productTitle.includes(searchValue)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}
function sortProducts() {
    let sortBy = document.getElementById("sort").value;  
    let productGrid = document.getElementById("product-grid");
    let productCards = Array.from(productGrid.getElementsByClassName("product-card"));
    productCards.sort((a, b) => {
        let valueA, valueB;

        if (sortBy === "price_asc" || sortBy === "price_desc") {
            valueA = parseFloat(a.querySelector(".product-price").textContent.replace('$', '').replace(',', ''));
            valueB = parseFloat(b.querySelector(".product-price").textContent.replace('$', '').replace(',', ''));
        } else if (sortBy === "date_asc" || sortBy === "date_desc") {
            let dateA = new Date(a.getAttribute('data-date'));
            let dateB = new Date(b.getAttribute('data-date'));

            if (sortBy === "date_asc") {
                return dateA - dateB;  
            } else if (sortBy === "date_desc") {
                return dateB - dateA;  
            }
        }
        if (sortBy === "price_asc" || sortBy === "price_desc") {
            return (sortBy === "price_asc" ? valueA - valueB : valueB - valueA);
        }

        valueA = a.querySelector(".product-title").textContent.trim();
        valueB = b.querySelector(".product-title").textContent.trim();
        return valueA.localeCompare(valueB);
    });
    productGrid.innerHTML = '';
    productCards.forEach(card => productGrid.appendChild(card));
}
