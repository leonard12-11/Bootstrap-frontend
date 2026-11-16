"""Codebuch: die Themen, nach denen wir JEV fragen.

Jede Frage ist eine Noul-Frage (Ja/Nein mit Wahrscheinlichkeit 0-1).
Die Fragen sind bewusst eng und woertlich formuliert (JEV liest woertlich, siehe
docs.typesafe.ai/model-jaggedness).
"""

# Lesbarer Name (Deutsch), Teilnote die das Thema abdeckt (None = keine), Frage an JEV
THEMES = {
    "complaint": ("Beschwerde (irgendeine)", None,
        "The guest describes at least one problem, complaint or disappointment with the hotel or the stay."),
    "staff_service": ("Personal & Service", None,
        "The guest complains about hotel staff or service: rude, unfriendly, unhelpful, incompetent or slow staff, or poor customer service."),
    "checkin_booking": ("Check-in, Reservation & Rechnung", None,
        "The guest complains about check-in, check-out, the reservation or billing: long waits, room not ready, booking errors, wrong room type, or being charged incorrectly."),
    "cleanliness": ("Sauberkeit & Geruch", "cleanliness",
        "The guest complains that the room, bathroom, bed or hotel was dirty, smelly or not cleaned properly."),
    "pests": ("Ungeziefer (Bettwanzen etc.)", "cleanliness",
        "The guest reports bed bugs, cockroaches, mice or other pests."),
    "room_condition": ("Zustand: alt, abgenutzt, defekt", "rooms",
        "The guest complains that the room or hotel is old, worn, outdated, run-down or in need of renovation, or that things in the room were broken."),
    "room_size": ("Zimmer zu klein", "rooms",
        "The guest complains that the room was too small or cramped."),
    "bathroom_plumbing": ("Bad, Dusche, Wasser", "rooms",
        "The guest complains about the bathroom, shower, water pressure, hot water or plumbing."),
    "ac_heating": ("Klimaanlage & Heizung", "rooms",
        "The guest complains about air conditioning, heating, or the room being too hot or too cold."),
    "noise": ("Lärm", "sleep_quality",
        "The guest complains about noise: from other guests, the street, construction, thin walls or hotel equipment."),
    "bed_comfort": ("Bett & Kissen", "sleep_quality",
        "The guest complains that the bed, mattress or pillows were uncomfortable."),
    "price_value": ("Preis & Zusatzgebühren", "value",
        "The guest complains that the hotel is overpriced or poor value for money, or about hidden or extra fees."),
    "food_breakfast": ("Frühstück, Restaurant, Bar", None,
        "The guest complains about breakfast, food, the restaurant or the bar."),
    "wifi": ("WLAN & Internet", None,
        "The guest complains about internet or WiFi: missing, slow, unreliable or expensive."),
    "parking": ("Parkieren & Valet", None,
        "The guest complains about parking or valet service: cost, availability or how the car was handled."),
    "location_safety": ("Lage & Sicherheit der Umgebung", "location",
        "The guest complains about the hotel's location or neighbourhood: far from things, inconvenient, or felt unsafe."),
    "facilities": ("Einrichtungen (Pool, Gym, Lift, Lobby)", None,
        "The guest complains about hotel facilities such as the pool, gym, elevators, lobby or spa."),
}

TOPICS = [k for k in THEMES if k != "complaint"]
LABEL = {k: v[0] for k, v in THEMES.items()}
SUBSCORE = {k: v[1] for k, v in THEMES.items()}

# Schwellen gemaess JEV-Doku (Reading a Noul): >0.7 = ja, <0.3 = nein, dazwischen = unsicher
YES, NO = 0.7, 0.3
