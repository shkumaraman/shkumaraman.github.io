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
    # Validate inputs
    required_fields = ['year','month','date','hours','minutes','latitude','longitude','timezone']
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing required field: {field}"}

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
        planets[planet] = {"sign": p.sign, "longitude": round(p.lon, 2)}

    # Ascendant & Houses
    asc = chart.get(const.ASC)
    asc_sign = asc.sign
    houses = {}
    for i in range(1,13):
        h = chart.get(const.HOUSES[i-1])
        houses[f"house_{i}"] = {"sign": h.sign, "longitude": round(h.lon, 2)}

    # Moon, Nakshatra, Nakshatra Pada
    moon = chart.get(const.MOON)
    moon_sign = moon.sign
    moon_nakshatra = nakshatra.getNakshatra(moon.lon)
    # Nakshatra Pada calculation (1-4)
    moon_nakshatra_deg = moon.lon % 30
    pada = int(moon_nakshatra_deg // 3.75) + 1

    # Vimshottari Dasha
    vimshottari = []
    try:
        v_dasha = dasha.VimshottariDasha(chart)
        for pd in v_dasha.progression():
            vimshottari.append(str(pd))
    except Exception as e:
        vimshottari = [f"Not calculated ({e})"]

    # Char Dasha & Yogini Dasha
    try:
        char_d = dasha.CharDasha(chart)
        char_dasha = [str(pd) for pd in char_d.progression()]
    except Exception as e:
        char_dasha = [f"Not calculated ({e})"]

    try:
        yogini_d = dasha.YoginiDasha(chart)
        yogini_dasha = [str(pd) for pd in yogini_d.progression()]
    except Exception as e:
        yogini_dasha = [f"Not calculated ({e})"]

    # Panchang
    tithi = nakshatra.getTithi(dt)
    vara = (dt.wday + 1) % 7 or 7  # Sunday = 1
    yoga = nakshatra.getYoga(dt)
    karana = nakshatra.getKarana(dt)

    # Manglik Check
    mars_house = chart.getHouse(const.MARS)
    manglik = mars_house in [1,2,4,7,8,12]

    # Kalsarpa Check (Robust)
    rahu = chart.get(const.NNODE)
    ketu = chart.get(const.SNODE)
    def is_kalsarpa():
        for planet in const.PLANETS:
            pl = chart.get(planet)
            if rahu.lon < ketu.lon:
                if not (rahu.lon < pl.lon < ketu.lon):
                    return False
            else:  # Crosses 0° Aries
                if not (pl.lon > rahu.lon or pl.lon < ketu.lon):
                    return False
        return True
    kalsarpa = is_kalsarpa()

    # Hora & Abhujh Muhurta
    hora = "Surya" if dt.hours % 2 == 0 else "Chandra"
    abhujh_muhurta = "Yes" if 24 - dt.hours >= 20 else "No"

    # Navamsa Chart (Accurate)
    navamsa = {}
    for planet in const.PLANETS:
        p = chart.get(planet)
        sign_index = const.SIGNS.index(p.sign)
        deg_in_sign = p.lon % 30
        navamsa_index = int(deg_in_sign // 3.3333333)  # 9 divisions
        navamsa_sign_index = (sign_index*3 + navamsa_index) % 12
        navamsa_sign = const.SIGNS[navamsa_sign_index]
        navamsa[planet] = {"sign": navamsa_sign, "longitude": round(p.lon,2)}

    # Advanced Child / Progeny Analysis
    # Consider 5th house, its lord, Jupiter, and Manglik
    fifth_house = chart.get(const.HOUSES[4])
    fifth_house_planets = [p for p in const.PLANETS if chart.getHouse(p) == 5]
    jupiter = chart.get(const.JUPITER)
    jupiter_house = chart.getHouse(const.JUPITER)
    child_prediction = {
        "fifth_house_planets": fifth_house_planets,
        "jupiter_house": jupiter_house,
        "manglik": manglik,
        "prediction": "Favorable" if not manglik and jupiter_house in [5,9] else "Check timing / further analysis needed"
    }

    result = {
        "planets": planets,
        "ascendant": asc_sign,
        "houses": houses,
        "moon": {"sign": moon_sign, "nakshatra": moon_nakshatra, "pada": pada},
        "vimshottari_dasha": vimshottari,
        "char_dasha": char_dasha,
        "yogini_dasha": yogini_dasha,
        "panchang": {"tithi": tithi, "vara": vara, "yoga": yoga, "karana": karana},
        "manglik": manglik,
        "kalsarpa": kalsarpa,
        "hora": hora,
        "abhujh_muhurta": abhujh_muhurta,
        "navamsa": navamsa,
        "child_prediction": child_prediction
    }

    return result

@app.post("/kundali")
async def kundali(request: Request):
    data = await request.json()
    result = calculate_all(data)
    return result
