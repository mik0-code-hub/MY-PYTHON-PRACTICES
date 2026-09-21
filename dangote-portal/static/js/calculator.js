/**
 * Dangote Group Portal - Shareholder Dividend & ROI Calculator
 */

const DividendCalculator = {
  defaultPrices: {
    "DANGCEM": 1050.00,
    "DANGSUGAR": 70.50,
    "NASCON": 176.00
  },

  async init() {
    const subSelect = document.getElementById('calcSubsidiary');
    const slider = document.getElementById('calcSharesSlider');
    const input = document.getElementById('calcSharesInput');
    const priceInput = document.getElementById('calcPurchasePrice');

    // Dynamically synchronize calculator with live NGX stock quotes
    try {
      const liveStocks = await window.API.getStocks();
      if (liveStocks) {
        for (const sym in liveStocks) {
          if (liveStocks[sym] && liveStocks[sym].price) {
            this.defaultPrices[sym] = liveStocks[sym].price;
          }
        }
        // Update select option labels with real-time live market prices
        if (subSelect) {
          const optDangcem = subSelect.querySelector('option[value="DANGCEM"]');
          const optSugar = subSelect.querySelector('option[value="DANGSUGAR"]');
          const optNascon = subSelect.querySelector('option[value="NASCON"]');
          if (optDangcem) optDangcem.textContent = `Dangote Cement Plc (DANGCEM - ₦${this.defaultPrices.DANGCEM.toFixed(2)})`;
          if (optSugar) optSugar.textContent = `Dangote Sugar Refinery Plc (DANGSUGAR - ₦${this.defaultPrices.DANGSUGAR.toFixed(2)})`;
          if (optNascon) optNascon.textContent = `NASCON Allied Industries Plc (NASCON - ₦${this.defaultPrices.NASCON.toFixed(2)})`;
        }
        if (priceInput && subSelect && this.defaultPrices[subSelect.value]) {
          priceInput.value = (this.defaultPrices[subSelect.value] * 0.85).toFixed(2);
        }
      }
    } catch (err) {
      console.warn('Could not sync calculator with live stocks', err);
    }

    if (slider && input) {
      slider.addEventListener('input', (e) => {
        input.value = e.target.value;
        this.recalculate();
      });

      input.addEventListener('input', (e) => {
        slider.value = e.target.value;
        this.recalculate();
      });
    }

    if (subSelect) {
      subSelect.addEventListener('change', (e) => {
        const symbol = e.target.value;
        if (priceInput && this.defaultPrices[symbol]) {
          priceInput.value = (this.defaultPrices[symbol] * 0.85).toFixed(2);
        }
        this.recalculate();
      });
    }

    if (priceInput) {
      priceInput.addEventListener('input', () => this.recalculate());
    }

    this.recalculate();
  },

  async recalculate() {
    const subsidiary = document.getElementById('calcSubsidiary')?.value || 'DANGCEM';
    const sharesCount = parseInt(document.getElementById('calcSharesInput')?.value || '5000', 10);
    const purchasePrice = parseFloat(document.getElementById('calcPurchasePrice')?.value || '550');

    if (isNaN(sharesCount) || isNaN(purchasePrice) || sharesCount <= 0 || purchasePrice <= 0) return;

    try {
      const result = await window.API.calculateDividend({
        subsidiary,
        sharesCount,
        purchasePrice
      });

      if (!result) return;

      // Update UI elements
      const formatNGN = (val) => '₦' + Number(val).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

      const marketValEl = document.getElementById('calcCurrentMarketVal');
      const capitalGainEl = document.getElementById('calcCapitalGain');
      const annualDivEl = document.getElementById('calcAnnualDividend');
      const yieldEl = document.getElementById('calcEffectiveYield');

      if (marketValEl) marketValEl.textContent = formatNGN(result.currentMarketValue);
      if (capitalGainEl) {
        const sign = result.capitalGain >= 0 ? '+' : '';
        capitalGainEl.textContent = `${sign}${formatNGN(result.capitalGain)} (${sign}${result.capitalGainPercent}%)`;
        capitalGainEl.style.color = result.capitalGain >= 0 ? 'var(--dangote-green)' : '#EF4444';
      }
      if (annualDivEl) annualDivEl.textContent = formatNGN(result.annualDividendIncome);
      if (yieldEl) yieldEl.textContent = `${result.effectiveYield}% p.a.`;

    } catch (e) {
      console.warn("Recalculate error", e);
    }
  }
};

window.DividendCalculator = DividendCalculator;
