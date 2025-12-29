from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const, nakshatra, dasha

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculate_all(data):
    # Birth details
    year = data['year']
    month = data['month']
    date_day = data['date']
    hours = data['hours']
    minutes = data['minutes']
    seconds = data.get('seconds', 0)
    latitude = data['latitude']
    longitude = data['longitude']
    timezone = data['timezone']

    dt = Datetime(f"{year}-{month:02}-{date_day:02}", f"{hours:02}:{minutes:02}:{seconds:02}", timezone)
    pos = GeoPos(latitude, longitude)
    chart = Chart(dt, pos, ayanamsa=const.AYAN_LAHIRI)

    # Planet Positions
    planets = {}
    for planet in const.PLANETS:
        p = chart.get(planet)
        planets[planet] = {"sign": p.sign, "longitude": round(p.lon,2)}

    # Ascendant & Houses
    asc = chart.get(const.ASC)
    asc_sign = asc.sign
    houses = {}
    for i in range(1,13):
        h = chart.get(const.HOUSES[i-1])
        houses[f"house_{i}"] = {"sign": h.sign, "longitude": round(h.lon,2)}

    # Moon & Nakshatra
    moon = chart.get(const.MOON)
    moon_sign = moon.sign
    moon_nakshatra = nakshatra.getNakshatra(moon.lon)

    # Vimshottari Dasha
    try:
        vimshottari = [str(pd) for pd in dasha.VimshottariDasha(chart).progression()]
    except:
        vimshottari = ["Not calculated"]

    # Char Dasha
    try:
        char_dasha = [str(pd) for pd in dasha.CharDasha(chart).progression()]
    except:
        char_dasha = ["Not calculated"]

    # Yogini Dasha
    try:
        yogini_dasha = [str(pd) for pd in dasha.YoginiDasha(chart).progression()]
    except:
        yogini_dasha = ["Not calculated"]

    # Panchang
    tithi = nakshatra.getTithi(dt)
    vara = dt.wday
    yoga = nakshatra.getYoga(dt)
    karana = nakshatra.getKarana(dt)

    # Manglik Check
    mars_house = chart.getHouse(const.MARS)
    manglik = "full" if mars_house in [1,2,4,7,8,12] else "none"

    # Kalsarpa Check
    rahu = chart.get(const.NNODE)
    ketu = chart.get(const.SNODE)
    kalsarpa = "full" if all(rahu.lon < chart.get(p).lon < ketu.lon or ketu.lon < chart.get(p).lon < rahu.lon for p in const.PLANETS) else "none"

    # Hora & Abhujh Muhurta
    hora = "Surya" if dt.hours % 2 == 0 else "Chandra"
    abhujh_muhurta = "Yes" if 24 - dt.hours >= 20 else "No"

    # Navamsa Chart
    navamsa = {}
    for planet in const.PLANETS:
        p = chart.get(planet)
        navamsa_deg = p.lon % 30 / 3.3333333
        navamsa_sign_index = int(navamsa_deg) % 12
        navamsa_sign = const.SIGNS[navamsa_sign_index]
        navamsa[planet] = {"sign": navamsa_sign, "longitude": round(p.lon,2)}

    result = {
        "planets": planets,
        "ascendant": asc_sign,
        "houses": houses,
        "moon": {"sign": moon_sign, "nakshatra": moon_nakshatra},
        "vimshottari_dasha": vimshottari,
        "char_dasha": char_dasha,
        "yogini_dasha": yogini_dasha,
        "panchang": {"tithi": tithi, "vara": vara, "yoga": yoga, "karana": karana},
        "manglik": manglik,
        "kalsarpa": kalsarpa,
        "hora": hora,
        "abhujh_muhurta": abhujh_muhurta,
        "navamsa": navamsa
    }

    return result

@app.post("/kundali")
async def kundali(request: Request):
    data = await request.json()
    return calculate_all(data)
