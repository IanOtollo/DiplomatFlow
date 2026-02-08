/**
 * IT HELPDESK SYSTEM - MAIN JAVASCRIPT
 * Advanced interactions, animations, and effects
 */

class FuturisticApp {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.createParticleSystem();
        this.setupScrollAnimations();
        this.setupFormEnhancements();
        this.setupThemeToggle();
    }

    init() {
        console.log('🚀 IT Helpdesk System initialized');
        this.addLoadingStates();
        this.setupKeyboardShortcuts();
    }

    setupEventListeners() {
        // Navbar scroll effect
        window.addEventListener('scroll', this.handleNavbarScroll.bind(this));
        
        // Card hover effects
        document.querySelectorAll('.card, .feature-card, .task-card').forEach(card => {
            card.addEventListener('mouseenter', this.handleCardHover.bind(this));
            card.addEventListener('mouseleave', this.handleCardLeave.bind(this));
        });

        // Button click effects
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', this.handleButtonClick.bind(this));
        });

        // Form enhancements - skip authentication forms
        document.querySelectorAll('form').forEach(form => {
            // Skip authentication forms to avoid interference
            if (form.action.includes('login') || form.action.includes('register') || form.action.includes('password')) {
                return;
            }
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        });

        // Input focus effects
        document.querySelectorAll('.form-control, .form-select').forEach(input => {
            input.addEventListener('focus', this.handleInputFocus.bind(this));
            input.addEventListener('blur', this.handleInputBlur.bind(this));
        });
    }

    handleNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(10, 10, 15, 0.95)';
            navbar.style.backdropFilter = 'blur(20px)';
            navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
        } else {
            navbar.style.background = 'rgba(10, 10, 15, 0.9)';
            navbar.style.backdropFilter = 'blur(10px)';
            navbar.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        }
    }

    handleCardHover(e) {
        const card = e.currentTarget;
        card.style.transform = 'translateY(-10px) scale(1.02)';
        card.style.boxShadow = '0 20px 40px rgba(0, 212, 255, 0.3), 0 0 60px rgba(0, 212, 255, 0.1)';
        card.style.borderColor = 'rgba(0, 212, 255, 0.5)';
        
        // Add glow effect to icons
        const icon = card.querySelector('i, .feature-icon');
        if (icon) {
            icon.style.textShadow = '0 0 20px rgba(0, 212, 255, 0.8)';
            icon.style.transform = 'scale(1.1)';
        }
    }

    handleCardLeave(e) {
        const card = e.currentTarget;
        card.style.transform = 'translateY(0) scale(1)';
        card.style.boxShadow = '';
        card.style.borderColor = '';
        
        // Remove glow effect
        const icon = card.querySelector('i, .feature-icon');
        if (icon) {
            icon.style.textShadow = '';
            icon.style.transform = 'scale(1)';
        }
    }

    handleButtonClick(e) {
        const btn = e.currentTarget;
        
        // Create ripple effect
        const ripple = document.createElement('span');
        const rect = btn.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        btn.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
        
        // Add click animation
        btn.style.transform = 'scale(0.95)';
        setTimeout(() => {
            btn.style.transform = 'scale(1)';
        }, 150);
    }

    handleFormSubmit(e) {
        const form = e.currentTarget;
        const submitBtn = form.querySelector('button[type="submit"]');
        // Only show "Processing" for forms that opt-in (e.g. AJAX forms). Regular POST forms
        // would stay on "Processing" if the server returns validation errors or 500.
        if (submitBtn && form.classList.contains('js-ajax-form') && form.checkValidity()) {
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            submitBtn.disabled = true;
        }
    }

    handleInputFocus(e) {
        const input = e.currentTarget;
        input.style.borderColor = 'rgba(0, 212, 255, 0.8)';
        input.style.boxShadow = '0 0 0 0.2rem rgba(0, 212, 255, 0.25)';
        input.style.transform = 'scale(1.02)';
        
        // Add floating label effect
        const label = input.previousElementSibling;
        if (label && label.classList.contains('form-label')) {
            label.style.color = 'var(--primary-color)';
            label.style.transform = 'translateY(-2px)';
        }
    }

    handleInputBlur(e) {
        const input = e.currentTarget;
        input.style.borderColor = '';
        input.style.boxShadow = '';
        input.style.transform = 'scale(1)';
        
        // Reset floating label
        const label = input.previousElementSibling;
        if (label && label.classList.contains('form-label')) {
            label.style.color = '';
            label.style.transform = '';
        }
    }

    createParticleSystem() {
        const container = document.createElement('div');
        container.className = 'particles-container';
        document.body.appendChild(container);
        
        setInterval(() => {
            this.createParticle(container);
        }, 200);
    }

    createParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random position and color
        particle.style.left = Math.random() * 100 + '%';
        particle.style.background = this.getRandomColor();
        particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
        
        container.appendChild(particle);
        
        // Remove particle after animation
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 6000);
    }

    getRandomColor() {
        const colors = [
            'rgba(0, 212, 255, 0.8)',
            'rgba(139, 92, 246, 0.8)',
            'rgba(16, 185, 129, 0.8)',
            'rgba(245, 158, 11, 0.8)'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fadeInUp');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.card, .feature-card, .stat-card, .task-card').forEach(el => {
            observer.observe(el);
        });
    }

    setupFormEnhancements() {
        // Password strength indicator
        const passwordInputs = document.querySelectorAll('input[type="password"]');
        passwordInputs.forEach(input => {
            input.addEventListener('input', this.updatePasswordStrength.bind(this));
        });

        // Real-time form validation
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('blur', () => this.validateField(input));
                input.addEventListener('input', () => this.clearFieldError(input));
            });
        });
    }

    updatePasswordStrength(e) {
        const input = e.target;
        const password = input.value;
        const strengthBar = document.getElementById('strengthBar');
        const strengthText = document.getElementById('strengthText');
        
        if (!strengthBar || !strengthText) return;

        let strength = 0;
        let requirements = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /\d/.test(password),
            special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };

        // Update requirement indicators
        Object.keys(requirements).forEach(req => {
            const icon = document.getElementById(`req-${req}`);
            if (icon) {
                if (requirements[req]) {
                    icon.className = 'requirement-icon requirement-met';
                    icon.innerHTML = '<i class="fas fa-check"></i>';
                    strength++;
                } else {
                    icon.className = 'requirement-icon requirement-unmet';
                    icon.innerHTML = '<i class="fas fa-times"></i>';
                }
            }
        });

        // Update strength bar
        strengthBar.className = 'strength-fill';
        if (strength === 0) {
            strengthBar.classList.add('strength-weak');
            strengthText.textContent = 'Very weak password';
            strengthText.className = 'text-danger';
        } else if (strength <= 2) {
            strengthBar.classList.add('strength-weak');
            strengthText.textContent = 'Weak password';
            strengthText.className = 'text-danger';
        } else if (strength === 3) {
            strengthBar.classList.add('strength-fair');
            strengthText.textContent = 'Fair password';
            strengthText.className = 'text-warning';
        } else if (strength === 4) {
            strengthBar.classList.add('strength-good');
            strengthText.textContent = 'Good password';
            strengthText.className = 'text-info';
        } else if (strength >= 5) {
            strengthBar.classList.add('strength-strong');
            strengthText.textContent = 'Strong password';
            strengthText.className = 'text-success';
        }
    }

    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let errorMessage = '';

        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = `${this.getFieldLabel(field)} is required`;
        }

        // Email validation
        if (fieldName === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address';
            }
        }

        // Password validation
        if (fieldName === 'password' && value) {
            if (value.length < 8) {
                isValid = false;
                errorMessage = 'Password must be at least 8 characters long';
            }
        }

        // Phone validation
        if (fieldName === 'phone_number' && value) {
            const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
            if (!phoneRegex.test(value.replace(/\s/g, ''))) {
                isValid = false;
                errorMessage = 'Please enter a valid phone number';
            }
        }

        this.showFieldError(field, isValid ? null : errorMessage);
        return isValid;
    }

    clearFieldError(field) {
        this.showFieldError(field, null);
    }

    showFieldError(field, message) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }

        if (message) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error text-danger small mt-1';
            errorDiv.innerHTML = `<i class="fas fa-exclamation-circle me-1"></i>${message}`;
            field.parentNode.appendChild(errorDiv);
            field.style.borderColor = 'var(--danger-color)';
        } else {
            field.style.borderColor = '';
        }
    }

    getFieldLabel(field) {
        const label = field.previousElementSibling;
        if (label && label.classList.contains('form-label')) {
            return label.textContent.replace('*', '').trim();
        }
        return field.name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    setupThemeToggle() {
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', this.toggleTheme.bind(this));
        }

        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'dark';
        this.setTheme(savedTheme);
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        const themeIcon = document.getElementById('theme-icon');
        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K for search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.focusSearch();
            }

            // Escape to close modals
            if (e.key === 'Escape') {
                this.closeModals();
            }

            // Ctrl/Cmd + Enter to submit forms
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                const form = document.querySelector('form');
                if (form) {
                    form.submit();
                }
            }
        });
    }

    focusSearch() {
        const searchInput = document.querySelector('input[type="search"], input[name="search"]');
        if (searchInput) {
            searchInput.focus();
            searchInput.select();
        }
    }

    closeModals() {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }

    addLoadingStates() {
        // Only show "Processing" for forms that opt-in via js-ajax-form (avoids stuck state on validation/500)
        document.querySelectorAll('form.js-ajax-form button[type="submit"]').forEach(btn => {
            if (btn.form && (btn.form.action.includes('login') || btn.form.action.includes('register') || btn.form.action.includes('password'))) return;
            btn.addEventListener('click', function() {
                if (this.form && this.form.checkValidity() && !this.disabled) {
                    this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                    this.disabled = true;
                }
            });
        });
    }
}

// Utility functions
const Utils = {
    debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
                clearTimeout(timeout);
                func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
    },

    throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
    },

    formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    },

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(notification);

        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FuturisticApp();
});

// Add ripple effect CSS
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }

    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }

    .field-error {
        animation: shake 0.5s ease-in-out;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);

// Export for global access
window.FuturisticApp = FuturisticApp;
window.Utils = Utils;
