from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const, nakshatra, dasha
from flatlib.aspects import Aspect
from flatlib.dignities import essential, accidental
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculate_shadbala(chart):
    planet_strength = {}
    for planet in const.PLANETS:
        if planet in [const.NNODE, const.SNODE]:
            continue
        p = chart.get(planet)
        strength_score = essential.totalScore(p) + accidental.totalScore(p, chart)
        planet_strength[planet] = round(strength_score, 2)
    return planet_strength

def calculate_aspects(chart):
    aspects_list = []
    planets = const.PLANETS[:7]
    for i, p1 in enumerate(planets):
        for p2 in planets[i+1:]:
            aspect = Aspect(chart.get(p1), chart.get(p2), const.MAJOR_ASPECTS)
            if aspect.type:
                aspects_list.append({
                    "planets": f"{p1}-{p2}",
                    "type": aspect.type,
                    "orb": round(aspect.orb, 2),
                    "nature": "Harmonic" if aspect.type in [const.TRINE, const.SEXTILE] else "Challenging"
                })
    return aspects_list

def calculate_yogas(chart):
    yogas = []
    
    moon = chart.get(const.MOON)
    jupiter = chart.get(const.JUPITER)
    saturn = chart.get(const.SATURN)
    mars = chart.get(const.MARS)
    sun = chart.get(const.SUN)
    
    if (chart.getHouse(const.MOON) == chart.getHouse(const.JUPITER) or 
        moon.sign == jupiter.sign):
        yogas.append({"name": "Gajakesari Yoga", "description": "Wisdom and prosperity"})
    
    if sun.sign == const.SIGNS[4] and moon.sign == const.SIGNS[4]:
        yogas.append({"name": "Ruchaka Yoga", "description": "Leadership and courage"})
    
    if mars.sign in [const.SIGNS[0], const.SIGNS[3], const.SIGNS[6], const.SIGNS[9]]:
        yogas.append({"name": "Dhruva Yoga", "description": "Stability and success"})
    
    if (chart.getHouse(const.VENUS) == chart.getHouse(const.MOON) or 
        chart.get(const.VENUS).sign == moon.sign):
        yogas.append({"name": "Chandra-Mangala Yoga", "description": "Artistic and emotional harmony"})
    
    return yogas

def calculate_arudha(chart):
    asc = chart.get(const.ASC)
    asc_sign_idx = const.SIGNS.index(asc.sign)
    asc_house = 1
    
    arudha_1_sign_idx = (asc_sign_idx + chart.getHouse(const.SUN) - 1) % 12
    arudha_1 = const.SIGNS[arudha_1_sign_idx]
    
    return {
        "arudha_lagna": arudha_1,
        "upapada_lagna": const.SIGNS[(asc_sign_idx + chart.getHouse(const.VENUS) - 1) % 12]
    }

def calculate_drishti(chart):
    graha_drishti = {}
    planets = const.PLANETS[:7]
    
    for planet in planets:
        p = chart.get(planet)
        aspects = []
        for other in planets:
            if other != planet:
                diff = abs(p.lon - chart.get(other).lon) % 360
                diff = min(diff, 360-diff)
                if diff <= 30:
                    aspects.append(other)
        graha_drishti[planet] = aspects
    
    return graha_drishti

def calculate_varshaphala(birth_chart, current_year):
    asc = birth_chart.get(const.ASC)
    varshaphala_asc_sign = const.SIGNS[(const.SIGNS.index(asc.sign) + current_year - birth_chart.date.year) % 12]
    
    return {
        "varshaphala_lagna": varshaphala_asc_sign,
        "year_ruler": const.SIGNS[(current_year - 1) % 12]
    }

def calculate_all(data):
    required_fields = ['year','month','date','hours','minutes','latitude','longitude','timezone']
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing field: {field}"}

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

    planets = {}
    for planet in const.PLANETS:
        p = chart.get(planet)
        house = chart.getHouse(planet)
        planets[planet] = {
            "sign": p.sign,
            "longitude": round(p.lon, 2),
            "house": house,
            "house_sign": chart.get(const.HOUSES[house-1]).sign,
            "nakshatra": nakshatra.getNakshatra(p.lon),
            "nakshatra_lord": nakshatra.nakshatraLord(p.lon)
        }

    asc = chart.get(const.ASC)
    houses = {}
    for i in range(1,13):
        h = chart.get(const.HOUSES[i-1])
        lord = const.SIGN_LORDS[const.SIGNS.index(h.sign)]
        houses[f"house_{i}"] = {
            "sign": h.sign,
            "longitude": round(h.lon, 2),
            "lord": lord,
            "lord_house": chart.getHouse(lord)
        }

    moon = chart.get(const.MOON)
    moon_nakshatra = nakshatra.getNakshatra(moon.lon)
    pada = int((moon.lon % 30) // 3.75) + 1

    vimshottari = []
    try:
        v_dasha = dasha.VimshottariDasha(chart)
        for pd in v_dasha.progression():
            vimshottari.append(str(pd))
    except:
        vimshottari = ["Error"]

    char_dasha = []
    try:
        char_d = dasha.CharDasha(chart)
        char_dasha = [str(pd) for pd in char_d.progression()]
    except:
        char_dasha = ["Error"]

    yogini_dasha = []
    try:
        yogini_d = dasha.YoginiDasha(chart)
        yogini_dasha = [str(pd) for pd in yogini_d.progression()]
    except:
        yogini_dasha = ["Error"]

    tithi = nakshatra.getTithi(dt)
    vara = (dt.wday + 1) % 7 or 7
    yoga = nakshatra.getYoga(dt)
    karana = nakshatra.getKarana(dt)

    mars_house = chart.getHouse(const.MARS)
    manglik = mars_house in [1,2,4,7,8,12]
    
    manglik_remedy = "Needs remedy" if manglik else "Not applicable"

    rahu = chart.get(const.NNODE)
    ketu = chart.get(const.SNODE)
    def is_kalsarpa():
        for planet in const.PLANETS:
            pl = chart.get(planet)
            if rahu.lon < ketu.lon:
                if not (rahu.lon < pl.lon < ketu.lon):
                    return False
            else:
                if not (pl.lon > rahu.lon or pl.lon < ketu.lon):
                    return False
        return True
    kalsarpa = is_kalsarpa()

    hora = "Surya" if dt.hours % 2 == 0 else "Chandra"
    abhujh_muhurta = "Yes" if 24 - dt.hours >= 20 else "No"

    navamsa = {}
    for planet in const.PLANETS:
        p = chart.get(planet)
        sign_index = const.SIGNS.index(p.sign)
        deg_in_sign = p.lon % 30
        navamsa_index = int(deg_in_sign // 3.3333333)
        navamsa_sign_index = (sign_index*3 + navamsa_index) % 12
        navamsa_sign = const.SIGNS[navamsa_sign_index]
        navamsa[planet] = {
            "sign": navamsa_sign,
            "longitude": round(p.lon,2),
            "navamsa_lord": const.SIGN_LORDS[navamsa_sign_index]
        }

    fifth_house = chart.get(const.HOUSES[4])
    fifth_house_planets = [p for p in const.PLANETS if chart.getHouse(p) == 5]
    jupiter = chart.get(const.JUPITER)
    jupiter_house = chart.getHouse(const.JUPITER)
    child_prediction = {
        "fifth_house_planets": fifth_house_planets,
        "fifth_house_lord": const.SIGN_LORDS[const.SIGNS.index(fifth_house.sign)],
        "fifth_lord_house": chart.getHouse(const.SIGN_LORDS[const.SIGNS.index(fifth_house.sign)]),
        "jupiter_house": jupiter_house,
        "jupiter_aspects_fifth": 5 in [jupiter_house, (jupiter_house + 4) % 12, (jupiter_house + 7) % 12],
        "manglik": manglik,
        "assessment": "Favorable" if (not manglik and jupiter_house in [5,9] and len(fifth_house_planets) > 0) else "Need detailed analysis"
    }

    dashamsha = {}
    for planet in const.PLANETS:
        p = chart.get(planet)
        sign_index = const.SIGNS.index(p.sign)
        deg_in_sign = p.lon % 30
        dashamsha_index = int(deg_in_sign // 3)
        dashamsha_sign_index = (sign_index + dashamsha_index) % 12
        dashamsha_sign = const.SIGNS[dashamsha_sign_index]
        dashamsha[planet] = {"sign": dashamsha_sign}

    trimsamsa = {}
    for planet in const.PLANETS:
        p = chart.get(planet)
        deg_in_sign = p.lon % 30
        if planet in [const.MARS, const.SUN, const.JUPITER]:
            section = int(deg_in_sign // 5)
        else:
            section = int(deg_in_sign // 6)
        trimsamsa[planet] = {"section": section + 1}

    result = {
        "basic_info": {
            "date_of_birth": f"{year}-{month:02}-{date_day:02}",
            "time_of_birth": f"{hours:02}:{minutes:02}",
            "place": {"latitude": latitude, "longitude": longitude},
            "timezone": timezone,
            "ayanamsa": "Lahiri"
        },
        "planetary_positions": planets,
        "ascendant": {
            "sign": asc.sign,
            "longitude": round(asc.lon, 2),
            "lord": const.SIGN_LORDS[const.SIGNS.index(asc.sign)]
        },
        "houses": houses,
        "moon_details": {
            "sign": moon.sign,
            "longitude": round(moon.lon, 2),
            "nakshatra": moon_nakshatra,
            "pada": pada,
            "nakshatra_lord": nakshatra.nakshatraLord(moon.lon)
        },
        "dasha_systems": {
            "vimshottari": vimshottari[:5],
            "char": char_dasha[:5],
            "yogini": yogini_dasha[:5],
            "current_maha_dasha": vimshottari[0] if vimshottari else "Unknown"
        },
        "panchang": {
            "tithi": tithi,
            "vara": vara,
            "yoga": yoga,
            "karana": karana,
            "nakshatra": moon_nakshatra
        },
        "special_conditions": {
            "manglik": manglik,
            "manglik_remedy": manglik_remedy,
            "kalsarpa": kalsarpa,
            "kalsarpa_type": "Partial" if kalsarpa else "None",
            "hora": hora,
            "abhujh_muhurta": abhujh_muhurta
        },
        "divisional_charts": {
            "navamsa": navamsa,
            "dashamsha": dashamsha,
            "trimsamsa": trimsamsa
        },
        "progeny_analysis": child_prediction,
        "advanced_analysis": {
            "shadbala": calculate_shadbala(chart),
            "yogas": calculate_yogas(chart),
            "arudha_padas": calculate_arudha(chart),
            "graha_drishti": calculate_drishti(chart),
            "aspects": calculate_aspects(chart)[:10]
        },
        "yearly_predictions": calculate_varshaphala(chart, 2024),
        "remedial_measures": {
            "gemstones": ["Consult astrologer"],
            "mantras": ["Based on ruling planet"],
            "donations": ["Based on planetary positions"],
            "fasting_days": ["Based on moon nakshatra"]
        },
        "life_areas": {
            "career": chart.get(const.HOUSES[9]).sign,
            "marriage": chart.get(const.HOUSES[6]).sign,
            "wealth": chart.get(const.HOUSES[1]).sign,
            "health": chart.get(const.HOUSES[5]).sign,
            "spirituality": chart.get(const.HOUSES[11]).sign
        }
    }

    return result

@app.post("/kundali")
async def kundali(request: Request):
    data = await request.json()
    result = calculate_all(data)
    return result

@app.get("/")
async def root():
    return {"message": "Vedic Astrology API - Send POST request to /kundali with birth details"}
