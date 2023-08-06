import itacovidlib.backend as icl_b, itacovidlib.functions as icl, itacovidlib.exceptions as icl_e

################################################################################################
# NOTE ON TESTING
# 
# This file contains tests specifically meant to be run without Internet connection, to test 
# the behaviour of code under this condition. However, these tests can also be executed with
# Internet connection without errors, even though they would yield nothing of interest.
# 
# NOTE: even though they are not specifically meant for this, tests in file
# test_icl_functions.py, which normally require an Internet connection, can also be run
# without it as a "bonus" test.
################################################################################################


def test_get_gets_fake_url_without_internet():
    """Tests whether icl_b._get raises the proper exception when handling fake URLs also without Internet connection."""
    try:
        icl_b._get("http://fakeurl")
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)

def test_get_gets_correct_url_but_cannot_connect():
    """Tests whether icl_b._get raises the proper exception when it cannot connect to the URLs with the data to gather."""
    # to be performed under no Internet connection
    links = ["https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.csv",
             "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.csv",
             "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea.csv",
             "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/punti-somministrazione-latest.csv",
             "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/punti-somministrazione-tipologia.csv",
             "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv",
             "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv",
             "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv",
             "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv",
             "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-latest.csv",
             "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-contratti-dpc-forniture/dpc-covid19-dati-contratti-dpc-forniture.csv",
             "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-contratti-dpc-forniture/dpc-covid19-dati-pagamenti-contratti-dpc-forniture.csv",
             "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv",
             "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-latest.csv",
             "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",
             "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv",
             "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-statistici-riferimento/popolazione-over80.csv",
             "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-statistici-riferimento/popolazione-istat-regione-range.csv",
             "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea-dose-booster.csv"]
    for link in links:
        try:
            icl_b._get(link)
        except Exception as e:
            assert isinstance(e, icl_e.ItaCovidLibConnectionError)

def test_getter_functions_cannot_connect():
    """Tests whether connection errors raised by icl_b._get propagate correctly and are yielded by get_<resource_name> functions, all using icl_b._get."""
    # to be performed under no Internet connection.
    functions = [icl.get_admin_sites, icl.get_admin_sites_types, icl.get_eligible, icl.get_equip_contracts, icl.get_equip_contracts_payments, icl.get_extra_dose_eligible, icl.get_booster_dose_eligible, icl.get_istat_region_data, icl.get_national_trend, icl.get_over_80, icl.get_province_cases, icl.get_region_cases, icl.get_vaccine_admin, icl.get_vaccine_admin_summary, icl.get_vaccine_ages, icl.get_vaccine_deliveries, icl.get_vaccine_general_summary, icl.get_istat_region_data]
    for function in functions:
        try:
            function()
        except Exception as e:
            assert isinstance(e, icl_e.ItaCovidLibConnectionError)
