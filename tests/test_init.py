import ghcnd


def test_instantiation_of_parser():
    parser = ghcnd.GHCNParser()
    assert parser
