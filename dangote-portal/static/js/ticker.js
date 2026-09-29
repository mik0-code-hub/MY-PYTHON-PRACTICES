/**
 * Dangote Group Portal - Live NGX Stock Ticker
 */

const StockTicker = {
  containerId: 'stockTickerTrack',
  pollInterval: 8000,
  previousPrices: {},

  init() {
    this.update();
    setInterval(() => this.update(), this.pollInterval);
  },

  async update() {
    const data = await window.API.getStocks();
    if (!data) return;

    const track = document.getElementById(this.containerId);
    if (!track) return;

    const liveTag = document.querySelector('.ticker-live-tag');
    let firstStock = null;
    let html = '';

    for (const key in data) {
      const stock = data[key];
      if (!firstStock) firstStock = stock;

      const isNeutral = Math.abs(stock.change) < 0.001;
      const isUp = stock.change > 0;
      const changeClass = isNeutral ? 'stock-neutral' : (isUp ? 'stock-up' : 'stock-down');
      const changeArrow = isNeutral ? '●' : (isUp ? '▲' : '▼');
      const sign = isUp ? '+' : '';

      // Check if price changed since last update for flash animation
      const prevPrice = this.previousPrices[key];
      const flashClass = prevPrice && prevPrice !== stock.price ? 'price-flash' : '';
      this.previousPrices[key] = stock.price;

      html += `
        <div class="stock-quote-item ${flashClass}" onclick="openStockModal('${key}')" title="Click for ${stock.name} detailed profile (NGX: ${stock.symbol})">
          <span class="stock-symbol">${stock.symbol}</span>
          <span class="stock-val">₦${stock.price.toFixed(2)}</span>
          <span class="${changeClass}">${changeArrow} ${sign}${stock.change.toFixed(2)} (${sign}${stock.changePercent.toFixed(2)}%)</span>
          <span style="color: rgba(255,255,255,0.3); margin-left: 6px;">|</span>
        </div>
      `;
    }

    track.innerHTML = html;

    // Dynamically calculate and update combined market cap and dividend in Investor Relations
    let totalMcap = 0;
    for (const key in data) {
      if (data[key].rawMarketCap) {
        totalMcap += data[key].rawMarketCap;
      }
    }
    const capEl = document.getElementById('invCombinedMarketCap');
    if (capEl && totalMcap > 0) {
      capEl.textContent = `₦${(totalMcap / 1e12).toFixed(2)}T`;
    }
    const divEl = document.getElementById('invCementDividend');
    if (divEl && data.DANGCEM && data.DANGCEM.latestDividend) {
      divEl.textContent = `₦${data.DANGCEM.latestDividend.toFixed(2)}`;
    }

    // Decoupled Market Session & Provider Status Tag
    if (liveTag && firstStock) {
      const isMarketOpen = firstStock.isMarketOpen;
      const providerHealthy = firstStock.providerHealthy !== false;
      const timeWAT = firstStock.lastUpdatedWAT || firstStock.lastUpdated || '';
      const sessionDesc = firstStock.sessionDescription || 'Official NGX Trading Schedule (09:00 - 16:00 WAT)';

      if (isMarketOpen) {
        if (providerHealthy) {
          liveTag.className = 'ticker-live-tag tag-open';
          const badgeLabel = firstStock.marketStatus || 'LIVE NGX (15m Delay)';
          liveTag.innerHTML = `<span class="pulse-dot"></span> ${badgeLabel}`;
          liveTag.title = `${sessionDesc}. Last update: ${timeWAT}. Quotes provided with official 15-minute exchange delay.`;
        } else {
          liveTag.className = 'ticker-live-tag tag-warning';
          liveTag.innerHTML = '<span class="pulse-dot"></span> NGX OPEN (Data Delay)';
          liveTag.title = `Nigerian Exchange is open, but market data feed is temporarily delayed/unavailable. Showing last verified closing quotes.`;
        }
      } else {
        liveTag.className = 'ticker-live-tag tag-closed';
        liveTag.innerHTML = '<span class="pulse-dot"></span> NGX CLOSED';
        liveTag.title = `Nigerian Exchange is closed (${sessionDesc}). Displaying official closing prices.`;
      }
    }
  }
};

window.StockTicker = StockTicker;
