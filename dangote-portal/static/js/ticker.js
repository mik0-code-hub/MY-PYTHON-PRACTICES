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

    let html = '';
    for (const key in data) {
      const stock = data[key];
      const isUp = stock.change >= 0;
      const changeClass = isUp ? 'stock-up' : 'stock-down';
      const changeArrow = isUp ? '▲' : '▼';
      const sign = isUp ? '+' : '';

      // Check if price changed since last update for flash animation
      const prevPrice = this.previousPrices[key];
      const flashClass = prevPrice && prevPrice !== stock.price ? 'price-flash' : '';
      this.previousPrices[key] = stock.price;

      html += `
        <div class="stock-quote-item ${flashClass}" onclick="openStockModal('${key}')" title="Click for ${stock.name} detailed profile">
          <span class="stock-symbol">${stock.symbol}</span>
          <span class="stock-val">₦${stock.price.toFixed(2)}</span>
          <span class="${changeClass}">${changeArrow} ${sign}${stock.change.toFixed(2)} (${sign}${stock.changePercent.toFixed(2)}%)</span>
          <span style="color: rgba(255,255,255,0.3); margin-left: 6px;">|</span>
        </div>
      `;
    }

    track.innerHTML = html;
  }
};

window.StockTicker = StockTicker;
