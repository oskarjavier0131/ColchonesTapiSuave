<script>
// Variables globales
// let searchTimeout;  // <- ELIMINAR ESTA LÍNEA
let comparisonList = JSON.parse(localStorage.getItem('comparisonList') || '[]');

// Inicialización cuando se carga el DOM
document.addEventListener('DOMContentLoaded', function() {
    // initializeSearch();  // <- ELIMINAR ESTA LÍNEA
    initializeComparison();
    initializeAnimations();
    initializeProductInteractions();
});

// =============================================================================
// SISTEMA DE BÚSQUEDA  // <- ELIMINAR TODO ESTE BLOQUE
// =============================================================================

/*
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        clearTimeout(searchTimeout);
        
        if (query.length >= 2) {
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        } else {
            hideSearchResults();
        }
    });
    
    // Cerrar resultados al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            hideSearchResults();
        }
    });
}

function performSearch(query) {
    fetch(`/busqueda-ajax/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data.results);
        })
        .catch(error => {
            console.error('Error en búsqueda:', error);
        });
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('searchResults');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="p-3 text-muted">No se encontraron productos</div>';
    } else {
        searchResults.innerHTML = results.map(product => `
            <a href="${product.url}" class="search-result-item">
                <img src="${product.image}" alt="${product.name}" class="search-result-image">
                <div class="search-result-info">
                    <div class="search-result-name">${product.name}</div>
                    <div class="search-result-price">${formatPrice(product.price)}</div>
                </div>
            </a>
        `).join('');
    }
    
    searchResults.style.display = 'block';
}

function hideSearchResults() {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.style.display = 'none';
    }
}
*/

// =============================================================================
// SISTEMA DE COMPARACIÓN
// =============================================================================

function initializeComparison() {
    updateComparisonWidget();
    
    // Agregar botones de comparación a productos
    document.querySelectorAll('.product-card').forEach(card => {
        addComparisonButton(card);
    });
}

function addComparisonButton(productCard) {
    const productId = productCard.dataset.productId;
    if (!productId) return;
    
    const button = document.createElement('button');
    button.className = 'btn btn-outline-primary btn-sm comparison-add-btn';
    button.innerHTML = '<i class="fas fa-plus me-1"></i>Comparar';
    button.onclick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        addToComparison(productId);
    };
    
    const productInfo = productCard.querySelector('.product-info');
    if (productInfo) {
        productInfo.appendChild(button);
    }
}

function addToComparison(productId) {
    if (comparisonList.includes(productId)) {
        showToast('El producto ya está en la comparación', 'warning');
        return;
    }
    
    if (comparisonList.length >= 3) {
        showToast('Máximo 3 productos para comparar', 'warning');
        return;
    }
    
    comparisonList.push(productId);
    localStorage.setItem('comparisonList', JSON.stringify(comparisonList));
    updateComparisonWidget();
    showToast('Producto agregado a la comparación', 'success');
}

function removeFromComparison(productId) {
    comparisonList = comparisonList.filter(id => id !== productId);
    localStorage.setItem('comparisonList', JSON.stringify(comparisonList));
    updateComparisonWidget();
    showToast('Producto removido de la comparación', 'info');
}

function clearComparison() {
    comparisonList = [];
    localStorage.removeItem('comparisonList');
    updateComparisonWidget();
    showToast('Comparación limpiada', 'info');
}

function updateComparisonWidget() {
    const widget = document.getElementById('comparisonWidget');
    const count = document.getElementById('comparisonCount');
    
    if (widget && count) {
        count.textContent = comparisonList.length;
        widget.style.display = comparisonList.length > 0 ? 'block' : 'none';
    }
}

function toggleComparison() {
    if (comparisonList.length === 0) {
        showToast('No hay productos para comparar', 'warning');
        return;
    }
    
    // Aquí cargarías los datos de los productos y mostrarías el modal
    showComparisonModal();
}

function showComparisonModal() {
    const modal = new bootstrap.Modal(document.getElementById('comparisonModal'));
    modal.show();
    
    // Aquí harías una petición AJAX para obtener los datos de los productos
    // y generarías la tabla de comparación
}

// =============================================================================
// ANIMACIONES Y EFECTOS
// =============================================================================

function initializeAnimations() {
    // Animación de números contadores
    animateCounters();
    
    // Lazy loading de imágenes
    initializeLazyLoading();
    
    // Efectos de hover para productos
    initializeHoverEffects();
}

function animateCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    
    counters.forEach(counter => {
        const target = parseInt(counter.dataset.counter);
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            counter.textContent = Math.floor(current).toLocaleString();
        }, 16);
    });
}

function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-lazy]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.lazy;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

function initializeHoverEffects() {
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// =============================================================================
// INTERACCIONES DE PRODUCTOS
// =============================================================================

function initializeProductInteractions() {
    // Favoritos
    initializeFavorites();
    
    // Compartir productos
    initializeSharing();
    
    // Galería de imágenes
    initializeImageGallery();
}

function initializeFavorites() {
    document.querySelectorAll('.favorite-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            toggleFavorite(this);
        });
    });
}

function toggleFavorite(button) {
    const isFavorite = button.classList.contains('favorited');
    
    if (isFavorite) {
        button.classList.remove('favorited');
        button.innerHTML = '<i class="far fa-heart me-2"></i>Favoritos';
        showToast('Removido de favoritos', 'info');
    } else {
        button.classList.add('favorited');
        button.innerHTML = '<i class="fas fa-heart me-2"></i>Favoritos';
        showToast('Agregado a favoritos', 'success');
    }
}

function initializeSharing() {
    document.querySelectorAll('.share-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            shareProduct(this);
        });
    });
}

function shareProduct(button) {
    if (navigator.share) {
        navigator.share({
            title: 'ColchonesTapiSuave',
            text: 'Mira este increíble colchón',
            url: window.location.href
        });
    } else {
        // Fallback: copiar URL al clipboard
        navigator.clipboard.writeText(window.location.href);
        showToast('URL copiada al portapapeles', 'success');
    }
}

function initializeImageGallery() {
    document.querySelectorAll('.thumbnail').forEach(thumb => {
        thumb.addEventListener('click', function() {
            changeMainImage(this);
        });
    });
}

function changeMainImage(thumbnail) {
    const mainImage = document.getElementById('mainImage');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    if (mainImage) {
        mainImage.src = thumbnail.src;
        
        thumbnails.forEach(thumb => thumb.classList.remove('active'));
        thumbnail.classList.add('active');
    }
}

// =============================================================================
// UTILIDADES
// =============================================================================

function showToast(message, type = 'info') {
    // Crear toast dinámicamente
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    // Agregar al container de toasts
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        toastContainer.style.zIndex = '1060';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.appendChild(toast);
    
    // Mostrar toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remover del DOM después de que se oculte
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function formatPrice(price) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(price);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// =============================================================================
// PERFORMANCE Y SEO
// =============================================================================

// Precarga de recursos críticos
function preloadCriticalResources() {
    const criticalImages = document.querySelectorAll('[data-preload]');
    criticalImages.forEach(img => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = img.dataset.preload;
        document.head.appendChild(link);
    });
}

// Lazy loading para iframes y videos
function initializeLazyMedia() {
    const media = document.querySelectorAll('iframe[data-lazy], video[data-lazy]');
    
    const mediaObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                element.src = element.dataset.lazy;
                mediaObserver.unobserve(element);
            }
        });
    });
    
    media.forEach(element => mediaObserver.observe(element));
}

// Inicializar todo cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    preloadCriticalResources();
    initializeLazyMedia();
});
</script>

<!-- =============================================================================
ESTILOS ADICIONALES PARA COMPONENTES
============================================================================= -->

<style>
/* Toast personalizado */
.toast {
    min-width: 300px;
}

/* Botones de favoritos */
.favorite-btn.favorited {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
    color: white;
}

/* Lazy loading placeholder */
img.lazy {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* Efectos de hover mejorados */
.product-card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

/* Animaciones de entrada */
.fade-in-up {
    animation: fadeInUp 0.6s ease forwards;
}

.fade-in-left {
    animation: fadeInLeft 0.6s ease forwards;
}

.fade-in-right {
    animation: fadeInRight 0.6s ease forwards;
}

@keyframes fadeInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Responsive improvements */
@media (max-width: 576px) {
    .whatsapp-widget {
        bottom: 15px;
        right: 15px;
    }
    
    .comparison-widget {
        bottom: 85px;
        right: 15px;
    }
    
    /* .search-container {  // <- ELIMINAR ESTAS LÍNEAS
        width: 100%;
    } */
}
</style>
