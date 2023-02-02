from dataclasses import dataclass

@dataclass
class Nutrient:
    id: str
    name: str
    unit_name: str
    nutrient_nbr: str


    @classmethod
    def from_dict(cls, data: dict):
        data.pop('_id')
        data.pop('rank')
        return cls(**data)