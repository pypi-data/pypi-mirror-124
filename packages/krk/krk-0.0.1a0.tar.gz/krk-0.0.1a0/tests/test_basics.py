from krakakai.krk.krk import KRK
from krakakai.krk import cli


def test_basics():
    krk = KRK("KRAKAKA")
    krk.do_the_krakakai()
    cli.main()
