// Main JavaScript for Apple Disease Detector

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize file upload handling
    initializeFileUpload();
    
    // Initialize image lazy loading
    initializeLazyLoading();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize file upload functionality
 */
function initializeFileUpload() {
    const fileInput = document.getElementById('file');
    const uploadForm = document.getElementById('uploadForm');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const submitBtn = document.getElementById('submitBtn');
    
    if (!fileInput || !uploadForm) return;
    
    // File input change handler
    fileInput.addEventListener('change', function(e) {
        handleFileSelection(e.target.files[0]);
    });
    
    // Drag and drop functionality
    const dropZone = fileInput.parentElement;
    
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });
    
    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelection(files[0]);
        }
    });
    
    // Form submission handler
    uploadForm.addEventListener('submit', function(e) {
        if (!validateFileUpload()) {
            e.preventDefault();
            return false;
        }
        
        // Show loading state
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Analyzing Image...
            `;
        }
    });
}

/**
 * Handle file selection and preview
 */
function handleFileSelection(file) {
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    
    if (!file) {
        if (imagePreview) imagePreview.style.display = 'none';
        return;
    }
    
    // Validate file type
    const allowedTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showAlert('Invalid file type. Please select PNG, JPG, JPEG, or WEBP images only.', 'error');
        return;
    }
    
    // Validate file size (16MB max)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showAlert('File is too large. Maximum size is 16MB.', 'error');
        return;
    }
    
    // Show preview
    if (imagePreview && previewImg) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            imagePreview.style.display = 'block';
            
            // Add fade-in animation
            imagePreview.style.opacity = '0';
            setTimeout(() => {
                imagePreview.style.opacity = '1';
            }, 100);
        };
        reader.readAsDataURL(file);
    }
}

/**
 * Validate file upload before submission
 */
function validateFileUpload() {
    const fileInput = document.getElementById('file');
    
    if (!fileInput || !fileInput.files[0]) {
        showAlert('Please select an image file first.', 'error');
        return false;
    }
    
    const file = fileInput.files[0];
    const allowedTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/webp'];
    
    if (!allowedTypes.includes(file.type)) {
        showAlert('Invalid file type. Please select PNG, JPG, JPEG, or WEBP images only.', 'error');
        return false;
    }
    
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showAlert('File is too large. Maximum size is 16MB.', 'error');
        return false;
    }
    
    return true;
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i data-feather="${type === 'error' ? 'alert-circle' : type === 'success' ? 'check-circle' : 'info'}" class="me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at top of main content
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        feather.replace();
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

/**
 * Initialize lazy loading for images
 */
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            const target = document.querySelector(href);
            
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Utility function to format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Utility function to format timestamp
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    // Less than 1 minute
    if (diff < 60000) {
        return 'Just now';
    }
    
    // Less than 1 hour
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    }
    
    // Less than 1 day
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    }
    
    // Default format
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

/**
 * Initialize keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + U: Focus upload input
        if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
            e.preventDefault();
            const fileInput = document.getElementById('file');
            if (fileInput) {
                fileInput.focus();
                fileInput.click();
            }
        }
        
        // Escape: Close modals or clear selection
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
}

// Initialize keyboard shortcuts
initializeKeyboardShortcuts();

// Export functions for use in other scripts
window.AppleDiseaseDetector = {
    showAlert,
    formatFileSize,
    formatTimestamp,
    validateFileUpload,
    handleFileSelection
};
