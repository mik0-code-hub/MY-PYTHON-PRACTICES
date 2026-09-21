/**
 * Dangote Group Portal - Interactive Pan-African Footprint Visualizer
 */

const AfricaMap = {
  countries: [],
  activeCountry: null,

  async init() {
    this.countries = await window.API.getCountries();
    this.renderMarkers();
    this.renderPills();
    if (this.countries.length > 0) {
      this.selectCountry(this.countries[0].country);
    }
  },

  renderMarkers() {
    const container = document.getElementById('mapMarkersContainer');
    if (!container) return;

    let markersHtml = '';
    this.countries.forEach(c => {
      markersHtml += `
        <div class="map-marker" id="marker-${c.country}" style="left: ${c.coords.x}%; top: ${c.coords.y}%;" onclick="AfricaMap.selectCountry('${c.country}')">
          <div class="marker-ring"></div>
          <div class="marker-dot"></div>
          <div class="marker-tooltip">${c.flag} ${c.country}</div>
        </div>
      `;
    });
    container.innerHTML = markersHtml;
  },

  renderPills() {
    const container = document.getElementById('countryPillsContainer');
    if (!container) return;

    let pillsHtml = '';
    this.countries.forEach(c => {
      pillsHtml += `
        <button class="country-pill-btn" id="pill-${c.country}" onclick="AfricaMap.selectCountry('${c.country}')">
          ${c.flag} ${c.country}
        </button>
      `;
    });
    container.innerHTML = pillsHtml;
  },

  selectCountry(countryName) {
    const country = this.countries.find(c => c.country.toLowerCase() === countryName.toLowerCase());
    if (!country) return;
    this.activeCountry = country;

    // Update markers active state
    document.querySelectorAll('.map-marker').forEach(m => m.classList.remove('active'));
    const activeMarker = document.getElementById(`marker-${country.country}`);
    if (activeMarker) activeMarker.classList.add('active');

    // Update pills active state
    document.querySelectorAll('.country-pill-btn').forEach(p => p.classList.remove('active'));
    const activePill = document.getElementById(`pill-${country.country}`);
    if (activePill) {
      activePill.classList.add('active');
      activePill.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }

    // Update details card
    const flagEl = document.getElementById('activeCountryFlag');
    const titleEl = document.getElementById('activeCountryName');
    const roleEl = document.getElementById('activeCountryRole');
    const facilitiesEl = document.getElementById('activeCountryFacilities');
    const employeesEl = document.getElementById('activeCountryEmployees');
    const statusEl = document.getElementById('activeCountryStatus');
    const cardEl = document.querySelector('.country-active-card');

    if (flagEl) flagEl.textContent = country.flag;
    if (titleEl) titleEl.textContent = country.country;
    if (roleEl) roleEl.textContent = country.role;
    if (facilitiesEl) facilitiesEl.textContent = country.facilities;
    if (employeesEl) employeesEl.textContent = country.employees;
    if (statusEl) statusEl.textContent = country.status;

    if (cardEl) {
      cardEl.style.transition = 'none';
      cardEl.style.opacity = '0.7';
      cardEl.style.transform = 'translateY(3px)';
      requestAnimationFrame(() => {
        cardEl.style.transition = 'all 0.3s ease';
        cardEl.style.opacity = '1';
        cardEl.style.transform = 'translateY(0)';
      });
    }
  }
};

window.AfricaMap = AfricaMap;
