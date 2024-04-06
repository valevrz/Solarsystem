import yaml
import openpyxl

def readFile(file: str) :
    with open('solar_system.yaml', 'r') as file:
        sun_system_data = yaml.safe_load(file)
        return sun_system_data

def safeData(sun_system_data) :
    planets_distances = {}

    for planet_data in sun_system_data['sun_system']['distance_to_sun']:
        # Extrahiere den Planetennamen und die Distanz aus dem Eintrag
        planet, distance = list(planet_data.items())[0]
        # Füge den Planeten und die Distanz dem Dictionary hinzu
        planets_distances[planet] = distance
    return planets_distances

def maxDistance(planets_distances) :
    max = {}

    for planet, distance in planets_distances.items():
        max[planet] = {}
        for planet2 in planets_distances:
            if planet == planet2:
                max[planet][planet2] = 0
            else:
                max[planet][planet2] = round((distance + planets_distances[planet2]), 2)
    return max

def minDistance(planets_distances) :
    min = {}

    for planet, distance in planets_distances.items():
        min[planet] = {}
        for planet2 in planets_distances:
            if planet == planet2:
                min[planet][planet2] = 0
            else:
                minDis = (distance - planets_distances[planet2])
                if minDis < 0:
                    min[planet][planet2] = (round(minDis, 2)) * -1
                else:
                    min[planet][planet2] = round(minDis, 2)
    return min

def write_to_excel(data, filename):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Write headers
    sheet.append([""] + list(data.keys()))

    # Write data
    for planet, distances in data.items():
        row = [planet]
        for planet2, distance in distances.items():
            row.append(distance)
        sheet.append(row)

    # Save the workbook
    workbook.save(filename)

sun_system_data = readFile("solar_system.yaml")
planets_distances = safeData(sun_system_data)
max_distances = maxDistance(planets_distances)
min_distances = minDistance(planets_distances)

write_to_excel(max_distances, "max_distances.xlsx")
write_to_excel(min_distances, "min_distances.xlsx")