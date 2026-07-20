from .models import CarMake, CarModel

def initiate():
    car_make_data = [
        {"name": "Toyota", "description": "Toyota Motor Corporation is a Japanese multinational automotive manufacturer.", "country": "Japan"},
        {"name": "Ford", "description": "Ford Motor Company is an American multinational automobile manufacturer.", "country": "USA"},
        {"name": "Nissan", "description": "Nissan Motor Co., Ltd. is a Japanese multinational automobile manufacturer.", "country": "Japan"},
        {"name": "Hyundai", "description": "Hyundai Motor Company is a South Korean multinational automotive manufacturer.", "country": "South Korea"},
        {"name": "Kia", "description": "Kia Corporation is a South Korean multinational automobile manufacturer.", "country": "South Korea"},
    ]

    car_make_instances = []
    for data in car_make_data:
        instance, created = CarMake.objects.get_or_create(
            name=data["name"],
            defaults={"description": data["description"], "country": data["country"]}
        )
        car_make_instances.append(instance)

    car_model_data = [
        {"name": "Corolla", "type": "Sedan", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "Camry", "type": "Sedan", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "RAV4", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "F-150", "type": "SUV", "year": 2023, "car_make": car_make_instances[1]},
        {"name": "Explorer", "type": "SUV", "year": 2023, "car_make": car_make_instances[1]},
        {"name": "Mustang", "type": "Convertible", "year": 2023, "car_make": car_make_instances[1]},
        {"name": "Sentra", "type": "Sedan", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "Altima", "type": "Sedan", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "Rogue", "type": "SUV", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "Elantra", "type": "Sedan", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Tucson", "type": "SUV", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Forte", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4]},
        {"name": "Sportage", "type": "SUV", "year": 2023, "car_make": car_make_instances[4]},
    ]

    for data in car_model_data:
        CarModel.objects.get_or_create(
            name=data["name"],
            car_make=data["car_make"],
            defaults={"type": data["type"], "year": data["year"]}
        )

