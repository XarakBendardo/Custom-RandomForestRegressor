from src.utilities import get_data_path, get_transformed_data_path, average
from src.Attributes import (
    Attribute,
    ATTRIBUTE_TYPE,
    AttributeType,
    OldAttribute,
)
from src.LinearRegression import LinearRegressionModel
import random
import csv
from statistics import mode
import pandas as pd
from datetime import datetime


class DataProcessor:
    regression_model: LinearRegressionModel
    data: list

    @staticmethod
    def _get_descrete_values_probability(attribute: int) -> dict:
        def get_values_dict() -> dict:
            values = {}
            for example in DataProcessor.data:
                if values.get(example[attribute]) is None:
                    values[example[attribute]] = 1
                else:
                    values[example[attribute]] += 1
            return values

        total = len(DataProcessor.data)
        values_freq = get_values_dict()
        for key in values_freq.keys():
            values_freq[key] = values_freq[key] / total
        return values_freq

    @staticmethod
    def _remove_duplicates() -> None:
        columns = [str(attrib) for attrib in OldAttribute]
        df = pd.DataFrame(DataProcessor.data, columns=columns)
        df = df.drop_duplicates(keep="first")
        DataProcessor.data = df.values.tolist()

    @staticmethod
    def _append_additional_data() -> None:
        for example in DataProcessor.data:
            for _ in range(18):
                example.append(None)

    @staticmethod
    def _transform_descrete_to_probability(attribute: int) -> None:
        values_freq = DataProcessor._get_descrete_values_probability(attribute)
        for example in DataProcessor.data:
            example[attribute] = str(values_freq.get(example[attribute]))

    @staticmethod
    def _extract_floor_and_data() -> None:
        for example in DataProcessor.data:
            data = example[OldAttribute.POSTED_ON.value]
            example[Attribute.YEAR.value] = int(data.split("-")[0])
            floor_str = example[OldAttribute.FLOOR.value]
            floor = floor_str.split(" ")[0]
            if floor == "Ground":
                floor = 0
            elif floor == "Upper":
                floor = 0
            elif floor == "Lower":
                floor = -1
            else:
                floor = int(floor) + 1
            total_floors = floor_str.split(" ")[-1]
            if total_floors == "Ground":
                total_floors = 0
            else:
                total_floors = int(total_floors)
            example[Attribute.FLOOR.value] = floor
            example[Attribute.TOTAL_FLOOR.value] = total_floors
            example[Attribute.DAY_OF_THE_WEEK.value] = (
                datetime.strptime(data, "%Y-%m-%d").weekday() + 1
            )
            example[Attribute.DAY_OF_THE_MONTH.value] = int(data.split("-")[2])
            example[Attribute.MONTH_OF_THE_YEAR.value] = int(data.split("-")[1])
            example[Attribute.QUARTER_OF_THE_YEAR.value] = (
                int((int(data.split("-")[1]) - 1) / 3) + 1
            )

    @staticmethod
    def _extract_true_false() -> None:
        for example in DataProcessor.data:
            furnishing_status = example[OldAttribute.FURNISHING_STATUS.value]
            tenants = example[OldAttribute.TENANT_PREFFERED.value]
            point_of_contact = example[OldAttribute.POINT_OF_CONTACT.value]
            city = example[OldAttribute.CITY.value]
            area_type = example[OldAttribute.AREA_TYPE.value]
            example[Attribute.FURNISHED.value] = 0
            example[Attribute.SEMI_FURNISHED.value] = 0
            example[Attribute.UNFURNISHED.value] = 0
            example[Attribute.FAMILY.value] = 0
            example[Attribute.BACHELORS.value] = 0
            example[Attribute.BACHELORS_FAMILY.value] = 0
            example[Attribute.CONTACT_OWNER.value] = 0
            example[Attribute.CONTACT_AGENT.value] = 0
            example[Attribute.CONTACT_BUILDER.value] = 0
            example[Attribute.BANGALORE.value] = 0
            example[Attribute.MUMBAI.value] = 0
            example[Attribute.CHENNAI.value] = 0
            example[Attribute.DELHI.value] = 0
            example[Attribute.HYDERABAD.value] = 0
            example[Attribute.KOLKATA.value] = 0
            example[Attribute.BUILT_AREA.value] = 0
            example[Attribute.CARPET_AREA.value] = 0
            example[Attribute.SUPER_AREA.value] = 0

            if furnishing_status == "Unfurnished":
                example[Attribute.UNFURNISHED.value] = 1
            elif furnishing_status == "Semi-Furnished":
                example[Attribute.SEMI_FURNISHED.value] = 1
            else:
                example[Attribute.FURNISHED.value] = 1
            if tenants == "Family":
                example[Attribute.FAMILY.value] = 1
            elif tenants == "Bachelors":
                example[Attribute.BACHELORS.value] = 1
            else:
                example[Attribute.BACHELORS_FAMILY.value] = 1
            if point_of_contact == "Owner":
                example[Attribute.CONTACT_OWNER.value] = 1
            elif point_of_contact == "Agent":
                example[Attribute.CONTACT_AGENT.value] = 1
            else:
                example[Attribute.CONTACT_BUILDER.value] = 1
            if city == "Bangalore":
                example[Attribute.BANGALORE.value] = 1
            elif city == "Mumbai":
                example[Attribute.MUMBAI.value] = 1
            elif city == "Chennai":
                example[Attribute.CHENNAI.value] = 1
            elif city == "Delhi":
                example[Attribute.DELHI.value] = 1
            elif city == "Hyderabad":
                example[Attribute.HYDERABAD.value] = 1
            else:
                example[Attribute.KOLKATA.value] = 1
            if area_type == "Built Area":
                example[Attribute.BUILT_AREA.value] = 1
            elif area_type == "Carpet Area":
                example[Attribute.CARPET_AREA.value] = 1
            else:
                example[Attribute.SUPER_AREA.value] = 1

    @staticmethod
    def get_data_from_file() -> None:
        rows = []
        with open(get_data_path(), "r") as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(row)
        DataProcessor.data = rows[1:]

    @staticmethod
    def save_transformed_data() -> None:
        with open(get_transformed_data_path(), "w") as file:
            writer = csv.writer(file)
            writer.writerows(map(lambda row: map(str, row), DataProcessor.data))

    @staticmethod
    def get_transformed_data_from_file() -> None:
        DataProcessor.data = []
        with open(get_transformed_data_path(), "r") as file:
            reader = csv.reader(file)
            for exampl in reader:
                for attrib in Attribute:
                    val = exampl[attrib.value]
                    exampl[attrib.value] = int(val) if val.isdigit() else float(val)
                DataProcessor.data.append(exampl)

    @staticmethod
    def transform_data() -> None:
        DataProcessor._remove_duplicates()
        DataProcessor._append_additional_data()
        DataProcessor._transform_descrete_to_probability(
            OldAttribute.AREA_LOCALITY.value
        )
        DataProcessor._extract_floor_and_data()
        DataProcessor._extract_true_false()

    @staticmethod
    def split_set(test_size: float = 0.3) -> tuple:
        """Split data to test set and training set (in given order)"""
        test_size = int(len(DataProcessor.data) * test_size)
        random.shuffle(DataProcessor.data)
        return [DataProcessor.data[:test_size], DataProcessor.data[test_size:]]
