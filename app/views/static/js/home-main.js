document.addEventListener('DOMContentLoaded', function() {
  const hero = document.getElementById('hero');
  const heroContent = document.querySelector('.hero-content');
  const heroScrollIndicator = document.querySelector('.hero-scroll-indicator');
  const heroOverlay = document.querySelector('.hero-overlay');
  const nav = document.getElementById('main_nav');

  let lastScrollY = 0;
  const heroHeight = hero ? hero.offsetHeight : 0;

  function handleScroll() {
    const currentScroll = window.pageYOffset;

    if (hero && heroContent && heroScrollIndicator && heroOverlay) {
      const scrollPercent = Math.min(currentScroll / (heroHeight * 0.5), 1);

      heroContent.style.transform = `translateY(${scrollPercent * 20}px)`;
      heroContent.style.opacity = 1 - scrollPercent * 0.7;

      heroOverlay.style.opacity = 0.6 + scrollPercent * 0.3;

      heroScrollIndicator.style.opacity = 1 - scrollPercent * 2;
      heroScrollIndicator.style.transform = `translateY(${scrollPercent * 30}px)`;
    }

    if (nav) {
      const heroBottom = heroHeight - 80;

      if (currentScroll > heroBottom) {
        nav.classList.add('nav-scrolled');
      } else {
        nav.classList.remove('nav-scrolled');
      }

      if (currentScroll > lastScrollY && currentScroll > heroBottom) {
        nav.style.transform = 'translateY(-100%)';
      } else {
        nav.style.transform = 'translateY(0)';
      }
    }

    lastScrollY = currentScroll;
  }

  window.addEventListener('scroll', handleScroll);
  handleScroll();

  const heroCta = document.querySelector('.hero-cta');
  if (heroCta && hero) {
    heroCta.addEventListener('click', function (event) {
      event.preventDefault();
      const targetSection = document.querySelector('.highlighted-collection');
      if (targetSection) {
        const rect = targetSection.getBoundingClientRect();
        const offset = rect.top + window.pageYOffset - 96;
        window.scrollTo({
          top: offset,
          behavior: 'smooth',
        });
      }
    });
  }

  const promoTexts = [
    'Frete Grátis para compras acima de R$ 299',
    '10% OFF na sua primeira compra',
    '5% OFF no pagamento via Pix'
  ];

  const promoElement = document.getElementById('promo-text');
  if (promoElement) {
    let promoIndex = 0;
    let isHovered = false;

    function updatePromoText() {
      if (isHovered) return;

      promoElement.style.opacity = 0;
      promoElement.style.transform = 'translateY(-5px)';

      setTimeout(() => {
        promoIndex = (promoIndex + 1) % promoTexts.length;
        promoElement.textContent = promoTexts[promoIndex];
        promoElement.style.opacity = 1;
        promoElement.style.transform = 'translateY(0)';
      }, 220);
    }

    let promoInterval = setInterval(updatePromoText, 4500);

    promoElement.addEventListener('mouseenter', () => {
      isHovered = true;
      clearInterval(promoInterval);
    });

    promoElement.addEventListener('mouseleave', () => {
      isHovered = false;
      promoInterval = setInterval(updatePromoText, 4500);
    });
  }

  const heroBackground = document.querySelector('.hero-background');
  if (heroBackground) {
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      heroBackground.style.transform = `translateY(${scrollY * 0.2}px)`;
    });
  }

  const discoveryCards = document.querySelectorAll('.discovery-card');
  if (discoveryCards.length > 0) {
    const discoveryObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            discoveryCards.forEach((card, index) => {
              card.style.animationDelay = `${index * 0.12}s`;
              card.classList.add('discovery-card-visible');
            });
            discoveryObserver.disconnect();
          }
        });
      },
      { threshold: 0.25 }
    );

    discoveryCards.forEach((card) => discoveryObserver.observe(card));
  }

  const collectionCards = document.querySelectorAll('.collection-card');
  if (collectionCards.length > 0) {
    const collectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            collectionCards.forEach((card, index) => {
              card.style.animationDelay = `${index * 0.08}s`;
              card.classList.add('collection-card-visible');
            });
            collectionObserver.disconnect();
          }
        });
      },
      { threshold: 0.3 }
    );

    collectionCards.forEach((card) => collectionObserver.observe(card));
  }

  const benefitsSection = document.querySelector('.benefits');
  const benefitItems = document.querySelectorAll('.benefit-item');

  if (benefitsSection && benefitItems.length > 0) {
    const benefitsObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            benefitItems.forEach((item, index) => {
              item.style.animationDelay = `${index * 0.1}s`;
              item.classList.add('benefit-item-visible');
            });
            benefitsObserver.disconnect();
          }
        });
      },
      { threshold: 0.3 }
    );

    benefitsObserver.observe(benefitsSection);
  }

  const storySection = document.querySelector('.brand-story');
  const storyCards = document.querySelectorAll('.story-card');

  if (storySection && storyCards.length > 0) {
    const storyObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            storyCards.forEach((card, index) => {
              card.style.animationDelay = `${index * 0.1}s`;
              card.classList.add('story-card-visible');
            });
            storyObserver.disconnect();
          }
        });
      },
      { threshold: 0.4 }
    );

    storyObserver.observe(storySection);
  }

  const heroCtaPrimary = document.querySelector('.hero-cta-primary');
  if (heroCtaPrimary) {
    heroCtaPrimary.addEventListener('mouseenter', () => {
      heroCtaPrimary.classList.add('cta-pulse');
    });
    heroCtaPrimary.addEventListener('mouseleave', () => {
      heroCtaPrimary.classList.remove('cta-pulse');
    });
  }

  const scrollPrompt = document.querySelector('.hero-scroll-indicator');
  if (scrollPrompt) {
    scrollPrompt.addEventListener('click', (event) => {
      event.preventDefault();
      const nextSection = document.querySelector('.highlighted-collection');
      if (nextSection) {
        const rect = nextSection.getBoundingClientRect();
        const offset = rect.top + window.pageYOffset - 96;
        window.scrollTo({
          top: offset,
          behavior: 'smooth',
        });
      }
    });
  }

  const collectionFilters = document.querySelectorAll(
    '.collection-filter button'
  );
  const collectionWrapper = document.querySelector('.collection-wrapper');

  if (collectionFilters.length > 0 && collectionWrapper) {
    collectionFilters.forEach((filter) => {
      filter.addEventListener('click', () => {
        collectionFilters.forEach((btn) => btn.classList.remove('active'));
        filter.classList.add('active');

        const filterValue = filter.dataset.filter;
        const cards = collectionWrapper.querySelectorAll('.collection-card');

        cards.forEach((card) => {
          const cardCategory = card.dataset.category;
          if (filterValue === 'all' || filterValue === cardCategory) {
            card.classList.remove('hidden');
          } else {
            card.classList.add('hidden');
          }
        });
      });
    });
  }

  const newsletterForm = document.querySelector('.newsletter-form');
  if (newsletterForm) {
    const emailInput = newsletterForm.querySelector('input[type="email"]');
    const submitButton = newsletterForm.querySelector('button[type="submit"]');

    newsletterForm.addEventListener('submit', (event) => {
      event.preventDefault();

      if (!emailInput || !submitButton) return;

      const emailValue = emailInput.value.trim();

      if (!emailValue || !emailValue.includes('@')) {
        emailInput.classList.add('input-error');
        setTimeout(() => emailInput.classList.remove('input-error'), 600);
        return;
      }

      submitButton.disabled = true;
      submitButton.textContent = 'Processando...';

      setTimeout(() => {
        submitButton.disabled = false;
        submitButton.textContent = 'Assinar newsletter';
        emailInput.value = '';
      }, 1500);
    });
  }

  const heroShapeLayers = document.querySelectorAll('.hero-shape');
  if (heroShapeLayers.length > 0) {
    document.addEventListener('mousemove', (e) => {
      const { innerWidth, innerHeight } = window;
      const xPos = (e.clientX / innerWidth) - 0.5;
      const yPos = (e.clientY / innerHeight) - 0.5;

      heroShapeLayers.forEach((shape, index) => {
        const depth = (index + 1) * 8;
        const translateX = -xPos * depth;
        const translateY = -yPos * depth;
        shape.style.transform = `translate(${translateX}px, ${translateY}px)`;
      });
    });
  }

  const heroScrollIndicatorArrow = document.querySelector(
    '.hero-scroll-indicator svg'
  );
  if (heroScrollIndicatorArrow) {
    heroScrollIndicatorArrow.classList.add('scroll-indicator-bounce');
  }

  const smoothLinks = document.querySelectorAll('a[data-scroll-target]');
  if (smoothLinks.length > 0) {
    smoothLinks.forEach((link) => {
      link.addEventListener('click', function (event) {
        event.preventDefault();
        const targetSelector = this.getAttribute('data-scroll-target');
        const targetElement = document.querySelector(targetSelector);

        if (!targetElement) return;

        const targetRect = targetElement.getBoundingClientRect();
        const headerOffset = 96;
        const targetPosition = targetRect.top + window.pageYOffset - headerOffset;

        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;

        let startTime = null;

        function customSmoothScroll(target, duration) {
          function animation(currentTime) {
            if (startTime === null) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const progress = Math.min(timeElapsed / duration, 1);

            const easeProgress =
              progress < 0.5
                ? 4 * progress * progress * progress
                : 1 - Math.pow(-2 * progress + 2, 3) / 2;

            window.scrollTo(0, startPosition + distance * easeProgress);

            if (timeElapsed < duration) {
              requestAnimationFrame(animation);
            }
          }

          requestAnimationFrame(animation);
        }

        const scrollDuration = 1200;
        customSmoothScroll(targetPosition, scrollDuration);
      });
    });
  }

  const faqLabels = document.querySelectorAll(".faq-item label");
  faqLabels.forEach((label) => {
    label.addEventListener("click", function () {
      const input = this.previousElementSibling;

      if (input && input.type === "checkbox") {
        input.checked = !input.checked;
      }
    });
  });

  const parallaxElements = document.querySelectorAll(
    ".story-image img, .category-image img"
  );
  window.addEventListener("scroll", function () {
    const scrolled = window.pageYOffset;
    parallaxElements.forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        const speed = 0.3;
        const yPos = -(scrolled * speed);
        el.style.transform = `translateY(${yPos * 0.05}px)`;
      }
    });
  });

  const testimonialCards = document.querySelectorAll(".testimonial-card");
  testimonialCards.forEach((card, index) => {
    card.style.transitionDelay = `${index * 0.1}s`;
  });

  const categoryCards = document.querySelectorAll(".category-card");
  if (categoryCards.length > 0) {
    let categoryIndex = 0;
    const categoryInterval = setInterval(() => {
      if (categoryIndex < categoryCards.length) {
        const card = categoryCards[categoryIndex];
        if (!card) {
          clearInterval(categoryInterval);
          return;
        }
        card.style.transform = "scale(1.05)";
        setTimeout(() => {
          card.style.transform = "scale(1)";
        }, 300);
        categoryIndex++;
      } else {
        clearInterval(categoryInterval);
      }
    }, 200);
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const stats = entry.target.querySelectorAll(".stat-number");
          stats.forEach((stat) => {
            let currentValue = 0;
            const finalValue = parseInt(stat.textContent.replace(/\D/g, ""), 10);
            const increment = finalValue / 50;

            const timer = setInterval(() => {
              currentValue += increment;
              if (currentValue >= finalValue) {
                stat.textContent =
                  finalValue + (stat.textContent.includes("+") ? "+" : "%");
                clearInterval(timer);
              } else {
                stat.textContent =
                  Math.floor(currentValue) +
                  (stat.textContent.includes("+") ? "+" : "%");
              }
            }, 30);
          });
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  const storyStats = document.querySelector(".story-stats");
  if (storyStats) {
    observer.observe(storyStats);
  }
});
