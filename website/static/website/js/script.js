// Initialize theme
(function() {
  const savedTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.dataset.theme = savedTheme;
  console.log(`[INIT] Theme set to: ${savedTheme}`);
})();

document.addEventListener('DOMContentLoaded', function() {
  console.log('[INIT] DOMContentLoaded event fired');

  // Cache DOM elements
  const elements = {
    navLinks: document.querySelectorAll('.nav-links a'),
    mobileMenuToggle: document.getElementById('mobileMenuToggle'),
    navLinksContainer: document.getElementById('navLinks'),
    navOverlay: document.getElementById('navOverlay'),
    toggleButton: document.querySelector('.toggle-dark'),
    toggleIcon: document.querySelector('.toggle-dark i'),
    header: document.querySelector('.nav-header'),
    messagesContainer: document.querySelector('.messages'),
    sections: document.querySelectorAll('section[id]'),
    faders: document.querySelectorAll('.fade-in'),
    testimonialVideos: document.querySelectorAll('.testimonial-item video'),
    playButtons: document.querySelectorAll('.play-button'),
    fullscreenButtons: document.querySelectorAll('.fullscreen-button'),
    contactForm: document.querySelector('.contact-form form'),
    imageContainer: document.querySelector('.image-container'),
    rotatingImages: document.querySelectorAll('.rotating-image'),
    // dialogBtn: document.querySelector('#showDialog'),
    // marketplaceDialog: document.getElementById('marketplaceDialog'),
    // marketPlaceOverlay: document.querySelector('#overlay')
  };

  // Function to handle message fade-out
  function fadeOutMessages(messages) {
    if (messages && messages.length > 0) {
      messages.forEach((message, index) => {
        if (!message.dataset.fadeOutScheduled) {
          message.dataset.fadeOutScheduled = true;
          console.log(`[MESSAGE] Scheduling fade-out for message ${index + 1}: ${message.textContent.trim()}`);
          setTimeout(() => {
            console.log(`[MESSAGE] Applying fade-out to message ${index + 1}`);
            message.classList.add('fade-out');
            message.addEventListener('transitionend', () => {
              console.log(`[MESSAGE] Removing message ${index + 1} from DOM`);
              message.remove();
            }, { once: true });
          }, 5000);
        }
      });
    } else {
      console.warn('[MESSAGE] No messages found to fade out');
    }
  }

  // Initial check for existing messages
  const initialMessages = document.querySelectorAll('.alert');
  console.log(`[MESSAGE] Found ${initialMessages.length} initial message elements with class .alert`);
  fadeOutMessages(initialMessages);

  // Observe dynamic message additions
  if (elements.messagesContainer) {
    console.log('[MESSAGE] MutationObserver set up for .messages container');
    const observer = new MutationObserver((mutations) => {
      mutations.forEach(mutation => {
        if (mutation.addedNodes.length) {
          const newMessages = document.querySelectorAll('.alert:not([data-fade-out-scheduled])');
          console.log(`[MESSAGE] Detected ${newMessages.length} new message elements`);
          fadeOutMessages(newMessages);
        }
      });
    });
    observer.observe(elements.messagesContainer, { childList: true, subtree: true });
  } else {
    console.warn('[MESSAGE] Messages container (.messages) not found');
  }

  // Fallback interval check for messages
  let messageCheckCount = 0;
  const messageCheckInterval = setInterval(() => {
    const newMessages = document.querySelectorAll('.alert:not([data-fade-out-scheduled])');
    if (newMessages.length > 0) {
      console.log(`[MESSAGE] Interval detected ${newMessages.length} new message elements`);
      fadeOutMessages(newMessages);
    }
    messageCheckCount++;
    if (messageCheckCount >= 10) {
      console.log('[MESSAGE] Stopping interval check after 10 attempts');
      clearInterval(messageCheckInterval);
    }
  }, 1000);

  // Theme toggle
  function toggleTheme() {
    const newTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = newTheme;
    localStorage.setItem('theme', newTheme);
    if (elements.toggleIcon) {
      elements.toggleIcon.className = `fa-solid fa-${newTheme === 'dark' ? 'sun' : 'moon'}`;
    }
    console.log(`[THEME] Switched to: ${newTheme}`);
  }

  if (elements.toggleButton && elements.toggleIcon) {
    elements.toggleIcon.className = `fa-solid fa-${document.documentElement.dataset.theme === 'dark' ? 'sun' : 'moon'}`;
    elements.toggleButton.addEventListener('click', toggleTheme);
  } else {
    console.error('[THEME] Theme toggle elements missing');
  }

  // Mobile menu toggle
  function toggleMobileMenu() {
    const isActive = elements.navLinksContainer.classList.contains('active');
    elements.navLinksContainer.classList.toggle('active');
    elements.mobileMenuToggle.classList.toggle('active');
    elements.navOverlay.classList.toggle('active');
    document.body.style.overflow = isActive ? 'auto' : 'hidden';
    const menuIcon = elements.mobileMenuToggle.querySelector('i');
    if (menuIcon) {
      menuIcon.className = isActive ? 'fa-solid fa-bars' : 'fa-solid fa-xmark';
    }
    console.log(`[MENU] Mobile menu: ${isActive ? 'Closed' : 'Opened'}`);
  }

  if (elements.mobileMenuToggle && elements.navLinksContainer && elements.navOverlay) {
    elements.mobileMenuToggle.addEventListener('click', toggleMobileMenu);
    elements.navOverlay.addEventListener('click', toggleMobileMenu);
    elements.navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (elements.navLinksContainer.classList.contains('active')) {
          toggleMobileMenu();
        }
      });
    });
  } else {
    console.error('[MENU] Mobile menu elements missing');
  }

  // Active link highlighting with IntersectionObserver
  function setupActiveLinkObserver() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const activeSectionId = entry.target.id;
          elements.navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('data-href') === activeSectionId) {
              link.classList.add('active');
            }
          });
          console.log(`[NAV] Active section: ${activeSectionId}, Active link: ${document.querySelector('.nav-links a.active')?.textContent || 'None'}`);
        }
      });
    }, {
      rootMargin: `-10% 0px -80% 0px`,
      threshold: 0.1
    });

    elements.sections.forEach(section => observer.observe(section));
  }

  // Smooth scrolling
  function handleNavClick(e) {
    e.preventDefault();
    const targetId = e.currentTarget.getAttribute('data-href');
    const targetSection = document.getElementById(targetId);
    if (targetSection) {
      const headerHeight = elements.header?.offsetHeight || 80;
      window.scrollTo({
        top: targetSection.getBoundingClientRect().top + window.scrollY - headerHeight,
        behavior: 'smooth'
      });
      elements.navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-href') === targetId) {
          link.classList.add('active');
        }
      });
      console.log(`[NAV] Clicked link: ${e.currentTarget.textContent} (Target: ${targetId})`);
    }
  }

  elements.navLinks.forEach(link => {
    link.addEventListener('click', handleNavClick);
  });

  // Handle hash navigation
  if (window.location.hash) {
    const targetId = window.location.hash.substring(1);
    const targetSection = document.getElementById(targetId);
    if (targetSection) {
      setTimeout(() => {
        const headerHeight = elements.header?.offsetHeight || 80;
        window.scrollTo({
          top: targetSection.getBoundingClientRect().top + window.scrollY - headerHeight,
          behavior: 'smooth'
        });
        elements.navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('data-href') === targetId) {
            link.classList.add('active');
          }
        });
        console.log(`[NAV] Hash navigation: Active link set to ${targetId}`);
      }, 100);
    }
  }

  // Initialize active link observer
  setupActiveLinkObserver();

  // Fade-in animations with IntersectionObserver
  function observeSections() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    
    elements.faders.forEach(fader => observer.observe(fader));
  }
  observeSections();

  // Video play and fullscreen interactions
  if (elements.testimonialVideos && elements.playButtons && elements.fullscreenButtons) {
    elements.testimonialVideos.forEach((video, index) => {
      const playButton = elements.playButtons[index];
      const fullscreenButton = elements.fullscreenButtons[index];

      video.addEventListener('loadedmetadata', () => {
        console.log(`[VIDEO] Video ${index + 1} metadata loaded: ${video.src}`);
      });

      video.addEventListener('error', (e) => {
        console.error(`[VIDEO] Error loading video ${index + 1}: ${e.message}, Source: ${video.src}`);
      });

      if (playButton) {
        playButton.addEventListener('click', () => {
          if (video.paused) {
            video.play().then(() => {
              video.parentElement.classList.add('playing');
              playButton.innerHTML = '<i class="fa-solid fa-pause"></i>';
              console.log(`[VIDEO] Playing video ${index + 1}`);
            }).catch(error => {
              console.warn(`[VIDEO] Play failed for video ${index + 1}: ${error.message}`);
            });
          } else {
            video.pause();
            video.parentElement.classList.remove('playing');
            playButton.innerHTML = '<i class="fa-solid fa-play"></i>';
            video.currentTime = 0;
            console.log(`[VIDEO] Paused video ${index + 1}`);
          }
        });
      }

      if (fullscreenButton) {
        fullscreenButton.addEventListener('click', () => {
          if (video.requestFullscreen) {
            video.requestFullscreen().catch(err => console.warn(`[VIDEO] Fullscreen failed for video ${index + 1}: ${err.message}`));
          } else if (video.webkitRequestFullscreen) {
            video.webkitRequestFullscreen().catch(err => console.warn(`[VIDEO] Fullscreen failed for video ${index + 1}: ${err.message}`));
          } else if (video.msRequestFullscreen) {
            video.msRequestFullscreen().catch(err => console.warn(`[VIDEO] Fullscreen failed for video ${index + 1}: ${err.message}`));
          }
          console.log(`[VIDEO] Fullscreen requested for video ${index + 1}`);
        });
      }

      video.addEventListener('play', () => {
        video.parentElement.classList.add('playing');
        console.log(`[VIDEO] Video ${index + 1} started playing`);
      });

      video.addEventListener('pause', () => {
        video.parentElement.classList.remove('playing');
        video.currentTime = 0;
        console.log(`[VIDEO] Video ${index + 1} paused`);
      });

      video.addEventListener('ended', () => {
        video.parentElement.classList.remove('playing');
        video.currentTime = 0;
        console.log(`[VIDEO] Video ${index + 1} ended`);
      });

      video.addEventListener('dblclick', () => {
        if (video.requestFullscreen) {
          video.requestFullscreen().catch(err => console.warn(`[VIDEO] Fullscreen failed for video ${index + 1}: ${err.message}`));
        }
        console.log(`[VIDEO] Double-click fullscreen for video ${index + 1}`);
      });

      video.addEventListener('mouseenter', () => {
        if (!video.paused) return;
        playButton.style.display = 'flex';
        console.log(`[VIDEO] Mouse enter on video ${index + 1}: Showing play button`);
      });

      video.addEventListener('mouseleave', () => {
        if (!video.paused) return;
        playButton.style.display = 'none';
        console.log(`[VIDEO] Mouse leave on video ${index + 1}: Hiding play button`);
      });
    });
    console.log(`[VIDEO] Initialized ${elements.testimonialVideos.length} testimonial videos with play and fullscreen buttons`);
  } else {
    console.warn('[VIDEO] No testimonial videos, play buttons, or fullscreen buttons found');
  }

  // Basic form validation
  if (elements.contactForm) {
    elements.contactForm.addEventListener('submit', (e) => {
      const phone = elements.contactForm.querySelector('#phone').value.trim();
      const email = elements.contactForm.querySelector('#email').value.trim();
      if (!email && !phone) {
        e.preventDefault();
        alert('Please provide either an email or phone number.');
        console.log('[FORM] Validation failed: Email or phone required');
      }
      if (phone && !/^\+?\d{10,15}$/.test(phone)) {
        e.preventDefault();
        alert('Please enter a valid phone number (10-15 digits, optional + prefix).');
        console.log('[FORM] Validation failed: Invalid phone number');
      }
    });
  } else {
    console.warn('[FORM] Contact form not found');
  }

  // Marquee duplication
  const servicesList = document.querySelector('.services-list');
  if (servicesList) {
    servicesList.innerHTML += servicesList.innerHTML;
    console.log('[MARQUEE] Services list duplicated for seamless loop');
  }

  // Image rotation (time-based)
  if (elements.imageContainer && elements.rotatingImages.length > 0) {
    let currentImage = 0;
    let rotationInterval;

    // Log initial state
    console.log(`[IMAGE] Found ${elements.rotatingImages.length} images for rotation`);

    // Set initial image
    elements.rotatingImages[currentImage].classList.add('active');
    console.log(`[IMAGE] Initial image: ${currentImage + 1}`);

    function rotateImage() {
      elements.rotatingImages[currentImage].classList.remove('active');
      currentImage = (currentImage + 1) % elements.rotatingImages.length;
      elements.rotatingImages[currentImage].classList.add('active');
      console.log(`[IMAGE] Rotated to image ${currentImage + 1}`);
    }

    // Start rotation only if there are multiple images
    function startRotation() {
      if (elements.rotatingImages.length > 1) {
        rotationInterval = setInterval(rotateImage, 5000); // Rotate every 5 seconds
        console.log('[IMAGE] Image rotation started');
      } else {
        console.log('[IMAGE] Only one image, rotation not started');
      }
    }

    // Stop rotation
    function stopRotation() {
      if (rotationInterval) {
        clearInterval(rotationInterval);
        console.log('[IMAGE] Image rotation stopped');
      }
    }

    // Pause/resume rotation on hover
    elements.imageContainer.addEventListener('mouseenter', () => {
      stopRotation();
      console.log('[IMAGE] Rotation paused on hover');
    });

    elements.imageContainer.addEventListener('mouseleave', () => {
      startRotation();
      console.log('[IMAGE] Rotation resumed after hover');
    });

    // Start rotation initially
    startRotation();

    // Debug image loading
    elements.rotatingImages.forEach((img, index) => {
      img.addEventListener('error', () => {
        console.error(`[IMAGE] Failed to load image ${index + 1}: ${img.src}`);
      });
      img.addEventListener('load', () => {
        console.log(`[IMAGE] Loaded image ${index + 1}: ${img.src}`);
      });
    });
  } else {
    console.warn('[IMAGE] No images or image container found');
  }
});