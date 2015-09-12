# -*- coding: utf-8 -*-
"""
    ghcnd
    ~~~~~

    Global Historical Climate Network (GHCN) database parsing class.
"""
from calendar import monthrange
from datetime import datetime

import pandas


def _RAW(x):
    return x


def _TENTHS(x):
    return x / 10.


def _PERCENT(x):
    return x / 100.


def _HHMM(x):
    # TODO lambda x: time(int(x[:2]), int(x[2:]))
    return _RAW(x)


class GHCNParser(object):
    #: List of all possible parameters that could be found within the GHCN
    #: database, per the 3.11 documentation.
    #:
    #: .. seealso::
    #:
    #:     Additional information on the meaning of all given parameters in the
    #:     GHCN database can be found in the `official README file associated
    #:     with GHCN
    #:     <http://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt>`_.
    parameters = ["ACMC", "ACMH", "ACSC", "ACSH", "AWDR", "AWND", "DAEV",
                  "DAPR", "DASF", "DATN", "DATX", "DAWM", "DWPR", "EVAP",
                  "FMTM", "FRGB", "FRGT", "FRTH", "GAHT", "MDEV", "MDPR",
                  "MDSF", "MDTN", "MDTX", "MDWM", "MNPN", "MXPN", "PGTM",
                  "PRCP", "PSUN", "SN01", "SN02", "SN03", "SN04", "SN05",
                  "SN06", "SN07", "SN11", "SN12", "SN13", "SN14", "SN15",
                  "SN16", "SN17", "SN21", "SN22", "SN23", "SN24", "SN25",
                  "SN26", "SN27", "SN31", "SN32", "SN33", "SN34", "SN35",
                  "SN36", "SN37", "SN41", "SN42", "SN43", "SN44", "SN45",
                  "SN46", "SN47", "SN51", "SN52", "SN53", "SN54", "SN55",
                  "SN56", "SN57", "SN61", "SN62", "SN63", "SN64", "SN65",
                  "SN66", "SN67", "SN71", "SN72", "SN73", "SN74", "SN75",
                  "SN76", "SN77", "SN81", "SN82", "SN83", "SN84", "SN85",
                  "SN86", "SN87", "SNOW", "SNWD", "SX01", "SX02", "SX03",
                  "SX04", "SX05", "SX06", "SX07", "SX11", "SX12", "SX13",
                  "SX14", "SX15", "SX16", "SX17", "SX21", "SX22", "SX23",
                  "SX24", "SX25", "SX26", "SX27", "SX31", "SX32", "SX33",
                  "SX34", "SX35", "SX36", "SX37", "SX41", "SX42", "SX43",
                  "SX44", "SX45", "SX46", "SX47", "SX51", "SX52", "SX53",
                  "SX54", "SX55", "SX56", "SX57", "SX61", "SX62", "SX63",
                  "SX64", "SX65", "SX66", "SX67", "SX71", "SX72", "SX73",
                  "SX74", "SX75", "SX76", "SX77", "SX81", "SX82", "SX83",
                  "SX84", "SX85", "SX86", "SX87", "TAVG", "THIC", "TMAX",
                  "TMIN", "TOBS", "TSUN", "WDF1", "WDF2", "WDF5", "WDFG",
                  "WDFI", "WDFM", "WDMV", "WESD", "WESF", "WSF1", "WSF2",
                  "WSF5", "WSFG", "WSFI", "WSFM", "WT01", "WT02", "WT03",
                  "WT04", "WT05", "WT06", "WT07", "WT08", "WT09", "WT10",
                  "WT11", "WT12", "WT13", "WT14", "WT15", "WT16", "WT17",
                  "WT18", "WT19", "WT21", "WT22", "WV01", "WV03", "WV07",
                  "WV18", "WV20"]

    #: Map of `parameters` to functions that will convert DLY formatted
    #: parameter values into to Python objects.
    parsers = {}

    def __init__(self, *args, **kwargs):
        self._init_parsers()

    def _init_parsers(self):
        """Initialize parameter/parsing function pairs.

        Functions for parsing variables from the DLY format.

        """
        self.parsers = {}

        # Assume that most entries in the GHCN file are tenths of some number
        for param in self.parameters:
            self.parsers[param] = _TENTHS

        # The value is fine how it is as it comes in to GHCN, so do not change
        for param in ["DAEV", "DAPR", "DASF", "DATN", "DATX", "DAWM", "DWPR",
                      "FRGB", "FRGT", "FRTH", "GAHT", "MDWM", "SNOW", "SNWD",
                      "WDF1", "WDF2", "WDF5", "WDFG", "WDFI", "WDFM", "WDMV",
                      "WT01", "WT02", "WT03", "WT04", "WT05", "WT06", "WT07",
                      "WT08", "WT09", "WT10", "WT11", "WT12", "WT13", "WT14",
                      "WT15", "WT16", "WT17", "WT18", "WT19", "WT21", "WT22",
                      "WV01", "WV03", "WV07", "WV18", "WV20"]:
            self.parsers[param] = _RAW

        # Convert parameters that are percents into proper percents
        for param in ["ACMC", "ACMH", "ACSC", "ACSH", "PSUN"]:
            self.parsers[param] = _PERCENT

        # Convert the time from HHMM string to `time`
        for param in ["FMTM", "PGTM"]:
            self.parsers[param] = _HHMM

    def read(self, filename):
        """Read GHCN formatted files into a native data structure or object.
        """

        index_tuples = []
        data = []

        fh = open(filename, "r")

        for r in fh:
            n = self.parse_dly_row(r)
            days_in_month = monthrange(n["year"], n["month"])[1]

            for day in range(days_in_month):
                idd = n["id"]
                dt = datetime(n["year"], n["month"], day + 1)
                param = n["element"]

                # apply parsing function to pull it into reality
                fn = self.parsers[param]
                vl = fn(float(n["value" + str(day + 1)]))

                sf = n["sflag" + str(day + 1)]
                mf = n["mflag" + str(day + 1)]
                qf = n["qflag" + str(day + 1)]

                index_tuples.append((idd, dt, param))
                data.append([vl, sf, mf, qf])

        fh.close()

        df = pandas.DataFrame(
            data,
            index=pandas.MultiIndex.from_tuples(
                index_tuples,
                names=["id", "dt", "parameter"]
            ),
            columns=["value", "sflag", "mflag", "qflag"]
        )

        return df

    def parse_dly_row(self, ghcn_row):
        """Pythonifies the GHCN daily formatted row based on the specification
        as defined by :meth:`dly_dict`
        """

        fields = self.dly_dict()

        results = {}
        for param in fields:
            idx0 = fields[param][0] - 1
            idx1 = fields[param][1]
            parsing_fn = fields[param][2]

            results[param] = parsing_fn(ghcn_row[idx0:idx1].strip())

            # Convert GHCN missing value to Python understood missing value
            if (results[param] == -9999) or (results[param] == ""):
                results[param] = None

        return results

    def dly_dict(self):
        """Template of fields, columns and type-casting functions of the
        GHCN-daily formatted file (dly)

        :returns: dictionary of fields, columns and type-casting function per
                  row of GHCN daily (dly) file
        :rtype: :class:`dict`

        """
        fields = {
            "id": (1, 11, str),
            "year": (12, 15, int),
            "month": (16, 17, int),
            "element": (18, 21, str),
        }

        value_fields = {
            "value": (22, 26, int),
            "mflag": (27, 27, str),
            "qflag": (28, 28, str),
            "sflag": (29, 29, str),
        }

        for day in range(31):
            for f in value_fields:
                fields[f + str(day + 1)] = (value_fields[f][0] + day * 8,
                                            value_fields[f][1] + day * 8,
                                            value_fields[f][2])

        return fields
