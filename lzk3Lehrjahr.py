from __future__ import annotations

from typing import Callable

import yaml

TEXT_BUFFER_OFFSET = 1


class Planet:
	def __init__(self, data: dict):
		# planet name is the key of the dict, distance is the value
		self.name = list(data.keys())[0]
		self.distance_from_sun = data[self.name]
	
	def minimal_distance_to(self, other: Planet) -> float:
		return abs(other.distance_from_sun - self.distance_from_sun)
	
	def maximal_distance_to(self, other: Planet) -> float:
		if other == self:
			return 0
		
		return other.distance_from_sun + self.distance_from_sun
	
	def __repr__(self) -> str:
		return f"{self.name}: {self.distance_from_sun}"
	
	def __str__(self) -> str:
		return f"{self.name}"
	
	def __eq__(self, other) -> bool:
		if isinstance(other, Planet):
			return other.name == self.name
		return False


class FileWriter:
	def __init__(self, path: str, max_length: int):
		self.file = open(path, "w")
		self.max_length = max_length
	
	def __repr__(self) -> str:
		return f"{self.file.name} ({self.max_length})"
	
	def __str__(self) -> str:
		return self.file.name
	
	def close(self) -> None:
		self.file.close()
	
	def write(self, content: str, end: str = "\n") -> None:
		self.file.write(f"{content}{end}")
	
	def write_header(self, planets: list[Planet]) -> None:
		buffer = " " * self.max_length
		self.write(buffer + (" | ".join([planet.name.rjust(self.max_length, " ") for planet in planets])))
	
	@staticmethod
	def _format_distance(distance: float, max_length: int) -> str:
		return "{:.2f}".format(distance).rjust(max_length, " ")
	
	def _write_planet_name(self, planet: Planet) -> None:
		self.write(planet.name.rjust(self.max_length - TEXT_BUFFER_OFFSET, " ") + "|", end="")
	
	def _write_distances(self, distances: list[float]) -> None:
		self.write(" | ".join([self._format_distance(distance, self.max_length) for distance in distances]))

	def write_line(self, planet: Planet, distances: list[float]) -> None:
		self._write_planet_name(planet)
		self._write_distances(distances)


def write_file(file: str, planets: list[Planet], operation: Callable[[Planet, Planet], float]) -> None:
	max_length = len(max([planet.name for planet in planets], key=len)) + TEXT_BUFFER_OFFSET

	output_file = FileWriter(file, max_length)
	
	output_file.write_header(planets)
	
	for planet1 in planets:
		distances: list[float] = []
		
		for planet2 in planets:
			distances.append(operation(planet2, planet1))
		
		output_file.write_line(planet1, distances)
	
	output_file.close()


def main() -> None:
	with open("solar_system.yaml", "r") as input_file:
		solar_system = yaml.safe_load(input_file)
	
	planets_data: list[dict[str, int]] = solar_system['sun_system']['distance_to_sun']
	
	planets = [Planet(data) for data in planets_data]
	
	write_file("minimal-distances.txt", planets, lambda p1, p2: p1.minimal_distance_to(p2))
	write_file("maximal-distances.txt", planets, lambda p1, p2: p1.maximal_distance_to(p2))


if __name__ == "__main__":
	main()
