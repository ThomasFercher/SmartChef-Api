from dataclasses import dataclass
import json 

def try_float(value, default=None):
    try:
        return float(value)
    except ValueError:
        return default


@dataclass
class Food:
    id: int
    name: str
    category: str
    unit: str
    calories: int
    joules: int
    fat: float
    saturatedFat: float
    monoSaturatedFat: float
    polySaturatedFat: float
    cholesterol_mg: float
    carbohydrates: float
    sugars: float
    starch: float
    fiber: float
    protein: float
    salt: float
    alcohol: float
    water: float
    vitaminA_RE_µgRE: float
    vitaminA_RAE_µgRE: float
    retinol_µg: float
    betaCaroteneActivity_µgBCE: float
    betaCarotene_µg: float
    vitaminB1Thiamin_µg: float
    vitaminB2Riboflavin_µg: float
    vitaminB6Pyridoxine_µg: float
    vitaminB12Cobalamin_µg: float
    niacin_mg: float
    folate_µg: float
    panthothenicAcid_mg: float
    vitaminC_mg: float
    vitaminD_µg: float
    vitaminEActivity_mgATE: float
    potassium_mg: float
    sodium_mg: float
    chloride_mg: float
    calcium_mg: float
    magnesium_mg: float
    phosphorus_mg: float
    iron_mg: float
    iodide_µg: float
    zinc_mg: float
    selenium_µg: float


    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


    @classmethod
    def from_dict(cls, data: dict):
        data.pop("_id")

        return cls(
            id=int(data.get("ID", "")),
            name=data.get("Name", ""),
            category=data.get("Category", ""),
            unit=data.get("Matrix unit", ""),
            calories=int(data.get("Energy, kilocalories (kcal)", None)),
            joules=int(data.get("Energy, kilojoules (kJ)", None)),
            fat=try_float(
                data.get("Fat, total (g)", None),
            ),
            saturatedFat=try_float(data.get("Fatty acids, saturated (g)", None)),
            monoSaturatedFat=try_float(
                data.get("Fatty acids, monounsaturated (g)", None)
            ),
            polySaturatedFat=try_float(
                data.get("Fatty acids, polyunsaturated (g)", None)
            ),
            cholesterol_mg=try_float(data.get("Cholesterol (mg)", None)),
            carbohydrates=try_float(data.get("Carbohydrates, available (g)", None)),
            sugars=try_float(data.get("Sugars (g)", None)),
            starch=try_float(data.get("Starch (g)", None)),
            fiber=try_float(data.get("Dietary fibres (g)", None)),
            protein=try_float(data.get("Protein (g)", None)),
            salt=try_float(data.get("Salt (NaCl) (g)", None)),
            alcohol=try_float(data.get("Alcohol (g)", None)),
            water=try_float(data.get("Water (g)", None)),
            vitaminA_RE_µgRE=try_float(
                data.get("Vitamin A activity, RE (µg-RE)", None)
            ),
            vitaminA_RAE_µgRE=try_float(
                data.get("Vitamin A activity, RAE (µg-RE)", None)
            ),
            retinol_µg=try_float(data.get("Retinol (µg)", None)),
            betaCaroteneActivity_µgBCE=try_float(
                data.get("Beta- carotene activity (µg-BCE)", None)
            ),
            betaCarotene_µg=try_float(data.get("Beta-carotene (µg)", None)),
            vitaminB1Thiamin_µg=try_float(data.get("Vitamin B1 (thiamine) (mg)", None)),
            vitaminB2Riboflavin_µg=try_float(
                data.get("Vitamin B2 (riboflavin) (mg)", None)
            ),
            vitaminB6Pyridoxine_µg=try_float(
                data.get("Vitamin B6 (pyridoxine) (mg)", None)
            ),
            vitaminB12Cobalamin_µg=try_float(
                data.get("Vitamin B12 (cobalamin) (µg)", None)
            ),
            niacin_mg=try_float(data.get("Niacin (mg)", None)),
            folate_µg=try_float(data.get("Folate (µg)", None)),
            panthothenicAcid_mg=try_float(data.get("Panthotenic acid (mg)", None)),
            vitaminC_mg=try_float(data.get("Vitamin C (ascorbic acid) (mg)", None)),
            vitaminD_µg=try_float(data.get("Vitamin D (calciferol) (µg)", None)),
            vitaminEActivity_mgATE=try_float(
                data.get("Vitamin E activity (mg-ATE)", None)
            ),
            potassium_mg=try_float(data.get("Potassium (K) (mg)", None)),
            sodium_mg=try_float(data.get("Sodium (Na) (mg)", None)),
            chloride_mg=try_float(data.get("Chloride (Cl) (mg)", None)),
            calcium_mg=try_float(data.get("Calcium (Ca) (mg)", None)),
            magnesium_mg=try_float(data.get("Magnesium (Mg) (mg)", None)),
            phosphorus_mg=try_float(data.get("Phosphorus (P) (mg)", None)),
            iron_mg=try_float(data.get("Iron (Fe) (mg)", None)),
            iodide_µg=try_float(data.get("Iodide (I) (µg)", None)),
            zinc_mg=try_float(data.get("Zinc (Zn) (mg)", None)),
            selenium_µg=try_float(data.get("Selenium (Se) (µg)", None)),
        )
