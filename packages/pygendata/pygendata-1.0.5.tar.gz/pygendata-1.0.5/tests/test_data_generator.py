from pygendata import DataGenerator

def test_not_passing_in_rows_results_in_no_rows():
    dg = DataGenerator('csv')
    assert len(dg.rows) == 0
