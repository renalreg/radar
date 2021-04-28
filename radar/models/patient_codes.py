from collections import OrderedDict

GENDER_MALE = 1
GENDER_FEMALE = 2
GENDER_NOT_SPECIFIED = 9

GENDERS = OrderedDict(
    [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_NOT_SPECIFIED, "Not Specified"),
    ]
)

SIGNED_OFF_NOT_COMPLETE = 0
SIGNED_OFF_NURTURE_BASELINE = 1
SIGNED_OFF_FOLLOW_UP = 2
SIGNED_OFF_FOLLOW_UP_REFUSED = 3
SIGNED_OFF_BASELINE_COMPLETE_NO_FUP = 4

SIGNED_OFF = OrderedDict(
    [
        (SIGNED_OFF_NOT_COMPLETE, "Not signed off"),
        (SIGNED_OFF_NURTURE_BASELINE, "Nurture baseline data complete"),
        (SIGNED_OFF_FOLLOW_UP, "Nurture baseline and follow up data complete"),
        (
            SIGNED_OFF_BASELINE_COMPLETE_NO_FUP,
            "Baseline complete, no FUP as Tx or dialysis",
        ),
        (SIGNED_OFF_FOLLOW_UP_REFUSED, "Patient refused Follow Up"),
    ]
)

ETHNICITIES = OrderedDict(
    [
        ("A", "White - British"),
        ("B", "White - Irish"),
        ("C", "Other White Background"),
        ("D", "Mixed - White and Black Caribbean"),
        ("E", "Mixed - White and Black African"),
        ("F", "Mixed - White and Asian"),
        ("G", "Other Mixed Background"),
        ("H", "Asian or Asian British - Indian"),
        ("J", "Asian or Asian British - Pakistani"),
        ("K", "Asian or Asian British - Bangladeshi"),
        ("L", "Other Asian Background"),
        ("M", "Black Carribean"),
        ("N", "Black African"),
        ("P", "Other Black Background"),
        ("R", "Chinese"),
        ("S", "Other Ethnic Background"),
        ("Z", "Refused / Not Stated"),
    ]
)
