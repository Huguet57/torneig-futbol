// Main JavaScript file for the Soccer Tournament Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any interactive elements
    initializeDropdowns();
    initializeFormValidation();
    initializeClickableRows();
    
    // Add event listeners for filter forms
    const filterForms = document.querySelectorAll('.filter-form');
    filterForms.forEach(form => {
        const selects = form.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', function() {
                form.submit();
            });
        });
    });
});

// Initialize dropdown menus
function initializeDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdownMenu = this.nextElementSibling;
            if (dropdownMenu.classList.contains('show')) {
                dropdownMenu.classList.remove('show');
            } else {
                // Close any open dropdowns first
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
                dropdownMenu.classList.add('show');
            }
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.matches('.dropdown-toggle')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
}

// Initialize form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Initialize clickable table rows
function initializeClickableRows() {
    const clickableRows = document.querySelectorAll('tr[data-href]');
    clickableRows.forEach(row => {
        row.addEventListener('click', function() {
            window.location.href = this.dataset.href;
        });
        
        // Add hover effect
        row.classList.add('clickable-row');
    });
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

// Format time for display
function formatTime(timeString) {
    if (!timeString) return '';
    const [hours, minutes] = timeString.split(':');
    return `${hours}:${minutes}`;
}

// Calculate statistics
function calculatePercentage(value, total) {
    if (total === 0) return '0%';
    return ((value / total) * 100).toFixed(1) + '%';
}

// Show confirmation dialog
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Handle form errors
function handleFormErrors(form, errors) {
    // Clear previous errors
    form.querySelectorAll('.is-invalid').forEach(field => {
        field.classList.remove('is-invalid');
    });
    form.querySelectorAll('.invalid-feedback').forEach(feedback => {
        feedback.remove();
    });
    
    // Add new error messages
    for (const [field, message] of Object.entries(errors)) {
        const inputField = form.querySelector(`[name="${field}"]`);
        if (inputField) {
            inputField.classList.add('is-invalid');
            const feedback = document.createElement('div');
            feedback.classList.add('invalid-feedback');
            feedback.textContent = message;
            inputField.parentNode.appendChild(feedback);
        }
    }
}

// Create a custom 404 page
function show404Page(container) {
    container.innerHTML = `
        <div class="error-container">
            <div class="error-code">404</div>
            <div class="error-message">The page you're looking for doesn't exist.</div>
            <a href="/" class="btn btn-primary">Go Home</a>
        </div>
    `;
}

// Format number with commas for thousands
function formatNumber(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Calculate and format statistics
function calculateStats(value, total) {
    if (total === 0) return '0%';
    return ((value / total) * 100).toFixed(1) + '%';
}

// Handle form submission with validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Add error handling for failed API requests
function handleApiError(error) {
    console.error('API Error:', error);
    // You could show a toast notification or alert here
    const errorMessage = error.response ? error.response.data.detail : 'An error occurred';
    alert(errorMessage);
}

// Export functions for use in other scripts
window.app = {
    formatNumber,
    formatDate,
    calculateStats,
    validateForm,
    handleApiError
}; 