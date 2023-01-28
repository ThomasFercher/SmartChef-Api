from dataclasses import dataclass

@dataclass
class FoodNutrientMapping:
    id: str
    fdc_id: str
    nutrient_id: str
    amount: str


    @classmethod
    def from_dict(cls, data: dict):
        data.pop('_id')
        data.pop('data_points')
        data.pop('derivation_id')
        return cls(**data)