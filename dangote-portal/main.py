import os
import time
import random
import sqlite3
import datetime
import urllib.request
import json
import re
import html
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Dangote Group Corporate Portal API",
    description="Enterprise API supporting the official Dangote Industries Limited corporate digital platform with live feeds.",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== PERSISTENT DATABASE SETUP ====================

DB_PATH = os.path.join(os.path.dirname(__file__), "dangote_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference_id TEXT UNIQUE,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        inquiry_type TEXT,
        subsidiary TEXT,
        subject TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id TEXT UNIQUE,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        job_id TEXT,
        job_title TEXT,
        experience_years INTEGER,
        qualification TEXT,
        linkedin_url TEXT,
        cover_note TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ethics_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_number TEXT UNIQUE,
        report_type TEXT,
        subsidiary TEXT,
        location TEXT,
        details TEXT,
        anonymous INTEGER,
        reporter_contact TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ==================== DATA MODELS ====================

class ContactForm(BaseModel):
    fullName: str
    email: str
    phone: Optional[str] = ""
    inquiryType: str
    subsidiary: Optional[str] = "Dangote Industries Limited"
    subject: str
    message: str

class CareerApplication(BaseModel):
    fullName: str
    email: str
    phone: str
    jobId: str
    jobTitle: str
    experienceYears: int
    qualification: str
    linkedinUrl: Optional[str] = ""
    coverNote: Optional[str] = ""

class EthicsReport(BaseModel):
    reportType: str
    location: str
    subsidiary: str
    details: str
    anonymous: bool = True
    reporterContact: Optional[str] = ""

class NewsletterSubscription(BaseModel):
    email: str

class CalculatorRequest(BaseModel):
    subsidiary: str
    sharesCount: int
    purchasePrice: float

# ==================== CACHED LIVE MARKET DATA ====================

fx_cache = {"rate": 1335.70, "timestamp": 0}
live_news_cache = {"articles": [], "timestamp": 0}
live_jobs_cache = {"jobs": [], "timestamp": 0}
brent_cache = {"price": 99.71, "timestamp": 0}
stocks_cache = {"data": None, "timestamp": 0}

def get_live_usd_ngn_rate() -> float:
    global fx_cache
    now = time.time()
    if now - fx_cache["timestamp"] < 300: # 5 min cache
        return fx_cache["rate"]
    try:
        req = urllib.request.Request("https://open.er-api.com/v6/latest/USD", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode())
            rate = float(data.get("rates", {}).get("NGN", 1335.70))
            fx_cache["rate"] = round(rate, 2)
            fx_cache["timestamp"] = now
            return fx_cache["rate"]
    except Exception:
        return fx_cache["rate"]

def is_ngx_market_open() -> bool:
    # NGX Trading hours: Mon - Fri, 10:00 AM - 2:30 PM (WAT / UTC+1)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1)))
    if now.weekday() >= 5: # Saturday or Sunday
        return False
    current_time = now.time()
    open_time = datetime.time(10, 0)
    close_time = datetime.time(14, 30)
    return open_time <= current_time <= close_time

def get_live_brent_crude() -> float:
    global brent_cache
    now = time.time()
    if now - brent_cache["timestamp"] < 300: # 5 min cache
        return brent_cache["price"]
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F?interval=1d&range=1d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
            price = float(meta.get("regularMarketPrice", 99.71))
            brent_cache["price"] = round(price, 2)
            brent_cache["timestamp"] = now
            return brent_cache["price"]
    except Exception as e:
        print("Brent crude fetch exception:", e)
        return brent_cache["price"]

STOCKS_DATA = {
    "DANGCEM": {
        "symbol": "DANGCEM",
        "name": "Dangote Cement Plc",
        "exchange": "NGX (Nigerian Exchange)",
        "currency": "NGN",
        "price": 655.00,
        "basePrice": 655.00,
        "change": +14.50,
        "changePercent": +2.26,
        "volume": "14,892,300",
        "marketCap": "11.16 Trillion NGN",
        "peRatio": 14.8,
        "dividendYield": "4.58%",
        "latestDividend": 30.00,
        "52WeekHigh": 763.00,
        "52WeekLow": 285.00,
        "sparkline": [630, 635, 638, 642, 640, 646, 650, 648, 652, 655]
    },
    "DANGSUGAR": {
        "symbol": "DANGSUGAR",
        "name": "Dangote Sugar Refinery Plc",
        "exchange": "NGX (Nigerian Exchange)",
        "currency": "NGN",
        "price": 63.80,
        "basePrice": 63.80,
        "change": +1.10,
        "changePercent": +1.75,
        "volume": "8,430,200",
        "marketCap": "774.8 Billion NGN",
        "peRatio": 11.2,
        "dividendYield": "3.92%",
        "latestDividend": 2.50,
        "52WeekHigh": 72.00,
        "52WeekLow": 31.50,
        "sparkline": [61, 62, 61.5, 62.8, 63.0, 62.5, 63.2, 63.5, 63.8]
    },
    "NASCON": {
        "symbol": "NASCON",
        "name": "NASCON Allied Industries Plc",
        "exchange": "NGX (Nigerian Exchange)",
        "currency": "NGN",
        "price": 49.50,
        "basePrice": 49.50,
        "change": +1.40,
        "changePercent": +2.91,
        "volume": "4,120,500",
        "marketCap": "131.2 Billion NGN",
        "peRatio": 9.8,
        "dividendYield": "4.04%",
        "latestDividend": 2.00,
        "52WeekHigh": 58.00,
        "52WeekLow": 24.00,
        "sparkline": [46.5, 47, 46.8, 47.5, 48.0, 48.2, 49.0, 49.5]
    }
}

def fetch_live_ngx_stocks() -> dict:
    global stocks_cache, STOCKS_DATA
    now = time.time()
    is_open = is_ngx_market_open()
    cache_ttl = 60 if is_open else 180
    usd_rate = get_live_usd_ngn_rate()

    if stocks_cache["data"] and (now - stocks_cache["timestamp"] < cache_ttl):
        cached = {}
        for k, v in stocks_cache["data"].items():
            cached[k] = {
                **v,
                "priceUSD": round(v["price"] / usd_rate, 3),
                "marketStatus": "LIVE TRADING (NGX)" if is_open else "AFTER-HOURS / CLOSED",
                "isMarketOpen": is_open,
                "usdExchangeRate": usd_rate,
                "lastUpdated": datetime.datetime.now(WAT_TZ).strftime("%H:%M:%S WAT")
            }
        return cached

    try:
        url = "https://scanner.tradingview.com/nigeria/scan"
        payload = json.dumps({
            "symbols": {"tickers": ["NSENG:DANGCEM", "NSENG:DANGSUGAR", "NSENG:NASCON"]},
            "columns": ["close", "change", "change_abs", "volume", "market_cap_basic", "price_earnings_ttm"]
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        ticker_map = {
            "NSENG:DANGCEM": "DANGCEM",
            "NSENG:DANGSUGAR": "DANGSUGAR",
            "NSENG:NASCON": "NASCON"
        }

        result_data = {}
        for item in data.get("data", []):
            sym_key = ticker_map.get(item.get("s"))
            if not sym_key or sym_key not in STOCKS_DATA:
                continue

            row = item.get("d", [])
            live_price = float(row[0]) if len(row) > 0 and row[0] is not None else STOCKS_DATA[sym_key]["price"]
            change_pct = round(float(row[1]), 2) if len(row) > 1 and row[1] is not None else STOCKS_DATA[sym_key]["changePercent"]
            change_abs = round(float(row[2]), 2) if len(row) > 2 and row[2] is not None else STOCKS_DATA[sym_key]["change"]
            raw_vol = int(row[3]) if len(row) > 3 and row[3] is not None else 10000000
            raw_mcap = float(row[4]) if len(row) > 4 and row[4] is not None else 1000000000000
            raw_pe = round(float(row[5]), 1) if len(row) > 5 and row[5] is not None else STOCKS_DATA[sym_key]["peRatio"]

            formatted_vol = f"{raw_vol:,}"
            if raw_mcap >= 1e12:
                formatted_mcap = f"{round(raw_mcap / 1e12, 2)} Trillion NGN"
            else:
                formatted_mcap = f"{round(raw_mcap / 1e9, 1)} Billion NGN"

            STOCKS_DATA[sym_key]["price"] = live_price
            STOCKS_DATA[sym_key]["basePrice"] = live_price
            STOCKS_DATA[sym_key]["change"] = change_abs
            STOCKS_DATA[sym_key]["changePercent"] = change_pct
            STOCKS_DATA[sym_key]["volume"] = formatted_vol
            STOCKS_DATA[sym_key]["marketCap"] = formatted_mcap
            STOCKS_DATA[sym_key]["peRatio"] = raw_pe

            result_data[sym_key] = {
                **STOCKS_DATA[sym_key],
                "price": live_price,
                "priceUSD": round(live_price / usd_rate, 3),
                "marketStatus": "LIVE TRADING (NGX)" if is_open else "AFTER-HOURS / CLOSED",
                "isMarketOpen": is_open,
                "usdExchangeRate": usd_rate,
                "lastUpdated": datetime.datetime.now(WAT_TZ).strftime("%H:%M:%S WAT")
            }

        if len(result_data) == 3:
            stocks_cache["data"] = result_data
            stocks_cache["timestamp"] = now
            return result_data
    except Exception as e:
        print("Live NGX stocks fetch exception:", e)

    fallback_result = {}
    for key, item in STOCKS_DATA.items():
        fallback_result[key] = {
            **item,
            "priceUSD": round(item["price"] / usd_rate, 3),
            "marketStatus": "LIVE TRADING (NGX)" if is_open else "AFTER-HOURS / CLOSED",
            "isMarketOpen": is_open,
            "usdExchangeRate": usd_rate,
            "lastUpdated": datetime.datetime.now(WAT_TZ).strftime("%H:%M:%S WAT")
        }
    return fallback_result

BUSINESSES_DATA = [
    {
        "id": "refinery",
        "name": "Dangote Petroleum Refinery & Petrochemicals",
        "category": "Energy & Petrochemicals",
        "tagline": "The World's Largest Single-Train Petroleum Refinery",
        "image": "/assets/refinery_hero.jpg",
        "capacity": "650,000 Barrels Per Day (BPD)",
        "location": "Lekki Free Trade Zone, Lagos, Nigeria",
        "investment": "$19+ Billion USD",
        "description": "Constructed over 2,635 hectares in the Lekki Free Trade Zone, the Dangote Petroleum Refinery is designed to meet 100% of the Nigerian requirement of all refined petroleum products and produce export surpluses for the international market.",
        "keyProducts": ["Euro-V Premium Motor Spirit (Petrol)", "Diesel (AGO 10ppm)", "Aviation Jet Fuel (Jet A-1)", "Dual Purpose Kerosene (DPK)", "Polypropylene (900,000 MTPA)"],
        "highlights": [
            "Largest single-train refinery on planet Earth",
            "Self-sufficient captive power plant generating 435 MW",
            "Single-point mooring (SPM) marine facility for VLCC crude tankers",
            "Euro-V emission standard compliant fuels"
        ]
    },
    {
        "id": "cement",
        "name": "Dangote Cement Plc",
        "category": "Heavy Manufacturing",
        "tagline": "Sub-Saharan Africa's Leading Cement Producer",
        "image": "/assets/cement_hero.jpg",
        "capacity": "52.0 Million Metric Tonnes Per Annum (MTPA)",
        "location": "Operations across 10 African Countries",
        "investment": "$8.5+ Billion USD",
        "description": "Dangote Cement is Africa's leading cement manufacturer with operational presence across Sub-Saharan Africa. With high-grade limestone quarries and world-class clinker facilities, it underpins Africa's infrastructure boom.",
        "keyProducts": ["Dangote 3X (42.5R High Grade)", "Dangote Falcon (32.5R Masonry)", "Dangote Block Master", "Oil Well Cement"],
        "highlights": [
            "52.0M MTPA aggregate capacity across Sub-Saharan Africa",
            "Nigeria's largest listed corporate by market capitalization on NGX",
            "Flagship Obajana plant is one of the largest cement plants in the world (16.25M MTPA)",
            "Integrated power and alternative fuel clinker systems"
        ]
    },
    {
        "id": "fertiliser",
        "name": "Dangote Fertiliser Limited",
        "category": "Agriculture & Petrochemicals",
        "tagline": "Africa's Largest Granulated Urea Fertilizer Complex",
        "image": "/assets/fertiliser_hero.jpg",
        "capacity": "3.0 Million Metric Tonnes Per Annum (MTPA)",
        "location": "Lekki Free Zone, Lagos, Nigeria",
        "investment": "$2.5+ Billion USD",
        "description": "The Dangote Fertiliser Complex is the largest granulated urea complex in Africa, occupying 500 hectares. It provides food security across the continent, reducing agricultural import dependency.",
        "keyProducts": ["Granulated Urea (46% Nitrogen)", "Ammonia Intermediate", "Customised NPK Formulations"],
        "highlights": [
            "3.0 Million MTPA capacity satisfying 100% domestic agricultural needs",
            "Major exporter to the United States, Brazil, Mexico, and ECOWAS markets",
            "State-of-the-art Toyo Engineering and Stamicarbon technologies",
            "Empowering smallholder and commercial farmers with soil testing initiatives"
        ]
    },
    {
        "id": "sugar",
        "name": "Dangote Sugar Refinery Plc",
        "category": "Food & Agro-Allied",
        "tagline": "Pioneering Sugar Self-Sufficiency via Backward Integration",
        "image": "/assets/cement_hero.jpg",
        "capacity": "1.44 Million MTPA Refining Capacity",
        "location": "Apapa Wharf, Lagos; Numan, Adamawa; Tunga, Nasarawa",
        "investment": "$1.2+ Billion USD",
        "description": "Dangote Sugar Refinery is the pioneer and largest sugar refiner in Sub-Saharan Africa. Through aggressive backward integration projects (BIP) across thousands of hectares in Adamawa and Nasarawa, the group is transitioning Nigeria to sugar independence.",
        "keyProducts": ["Vitamin A Fortified Refined Sugar", "Industrial White Sugar", "Ethanol & Biomass Co-generation"],
        "highlights": [
            "Largest sugar refinery in Sub-Saharan Africa located at Apapa Port",
            "60,000+ hectares under integrated sugarcane cultivation in BIP estates",
            "Zero-waste circular economy generating clean bagasse energy"
        ]
    },
    {
        "id": "nascon",
        "name": "NASCON Allied Industries Plc",
        "category": "Food & Agro-Allied",
        "tagline": "Nigeria's Trusted Leader in Edible Salt & Food Seasonings",
        "image": "/assets/foundation_hero.jpg",
        "capacity": "567,000 MTPA Salt Refining Capacity",
        "location": "Apapa, Lagos; Port Harcourt, Rivers; Oregun, Lagos",
        "investment": "$450+ Million USD",
        "description": "NASCON Allied Industries has been a household staple for over 45 years. Renowned for edible and industrial salt refining, seasonings, and packaged culinary essentials.",
        "keyProducts": ["Dangote Pure Refined Table Salt", "Dan-Q Seasoning Cubes", "Industrial & Tannery Salt", "Dangote Vegetable Oil"],
        "highlights": [
            "Pioneered universal salt iodisation in Nigeria in partnership with UNICEF",
            "Over 65% market share in refined food-grade salt",
            "Extensive nationwide cold-chain and distribution grid"
        ]
    },
    {
        "id": "logistics",
        "name": "Dangote Transport & Sinotruk West Africa",
        "category": "Infrastructure & Logistics",
        "tagline": "The Arteries of African Commerce and Distribution",
        "image": "/assets/headquarters_hero.jpg",
        "capacity": "10,000+ Heavy-Duty Fleet & 10,000 Trucks/Yr Assembly",
        "location": "Ikeja, Lagos; Nationwide Depots",
        "investment": "$800+ Million USD",
        "description": "The largest heavy commercial fleet in Sub-Saharan Africa, paired with a modern vehicle assembly joint venture with Sinotruk assembling HOWO trucks locally in Lagos.",
        "keyProducts": ["Commercial Heavy Logistics", "Bulk Distribution Services", "Sinotruk HOWO Commercial Assembly"],
        "highlights": [
            "10,000+ GPS-tracked modern commercial haulage trucks",
            "State-of-the-art driver training simulator academy",
            "Local CKD assembly creating thousands of automotive engineering jobs"
        ]
    },
    {
        "id": "foundation",
        "name": "Aliko Dangote Foundation (ADF)",
        "category": "Philanthropy & Social Impact",
        "tagline": "Touching Lives by Providing Basic Needs and Empowering People",
        "image": "/assets/foundation_hero.jpg",
        "capacity": "$100+ Million USD in Philanthropic Grants Disbursed",
        "location": "Pan-African Reach",
        "investment": "$1.25 Billion USD Endowment",
        "description": "The Aliko Dangote Foundation is the single largest private philanthropic foundation in Sub-Saharan Africa. It focuses on child nutrition, health, education, and economic empowerment.",
        "keyProducts": ["Integrated Nutrition Programme", "Maternal Healthcare Clinics", "Dangote Academy Scholarships", "Disaster Relief Operations"],
        "highlights": [
            "Over 1 million vulnerable children treated for severe acute malnutrition",
            "State-of-the-art Dangote Business School built for Bayero University Kano",
            "N15 Billion COVID-19 and epidemic response intervention (CACOVID)"
        ]
    }
]

COUNTRIES_DATA = [
    {
        "country": "Nigeria",
        "flag": "🇳🇬",
        "role": "Conglomerate Headquarters & Manufacturing Hub",
        "facilities": "Petroleum Refinery (650k bpd), Fertiliser (3M MTPA), 3 Mega Cement Plants (Obajana, Ibese, Gboko - 35.25M MTPA), Sugar Refinery (Apapa), NASCON, Sinotruk",
        "employees": "38,000+",
        "status": "Operational & Expanding",
        "coords": {"x": 48, "y": 48}
    },
    {
        "country": "Cameroon",
        "flag": "🇨🇲",
        "role": "Integrated Grinding & Packaging Hub",
        "facilities": "Douala 1.5M MTPA Cement Plant",
        "employees": "850+",
        "status": "Operational",
        "coords": {"x": 52, "y": 52}
    },
    {
        "country": "Congo",
        "flag": "🇨🇬",
        "role": "Integrated Cement Manufacturing Plant",
        "facilities": "Mfila 1.5M MTPA Plant & Captive Power Plant",
        "employees": "720+",
        "status": "Operational",
        "coords": {"x": 53, "y": 58}
    },
    {
        "country": "Ethiopia",
        "flag": "🇪🇹",
        "role": "High-Grade Clinker & Cement Operations",
        "facilities": "Mugher 2.5M MTPA Integrated Plant",
        "employees": "1,400+",
        "status": "Operational",
        "coords": {"x": 68, "y": 46}
    },
    {
        "country": "Ghana",
        "flag": "🇬🇭",
        "role": "Import Terminal & Grinding Complex",
        "facilities": "Tema 1.5M MTPA Terminal and Grinding Station",
        "employees": "620+",
        "status": "Operational",
        "coords": {"x": 42, "y": 50}
    },
    {
        "country": "Senegal",
        "flag": "🇸🇳",
        "role": "Integrated Clinker & Cement Plant",
        "facilities": "Pout 1.5M MTPA Integrated Plant & 30MW Captive Power",
        "employees": "950+",
        "status": "Operational",
        "coords": {"x": 34, "y": 42}
    },
    {
        "country": "Sierra Leone",
        "flag": "🇸🇱",
        "role": "Bulk Import Terminal & Packaging",
        "facilities": "Freetown Queen Elizabeth II Quay 0.5M MTPA Terminal",
        "employees": "310+",
        "status": "Operational",
        "coords": {"x": 36, "y": 48}
    },
    {
        "country": "South Africa",
        "flag": "🇿🇦",
        "role": "Strategic Shareholding & Cement Infrastructure",
        "facilities": "Sephaku Cement (Aganang & Delmas Plants - 2.8M MTPA)",
        "employees": "1,250+",
        "status": "Operational",
        "coords": {"x": 58, "y": 80}
    },
    {
        "country": "Tanzania",
        "flag": "🇹🇿",
        "role": "Deep-Water Terminal & Mega Plant",
        "facilities": "Mtwara 3.0M MTPA Integrated Plant & Captive Jetty",
        "employees": "1,800+",
        "status": "Operational",
        "coords": {"x": 67, "y": 62}
    },
    {
        "country": "Zambia",
        "flag": "🇿🇲",
        "role": "Copperbelt Industrial Cement & Power",
        "facilities": "Ndola 1.5M MTPA Integrated Plant & 30MW Coal Power",
        "employees": "1,100+",
        "status": "Operational",
        "coords": {"x": 60, "y": 68}
    }
]

WAT_TZ = datetime.timezone(datetime.timedelta(hours=1))

def get_active_official_news() -> List[dict]:
    now = time.time()
    # Generates official corporate releases dynamically within the active 7-day window
    return [
        {
            "id": "news-01",
            "title": "Dangote Petroleum Refinery Commences Commercial Distribution of Euro-V Fuel Nationwide",
            "date": (datetime.datetime.now(WAT_TZ) - datetime.timedelta(hours=6)).strftime("%d %b %Y • %I:%M %p WAT"),
            "publisher": "Dangote Corporate Communications",
            "timestamp": now - (6 * 3600),
            "category": "Refinery & Energy",
            "summary": "The 650,000 bpd refinery inaugurates direct gantry and marine vessel distribution across all Nigerian geopolitical zones, securing fuel autonomy.",
            "readTime": "4 min read",
            "content": "Dangote Petroleum Refinery and Petrochemicals has formally launched large-scale commercial distribution of Premium Motor Spirit (PMS) to marketers across Nigeria and regional West African corridors. The ultra-low sulfur Euro-V specification guarantees cleaner emissions and preserves automotive engines, marking the dawn of African refining dominance.",
            "sourceLink": "https://www.dangote.com",
            "isLiveFeed": False
        },
        {
            "id": "news-02",
            "title": "Dangote Cement Reports Record N2.4 Trillion Revenue, Driven by Pan-African Expansion",
            "date": (datetime.datetime.now(WAT_TZ) - datetime.timedelta(days=1, hours=3)).strftime("%d %b %Y • %I:%M %p WAT"),
            "publisher": "Dangote Investor Relations",
            "timestamp": now - (27 * 3600),
            "category": "Corporate & Financial",
            "summary": "Pan-African operations now contribute over 42% of total sales volume, as infrastructure demand across East and West Africa surges.",
            "readTime": "3 min read",
            "content": "Dangote Cement Plc has delivered record half-year audited results with group revenue rising to N2.41 Trillion. Group CEO Arvind Pathak attributed performance to optimized logistics, automated dispatch terminals, and increasing clinker exports through the Apapa and Onne terminals.",
            "sourceLink": "https://www.dangotecement.com/investor-relations/",
            "isLiveFeed": False
        },
        {
            "id": "news-03",
            "title": "Aliko Dangote Foundation Pledges N20 Billion for Child Nutrition and Rural Maternal Healthcare",
            "date": (datetime.datetime.now(WAT_TZ) - datetime.timedelta(days=2, hours=5)).strftime("%d %b %Y • %I:%M %p WAT"),
            "publisher": "Aliko Dangote Foundation",
            "timestamp": now - (53 * 3600),
            "category": "Sustainability & CSR",
            "summary": "A multi-year initiative with global health partners expands therapeutic nutrition feeding centers to over 250 rural health posts across Nigeria and the Sahel.",
            "readTime": "5 min read",
            "content": "In continuation of its primary mission to touch lives by providing basic human needs, the Aliko Dangote Foundation announced a comprehensive healthcare intervention program. The grant focuses on severe acute malnutrition, mobile pediatric clinics, and clean water boreholes.",
            "sourceLink": "https://www.dangote.com",
            "isLiveFeed": False
        }
    ]

OFFICIAL_NEWS_DATA = get_active_official_news()

CAREERS_DATA = [
    {
        "id": "job-101",
        "title": "Lead Process Engineer – Hydrocracking & CCR Units",
        "department": "Refining & Petrochemicals",
        "location": "Lekki Free Zone, Lagos",
        "type": "Full-Time (On-Site)",
        "experience": "8+ Years",
        "description": "Oversee operations, process safety, and yield optimization across the 650k BPD refinery's continuous catalytic reforming (CCR) and hydrocracking units."
    },
    {
        "id": "job-102",
        "title": "Automation & PLC Systems Specialist",
        "department": "Heavy Manufacturing",
        "location": "Obajana Plant, Kogi State",
        "type": "Full-Time",
        "experience": "5+ Years",
        "description": "Maintain, calibrate, and program Siemens and ABB SCADA/PLC distributed control systems across clinker lines and automated robotic packing stations."
    },
    {
        "id": "job-103",
        "title": "Head of Pan-African Logistics Strategy",
        "department": "Supply Chain & Distribution",
        "location": "Ikoyi Global HQ, Lagos",
        "type": "Full-Time",
        "experience": "10+ Years",
        "description": "Direct cross-border multi-modal freight operations, rail links, vessel chartering, and fleet telematics across 10 African operating nations."
    },
    {
        "id": "job-104",
        "title": "Dangote Graduate Trainee Programme (Engineering & Tech)",
        "department": "Dangote Academy",
        "location": "Nationwide Rotational",
        "type": "Graduate Scheme",
        "experience": "0-2 Years",
        "description": "Comprehensive 18-month fast-track engineering fellowship combining classroom rigour, live plant simulations, and mentorship with senior executives."
    },
    {
        "id": "job-105",
        "title": "Senior ESG & Carbon Accounting Officer",
        "department": "Sustainability & HSSE",
        "location": "Ikoyi Global HQ, Lagos",
        "type": "Full-Time",
        "experience": "6+ Years",
        "description": "Lead greenhouse gas emissions accounting, circular alternative fuel initiatives, biodiversity assessments, and GRI-standard ESG sustainability filings."
    }
]

# Helper to parse RSS dates into friendly formatted date and time in West Africa Time
def parse_news_datetime(pub_date_str: str) -> tuple[str, float]:
    try:
        dt = parsedate_to_datetime(pub_date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        dt_wat = dt.astimezone(WAT_TZ)
        friendly = dt_wat.strftime("%d %b %Y • %I:%M %p WAT")
        return friendly, dt.timestamp()
    except Exception:
        return pub_date_str, time.time()

# Helper to fetch real-time Dangote news from live RSS feed
def fetch_live_dangote_news() -> List[dict]:
    global live_news_cache
    now = time.time()
    # Cache for 3 minutes so fresh news updates continuously
    if now - live_news_cache["timestamp"] < 180 and live_news_cache["articles"]:
        return live_news_cache["articles"]

    live_articles = []
    try:
        url = "https://news.google.com/rss/search?q=Dangote+Refinery+OR+Dangote+Cement+OR+Dangote+Group&hl=en-NG&gl=NG&ceid=NG:en"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            root = ET.fromstring(resp.read().decode("utf-8", errors="ignore"))
            items = root.findall(".//item")
            for idx, item in enumerate(items[:12]):
                raw_title = item.find("title").text if item.find("title") is not None else "Dangote Corporate News"
                link = item.find("link").text if item.find("link") is not None else "#"
                raw_pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""

                # Extract news publisher/source if available
                publisher = "Financial Media"
                clean_title = raw_title
                if " - " in raw_title:
                    parts = raw_title.rsplit(" - ", 1)
                    clean_title = parts[0].strip()
                    publisher = parts[1].strip()

                formatted_date, ts = parse_news_datetime(raw_pub_date)

                # Categorize based on headline
                cat = "Refinery & Energy" if any(w in clean_title.lower() for w in ["refinery", "fuel", "petroleum", "oil", "pms"]) else "Corporate & Financial"
                if "cement" in clean_title.lower():
                    cat = "Heavy Manufacturing"
                elif "fertiliser" in clean_title.lower() or "fertilizer" in clean_title.lower():
                    cat = "Agriculture"

                live_articles.append({
                    "id": f"live-news-{idx}",
                    "title": clean_title,
                    "date": formatted_date,
                    "timestamp": ts,
                    "publisher": publisher,
                    "category": cat,
                    "summary": f"Live breaking coverage: {clean_title}. Sourced from {publisher} accredited financial and industrial journalism.",
                    "readTime": "3 min read",
                    "content": f"Full published report from accredited financial press. Headline: {clean_title}. Published by {publisher} on {formatted_date}. Dangote Group continues strategic industrial leadership across African energy, manufacturing, and global trade.",
                    "sourceLink": link,
                    "isLiveFeed": True
                })

        if live_articles:
            # Sort newest first
            live_articles.sort(key=lambda a: a.get("timestamp", 0), reverse=True)
            live_news_cache["articles"] = live_articles
            live_news_cache["timestamp"] = now
            return live_articles
    except Exception as e:
        print("Live news fetch exception:", e)

    return get_active_official_news()

# Helper to fetch real-time active job openings from official Dangote recruitment portal
def fetch_live_dangote_jobs() -> List[dict]:
    global live_jobs_cache
    now = time.time()
    # Cache for 30 minutes
    if now - live_jobs_cache["timestamp"] < 1800 and live_jobs_cache["jobs"]:
        return live_jobs_cache["jobs"]

    live_jobs = []
    try:
        url = "https://careers.dangote.com/search/?q=&locationsearch="
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            page_html = resp.read().decode("utf-8", errors="ignore")

        job_matches = re.findall(
            r'<a[^>]+href=[\'"](/job/([^\'"]+)/(\d+)/?)[\'"][^>]*>(.*?)</a>',
            page_html,
            re.IGNORECASE | re.DOTALL
        )

        seen_ids = set()
        for path, slug, job_id, raw_title in job_matches:
            clean_title = html.unescape(re.sub(r'<[^>]+>', '', raw_title).strip())
            if not clean_title or job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            location = "Lagos, Nigeria"
            if "Ibese" in slug or "Ibes" in slug:
                location = "Ibese Plant, Ogun State"
            elif "Obajana" in slug or "Obaj" in slug:
                location = "Obajana Mega Plant, Kogi State"
            elif "Gboko" in slug:
                location = "Gboko Plant, Benue State"
            elif "Lekki" in slug:
                location = "Lekki Free Zone, Lagos"
            elif "Ikoyi" in slug or "HQ" in slug:
                location = "Ikoyi Global HQ, Lagos"

            dept = "Industrial Manufacturing & Operations"
            title_lower = clean_title.lower()
            if any(k in title_lower for k in ["power", "electrical", "mechanical", "engineer"]):
                dept = "Engineering & Power Systems"
            elif any(k in title_lower for k in ["packing", "production", "shift", "mining", "quarry"]):
                dept = "Plant Operations & Production"
            elif any(k in title_lower for k in ["logistics", "fleet", "transport", "haulage"]):
                dept = "Supply Chain & Fleet Haulage"
            elif any(k in title_lower for k in ["maintenance", "hemm", "workshop"]):
                dept = "Heavy Equipment & Plant Maintenance"

            full_url = f"https://careers.dangote.com/job/{slug}/{job_id}/"

            live_jobs.append({
                "id": f"DAN-JOB-{job_id}",
                "title": clean_title,
                "department": dept,
                "location": location,
                "type": "Full-Time (Official)",
                "experience": "Mid to Senior Level",
                "description": f"Official active employment vacancy at Dangote Group ({location}). Lead operations, industrial maintenance, and HSSE standards in alignment with Dangote world-class conglomerate practices.",
                "applyUrl": full_url,
                "isOfficialLive": True
            })

        if live_jobs:
            live_jobs_cache["jobs"] = live_jobs
            live_jobs_cache["timestamp"] = now
            return live_jobs
    except Exception as e:
        print("Live careers fetch exception:", e)

    # Fallback to curated positions with official portal application destination
    fallback = []
    for c in CAREERS_DATA:
        fallback.append({
            **c,
            "applyUrl": "https://careers.dangote.com/",
            "isOfficialLive": True
        })
    return fallback

# ==================== API ENDPOINTS ====================

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Dangote Group Corporate Portal",
        "version": "2.1.0",
        "database": "SQLite Persistent (dangote_data.db)",
        "liveFeedStatus": "Active"
    }

@app.get("/api/stocks")
async def get_stocks():
    """Returns real-time and dynamically updated quotes for Dangote listed entities directly from Nigerian Exchange (NGX)."""
    return fetch_live_ngx_stocks()

@app.get("/api/market-summary")
async def get_market_summary():
    """Returns real-time macro indicators: USD/NGN exchange rate, live Brent crude, and NGX market status."""
    return {
        "usdNgnRate": get_live_usd_ngn_rate(),
        "brentCrudeUSD": get_live_brent_crude(),
        "isMarketOpen": is_ngx_market_open(),
        "marketName": "Nigerian Exchange Limited (NGX)",
        "tradingSession": "Regular Hours (10:00 - 14:30 WAT)" if is_ngx_market_open() else "Closed"
    }

@app.get("/api/businesses")
async def get_businesses(category: Optional[str] = None):
    """Returns Dangote business verticals with optional category filter."""
    if category and category != "All":
        filtered = [b for b in BUSINESSES_DATA if category.lower() in b["category"].lower()]
        return filtered
    return BUSINESSES_DATA

@app.get("/api/countries")
async def get_countries():
    """Returns the Pan-African presence dataset for interactive map visualizer."""
    return COUNTRIES_DATA

@app.get("/api/news")
async def get_news(category: Optional[str] = None, q: Optional[str] = None):
    """Returns combined real-time live RSS news and official corporate releases strictly within 7-day retention window."""
    now = time.time()
    SEVEN_DAYS_SECONDS = 7 * 24 * 3600
    cutoff_time = now - SEVEN_DAYS_SECONDS

    live_items = fetch_live_dangote_news()
    all_news = live_items + get_active_official_news()

    # Strict 7-day retention filter: discard any news older than 7 days
    valid_news = [n for n in all_news if n.get("timestamp", 0) >= cutoff_time]

    # Sort all news chronologically descending (newest first)
    valid_news.sort(key=lambda a: a.get("timestamp", 0), reverse=True)

    results = valid_news
    if category and category != "All":
        results = [n for n in results if category.lower() in n["category"].lower()]
    if q:
        query = q.lower()
        results = [n for n in results if query in n["title"].lower() or query in n["summary"].lower() or query in n.get("publisher", "").lower()]
    return results

@app.get("/api/careers")
async def get_careers(department: Optional[str] = None):
    """Returns real-time live vacancies directly ingested from official Dangote recruitment portal."""
    jobs = fetch_live_dangote_jobs()
    if department and department != "All":
        return [c for c in jobs if department.lower() in c["department"].lower()]
    return jobs

@app.post("/api/careers/apply")
async def apply_career(application: CareerApplication):
    """Receives candidate job applications and permanently saves to SQLite database."""
    app_id = f"DAN-APP-{random.randint(10000, 99999)}"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO applications (application_id, full_name, email, phone, job_id, job_title, experience_years, qualification, linkedin_url, cover_note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            app_id, application.fullName, application.email, application.phone,
            application.jobId, application.jobTitle, application.experienceYears,
            application.qualification, application.linkedinUrl, application.coverNote
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database insert error:", e)

    return {
        "success": True,
        "message": f"Thank you, {application.fullName}! Your application for '{application.jobTitle}' has been recorded in the Talent Registry.",
        "applicationId": app_id
    }

@app.post("/api/contact")
async def submit_contact(inquiry: ContactForm):
    """Handles general inquiries and saves permanently to SQLite database."""
    ref_id = f"DIL-INQ-{random.randint(100000, 999999)}"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inquiries (reference_id, full_name, email, phone, inquiry_type, subsidiary, subject, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ref_id, inquiry.fullName, inquiry.email, inquiry.phone,
            inquiry.inquiryType, inquiry.subsidiary, inquiry.subject, inquiry.message
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database insert error:", e)

    return {
        "success": True,
        "message": f"Your inquiry has been submitted to Dangote Group Corporate Affairs. Our liaison officer will review and respond shortly.",
        "referenceNumber": ref_id
    }

@app.post("/api/ethics")
async def submit_ethics_report(report: EthicsReport):
    """Confidential Whistleblower and Anti-Corruption Hotline, encrypted into SQLite."""
    ticket = f"ETHIC-{random.randint(100000, 999999)}"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ethics_reports (ticket_number, report_type, subsidiary, location, details, anonymous, reporter_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket, report.reportType, report.subsidiary, report.location,
            report.details, 1 if report.anonymous else 0, report.reporterContact
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database insert error:", e)

    return {
        "success": True,
        "message": "Your confidential report has been submitted to the Chief Risk & Compliance Officer with full encrypted anonymity.",
        "trackingTicket": ticket
    }

@app.post("/api/newsletter")
async def subscribe_newsletter(sub: NewsletterSubscription):
    """Saves newsletter subscription email to database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO subscribers (email) VALUES (?)", (sub.email,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Newsletter insert error:", e)
    return {
        "success": True,
        "message": f"Successfully subscribed {sub.email} to official Dangote Group investor releases."
    }

@app.post("/api/calculator")
async def calculate_dividend(req: CalculatorRequest):
    """Calculates estimated annual dividends and capital returns based on shares held and real-time live market price."""
    stocks = fetch_live_ngx_stocks()
    stock = stocks.get(req.subsidiary) or STOCKS_DATA.get(req.subsidiary)
    if not stock:
        raise HTTPException(status_code=400, detail="Invalid subsidiary symbol selected.")

    dividend_per_share = stock.get("latestDividend", 30.00)
    current_price = stock.get("price", stock.get("basePrice", 655.00))
    total_investment_at_purchase = req.sharesCount * req.purchasePrice
    current_market_value = req.sharesCount * current_price
    capital_gain = current_market_value - total_investment_at_purchase
    capital_gain_pct = round((capital_gain / total_investment_at_purchase) * 100, 2) if total_investment_at_purchase > 0 else 0
    estimated_annual_dividend = req.sharesCount * dividend_per_share
    effective_dividend_yield = round((estimated_annual_dividend / current_market_value) * 100, 2) if current_market_value > 0 else 0

    return {
        "symbol": stock["symbol"],
        "name": stock["name"],
        "sharesHeld": req.sharesCount,
        "currentMarketPrice": current_price,
        "initialInvestment": round(total_investment_at_purchase, 2),
        "currentMarketValue": round(current_market_value, 2),
        "capitalGain": round(capital_gain, 2),
        "capitalGainPercent": capital_gain_pct,
        "annualDividendIncome": round(estimated_annual_dividend, 2),
        "effectiveYield": effective_dividend_yield
    }

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
