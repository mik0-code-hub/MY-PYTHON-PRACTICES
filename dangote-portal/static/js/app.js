/**
 * Dangote Group Portal - Main Application Orchestrator
 */

document.addEventListener('DOMContentLoaded', () => {
  App.init();
});

const App = {
  allBusinesses: [],
  allNews: [],
  allCareers: [],

  async init() {
    this.initTheme();
    this.initHeaderScroll();
    this.initHeroSlider();
    this.initCounterAnimation();
    this.initMobileDrawer();
    this.initSearchModal();
    this.initContactForm();
    this.initEthicsModal();
    this.initBranchTabs();

    // Initialize Submodules
    if (window.StockTicker) window.StockTicker.init();
    if (window.AfricaMap) window.AfricaMap.init();
    if (window.DividendCalculator) window.DividendCalculator.init();

    // Load dynamic data
    await this.loadBusinesses();
    await this.loadNews();
    await this.loadCareers();
  },

  /* ==================== THEME CONTROLLER ==================== */
  initTheme() {
    const savedTheme = localStorage.getItem('dangote_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    this.updateThemeIcon(savedTheme);

    const toggleBtn = document.getElementById('themeToggleBtn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('dangote_theme', next);
        this.updateThemeIcon(next);
      });
    }
  },

  updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (icon) {
      icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
  },

  /* ==================== HEADER SCROLL ==================== */
  initHeaderScroll() {
    const header = document.getElementById('mainHeader');
    window.addEventListener('scroll', () => {
      if (window.scrollY > 40) {
        header?.classList.add('scrolled');
      } else {
        header?.classList.remove('scrolled');
      }
    });
  },

  /* ==================== CINEMATIC HERO SLIDER ==================== */
  initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    const prevBtn = document.getElementById('heroPrevBtn');
    const nextBtn = document.getElementById('heroNextBtn');
    if (!slides.length) return;

    let current = 0;
    let timer = null;
    const intervalTime = 6500;

    const goToSlide = (index) => {
      slides.forEach((s, i) => {
        s.classList.toggle('active', i === index);
      });
      dots.forEach((d, i) => {
        d.classList.toggle('active', i === index);
      });
      current = index;
    };

    const nextSlide = () => {
      let next = (current + 1) % slides.length;
      goToSlide(next);
    };

    const prevSlide = () => {
      let prev = (current - 1 + slides.length) % slides.length;
      goToSlide(prev);
    };

    const startTimer = () => {
      stopTimer();
      timer = setInterval(nextSlide, intervalTime);
    };

    const stopTimer = () => {
      if (timer) clearInterval(timer);
    };

    if (nextBtn) nextBtn.addEventListener('click', () => { nextSlide(); startTimer(); });
    if (prevBtn) prevBtn.addEventListener('click', () => { prevSlide(); startTimer(); });

    dots.forEach((dot, idx) => {
      dot.addEventListener('click', () => {
        goToSlide(idx);
        startTimer();
      });
    });

    const heroSection = document.getElementById('heroSection');
    if (heroSection) {
      heroSection.addEventListener('mouseenter', stopTimer);
      heroSection.addEventListener('mouseleave', startTimer);
    }

    startTimer();
  },

  /* ==================== STAT COUNTERS ==================== */
  initCounterAnimation() {
    const counters = document.querySelectorAll('.metric-number[data-target]');
    if (!counters.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const target = +entry.target.getAttribute('data-target');
          const duration = 1800; // ms
          const stepTime = 25;
          const steps = duration / stepTime;
          const increment = target / steps;
          let currentVal = 0;

          const timer = setInterval(() => {
            currentVal += increment;
            if (currentVal >= target) {
              entry.target.textContent = Number(target).toLocaleString();
              clearInterval(timer);
            } else {
              entry.target.textContent = Math.floor(currentVal).toLocaleString();
            }
          }, stepTime);

          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    counters.forEach(c => observer.observe(c));
  },

  /* ==================== MOBILE DRAWER ==================== */
  initMobileDrawer() {
    const openBtn = document.getElementById('mobileMenuToggle');
    const closeBtn = document.getElementById('closeMobileDrawer');
    const drawer = document.getElementById('mobileNavDrawer');
    const drawerLinks = document.querySelectorAll('.drawer-link');

    const toggle = (show) => {
      drawer?.classList.toggle('active', show);
      document.body.style.overflow = show ? 'hidden' : '';
    };

    if (openBtn) openBtn.addEventListener('click', () => toggle(true));
    if (closeBtn) closeBtn.addEventListener('click', () => toggle(false));
    if (drawer) {
      drawer.addEventListener('click', (e) => {
        if (e.target === drawer) toggle(false);
      });
    }

    drawerLinks.forEach(l => l.addEventListener('click', () => toggle(false)));
  },

  /* ==================== GLOBAL SEARCH ==================== */
  initSearchModal() {
    const triggerBtn = document.getElementById('searchTriggerBtn');
    const modal = document.getElementById('searchModal');
    const closeBtn = document.getElementById('closeSearchModal');
    const input = document.getElementById('globalSearchInput');
    const resultsContainer = document.getElementById('searchResultsContainer');

    const toggleSearch = (show) => {
      modal?.classList.toggle('active', show);
      if (show) {
        setTimeout(() => input?.focus(), 150);
      } else {
        if (input) input.value = '';
        if (resultsContainer) resultsContainer.innerHTML = '';
      }
    };

    if (triggerBtn) triggerBtn.addEventListener('click', () => toggleSearch(true));
    if (closeBtn) closeBtn.addEventListener('click', () => toggleSearch(false));
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) toggleSearch(false);
      });
    }

    // Keyboard shortcut Ctrl+K or Cmd+K
    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        toggleSearch(true);
      }
      if (e.key === 'Escape') toggleSearch(false);
    });

    if (input) {
      input.addEventListener('input', (e) => {
        const query = e.target.value.trim().toLowerCase();
        if (!query) {
          resultsContainer.innerHTML = '<p style="color: var(--text-muted); font-size: 0.9rem; text-align: center; padding: 20px;">Type keywords like "Refinery", "Cement", "Dividend", or "Jobs"...</p>';
          return;
        }

        const hits = [];
        // Search in businesses
        this.allBusinesses.forEach(b => {
          if (b.name.toLowerCase().includes(query) || b.tagline.toLowerCase().includes(query) || b.description.toLowerCase().includes(query)) {
            hits.push({ type: 'Subsidiary', title: b.name, desc: b.tagline, action: () => { toggleSearch(false); openBusinessModal(b.id); } });
          }
        });
        // Search in news
        this.allNews.forEach(n => {
          if (n.title.toLowerCase().includes(query) || n.summary.toLowerCase().includes(query)) {
            hits.push({ type: 'News & Media', title: n.title, desc: n.date, action: () => { toggleSearch(false); openNewsModal(n.id); } });
          }
        });
        // Search in careers
        this.allCareers.forEach(c => {
          if (c.title.toLowerCase().includes(query) || c.department.toLowerCase().includes(query)) {
            hits.push({ type: 'Careers', title: c.title, desc: `${c.department} • ${c.location}`, action: () => { toggleSearch(false); openApplyModal(c.id, c.title); } });
          }
        });

        if (hits.length === 0) {
          resultsContainer.innerHTML = `<p style="color: var(--text-muted); font-size: 0.9rem; text-align: center; padding: 20px;">No matches found for "${query}". Try "Refinery" or "Cement".</p>`;
          return;
        }

        let html = '';
        hits.slice(0, 8).forEach((hit, idx) => {
          html += `
            <div class="search-result-item" onclick="App.runSearchHit(${idx})">
              <span class="search-item-cat">${hit.type}</span>
              <span class="search-item-title">${hit.title}</span>
              <span style="font-size: 0.8rem; color: var(--text-muted);">${hit.desc}</span>
            </div>
          `;
        });
        this.currentSearchHits = hits;
        resultsContainer.innerHTML = html;
      });
    }
  },

  runSearchHit(idx) {
    if (this.currentSearchHits && this.currentSearchHits[idx]) {
      this.currentSearchHits[idx].action();
    }
  },

  /* ==================== LOAD BUSINESSES ==================== */
  async loadBusinesses(category = 'All') {
    this.allBusinesses = await window.API.getBusinesses();
    this.renderBusinesses(category);
    this.setupBusinessTabs();
  },

  setupBusinessTabs() {
    const tabs = document.querySelectorAll('.filter-tab-btn');
    tabs.forEach(tab => {
      tab.addEventListener('click', (e) => {
        tabs.forEach(t => t.classList.remove('active'));
        e.target.classList.add('active');
        const cat = e.target.getAttribute('data-cat');
        this.renderBusinesses(cat);
      });
    });
  },

  renderBusinesses(category = 'All') {
    const grid = document.getElementById('businessesGrid');
    if (!grid) return;

    const filtered = category === 'All'
      ? this.allBusinesses
      : this.allBusinesses.filter(b => b.category.toLowerCase().includes(category.toLowerCase()));

    let html = '';
    filtered.forEach(b => {
      html += `
        <div class="business-card">
          <div class="business-card-img-wrap">
            <img src="${b.image}" alt="${b.name}" class="business-card-img" />
            <span class="card-category-badge">${b.category}</span>
          </div>
          <div class="business-card-body">
            <div class="card-stat-pill">
              <span>⚡</span> ${b.capacity}
            </div>
            <h3 class="business-card-title">${b.name}</h3>
            <p class="business-card-desc">${b.description}</p>
            <div class="card-highlights-list">
              ${b.highlights.slice(0, 2).map(h => `<div class="card-highlight-item"><i>✓</i> ${h}</div>`).join('')}
            </div>
            <div class="card-footer-action">
              <button class="card-cta-btn" onclick="openBusinessModal('${b.id}')">
                <span>Explore Technical Profile</span>
                <span>→</span>
              </button>
            </div>
          </div>
        </div>
      `;
    });

    grid.innerHTML = html;
  },

  /* ==================== LOAD NEWS ==================== */
  async loadNews() {
    this.allNews = await window.API.getNews();
    const grid = document.getElementById('newsGrid');
    if (!grid) return;

    let html = '';
    this.allNews.forEach(n => {
      html += `
        <div class="news-card" onclick="openNewsModal('${n.id}')">
          <div class="news-meta-row">
            <span class="badge badge-red">${n.category}</span>
            <span class="news-date">${n.date}</span>
          </div>
          <h4 class="news-card-title">${n.title}</h4>
          <p class="news-card-summary">${n.summary}</p>
          <div class="news-card-footer">
            <span>Read Article</span>
            <span>${n.readTime} →</span>
          </div>
        </div>
      `;
    });
    grid.innerHTML = html;
  },

  /* ==================== LOAD CAREERS ==================== */
  async loadCareers() {
    this.allCareers = await window.API.getCareers();
    const grid = document.getElementById('jobsGrid');
    if (!grid) return;

    let html = '';
    this.allCareers.forEach(job => {
      html += `
        <div class="job-card">
          <span class="job-dept-badge">${job.department}</span>
          <h3 class="job-title">${job.title}</h3>
          <div class="job-pills-row">
            <span>📍 ${job.location}</span>
            <span>💼 ${job.type}</span>
            <span>⭐ ${job.experience}</span>
          </div>
          <p class="job-desc">${job.description}</p>
          <div class="job-footer">
            <span style="font-size: 0.8rem; color: var(--text-muted);">Ref ID: ${job.id.toUpperCase()}</span>
            <button class="btn btn-primary btn-sm" onclick="openApplyModal('${job.id}', '${job.title.replace(/'/g, "\\'")}')">
              Apply Now
            </button>
          </div>
        </div>
      `;
    });
    grid.innerHTML = html;
  },

  /* ==================== CONTACT FORM ==================== */
  initContactForm() {
    const form = document.getElementById('corporateContactForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting Inquiries...';
      }

      const payload = {
        fullName: document.getElementById('contactFullName')?.value,
        email: document.getElementById('contactEmail')?.value,
        phone: document.getElementById('contactPhone')?.value || '',
        inquiryType: document.getElementById('contactInquiryType')?.value,
        subsidiary: document.getElementById('contactSubsidiary')?.value || 'Dangote Industries Limited',
        subject: document.getElementById('contactSubject')?.value,
        message: document.getElementById('contactMessage')?.value
      };

      try {
        const res = await window.API.submitContact(payload);
        showToast('Inquiry Dispatched', `${res.message} (Reference: ${res.referenceNumber})`, 'success');
        form.reset();
      } catch (err) {
        showToast('Submission Error', 'Failed to dispatch inquiry. Please check your network and try again.', 'error');
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Send Corporate Inquiry';
        }
      }
    });
  },

  /* ==================== ETHICS HOTLINE ==================== */
  initEthicsModal() {
    const openBtn = document.getElementById('openEthicsModalBtn');
    const closeBtn = document.getElementById('closeEthicsModal');
    const modal = document.getElementById('ethicsModal');
    const form = document.getElementById('ethicsForm');

    const toggle = (show) => modal?.classList.toggle('active', show);

    if (openBtn) openBtn.addEventListener('click', () => toggle(true));
    if (closeBtn) closeBtn.addEventListener('click', () => toggle(false));
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) toggle(false);
      });
    }

    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
          reportType: document.getElementById('ethicsType')?.value,
          subsidiary: document.getElementById('ethicsSubsidiary')?.value,
          location: document.getElementById('ethicsLocation')?.value,
          details: document.getElementById('ethicsDetails')?.value,
          anonymous: document.getElementById('ethicsAnonymous')?.checked ?? true,
          reporterContact: document.getElementById('ethicsContact')?.value || ''
        };

        try {
          const res = await window.API.submitEthics(payload);
          toggle(false);
          form.reset();
          showToast('Confidential Report Received', `${res.message} Ticket: ${res.trackingTicket}`, 'success');
        } catch (err) {
          showToast('Submission Failed', 'Could not transmit encrypted report.', 'error');
        }
      });
    }
  },

  /* ==================== BRANCH DIRECTORY TABS ==================== */
  initBranchTabs() {
    const tabs = document.querySelectorAll('.branch-tab-btn');
    const branches = {
      lagos: {
        name: "Global Headquarters (Leadway Marble House)",
        address: "1 Alfred Rewane Road (formerly Kingsway Road), Falomo, Ikoyi, Lagos, Nigeria",
        phone: "+234 1 448 0815 / +234 1 448 0816",
        email: "corporate.affairs@dangote.com",
        hours: "Monday - Friday: 8:00 AM - 5:30 PM (WAT)"
      },
      abuja: {
        name: "Abuja Corporate & Government Liaison Office",
        address: "Dangote House, 3 Gimbiya Street, Area 11, Garki, Abuja, FCT, Nigeria",
        phone: "+234 9 234 5678",
        email: "abuja.liaison@dangote.com",
        hours: "Monday - Friday: 8:00 AM - 5:00 PM (WAT)"
      },
      lekki: {
        name: "Dangote Petroleum Refinery & Petrochemicals Complex",
        address: "Lekki Free Trade Zone, Ibeju-Lekki, Lagos State, Nigeria",
        phone: "+234 1 890 1234",
        email: "refinery.operations@dangote.com",
        hours: "24/7 Continuous Operational Facility"
      },
      london: {
        name: "Dangote Global Investments (UK)",
        address: "15 Berkeley Street, Mayfair, London W1J 8DY, United Kingdom",
        phone: "+44 20 7499 8888",
        email: "london.office@dangote.com",
        hours: "Monday - Friday: 9:00 AM - 5:30 PM (GMT)"
      },
      southafrica: {
        name: "Dangote Southern Africa Regional Hub (Sephaku)",
        address: "Southdowns Office Park, Karee Street, Centurion, Pretoria, South Africa",
        phone: "+27 12 612 0000",
        email: "southernafrica@dangote.com",
        hours: "Monday - Friday: 8:00 AM - 5:00 PM (SAST)"
      }
    };

    tabs.forEach(tab => {
      tab.addEventListener('click', (e) => {
        tabs.forEach(t => t.classList.remove('active'));
        e.target.classList.add('active');
        const key = e.target.getAttribute('data-branch');
        const data = branches[key];
        if (!data) return;

        document.getElementById('branchName').textContent = data.name;
        document.getElementById('branchAddress').textContent = data.address;
        document.getElementById('branchPhone').textContent = data.phone;
        document.getElementById('branchEmail').textContent = data.email;
        document.getElementById('branchHours').textContent = data.hours;
      });
    });
  }
};

/* ==================== GLOBAL HELPER MODAL OPENERS ==================== */

function openBusinessModal(bizId) {
  const biz = App.allBusinesses.find(b => b.id === bizId);
  if (!biz) return;

  const modal = document.getElementById('detailModal');
  const modalTitle = document.getElementById('detailModalTitle');
  const modalBody = document.getElementById('detailModalBody');

  modalTitle.textContent = biz.name;
  modalBody.innerHTML = `
    <div style="margin-bottom: 20px;">
      <img src="${biz.image}" alt="${biz.name}" style="width: 100%; height: 260px; object-fit: cover; border-radius: var(--radius-md); margin-bottom: 16px;" />
      <span class="badge badge-red" style="margin-bottom: 10px;">${biz.category}</span>
      <h4 style="font-size: 1.15rem; margin-top: 8px; margin-bottom: 12px; color: var(--dangote-navy);">${biz.tagline}</h4>
      <p style="color: var(--text-secondary); line-height: 1.7; margin-bottom: 20px;">${biz.description}</p>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
      <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--surface-border);">
        <strong style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); display: block;">Installed Capacity</strong>
        <span style="font-size: 1.1rem; font-weight: 700; color: var(--dangote-navy);">${biz.capacity}</span>
      </div>
      <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--surface-border);">
        <strong style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); display: block;">Capital Investment</strong>
        <span style="font-size: 1.1rem; font-weight: 700; color: var(--dangote-red);">${biz.investment}</span>
      </div>
    </div>

    <div style="margin-bottom: 24px;">
      <h5 style="font-size: 1rem; margin-bottom: 10px; font-weight: 700;">Key Commercial Products</h5>
      <ul style="display: flex; flex-wrap: wrap; gap: 8px;">
        ${biz.keyProducts.map(p => `<li style="background: var(--bg-secondary); border: 1px solid var(--surface-border); padding: 6px 12px; border-radius: var(--radius-full); font-size: 0.85rem; font-weight: 600;">${p}</li>`).join('')}
      </ul>
    </div>

    <div>
      <h5 style="font-size: 1rem; margin-bottom: 10px; font-weight: 700;">Operational Distinctions</h5>
      <ul style="display: flex; flex-direction: column; gap: 8px;">
        ${biz.highlights.map(h => `<li style="font-size: 0.9rem; color: var(--text-secondary); display: flex; align-items: center; gap: 8px;"><span style="color: var(--dangote-green);">✔</span> ${h}</li>`).join('')}
      </ul>
    </div>
  `;

  modal.classList.add('active');
}

function openNewsModal(newsId) {
  const news = App.allNews.find(n => n.id === newsId);
  if (!news) return;

  const modal = document.getElementById('detailModal');
  const modalTitle = document.getElementById('detailModalTitle');
  const modalBody = document.getElementById('detailModalBody');

  modalTitle.textContent = news.title;
  modalBody.innerHTML = `
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 18px;">
      <span class="badge badge-red">${news.category}</span>
      <span style="color: var(--text-muted); font-size: 0.85rem;">${news.date}</span>
      <span style="color: var(--text-muted); font-size: 0.85rem;">• ${news.readTime}</span>
    </div>
    <div style="border-left: 3px solid var(--dangote-red); padding-left: 16px; margin-bottom: 20px;">
      <p style="font-size: 1.05rem; font-weight: 600; color: var(--text-primary); line-height: 1.6;">${news.summary}</p>
    </div>
    <div style="font-size: 0.95rem; color: var(--text-secondary); line-height: 1.8;">
      <p style="margin-bottom: 16px;">${news.content}</p>
      <p>For additional media inquiries, investor statements, or high-resolution press collateral, please contact the Dangote Group Corporate Communications Directorate via <a href="mailto:media@dangote.com" style="color: var(--dangote-red); font-weight: 700;">media@dangote.com</a>.</p>
    </div>
  `;

  modal.classList.add('active');
}

function openStockModal(symbol) {
  const modal = document.getElementById('detailModal');
  const modalTitle = document.getElementById('detailModalTitle');
  const modalBody = document.getElementById('detailModalBody');

  const stockNames = {
    "DANGCEM": "Dangote Cement Plc",
    "DANGSUGAR": "Dangote Sugar Refinery Plc",
    "NASCON": "NASCON Allied Industries Plc"
  };

  modalTitle.textContent = `${stockNames[symbol] || symbol} (NGX: ${symbol})`;
  modalBody.innerHTML = `
    <div style="padding: 10px 0;">
      <p style="color: var(--text-secondary); margin-bottom: 20px;">
        Listed on the Nigerian Exchange Limited (NGX). Live trading parameters and investor fundamentals.
      </p>
      <div style="background: var(--bg-secondary); border: 1px solid var(--surface-border); border-radius: var(--radius-md); padding: 20px; text-align: center; margin-bottom: 24px;">
        <span style="font-size: 0.85rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Simulate Shares & Dividend</span>
        <div style="margin-top: 14px;">
          <a href="#investors" onclick="closeDetailModal();" class="btn btn-primary btn-sm">Open Dividend Calculator</a>
        </div>
      </div>
    </div>
  `;

  modal.classList.add('active');
}

function openApplyModal(jobId, jobTitle) {
  const modal = document.getElementById('applyJobModal');
  const modalTitle = document.getElementById('applyJobTitle');
  const jobIdInput = document.getElementById('applyJobIdInput');

  if (modalTitle) modalTitle.textContent = `Apply for ${jobTitle}`;
  if (jobIdInput) jobIdInput.value = jobId;
  modal?.classList.add('active');
}

function closeApplyModal() {
  document.getElementById('applyJobModal')?.classList.remove('active');
}

function closeDetailModal() {
  document.getElementById('detailModal')?.classList.remove('active');
}

// Bind Career Apply Form Submit
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('jobApplicationForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Submitting Application...';
    }

    const payload = {
      fullName: document.getElementById('applicantName')?.value,
      email: document.getElementById('applicantEmail')?.value,
      phone: document.getElementById('applicantPhone')?.value,
      jobId: document.getElementById('applyJobIdInput')?.value || 'GEN',
      jobTitle: document.getElementById('applyJobTitle')?.textContent?.replace('Apply for ', '') || 'Corporate Role',
      experienceYears: parseInt(document.getElementById('applicantExp')?.value || '3', 10),
      qualification: document.getElementById('applicantQualification')?.value,
      linkedinUrl: document.getElementById('applicantLinkedin')?.value || '',
      coverNote: document.getElementById('applicantCover')?.value || ''
    };

    try {
      const res = await window.API.submitApplication(payload);
      closeApplyModal();
      form.reset();
      showToast('Application Submitted!', res.message, 'success');
    } catch (err) {
      showToast('Error', 'Unable to upload application credentials.', 'error');
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.textContent = 'Submit Formal Application';
      }
    }
  });

  // Modal backdrop click handlers
  document.getElementById('detailModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'detailModal') closeDetailModal();
  });
  document.getElementById('applyJobModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'applyJobModal') closeApplyModal();
  });
});

/* ==================== TOAST NOTIFICATION DISPATCHER ==================== */

function showToast(title, message, type = 'success') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  const icon = type === 'success' ? '✔' : '⚠';
  const iconColor = type === 'success' ? 'var(--dangote-green)' : '#EF4444';

  toast.innerHTML = `
    <div class="toast-icon" style="color: ${iconColor}">${icon}</div>
    <div class="toast-content">
      <h6>${title}</h6>
      <p>${message}</p>
    </div>
  `;

  container.appendChild(toast);

  // Trigger animation
  setTimeout(() => toast.classList.add('show'), 10);

  // Auto remove after 5s
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 400);
  }, 5000);
}

window.App = App;
window.showToast = showToast;
window.openBusinessModal = openBusinessModal;
window.openNewsModal = openNewsModal;
window.openStockModal = openStockModal;
window.openApplyModal = openApplyModal;
window.closeApplyModal = closeApplyModal;
window.closeDetailModal = closeDetailModal;
