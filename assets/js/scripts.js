// Mills Shirley LLP Website JavaScript
// Navigation, smooth scrolling, and mobile menu functionality

document.addEventListener('DOMContentLoaded', function() {
    
    // Enhanced Mobile Menu Toggle with Accessibility
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    let isMenuOpen = false;
    
    // Create mobile menu backdrop
    const backdrop = document.createElement('div');
    backdrop.className = 'mobile-menu-backdrop';
    document.body.appendChild(backdrop);
    
    if (mobileMenuButton && mobileMenu) {
        // Set initial ARIA attributes
        mobileMenuButton.setAttribute('aria-expanded', 'false');
        mobileMenuButton.setAttribute('aria-controls', 'mobile-menu');
        mobileMenu.setAttribute('aria-hidden', 'true');
        
        function toggleMobileMenu() {
            isMenuOpen = !isMenuOpen;
            
            if (isMenuOpen) {
                // Open menu
                mobileMenu.classList.remove('hidden');
                backdrop.classList.add('active');
                mobileMenuButton.setAttribute('aria-expanded', 'true');
                mobileMenu.setAttribute('aria-hidden', 'false');
                document.body.style.overflow = 'hidden'; // Prevent scroll
                
                // Focus first menu item
                const firstMenuItem = mobileMenu.querySelector('a');
                if (firstMenuItem) {
                    setTimeout(() => firstMenuItem.focus(), 100);
                }
            } else {
                // Close menu
                mobileMenu.classList.add('hidden');
                backdrop.classList.remove('active');
                mobileMenuButton.setAttribute('aria-expanded', 'false');
                mobileMenu.setAttribute('aria-hidden', 'true');
                document.body.style.overflow = '';
                
                // Return focus to button
                mobileMenuButton.focus();
            }
            
            // Update button icon with animation
            const buttonSvg = mobileMenuButton.querySelector('svg path');
            if (isMenuOpen) {
                buttonSvg.setAttribute('d', 'M6 18L18 6M6 6l12 12'); // X icon
            } else {
                buttonSvg.setAttribute('d', 'M4 6h16M4 12h16M4 18h16'); // Hamburger icon
            }
        }
        
        mobileMenuButton.addEventListener('click', toggleMobileMenu);
        
        // Close mobile menu when clicking backdrop
        backdrop.addEventListener('click', function() {
            if (isMenuOpen) {
                toggleMobileMenu();
            }
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (isMenuOpen && !mobileMenuButton.contains(e.target) && !mobileMenu.contains(e.target)) {
                toggleMobileMenu();
            }
        });
        
        // Close mobile menu when clicking on a menu item
        const mobileMenuLinks = mobileMenu.querySelectorAll('a');
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (isMenuOpen) {
                    toggleMobileMenu();
                }
            });
        });
        
        // Focus management within mobile menu
        const menuItems = mobileMenu.querySelectorAll('a, button');
        if (menuItems.length > 0) {
            // Trap focus within menu when open
            mobileMenu.addEventListener('keydown', function(e) {
                if (e.key === 'Tab' && isMenuOpen) {
                    const firstItem = menuItems[0];
                    const lastItem = menuItems[menuItems.length - 1];
                    
                    if (e.shiftKey) {
                        // Shift + Tab
                        if (document.activeElement === firstItem) {
                            e.preventDefault();
                            lastItem.focus();
                        }
                    } else {
                        // Tab
                        if (document.activeElement === lastItem) {
                            e.preventDefault();
                            firstItem.focus();
                        }
                    }
                }
            });
        }
    }
    
    // Smooth Scrolling for Anchor Links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Skip if it's just '#' or empty
            if (href === '#' || href === '') {
                return;
            }
            
            const targetElement = document.querySelector(href);
            
            if (targetElement) {
                e.preventDefault();
                
                // Get header height for offset (sticky header)
                const header = document.querySelector('header');
                const headerHeight = header ? header.offsetHeight : 0;
                
                // Calculate scroll position
                const elementPosition = targetElement.offsetTop;
                const offsetPosition = elementPosition - headerHeight - 20; // 20px extra padding
                
                // Smooth scroll to target
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Header Shadow on Scroll
    const header = document.querySelector('header');
    
    if (header) {
        function updateHeaderShadow() {
            if (window.scrollY > 16) { // 16px threshold for smoother activation
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }
        
        // Initial check
        updateHeaderShadow();
        
        // Update on scroll with throttling for performance
        let isScrolling = false;
        window.addEventListener('scroll', function() {
            if (!isScrolling) {
                window.requestAnimationFrame(function() {
                    updateHeaderShadow();
                    isScrolling = false;
                });
                isScrolling = true;
            }
        });
    }
    
    // Form Enhancement (Basic Validation)
    const contactForm = document.querySelector('form[action="#"]');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Basic form validation
            const requiredFields = contactForm.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                    field.classList.remove('border-gray-300');
                } else {
                    field.classList.remove('border-red-500');
                    field.classList.add('border-gray-300');
                }
            });
            
            // Email validation
            const emailField = contactForm.querySelector('input[type="email"]');
            if (emailField && emailField.value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(emailField.value)) {
                    isValid = false;
                    emailField.classList.add('border-red-500');
                    emailField.classList.remove('border-gray-300');
                }
            }
            
            if (isValid) {
                // TODO: Replace with actual form submission logic
                // For now, show a simple alert
                alert('Thank you for your message! We will get back to you soon.');
                
                // Reset form
                contactForm.reset();
            } else {
                // Show error message
                alert('Please fill in all required fields correctly.');
            }
        });
        
        // Remove error styling on input
        const formInputs = contactForm.querySelectorAll('input, textarea');
        formInputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.classList.remove('border-red-500');
                    this.classList.add('border-gray-300');
                }
            });
        });
    }
    
    // Scroll to Top Button (Optional Enhancement)
    // Create scroll to top button
    const scrollToTopButton = document.createElement('button');
    scrollToTopButton.innerHTML = `
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path>
        </svg>
    `;
    scrollToTopButton.className = 'fixed bottom-8 right-8 bg-navy-900 text-white p-3 rounded-full shadow-lg hover:bg-navy-950 transition-all duration-300 opacity-0 pointer-events-none z-50';
    scrollToTopButton.setAttribute('aria-label', 'Scroll to top');
    
    document.body.appendChild(scrollToTopButton);
    
    // Show/hide scroll to top button
    function updateScrollToTopButton() {
        if (window.scrollY > 300) {
            scrollToTopButton.classList.remove('opacity-0', 'pointer-events-none');
            scrollToTopButton.classList.add('opacity-100');
        } else {
            scrollToTopButton.classList.add('opacity-0', 'pointer-events-none');
            scrollToTopButton.classList.remove('opacity-100');
        }
    }
    
    window.addEventListener('scroll', updateScrollToTopButton);
    
    // Scroll to top functionality
    scrollToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Animation on Scroll (Optional Enhancement)
    // Simple fade-in animation for elements as they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe sections for animation
    const sectionsToAnimate = document.querySelectorAll('section > div');
    sectionsToAnimate.forEach(section => {
        section.classList.add('opacity-0', 'translate-y-8', 'transition-all', 'duration-700');
        observer.observe(section);
    });
    
    // Add CSS for fade-in animation
    const style = document.createElement('style');
    style.textContent = `
        .animate-fade-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);
    
    // Enhanced Accessibility
    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-nav';
    skipLink.setAttribute('tabindex', '0');
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Add skip to navigation link
    const skipNavLink = document.createElement('a');
    skipNavLink.href = '#main-navigation';
    skipNavLink.textContent = 'Skip to navigation';
    skipNavLink.className = 'skip-nav';
    skipNavLink.style.left = '30%';
    
    document.body.insertBefore(skipNavLink, skipLink.nextSibling);
    
    // Add main content and navigation IDs if they don't exist
    const mainContent = document.querySelector('main') || document.querySelector('section');
    if (mainContent && !mainContent.id) {
        mainContent.id = 'main-content';
        mainContent.setAttribute('tabindex', '-1'); // Allow programmatic focus
    }
    
    const navigation = document.querySelector('nav');
    if (navigation && !navigation.id) {
        navigation.id = 'main-navigation';
    }
    
    // Improve focus indicators for all interactive elements
    const interactiveElements = document.querySelectorAll('a, button, input, textarea, select');
    interactiveElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.classList.add('focus-visible');
        });
        
        element.addEventListener('blur', function() {
            this.classList.remove('focus-visible');
        });
    });
    
    // Enhanced announcement for screen readers
    const srAnnouncer = document.createElement('div');
    srAnnouncer.setAttribute('aria-live', 'polite');
    srAnnouncer.setAttribute('aria-atomic', 'true');
    srAnnouncer.className = 'sr-only';
    document.body.appendChild(srAnnouncer);
    
    function announceToScreenReader(message) {
        srAnnouncer.textContent = message;
        setTimeout(() => {
            srAnnouncer.textContent = '';
        }, 1000);
    }
    
    // Announce menu state changes
    if (mobileMenuButton) {
        const originalToggle = toggleMobileMenu;
        toggleMobileMenu = function() {
            originalToggle();
            announceToScreenReader(isMenuOpen ? 'Menu opened' : 'Menu closed');
        };
    }
    
    // Enhanced keyboard navigation
    document.addEventListener('keydown', function(e) {
        // Escape key to close mobile menu
        if (e.key === 'Escape' && isMenuOpen) {
            toggleMobileMenu();
        }
        
        // Enter or Space to activate mobile menu button
        if ((e.key === 'Enter' || e.key === ' ') && e.target === mobileMenuButton) {
            e.preventDefault();
            toggleMobileMenu();
        }
    });
    
    console.log('Mills Shirley LLP website scripts loaded successfully');
});