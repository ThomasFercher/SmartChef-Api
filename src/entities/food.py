from dataclasses import dataclass

@dataclass
class Food:
    fdc_id: str
    description: str
    food_category_id: str

    @classmethod
    def from_dict(cls, data: dict):
        data.pop('_id')
        data.pop('data_type')
        data.pop('publication_date')
        return cls(**data)