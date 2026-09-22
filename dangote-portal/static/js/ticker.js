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

    // Dynamically update the live ticker tag to reflect actual NGX trading session
    if (liveTag && firstStock) {
      if (firstStock.isMarketOpen) {
        liveTag.innerHTML = '<span class="pulse-dot"></span> LIVE NGX';
        liveTag.title = 'Nigerian Exchange Regular Trading Session Active (10:00 - 14:30 WAT)';
      } else {
        liveTag.innerHTML = '<span class="pulse-dot" style="background: #94a3b8; box-shadow: none;"></span> NGX CLOSED';
        liveTag.title = 'Nigerian Exchange is currently closed (Trading hours: Mon-Fri 10:00 - 14:30 WAT). Showing official closing quotes.';
      }
    }
  }
};

window.StockTicker = StockTicker;
