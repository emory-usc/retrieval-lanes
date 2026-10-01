"""Synthetic knowledge corpus.

Twelve documents about space exploration, each with a stable id, a category,
and tags. Everything here is hand-written synthetic content — no real source
material is involved.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    category: str
    tags: tuple[str, ...]
    body: str


DOCS: list[Document] = [
    Document(
        "doc-001",
        "Reusable Rocket Boosters",
        "technology",
        ("rocketry", "reusability", "cost"),
        "Reusable boosters return to Earth and land vertically so they can be "
        "flown again, sharply lowering the cost per launch. Grid fins and "
        "landing legs guide the stage back to the pad or a droneship.",
    ),
    Document(
        "doc-002",
        "The Saturn V Program",
        "mission",
        ("apollo", "moon", "saturn"),
        "Saturn V was the launch vehicle for the Apollo program. It carried "
        "astronauts toward the Moon across the late 1960s and early 1970s.",
    ),
    Document(
        "doc-003",
        "Apollo 11 Landing",
        "mission",
        ("apollo", "moon", "1969"),
        "Apollo 11 landed on the Moon in July 1969. The crew deployed "
        "instruments, collected samples, and returned safely to Earth.",
    ),
    Document(
        "doc-004",
        "Lunar Sample Analysis",
        "science",
        ("moon", "geology", "apollo"),
        "Lunar samples returned by Apollo showed the Moon's crust is largely "
        "anorthosite, informing theories of how the Moon formed.",
    ),
    Document(
        "doc-005",
        "Orbital Mechanics Basics",
        "science",
        ("physics", "orbits"),
        "Orbits are governed by Kepler's laws. A change in velocity alters the "
        "shape of an orbit; gravity assists trade momentum with a planet.",
    ),
    Document(
        "doc-006",
        "The Space Shuttle Era",
        "mission",
        ("shuttle", "reusability", "history"),
        "The Space Shuttle was a partially reusable orbital vehicle flown from "
        "1981 to 2011, used to build and service the International Space Station.",
    ),
    Document(
        "doc-007",
        "The International Space Station",
        "station",
        ("iss", "orbit", "cooperation"),
        "The ISS is a modular laboratory in low Earth orbit, assembled through "
        "international cooperation and continuously crewed since 2000.",
    ),
    Document(
        "doc-008",
        "Mars Rovers",
        "science",
        ("mars", "robotics"),
        "Rovers on Mars, from Sojourner to Perseverance, have analyzed soil, "
        "searched for signs of past water, and cached samples for return.",
    ),
    Document(
        "doc-009",
        "Crewed Mars Mission Planning",
        "planning",
        ("mars", "crew", "future"),
        "A crewed Mars mission requires long-duration life support, radiation "
        "shielding, and in-situ resource utilization to reduce the mass launched.",
    ),
    Document(
        "doc-010",
        "Deep Space Network",
        "technology",
        ("communications", "tracking"),
        "The Deep Space Network uses large antennas on three continents to "
        "communicate with spacecraft across the solar system.",
    ),
    Document(
        "doc-011",
        "Gravity Assist Maneuvers",
        "science",
        ("physics", "orbits", "trajectory"),
        "A gravity assist uses a planet's motion to change a spacecraft's "
        "trajectory and speed without expending propellant.",
    ),
    Document(
        "doc-012",
        "Commercial Crew Program",
        "planning",
        ("crew", "commercial", "future"),
        "The commercial crew program funds private spacecraft to transport "
        "astronauts to and from the International Space Station.",
    ),
]

DOC_BY_ID = {d.id: d for d in DOCS}
