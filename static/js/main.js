// Main JavaScript functions for Warehouse Inventory System

// Global functions
function showLoading(element) {
    element.classList.add('loading');
    element.style.pointerEvents = 'none';
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.style.pointerEvents = 'auto';
}

// Search functionality
function performSearch(ssid) {
    if (!ssid.trim()) return;
    
    fetch(`/search?ssid=${encodeURIComponent(ssid)}`)
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('searchResult');
            if (data.error) {
                resultDiv.innerHTML = `<div class="alert alert-warning">${data.error}</div>`;
            } else {
                resultDiv.innerHTML = `
                    <div class="alert alert-success">
                        <strong>${data.ssid}</strong> - ${data.name}<br>
                        <small>Warehouse: ${data.warehouse} | Category: ${data.category}</small><br>
                        <small>Stock: ${data.current_stock} ${data.unit} ${data.is_low_stock ? '<span class="badge bg-danger">LOW STOCK</span>' : ''}</small>
                    </div>
                `;
            }
            resultDiv.style.display = 'block';
        })
        .catch(error => {
            const resultDiv = document.getElementById('searchResult');
            resultDiv.innerHTML = '<div class="alert alert-danger">Search failed. Please try again.</div>';
            resultDiv.style.display = 'block';
        });
}

// Form validation helpers
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Auto-hide alerts
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide success alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-success');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add form validation to all forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
    
    // Add loading states to buttons
    const submitButtons = document.querySelectorAll('button[type="submit"], .btn[href*="export"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            showLoading(this);
            setTimeout(() => hideLoading(this), 3000); // Auto-hide after 3 seconds
        });
    });
});

// Utility functions for reports
function exportData(url, params = {}) {
    const query = new URLSearchParams(params).toString();
    const fullUrl = query ? `${url}?${query}` : url;
    window.location.href = fullUrl;
}

// Date helpers
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getDateDaysAgo(days) {
    const date = new Date();
    date.setDate(date.getDate() - days);
    return date.toISOString().split('T')[0];
}

// Stock level helpers
function getStockStatus(currentStock, reorderLevel) {
    if (currentStock <= 0) return { class: 'danger', text: 'OUT OF STOCK' };
    if (currentStock <= reorderLevel) return { class: 'warning', text: 'LOW STOCK' };
    return { class: 'success', text: 'IN STOCK' };
}

// Transaction type helpers
function getTransactionBadgeClass(type) {
    switch (type.toLowerCase()) {
        case 'in': return 'success';
        case 'out': return 'danger';
        case 'adjustment': return 'warning';
        default: return 'secondary';
    }
}
