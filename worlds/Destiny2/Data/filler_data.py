from dataclasses import dataclass

@dataclass
class filler_data():
    id: int
    max: int = None

FILLER_DATA = {
    "filler": filler_data( -1),
}