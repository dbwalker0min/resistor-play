from best_resistance.eseries import generate_e_series
from best_resistance.types import Resistor
from pytest import approx
from inline_snapshot import snapshot


def test_e6():
    e6 = generate_e_series(6, min_decade=0, max_decade=6)


    assert len(e6) == snapshot(37), f"Expected got {len(e6)}"
    assert e6 == snapshot([Resistor (sym ='0',value =0 ),Resistor (sym ='1.0',value =1.0 ),Resistor (sym ='1.5',value =1.5 ),Resistor (sym ='2.2',value =2.2 ),Resistor (sym ='3.3',value =3.3 ),Resistor (sym ='4.7',value =4.7 ),Resistor (sym ='6.8',value =6.8 ),Resistor (sym ='10',value =10.0 ),Resistor (sym ='15',value =15.0 ),Resistor (sym ='22',value =22.0 ),Resistor (sym ='33',value =33.0 ),Resistor (sym ='47',value =47.0 ),Resistor (sym ='68',value =68.0 ),Resistor (sym ='100',value =100.0 ),Resistor (sym ='150',value =150.0 ),Resistor (sym ='220',value =220.00000000000003 ),Resistor (sym ='330',value =330.0 ),Resistor (sym ='470',value =470.0 ),Resistor (sym ='680',value =680.0 ),Resistor (sym ='1.0k',value =1000.0 ),Resistor (sym ='1.5k',value =1500.0 ),Resistor (sym ='2.2k',value =2200.0 ),Resistor (sym ='3.3k',value =3300.0 ),Resistor (sym ='4.7k',value =4700.0 ),Resistor (sym ='6.8k',value =6800.0 ),Resistor (sym ='10k',value =10000.0 ),Resistor (sym ='15k',value =15000.0 ),Resistor (sym ='22k',value =22000.0 ),Resistor (sym ='33k',value =33000.0 ),Resistor (sym ='47k',value =47000.0 ),Resistor (sym ='68k',value =68000.0 ),Resistor (sym ='100k',value =100000.0 ),Resistor (sym ='150k',value =150000.0 ),Resistor (sym ='220k',value =220000.00000000003 ),Resistor (sym ='330k',value =330000.0 ),Resistor (sym ='470k',value =470000.0 ),Resistor (sym ='680k',value =680000.0 )]), "Doesn't match snapshot"

