"""
// Lazy Loading inteligente con IntersectionObserver
class LazyImageLoader {
    constructor() {
        this.imageObserver = null;
        this.init();
    }
    
    init() {
        if ('IntersectionObserver' in window) {
            this.imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.loadImage(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                rootMargin: '50px 0px',  // Cargar 50px antes de que sea visible
                threshold: 0.01
            });
            
            this.observeImages();
        } else {
            // Fallback para navegadores antiguos
            this.loadAllImages();
        }
    }
    
    observeImages() {
        const lazyImages = document.querySelectorAll('img[data-lazy], source[data-lazy]');
        lazyImages.forEach(img => this.imageObserver.observe(img));
    }
    
    loadImage(element) {
        if (element.dataset.lazy) {
            element.src = element.dataset.lazy;
            element.srcset = element.dataset.lazy;
            element.classList.remove('lazy');
            element.classList.add('loaded');
            
            // Efecto fade-in suave
            element.style.opacity = '0';
            element.style.transition = 'opacity 0.3s ease';
            
            element.onload = () => {
                element.style.opacity = '1';
            };
        }
    }
    
    loadAllImages() {
        const lazyImages = document.querySelectorAll('img[data-lazy], source[data-lazy]');
        lazyImages.forEach(img => this.loadImage(img));
    }
}

// Detección de formato WebP
class WebPDetector {
    constructor() {
        this.isSupported = false;
        this.detect();
    }
    
    detect() {
        const webP = new Image();
        webP.onload = webP.onerror = () => {
            this.isSupported = (webP.height === 2);
            document.documentElement.classList.toggle('webp', this.isSupported);
            document.documentElement.classList.toggle('no-webp', !this.isSupported);
        };
        webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
    }
}

// Compresión de imágenes antes de subir (para admin)
class ImageCompressor {
    constructor(maxWidth = 1200, maxHeight = 900, quality = 0.85) {
        this.maxWidth = maxWidth;
        this.maxHeight = maxHeight;
        this.quality = quality;
    }
    
    compress(file) {
        return new Promise((resolve) => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();
            
            img.onload = () => {
                // Calcular nuevas dimensiones manteniendo aspecto
                const { width, height } = this.calculateDimensions(img.width, img.height);
                
                canvas.width = width;
                canvas.height = height;
                
                // Dibujar imagen redimensionada
                ctx.drawImage(img, 0, 0, width, height);
                
                // Convertir a blob
                canvas.toBlob(resolve, 'image/jpeg', this.quality);
            };
            
            img.src = URL.createObjectURL(file);
        });
    }
    
    calculateDimensions(width, height) {
        if (width <= this.maxWidth && height <= this.maxHeight) {
            return { width, height };
        }
        
        const ratio = Math.min(this.maxWidth / width, this.maxHeight / height);
        return {
            width: Math.round(width * ratio),
            height: Math.round(height * ratio)
        };
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    new LazyImageLoader();
    new WebPDetector();
    
    // Compresión automática en formularios de admin
    const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    const compressor = new ImageCompressor();
    
    fileInputs.forEach(input => {
        input.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                // Mostrar progreso
                const progress = document.createElement('div');
                progress.textContent = 'Optimizando imagen...';
                progress.className = 'image-progress';
                input.parentNode.appendChild(progress);
                
                try {
                    const compressedFile = await compressor.compress(file);
                    
                    // Crear nuevo input con archivo comprimido
                    const dt = new DataTransfer();
                    dt.items.add(new File([compressedFile], file.name, {
                        type: 'image/jpeg'
                    }));
                    input.files = dt.files;
                    
                    progress.textContent = `✅ Optimizado: ${(file.size / 1024 / 1024).toFixed(1)}MB → ${(compressedFile.size / 1024 / 1024).toFixed(1)}MB`;
                    progress.style.color = 'green';
                    
                    setTimeout(() => progress.remove(), 3000);
                } catch (error) {
                    progress.textContent = '❌ Error optimizando imagen';
                    progress.style.color = 'red';
                    setTimeout(() => progress.remove(), 3000);
                }
            }
        });
    });
});
"""