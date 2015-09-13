from datetime import date

import ghcnd


def test_parser():
    parser = ghcnd.GHCNParser()

    expected_values = [0.8, 0.0, 4.3, 7.6, 0.8, 21.8, 15.0, 4.6, 0.3, 17.3,
                       1.0, 0.0, 4.6, 0.0, 0.0, 0.8, 27.9, None, 0.0, 3.3, 2.8,
                       0.0, 8.6, 0.8, 0.0, 0.0, 0.0, 1.8, 36.8, 18.8, None]

    test_str = (
        "US1FLAL0004"
        "2014"
        "09"
        "PRCP"
        "    8  N"
        "    0  N"
        "   43  N"
        "   76  N"
        "    8  N"
        "  218  N"
        "  150  N"
        "   46  N"
        "    3  N"
        "  173  N"
        "   10  N"
        "    0  N"
        "   46  N"
        "    0T N"
        "    0  N"
        "    8  N"
        "  279  N"
        "-9999   "
        "    0  N"
        "   33  N"
        "   28  N"
        "    0  N"
        "   86  N"
        "    8  N"
        "    0  N"
        "    0  N"
        "    0  N"
        "   18  N"
        "  368  N"
        "  188  N"
        "-9999   "
    )

    day = 1
    for _id, dt, param, value, sflag, mflag, qflag in parser.parse(test_str):
        assert _id == "US1FLAL0004"
        assert isinstance(dt, date)
        assert dt.month == 9
        assert dt.year == 2014
        assert dt.day == day
        assert param == "PRCP"
        assert sflag == "N" or sflag is None
        assert mflag == "T" or mflag is None
        assert qflag is None
        assert value == expected_values[day - 1]
        day += 1
