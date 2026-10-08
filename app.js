// ApexMart AI Dynamic Pricing Client Application

let allProducts = [];
let activeCategory = 'All';
let currentSearch = '';
let currentSort = 'default';
let currentPage = 1;
let totalPages = 1;
let totalCount = 0;
let pageLimit = 24;
let cart = [];

// Active Dynamic Pricing State
let selectedProduct = null;
let currentPricingData = null;
let pricingChartInstance = null;
let activeChartMode = 'revenue'; // 'revenue' or 'probability'
let batchOptimizationData = null;

// ==================== DEALS CAROUSEL ====================
let carouselIndex = 0;
let carouselTotal = 4;
let carouselAutoplayTimer = null;

function initCarousel() {
  carouselTotal = document.querySelectorAll('.deal-slide').length;
  carouselGoTo(0);
  startCarouselAutoplay();
  initDealTimers();
}

function carouselGoTo(idx) {
  const slides = document.querySelectorAll('.deal-slide');
  const dots = document.querySelectorAll('.carousel-dot');
  slides.forEach(s => s.classList.remove('active'));
  dots.forEach(d => d.classList.remove('active'));
  carouselIndex = ((idx % carouselTotal) + carouselTotal) % carouselTotal;
  if (slides[carouselIndex]) slides[carouselIndex].classList.add('active');
  if (dots[carouselIndex]) dots[carouselIndex].classList.add('active');
}

function carouselNext() {
  carouselGoTo(carouselIndex + 1);
  restartCarouselAutoplay();
}

function carouselPrev() {
  carouselGoTo(carouselIndex - 1);
  restartCarouselAutoplay();
}

function startCarouselAutoplay() {
  carouselAutoplayTimer = setInterval(() => carouselGoTo(carouselIndex + 1), 5000);
}

function restartCarouselAutoplay() {
  clearInterval(carouselAutoplayTimer);
  startCarouselAutoplay();
}

// Live countdown timers for deals
function initDealTimers() {
  // Each deal ends at a different fixed seconds-from-now offset for realism
  const offsets = [
    5 * 3600 + 42 * 60 + 17,
    3 * 3600 + 15 * 60 + 44,
    7 * 3600 + 58 * 60 + 2,
    1 * 3600 + 29 * 60 + 55
  ];
  const starts = offsets.map(o => Date.now() + o * 1000);
  const ids = [
    ['t1-h','t1-m','t1-s'],
    ['t2-h','t2-m','t2-s'],
    ['t3-h','t3-m','t3-s'],
    ['t4-h','t4-m','t4-s'],
  ];

  function tick() {
    const now = Date.now();
    ids.forEach((trio, i) => {
      let rem = Math.max(0, Math.floor((starts[i] - now) / 1000));
      const h = Math.floor(rem / 3600); rem -= h * 3600;
      const m = Math.floor(rem / 60);   rem -= m * 60;
      const s = rem;
      const hEl = document.getElementById(trio[0]);
      const mEl = document.getElementById(trio[1]);
      const sEl = document.getElementById(trio[2]);
      if (hEl) hEl.textContent = String(h).padStart(2,'0');
      if (mEl) mEl.textContent = String(m).padStart(2,'0');
      if (sEl) sEl.textContent = String(s).padStart(2,'0');
    });
  }
  tick();
  setInterval(tick, 1000);
}
// ==================== END CAROUSEL ====================

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  fetchProducts(1);
  fetchModelStats();
  initCarousel();
});


// Toast notification helper
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <i class="fa-solid ${type === 'success' ? 'fa-circle-check' : 'fa-circle-info'}"></i>
    <span>${message}</span>
  `;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Helper to render realistic full/half/empty stars with review count
function renderStarRating(score, reviewsCount) {
  const fullStars = Math.floor(score);
  const hasHalf = (score - fullStars) >= 0.4;
  let starsHtml = '';
  
  for (let i = 1; i <= 5; i++) {
    if (i <= fullStars) {
      starsHtml += '<i class="fa-solid fa-star"></i>';
    } else if (i === fullStars + 1 && hasHalf) {
      starsHtml += '<i class="fa-solid fa-star-half-stroke"></i>';
    } else {
      starsHtml += '<i class="fa-regular fa-star" style="color: #cbd5e1;"></i>';
    }
  }
  
  let color = score >= 4.2 ? '#d97706' : (score >= 3.0 ? '#ca8a04' : '#ef4444');
  
  return `
    <div class="product-rating" style="color: ${color};">
      <span class="stars-icon-group">${starsHtml}</span>
      <span style="font-weight: 700; margin-left: 2px;">${score.toFixed(1)}</span>
      <span style="color: var(--text-light); font-weight: 400; font-size: 0.76rem;">(${reviewsCount.toLocaleString()})</span>
    </div>
  `;
}

// Fetch Catalog Products with Pagination & Filtering
async function fetchProducts(page = 1) {
  currentPage = page;
  try {
    const params = new URLSearchParams();
    if (activeCategory && activeCategory !== 'All') params.append('category', activeCategory);
    if (currentSearch) params.append('search', currentSearch);
    if (currentSort !== 'default') params.append('sort', currentSort);
    params.append('page', currentPage);
    params.append('limit', pageLimit);

    const res = await fetch(`/api/products?${params.toString()}`);
    const data = await res.json();
    allProducts = data.products || [];
    totalPages = data.total_pages || 1;
    totalCount = data.total || 0;

    renderProductGrid(allProducts);
    renderPagination();
    updateCategoryCounts(data.category_counts);
    
    document.getElementById('catalog-count-label').textContent = 
      `Showing ${allProducts.length} of ${totalCount.toLocaleString()} products available for dynamic price analysis`;
  } catch (err) {
    console.error('Error fetching products:', err);
    document.getElementById('products-grid').innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--danger);">
        <i class="fa-solid fa-triangle-exclamation fa-2x"></i>
        <p style="margin-top: 10px;">Failed to load catalog. Ensure backend server is running.</p>
      </div>
    `;
  }
}

// Update Category Count Badges
function updateCategoryCounts(counts) {
  if (!counts) return;
  if (document.getElementById('count-all')) document.getElementById('count-all').textContent = counts.All ? counts.All.toLocaleString() : '1,225';
  if (document.getElementById('count-electronics')) document.getElementById('count-electronics').textContent = counts.Electronics || '300';
  if (document.getElementById('count-books')) document.getElementById('count-books').textContent = counts.Books || '308';
  if (document.getElementById('count-clothing')) document.getElementById('count-clothing').textContent = counts.Clothing || '301';
  if (document.getElementById('count-home')) document.getElementById('count-home').textContent = counts['Home & Kitchen'] || '316';
  if (document.getElementById('stat-products')) document.getElementById('stat-products').textContent = (counts.All || 1225).toLocaleString();
}

// Active Product Variant Selections: { [productId]: { color: '...', image: '...', size: '...' } }
let selectedProductVariants = {};

function selectProductColor(productId, colorName, imageUrl, btnEl, event) {
  if (event) event.stopPropagation();
  if (!selectedProductVariants[productId]) selectedProductVariants[productId] = {};
  selectedProductVariants[productId].color = colorName;
  if (imageUrl) {
    selectedProductVariants[productId].image = imageUrl;
  }

  // Update card color buttons
  const container = document.getElementById(`colors-${productId}`);
  if (container) {
    container.querySelectorAll('.color-swatch-btn').forEach(b => b.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');
  }
  const label = document.getElementById(`color-name-${productId}`);
  if (label) label.textContent = colorName;

  // Dynamically change product image on the card
  const cardImg = document.querySelector(`#card-${productId} .product-image`);
  if (cardImg && imageUrl) {
    cardImg.style.transition = 'opacity 0.15s ease';
    cardImg.style.opacity = '0.3';
    setTimeout(() => {
      cardImg.src = imageUrl;
      cardImg.style.opacity = '1';
    }, 120);
  }

  // Dynamically update modal if currently viewing this product
  const modalImg = document.getElementById('modal-product-img');
  if (modalImg && selectedProduct && selectedProduct.id === productId && imageUrl) {
    modalImg.style.transition = 'opacity 0.15s ease';
    modalImg.style.opacity = '0.3';
    setTimeout(() => {
      modalImg.src = imageUrl;
      modalImg.style.opacity = '1';
    }, 120);
  }
  const modalColorVal = document.getElementById('modal-color-selected-val');
  if (modalColorVal) modalColorVal.textContent = colorName;
  const modalContainer = document.getElementById(`modal-colors-${productId}`);
  if (modalContainer) {
    modalContainer.querySelectorAll('.color-swatch-btn').forEach(b => b.classList.remove('active'));
    if (btnEl && btnEl.parentElement === modalContainer) btnEl.classList.add('active');
  }
}

function selectProductSize(productId, sizeName, btnEl, event) {
  if (event) event.stopPropagation();
  if (!selectedProductVariants[productId]) selectedProductVariants[productId] = {};
  selectedProductVariants[productId].size = sizeName;

  const container = document.getElementById(`sizes-${productId}`);
  if (container) {
    container.querySelectorAll('.size-pill-btn').forEach(b => b.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');
  }
  const label = document.getElementById(`size-name-${productId}`);
  if (label) label.textContent = sizeName;
}

// Render Product Cards with Realistic Badges, Low Stock Alerts, Color/Size Swatches & Bank Offers
function renderProductGrid(products) {
  const grid = document.getElementById('products-grid');
  if (!products.length) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px; color: var(--text-muted);">
        <i class="fa-solid fa-box-open fa-3x" style="color: var(--border-hover); margin-bottom: 12px;"></i>
        <h3>No matching products found</h3>
        <p>Try searching with another keyword or resetting the category filter.</p>
      </div>
    `;
    return;
  }

  grid.innerHTML = products.map(product => {
    const originalPrice = product.original_base_price || product.price;
    const isDynamic = product.is_dynamically_priced;
    const diffPct = product.price_change_pct || 0;
    const hasDiscount = product.discount > 0;
    const listPrice = (product.price + (hasDiscount ? product.discount : 0)).toFixed(2);
    
    // Realistic badge handling
    const badgeHtml = product.badge ? `
      <span class="card-badge-top ${product.badge_class || 'badge-staff'}">${product.badge}</span>
    ` : '';

    // Stock Quantity & Urgency Indicator
    const stock = product.stock_quantity;
    let stockHtml = '';
    if (stock !== undefined && stock !== null) {
      if (stock <= 4) {
        stockHtml = `
          <div class="product-stock-alert stock-critical">
            <span class="stock-pulse-dot"></span>
            <i class="fa-solid fa-fire-flame-curved"></i>
            <span>Only <strong>${stock} left</strong> in stock - order soon</span>
          </div>
        `;
      } else if (stock <= 9) {
        stockHtml = `
          <div class="product-stock-alert stock-warning">
            <i class="fa-solid fa-triangle-exclamation"></i>
            <span>Limited stock: <strong>${stock} left</strong></span>
          </div>
        `;
      }
    }

    // Varied Bank Credit Card Offers (HDFC, Chase, ICICI, Amex, Axis, Citi, Capital One)
    let cardOfferHtml = '';
    const offer = product.card_offer;
    if (offer) {
      const discPct = offer.discount_pct || 10;
      const discountAmount = Math.min(product.price * (discPct / 100), offer.max_discount || 999);
      const cardFinalPrice = (product.price - discountAmount).toFixed(2);
      const bankSlug = (offer.bank || 'bank').toLowerCase().replace(/[^a-z0-9]/g, '');

      cardOfferHtml = `
        <div class="card-bank-offer bank-theme-${bankSlug}" title="${offer.label || ''} (${offer.card || ''})">
          <div class="bank-badge-tag">
            <i class="fa-solid fa-credit-card"></i>
            <span>${offer.bank}</span>
          </div>
          <div class="bank-offer-desc">
            <span class="offer-highlight">${discPct}% Instant Off</span>
            <span class="offer-price">Pay <strong>$${cardFinalPrice}</strong></span>
          </div>
        </div>
      `;
    }

    // Always use the product's default image — no colour picker on any card
    const currentCardImage = product.image;


    // Size Selector Variant Selector (for Clothing)
    let sizesHtml = '';
    if (product.sizes && product.sizes.length) {
      const currentSelectedSize = (selectedProductVariants[product.id] && selectedProductVariants[product.id].size) || product.sizes[0];
      sizesHtml = `
        <div class="product-variant-section">
          <div class="variant-header">
            <span class="variant-label">Select Size:</span>
            <span class="variant-current" id="size-name-${product.id}">${currentSelectedSize}</span>
          </div>
          <div class="size-pills-grid" id="sizes-${product.id}">
            ${product.sizes.map(s => `
              <button type="button" class="size-pill-btn ${s === currentSelectedSize ? 'active' : ''}" 
                onclick="selectProductSize('${product.id}', '${s.replace(/'/g, "\\'")}', this, event)">
                ${s}
              </button>
            `).join('')}
          </div>
        </div>
      `;
    }

    return `
      <article class="product-card" id="card-${product.id}">
        <div class="product-image-container">
          <img src="${currentCardImage}" alt="${product.name}" class="product-image" loading="lazy" onerror="this.src='https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=800'">
          ${badgeHtml}
          ${hasDiscount ? `<span class="card-discount-badge">-$${product.discount.toFixed(0)} OFF</span>` : ''}
          ${isDynamic ? `
            <span class="card-dynamic-tag" title="Dynamic AI Price Applied">
              <i class="fa-solid fa-bolt"></i> AI ${diffPct > 0 ? '+' : ''}${diffPct}%
            </span>
          ` : ''}
        </div>

        <div class="product-body">
          <div class="product-category-row">
            <span class="product-category">${product.category}</span>
            ${renderStarRating(product.review_score || 3.5, product.reviews_count || 120)}
          </div>

          <h3 class="product-title" title="${product.name}">${product.name}</h3>
          <p class="product-desc">${product.description}</p>

          ${sizesHtml}
          ${cardOfferHtml}

          <div class="product-pricing-row">
            <span class="current-price">$${product.price.toFixed(2)}</span>
            ${hasDiscount ? `<span class="original-price">$${listPrice}</span>` : ''}
            ${isDynamic ? `<span class="save-amount" style="background: #e0e7ff; color: var(--primary);">Dynamic Price</span>` : ''}
          </div>

          ${stockHtml}

          <div class="product-actions">
            <button class="btn-analyze-price" onclick="openPricingModal('${product.id}')">
              <i class="fa-solid fa-wand-magic-sparkles"></i>
              <span>Analyze Price</span>
            </button>
            <button class="btn-add-cart" onclick="addToCart('${product.id}')" title="Add to Cart">
              <i class="fa-solid fa-cart-plus"></i>
            </button>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

// Render Pagination Controls
function renderPagination() {
  const container = document.getElementById('pagination-controls');
  if (totalPages <= 1) {
    container.innerHTML = '';
    return;
  }

  let html = `
    <button class="btn-page" ${currentPage === 1 ? 'disabled' : ''} onclick="fetchProducts(${currentPage - 1})">
      <i class="fa-solid fa-chevron-left"></i> Previous
    </button>
  `;

  let startPage = Math.max(1, currentPage - 2);
  let endPage = Math.min(totalPages, currentPage + 2);

  if (startPage > 1) {
    html += `<button class="btn-page" onclick="fetchProducts(1)">1</button>`;
    if (startPage > 2) html += `<span style="padding: 0 4px; color: var(--text-light);">...</span>`;
  }

  for (let i = startPage; i <= endPage; i++) {
    html += `
      <button class="btn-page ${i === currentPage ? 'active' : ''}" onclick="fetchProducts(${i})">
        ${i}
      </button>
    `;
  }

  if (endPage < totalPages) {
    if (endPage < totalPages - 1) html += `<span style="padding: 0 4px; color: var(--text-light);">...</span>`;
    html += `<button class="btn-page" onclick="fetchProducts(${totalPages})">${totalPages}</button>`;
  }

  html += `
    <button class="btn-page" ${currentPage === totalPages ? 'disabled' : ''} onclick="fetchProducts(${currentPage + 1})">
      Next <i class="fa-solid fa-chevron-right"></i>
    </button>
  `;

  container.innerHTML = html;
}

// Search & Filter Handlers
let searchTimeout = null;
function handleSearch(val) {
  currentSearch = val;
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    fetchProducts(1);
  }, 250);
}

function filterByCategory(cat, btn) {
  activeCategory = cat;
  if (btn) {
    document.querySelectorAll('.category-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  document.getElementById('catalog-heading').textContent = cat === 'All' ? 'Featured Products' : `${cat} Catalog`;
  fetchProducts(1);
}

function handleSort(val) {
  currentSort = val;
  fetchProducts(1);
}

// Open Dynamic Pricing Modal for a Product
async function openPricingModal(productId) {
  selectedProduct = allProducts.find(p => p.id === productId);
  if (!selectedProduct) {
    try {
      const res = await fetch(`/api/product/${productId}`);
      selectedProduct = await res.json();
    } catch (e) {
      console.error(e);
      return;
    }
  }
  if (!selectedProduct) return;

  // Determine active variant image & color
  let activeVariantImg = selectedProduct.image;
  let activeColor = null;
  if (selectedProduct.colors && selectedProduct.colors.length) {
    const selected = selectedProductVariants[selectedProduct.id];
    activeColor = (selected && selected.color) || selectedProduct.colors[0].name;
    const matched = selectedProduct.colors.find(c => c.name === activeColor) || selectedProduct.colors[0];
    if (matched && matched.image) {
      activeVariantImg = matched.image;
    }
  }

  // Set initial product info
  document.getElementById('modal-product-img').src = activeVariantImg;
  document.getElementById('modal-product-name').textContent = selectedProduct.name;
  document.getElementById('modal-product-category').textContent = selectedProduct.category.toUpperCase();
  document.getElementById('modal-base-price').textContent = `$${selectedProduct.price.toFixed(2)}`;
  document.getElementById('modal-base-discount').textContent = `$${selectedProduct.discount.toFixed(2)}`;
  
  const score = selectedProduct.review_score || 3.5;
  const reviewsCount = selectedProduct.reviews_count || 120;
  document.getElementById('modal-rating-stars').innerHTML = `
    <i class="fa-solid fa-star" style="color: ${score >= 4 ? '#d97706' : (score >= 3 ? '#ca8a04' : '#ef4444')}"></i> ${score.toFixed(1)} (${reviewsCount} reviews)
  `;

  // Set stock badge in modal
  const stock = selectedProduct.stock_quantity;
  const stockEl = document.getElementById('modal-stock-badge');
  if (stockEl) {
    if (stock !== undefined && stock !== null) {
      if (stock <= 4) {
        stockEl.className = 'stock-badge stock-critical';
        stockEl.innerHTML = `<span class="stock-pulse-dot"></span><i class="fa-solid fa-fire-flame-curved"></i> Only ${stock} left in stock`;
        stockEl.style.display = 'inline-flex';
      } else if (stock <= 9) {
        stockEl.className = 'stock-badge stock-warning';
        stockEl.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Limited Stock (${stock} left)`;
        stockEl.style.display = 'inline-flex';
      } else {
        stockEl.className = 'stock-badge stock-normal';
        stockEl.innerHTML = `<i class="fa-solid fa-boxes-stacked"></i> In Stock (${stock} units)`;
        stockEl.style.display = 'inline-flex';
      }
    } else {
      stockEl.style.display = 'none';
    }
  }

  // Set credit card / bank offer badge in modal
  const ccEl = document.getElementById('modal-cc-badge');
  if (ccEl) {
    const offer = selectedProduct.card_offer;
    if (offer) {
      const discPct = offer.discount_pct || 10;
      const discountAmount = Math.min(selectedProduct.price * (discPct / 100), offer.max_discount || 999);
      const ccPrice = (selectedProduct.price - discountAmount).toFixed(2);
      const bankSlug = (offer.bank || 'bank').toLowerCase().replace(/[^a-z0-9]/g, '');
      ccEl.className = `cc-modal-badge card-bank-offer bank-theme-${bankSlug}`;
      ccEl.innerHTML = `<i class="fa-solid fa-credit-card"></i> <span><strong>${offer.bank}</strong>: ${discPct}% Instant Off &bull; Pay <strong>$${ccPrice}</strong></span>`;
      ccEl.style.display = 'inline-flex';
    } else {
      ccEl.style.display = 'none';
    }
  }

  // Set color/size variants in modal
  const variantsRow = document.getElementById('modal-variants-row');
  if (variantsRow) {
    let vHtml = '';
    if (selectedProduct.colors && selectedProduct.colors.length) {
      vHtml += `
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.78rem; flex-wrap: wrap;">
          <span style="color: var(--text-muted); font-weight: 600;">Colors:</span>
          <div style="display: flex; gap: 6px;" id="modal-colors-${selectedProduct.id}">
            ${selectedProduct.colors.map(c => `
              <button type="button" class="color-swatch-btn ${c.name === activeColor ? 'active' : ''}" 
                data-color="${c.name}"
                style="width: 20px; height: 20px; border-radius: 50%; background-color: ${c.hex}; cursor: pointer; border: 2px solid ${c.name === activeColor ? 'var(--primary)' : '#cbd5e1'};" 
                title="${c.name}"
                onclick="selectProductColor('${selectedProduct.id}', '${c.name.replace(/'/g, "\\'")}', '${(c.image || '').replace(/'/g, "\\'")}', this, event)">
              </button>
            `).join('')}
          </div>
          <span style="font-weight: 700; color: var(--dark);" id="modal-color-selected-val">${activeColor}</span>
        </div>
      `;
    }
    if (selectedProduct.sizes && selectedProduct.sizes.length) {
      const activeSize = (selectedProductVariants[selectedProduct.id] && selectedProductVariants[selectedProduct.id].size) || selectedProduct.sizes[0];
      vHtml += `
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.78rem; margin-top: 6px; flex-wrap: wrap;">
          <span style="color: var(--text-muted); font-weight: 600;">Sizes:</span>
          <div style="display: flex; gap: 4px;" id="modal-sizes-${selectedProduct.id}">
            ${selectedProduct.sizes.map(s => `
              <button type="button" class="size-pill-btn ${s === activeSize ? 'active' : ''}" 
                style="font-size: 0.72rem; padding: 2px 8px; border-radius: 4px; border: 1px solid ${s === activeSize ? 'var(--primary)' : 'var(--border-light)'}; background: ${s === activeSize ? 'var(--primary-light)' : '#ffffff'}; color: ${s === activeSize ? 'var(--primary)' : 'inherit'}; font-weight: 700; cursor: pointer;"
                onclick="selectProductSize('${selectedProduct.id}', '${s.replace(/'/g, "\\'")}', this, event)">
                ${s}
              </button>
            `).join('')}
          </div>
        </div>
      `;
    }

    if (vHtml) {
      variantsRow.innerHTML = vHtml;
      variantsRow.style.display = 'block';
    } else {
      variantsRow.style.display = 'none';
    }
  }
  
  // Set slider rating default to match product rating (1 to 5)
  document.getElementById('sim-rating').value = selectedProduct.rating || 3;
  document.getElementById('val-rating').textContent = `${selectedProduct.rating || 3}.0 ★`;

  // Open backdrop
  document.getElementById('pricing-modal-backdrop').classList.add('active');
  document.body.style.overflow = 'hidden';

  // Trigger calculation
  await recalculateDynamicPrice();
}

function closePricingModal() {
  document.getElementById('pricing-modal-backdrop').classList.remove('active');
  document.body.style.overflow = '';
}

// Recalculate Dynamic Price via ML API
async function recalculateDynamicPrice() {
  if (!selectedProduct) return;

  const modelName = document.getElementById('ml-model-select').value;
  const customerAge = parseInt(document.getElementById('sim-age').value, 10);
  const reviewRating = parseInt(document.getElementById('sim-rating').value, 10);
  const customerGender = document.getElementById('sim-gender').value;
  const paymentMethod = document.getElementById('sim-payment').value;
  const shippingType = document.getElementById('sim-shipping').value;
  const priceRange = parseFloat(document.getElementById('sim-range').value);

  // Update badge info
  updateModelInfoBadge(modelName);

  try {
    const payload = {
      product_id: selectedProduct.id,
      price: selectedProduct.price,
      discount: selectedProduct.discount,
      category: selectedProduct.category,
      model_name: modelName,
      customer_age: customerAge,
      review_rating: reviewRating,
      customer_gender: customerGender,
      payment_method: paymentMethod,
      shipping_type: shippingType,
      price_range_pct: priceRange,
      num_points: 15
    };

    const res = await fetch('/api/predict_price', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    currentPricingData = data;
    renderPricingResults(data);
  } catch (err) {
    console.error('Dynamic pricing error:', err);
    showToast('Failed to run ML inference', 'error');
  }
}

function updateModelInfoBadge(modelName) {
  const nameEl = document.getElementById('model-badge-name');
  const descEl = document.getElementById('model-badge-desc');
  
  if (modelName === 'Random Forest') {
    nameEl.textContent = 'Random Forest Classifier (Ensemble)';
    descEl.textContent = 'Ensemble of 120 trees capturing price elasticity, customer age, and rating non-linearities.';
  } else if (modelName === 'Logistic Regression') {
    nameEl.textContent = 'Logistic Regression (Probabilistic Logits)';
    descEl.textContent = 'Continuous monotonic logistic function modeling consumer price sensitivity curves.';
  } else if (modelName === 'Decision Tree') {
    nameEl.textContent = 'Decision Tree Classifier (Rule Partitioning)';
    descEl.textContent = 'Hierarchical tree rules partitioning conversion based on price brackets and rating thresholds.';
  }
}

// Render Results in Modal
function renderPricingResults(data) {
  document.getElementById('rec-current-price').textContent = `$${data.current_price.toFixed(2)}`;
  document.getElementById('rec-current-prob').textContent = `${(data.current_probability * 100).toFixed(1)}%`;
  document.getElementById('rec-current-rev').textContent = `$${data.current_expected_revenue.toFixed(2)}`;

  document.getElementById('rec-optimal-price').textContent = `$${data.recommended_price.toFixed(2)}`;
  document.getElementById('rec-optimal-prob').textContent = `${(data.recommended_probability * 100).toFixed(1)}%`;
  document.getElementById('rec-optimal-rev').textContent = `$${data.recommended_expected_revenue.toFixed(2)}`;

  document.getElementById('rec-strategy').textContent = data.strategy;
  const upliftBadge = document.getElementById('rec-uplift-badge');
  const isPositive = data.revenue_uplift_pct >= 0;
  upliftBadge.textContent = `${isPositive ? '+' : ''}${data.revenue_uplift_pct}% Revenue Lift (+$${data.revenue_diff.toFixed(2)})`;
  upliftBadge.className = isPositive ? 'badge-tag badge-green' : 'badge-tag badge-blue';

  document.getElementById('rec-rationale-text').textContent = data.reasoning;

  renderTestedPricesTable(data.curve);
  renderPricingChart(data.curve);
}

// Render Tested Price Points Table
function renderTestedPricesTable(curve) {
  const tbody = document.getElementById('tested-prices-tbody');
  tbody.innerHTML = curve.map(pt => {
    let rowClass = '';
    let tag = `<span style="color: var(--text-light);">-</span>`;
    
    if (pt.is_optimal) {
      rowClass = 'row-optimal';
      tag = `<span class="table-tag tag-opt"><i class="fa-solid fa-crown"></i> OPTIMAL PEAK</span>`;
    } else if (pt.is_current) {
      rowClass = 'row-current';
      tag = `<span class="table-tag tag-curr">CURRENT BASELINE</span>`;
    }

    return `
      <tr class="${rowClass}">
        <td><strong>$${pt.price.toFixed(2)}</strong></td>
        <td>$${pt.discount.toFixed(2)}</td>
        <td>$${pt.effective_price.toFixed(2)}</td>
        <td>
          <div style="display: flex; align-items: center; gap: 6px;">
            <span>${pt.probability_pct}%</span>
            <div style="width: 40px; height: 5px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
              <div style="width: ${pt.probability_pct}%; height: 100%; background: ${pt.is_optimal ? '#10b981' : 'var(--primary)'};"></div>
            </div>
          </div>
        </td>
        <td><strong>$${pt.expected_revenue.toFixed(2)}</strong></td>
        <td>${tag}</td>
      </tr>
    `;
  }).join('');
}

// Render Interactive Chart.js
function renderPricingChart(curve) {
  const ctx = document.getElementById('pricingChart');
  if (!ctx) return;

  const labels = curve.map(pt => `$${pt.price.toFixed(0)}`);
  const revenueData = curve.map(pt => pt.expected_revenue);
  const probData = curve.map(pt => pt.probability_pct);

  const pointColors = curve.map(pt => {
    if (pt.is_optimal) return '#10b981';
    if (pt.is_current) return '#f59e0b';
    return '#4f46e5';
  });

  const pointRadius = curve.map(pt => (pt.is_optimal || pt.is_current) ? 8 : 4);

  if (pricingChartInstance) {
    pricingChartInstance.destroy();
  }

  const isRevenue = activeChartMode === 'revenue';
  const title = isRevenue ? 'Expected Revenue ($)' : 'Purchase Probability (%)';

  pricingChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: title,
        data: isRevenue ? revenueData : probData,
        borderColor: isRevenue ? '#4f46e5' : '#0ea5e9',
        backgroundColor: isRevenue ? 'rgba(79, 70, 229, 0.08)' : 'rgba(14, 165, 233, 0.08)',
        fill: true,
        tension: 0.35,
        pointBackgroundColor: pointColors,
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: pointRadius,
        pointHoverRadius: 10
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            title: (items) => `Tested Price: ${items[0].label}`,
            label: (item) => {
              const pt = curve[item.dataIndex];
              const optTag = pt.is_optimal ? ' [AI Optimal Peak]' : '';
              const currTag = pt.is_current ? ' [Current Baseline]' : '';
              if (isRevenue) {
                return `Expected Rev: $${pt.expected_revenue.toFixed(2)} (Prob: ${pt.probability_pct}%)${optTag}${currTag}`;
              } else {
                return `Purchase Probability: ${pt.probability_pct}% (Exp. Rev: $${pt.expected_revenue.toFixed(2)})${optTag}${currTag}`;
              }
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          title: { display: true, text: 'Tested Product Price ($)', font: { size: 11, weight: 'bold' } }
        },
        y: {
          grid: { color: '#f1f5f9' },
          title: { display: true, text: title, font: { size: 11, weight: 'bold' } },
          ticks: {
            callback: (val) => isRevenue ? `$${val}` : `${val}%`
          }
        }
      }
    }
  });
}

function switchChartMode(mode) {
  activeChartMode = mode;
  document.getElementById('tab-revenue').classList.toggle('active', mode === 'revenue');
  document.getElementById('tab-probability').classList.toggle('active', mode === 'probability');
  document.getElementById('chart-main-title').textContent = 
    mode === 'revenue' ? 'Expected Revenue Curve ($ vs Price)' : 'Demand Elasticity Curve (% Probability vs Price)';
  
  if (currentPricingData) {
    renderPricingChart(currentPricingData.curve);
  }
}

// Apply Dynamic Price to Storefront
async function applyDynamicPriceToStore() {
  if (!currentPricingData || !selectedProduct) return;

  try {
    const res = await fetch('/api/apply_price', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        product_id: selectedProduct.id,
        price: currentPricingData.recommended_price
      })
    });

    const data = await res.json();
    if (data.status === 'success') {
      showToast(`Applied dynamic price $${currentPricingData.recommended_price.toFixed(2)} to ${selectedProduct.name}!`);
      closePricingModal();
      fetchProducts(currentPage);
    }
  } catch (err) {
    console.error('Error applying dynamic price:', err);
    showToast('Failed to apply dynamic price', 'error');
  }
}

// Reset Store Prices
async function resetAllStorePrices() {
  try {
    const res = await fetch('/api/reset_prices', { method: 'POST' });
    const data = await res.json();
    showToast(data.message);
    fetchProducts(currentPage);
  } catch (err) {
    console.error('Error resetting prices:', err);
  }
}

// Fetch ML Model Stats & Benchmarks
async function fetchModelStats() {
  try {
    const res = await fetch('/api/models');
    const data = await res.json();
    
    if (data.dataset_summary) {
      document.getElementById('stat-records').textContent = data.dataset_summary.total_records.toLocaleString();
    }
    
    const tbody = document.getElementById('metrics-tbody');
    if (tbody && data.metrics) {
      tbody.innerHTML = Object.entries(data.metrics).map(([model, m]) => {
        const isBest = model === 'Random Forest';
        return `
          <tr style="${isBest ? 'background: #f8fafc; font-weight: 600;' : ''}">
            <td>
              <strong>${model}</strong>
              ${isBest ? '<span class="badge-tag badge-green" style="margin-left: 6px;">Top Accuracy</span>' : ''}
            </td>
            <td>${(m.accuracy * 100).toFixed(1)}%</td>
            <td>${(m.precision * 100).toFixed(1)}%</td>
            <td>${(m.recall * 100).toFixed(1)}%</td>
            <td>${m.f1.toFixed(3)}</td>
            <td><strong style="color: var(--primary);">${m.roc_auc.toFixed(3)}</strong></td>
          </tr>
        `;
      }).join('');
    }
  } catch (err) {
    console.error('Error fetching model stats:', err);
  }
}

function openModelMetricsModal() {
  fetchModelStats();
  document.getElementById('metrics-modal-backdrop').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeModelMetricsModal() {
  document.getElementById('metrics-modal-backdrop').classList.remove('active');
  document.body.style.overflow = '';
}

// Store-Wide Batch Optimizer
async function openBatchOptimizerModal() {
  document.getElementById('batch-modal-backdrop').classList.add('active');
  document.body.style.overflow = 'hidden';

  const tbody = document.getElementById('batch-tbody');
  tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 30px;"><i class="fa-solid fa-spinner fa-spin"></i> Running batch ML dynamic optimization...</td></tr>`;

  try {
    const res = await fetch('/api/batch_optimize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model_name: 'Random Forest' })
    });

    const data = await res.json();
    batchOptimizationData = data;

    document.getElementById('batch-baseline-rev').textContent = `$${data.total_current_revenue.toFixed(2)}`;
    document.getElementById('batch-optimal-rev').textContent = `$${data.total_optimal_revenue.toFixed(2)}`;
    document.getElementById('batch-lift-pct').textContent = `+${data.store_lift_pct}% (+$${data.total_revenue_gain.toFixed(2)})`;

    tbody.innerHTML = data.optimizations.map(item => `
      <tr>
        <td><strong>${item.name}</strong></td>
        <td><span class="product-category">${item.category}</span></td>
        <td>$${item.current_price.toFixed(2)}</td>
        <td><strong style="color: #059669;">$${item.recommended_price.toFixed(2)}</strong></td>
        <td>${(item.current_prob*100).toFixed(0)}% &rarr; ${(item.recommended_prob*100).toFixed(0)}%</td>
        <td><span class="badge-tag badge-green">+${item.lift_pct}%</span></td>
        <td><span style="font-size: 0.78rem; font-weight: 600;">${item.strategy}</span></td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Batch optimizer error:', err);
    tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--danger);">Failed to run batch optimization.</td></tr>`;
  }
}

function closeBatchOptimizerModal() {
  document.getElementById('batch-modal-backdrop').classList.remove('active');
  document.body.style.overflow = '';
}

async function applyAllBatchPrices() {
  if (!batchOptimizationData || !batchOptimizationData.optimizations) return;

  let appliedCount = 0;
  for (const item of batchOptimizationData.optimizations) {
    await fetch('/api/apply_price', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: item.id, price: item.recommended_price })
    });
    appliedCount++;
  }

  showToast(`Successfully applied AI optimized prices to all ${appliedCount} catalog products!`);
  closeBatchOptimizerModal();
  fetchProducts(currentPage);
}

// Shopping Cart Logic with Variant Support
function addToCart(productId) {
  const prod = allProducts.find(p => p.id === productId);
  if (!prod) return;

  const userVariant = selectedProductVariants[productId] || {};
  let chosenColor = userVariant.color;
  let chosenImg = userVariant.image;
  if (!chosenColor && prod.colors && prod.colors.length) {
    chosenColor = prod.colors[0].name;
    chosenImg = prod.colors[0].image || prod.image;
  }
  if (!chosenImg) chosenImg = prod.image;
  const chosenSize = userVariant.size || (prod.sizes && prod.sizes[0] ? prod.sizes[0] : null);

  const cartKey = `${productId}__${chosenColor || 'def'}__${chosenSize || 'def'}`;
  const existing = cart.find(item => item.cartKey === cartKey);
  
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({
      ...prod,
      image: chosenImg,
      cartKey: cartKey,
      selectedColor: chosenColor,
      selectedSize: chosenSize,
      qty: 1
    });
  }

  updateCartUI();

  let variantDetails = [];
  if (chosenColor) variantDetails.push(`Color: ${chosenColor}`);
  if (chosenSize) variantDetails.push(`Size: ${chosenSize}`);
  const variantSuffix = variantDetails.length ? ` (${variantDetails.join(', ')})` : '';

  showToast(`Added "${prod.name}"${variantSuffix} to cart!`);
}

function removeFromCart(cartKeyOrId) {
  cart = cart.filter(item => item.cartKey !== cartKeyOrId && item.id !== cartKeyOrId);
  updateCartUI();
}

function updateCartUI() {
  const counter = document.getElementById('cart-counter');
  const countLabel = document.getElementById('cart-items-count');
  const list = document.getElementById('cart-items-list');
  const subtotalEl = document.getElementById('cart-subtotal');
  const savingsEl = document.getElementById('cart-savings');

  const totalQty = cart.reduce((acc, item) => acc + item.qty, 0);
  counter.textContent = totalQty;
  countLabel.textContent = `${totalQty} item${totalQty === 1 ? '' : 's'}`;

  if (!cart.length) {
    list.innerHTML = `
      <div style="text-align: center; padding: 40px 20px; color: var(--text-muted);">
        <i class="fa-solid fa-cart-shopping fa-3x" style="color: var(--border-hover); margin-bottom: 12px;"></i>
        <p>Your shopping cart is empty.</p>
      </div>
    `;
    subtotalEl.textContent = '$0.00';
    savingsEl.textContent = '$0.00';
    return;
  }

  let subtotal = 0;
  let totalSavings = 0;

  list.innerHTML = cart.map(item => {
    const itemTotal = item.price * item.qty;
    subtotal += itemTotal;
    const orig = item.original_base_price || item.price;
    if (orig > item.price) {
      totalSavings += (orig - item.price) * item.qty;
    }

    let variantTags = '';
    if (item.selectedColor || item.selectedSize) {
      variantTags = `
        <div style="display: flex; gap: 6px; align-items: center; margin-top: 3px; font-size: 0.73rem; color: var(--text-muted);">
          ${item.selectedColor ? `<span style="background: #f1f5f9; padding: 1px 6px; border-radius: 4px; font-weight: 600; color: var(--dark); border: 1px solid #e2e8f0;">🎨 ${item.selectedColor}</span>` : ''}
          ${item.selectedSize ? `<span style="background: #f1f5f9; padding: 1px 6px; border-radius: 4px; font-weight: 700; color: var(--primary); border: 1px solid #e2e8f0;">📏 ${item.selectedSize}</span>` : ''}
        </div>
      `;
    }

    return `
      <div style="display: flex; gap: 12px; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--border-light);">
        <img src="${item.image}" style="width: 52px; height: 52px; border-radius: 8px; object-fit: cover; flex-shrink: 0;">
        <div style="flex: 1; min-width: 0;">
          <div style="font-weight: 600; font-size: 0.85rem; color: var(--dark); line-height: 1.3; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${item.name}</div>
          ${variantTags}
          <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 3px;">
            $${item.price.toFixed(2)} &times; ${item.qty}
            ${item.is_dynamically_priced ? '<span style="color: var(--primary); font-weight: 700; margin-left: 4px;">⚡ AI Price</span>' : ''}
          </div>
        </div>
        <div style="text-align: right; flex-shrink: 0;">
          <div style="font-weight: 700; font-size: 0.9rem;">$${itemTotal.toFixed(2)}</div>
          <button onclick="removeFromCart('${item.cartKey || item.id}')" style="background: none; border: none; color: var(--danger); font-size: 0.75rem; cursor: pointer; margin-top: 4px; font-weight: 600;">Remove</button>
        </div>
      </div>
    `;
  }).join('');

  subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
  savingsEl.textContent = `$${totalSavings.toFixed(2)}`;
}

function toggleCartDrawer() {
  const drawer = document.getElementById('cart-drawer-backdrop');
  drawer.classList.toggle('active');
  document.body.style.overflow = drawer.classList.contains('active') ? 'hidden' : '';
}

function simulateCheckout() {
  if (!cart.length) {
    showToast('Your cart is empty', 'error');
    return;
  }
  showToast('Order placed successfully! Thank you for testing ApexMart AI demo.');
  cart = [];
  updateCartUI();
  toggleCartDrawer();
}

function handleBackdropClick(e) {
  if (e.target.classList.contains('modal-backdrop')) {
    e.target.classList.remove('active');
    document.body.style.overflow = '';
  }
}
