// Load product data from JSON
fetch("products.json")
  .then(response => response.json())
  .then(data => {
    const product = data[0]; // Show first product
    displayProduct(product);
  });

function displayProduct(product) {
  const container = document.getElementById("productContainer");

  const stars = "★".repeat(product.rating) + "☆".repeat(5 - product.rating);

  container.innerHTML = `
    <img class="product-image" src="${product.image}" alt="${product.title}" />
    <h1 class="product-title">${product.title}</h1>
    <div class="product-price">₹${product.price}</div>
    <div class="rating">${stars} (${product.rating} / 5)</div>
    <div class="product-description">${product.description}</div>
    <div class="reviews">
      <h4>Customer Reviews</h4>
      ${product.reviews.map(review => `<div class="review">"${review}"</div>`).join('')}
    </div>
  `;
}
