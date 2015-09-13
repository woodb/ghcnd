from datetime import date

import ghcnd


def test_instantiation_of_parser():
    parser = ghcnd.GHCNParser()

    test_str = (
        "US1FLAL0004201409PRCP    8  N    0  N   43  N   76  N    8  N  "
        "218  N  150  N   46  N    3  N  173  N   10  N    0  N   46  N    "
        "0T N    0  N    8  N  279  N-9999       0  N   33  N   28  N    "
        "0  N   86  N    8  N    0  N    0  N    0  N   18  N  368  N  "
        "188  N-9999   "
    )

    day = 1
    for _id, dt, param, value, sflag, mflag, qflag in parser.parse(test_str):
        assert _id == "US1FLAL0004"
        assert isinstance(dt, date)
        assert dt.month == 9
        assert dt.year == 2014
        assert dt.day == day
        day += 1
