from enum import Enum


class Attribute(Enum):
    YEAR = 0  # year
    BHK = 1
    RENT = 2
    SIZE = 3
    FLOOR = 4  # just floor
    TOTAL_FLOOR = 5
    AREA_LOCALITY = 6
    SUPER_AREA = 7
    BANGALORE = 8
    CHENNAI = 9
    BATHROOM = 10
    DELHI = 11
    HYDERABAD = 12
    KOLKATA = 13
    MUMBAI = 14
    SEMI_FURNISHED = 15
    UNFURNISHED = 16
    FURNISHED = 17
    BACHELORS_FAMILY = 18
    BACHELORS = 19
    FAMILY = 20
    CONTACT_OWNER = 21
    CONTACT_AGENT = 22
    CONTACT_BUILDER = 23
    DAY_OF_THE_WEEK = 24
    DAY_OF_THE_MONTH = 25
    MONTH_OF_THE_YEAR = 26
    QUARTER_OF_THE_YEAR = 27
    BUILT_AREA = 28
    CARPET_AREA = 29


class OldAttribute(Enum):
    POSTED_ON = 0
    BHK = 1
    RENT = 2
    SIZE = 3
    FLOOR = 4  # at first floor + total floors
    AREA_TYPE = 5
    AREA_LOCALITY = 6
    CITY = 7
    FURNISHING_STATUS = 8
    TENANT_PREFFERED = 9
    BATHROOM = 10
    POINT_OF_CONTACT = 11


ATTRIBUTES_FOR_MODEL = [
    Attribute.YEAR,
    Attribute.BHK,
    Attribute.SIZE,
    Attribute.FLOOR,
    Attribute.TOTAL_FLOOR,
    Attribute.AREA_LOCALITY,
    Attribute.SUPER_AREA,
    Attribute.BANGALORE,
    Attribute.CHENNAI,
    Attribute.BATHROOM,
    Attribute.DELHI,
    Attribute.HYDERABAD,
    Attribute.KOLKATA,
    Attribute.MUMBAI,
    Attribute.SEMI_FURNISHED,
    Attribute.UNFURNISHED,
    Attribute.FURNISHED,
    Attribute.BACHELORS_FAMILY,
    Attribute.BACHELORS,
    Attribute.FAMILY,
    Attribute.CONTACT_OWNER,
    Attribute.CONTACT_AGENT,
    Attribute.CONTACT_BUILDER,
    Attribute.DAY_OF_THE_WEEK,
    Attribute.DAY_OF_THE_MONTH,
    Attribute.MONTH_OF_THE_YEAR,
    Attribute.QUARTER_OF_THE_YEAR,
    Attribute.BUILT_AREA,
    Attribute.CARPET_AREA,
]


class AttributeType(Enum):
    ORDINAL = 0
    NOMINAL = 1
    CONTINUAL = 2


ATTRIBUTE_TYPE = {
    Attribute.YEAR: AttributeType.ORDINAL,
    Attribute.BHK: AttributeType.ORDINAL,
    Attribute.RENT: AttributeType.CONTINUAL,
    Attribute.SIZE: AttributeType.CONTINUAL,
    Attribute.FLOOR: AttributeType.ORDINAL,
    Attribute.AREA_LOCALITY: AttributeType.CONTINUAL,  # transformed to frequency by DataProcessor
    Attribute.BATHROOM: AttributeType.ORDINAL,
    Attribute.TOTAL_FLOOR: AttributeType.ORDINAL,
    Attribute.DAY_OF_THE_WEEK: AttributeType.ORDINAL,
    Attribute.DAY_OF_THE_MONTH: AttributeType.ORDINAL,
    Attribute.MONTH_OF_THE_YEAR: AttributeType.ORDINAL,
    Attribute.QUARTER_OF_THE_YEAR: AttributeType.ORDINAL,
    Attribute.BUILT_AREA: AttributeType.NOMINAL,
    Attribute.CARPET_AREA: AttributeType.NOMINAL,
    Attribute.SUPER_AREA: AttributeType.NOMINAL,
    Attribute.BANGALORE: AttributeType.NOMINAL,
    Attribute.CHENNAI: AttributeType.NOMINAL,
    Attribute.DELHI: AttributeType.NOMINAL,
    Attribute.HYDERABAD: AttributeType.NOMINAL,
    Attribute.KOLKATA: AttributeType.NOMINAL,
    Attribute.MUMBAI: AttributeType.NOMINAL,
    Attribute.SEMI_FURNISHED: AttributeType.NOMINAL,
    Attribute.UNFURNISHED: AttributeType.NOMINAL,
    Attribute.FURNISHED: AttributeType.NOMINAL,
    Attribute.BACHELORS_FAMILY: AttributeType.NOMINAL,
    Attribute.BACHELORS: AttributeType.NOMINAL,
    Attribute.FAMILY: AttributeType.NOMINAL,
    Attribute.CONTACT_OWNER: AttributeType.NOMINAL,
    Attribute.CONTACT_AGENT: AttributeType.NOMINAL,
    Attribute.CONTACT_BUILDER: AttributeType.NOMINAL,
}
