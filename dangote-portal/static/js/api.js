/**
 * Dangote Group Portal - API Client Module
 */

const API = {
  baseUrl: window.location.origin,

  async getStocks() {
    try {
      const res = await fetch(`${this.baseUrl}/api/stocks`);
      if (!res.ok) throw new Error("Stocks fetch error");
      return await res.json();
    } catch (e) {
      console.warn("Using fallback stock data", e);
      return null;
    }
  },

  async getBusinesses(category = null) {
    try {
      const url = category && category !== 'All' 
        ? `${this.baseUrl}/api/businesses?category=${encodeURIComponent(category)}`
        : `${this.baseUrl}/api/businesses`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("Businesses fetch error");
      return await res.json();
    } catch (e) {
      console.warn("Businesses fetch failed", e);
      return [];
    }
  },

  async getCountries() {
    try {
      const res = await fetch(`${this.baseUrl}/api/countries`);
      if (!res.ok) throw new Error("Countries fetch error");
      return await res.json();
    } catch (e) {
      console.warn("Countries fetch failed", e);
      return [];
    }
  },

  async getGovernance() {
    try {
      const res = await fetch(`${this.baseUrl}/api/governance`);
      if (!res.ok) throw new Error("Governance fetch error");
      return await res.json();
    } catch (e) {
      console.warn("Governance fetch failed", e);
      return [];
    }
  },

  async getNews(category = null, q = null) {
    try {
      let url = `${this.baseUrl}/api/news?`;
      if (category && category !== 'All') url += `category=${encodeURIComponent(category)}&`;
      if (q) url += `q=${encodeURIComponent(q)}&`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("News fetch error");
      return await res.json();
    } catch (e) {
      console.warn("News fetch failed", e);
      return [];
    }
  },

  async getCareers(department = null) {
    try {
      const url = department && department !== 'All' 
        ? `${this.baseUrl}/api/careers?department=${encodeURIComponent(department)}`
        : `${this.baseUrl}/api/careers`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("Careers fetch error");
      return await res.json();
    } catch (e) {
      console.warn("Careers fetch failed", e);
      return [];
    }
  },

  async submitContact(data) {
    const res = await fetch(`${this.baseUrl}/api/contact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Contact submission failed");
    return await res.json();
  },

  async submitApplication(data) {
    const res = await fetch(`${this.baseUrl}/api/careers/apply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Job application submission failed");
    return await res.json();
  },

  async submitEthics(data) {
    const res = await fetch(`${this.baseUrl}/api/ethics`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Ethics report submission failed");
    return await res.json();
  },

  async calculateDividend(data) {
    const res = await fetch(`${this.baseUrl}/api/calculator`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Calculator calculation failed");
    return await res.json();
  }
};

window.API = API;
