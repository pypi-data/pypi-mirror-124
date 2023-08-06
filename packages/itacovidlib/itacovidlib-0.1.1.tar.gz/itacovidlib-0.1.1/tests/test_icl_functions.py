import geopandas
import itacovidlib.backend as icl_b, itacovidlib.functions as icl, itacovidlib.exceptions as icl_e

################################################################################################
# NOTE ON TESTING
#
# Tests in this file are meant to be run under Internet connection, but they can also work
# without it (in this case, they turn into a "bonus" extra test checking that the proper
# exception for this situation is raised).
################################################################################################

################################################################################################
# NOTE ON TESTING - suggested manual testing
#
# There is no automatic test to check whether results returned by "tell_" functions correspond
# to the real ones since there is no way to implement an automatic check for this (values
# change every day and hour).
# Interested users may compare these data with the ones made available by the Government
# at the website: https://www.governo.it/it/cscovid19/report-vaccini/
################################################################################################


def test_get_gets_fake_url_with_internet():
    """Tests whether icl_b._get raises the proper exception when handling fake URLs with Internet connection available."""
    try:
        icl_b._get("http://fakeurl")
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
            
def test_istat_region_data_ranging():
    """Tests whether ranging in DataFrame returned by icl.get_istat_region_data works properly."""
    try:
        istat_region_data = icl.get_istat_region_data()
        # there should NOT be 5 rows, since there are more rows with the same index
        # if there are indeed, it means it still ranges by "default index number" (i.e the default index numbers given to a DataFrame) and the test fails
        assert len(istat_region_data["1":"5"].index) != 5
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)

def test_admin_sites_ranging():
    """Tests whether ranging in DataFrame returned by icl.get_admin_sites works properly."""
    try:
        admin_sites = icl.get_admin_sites()
        # there should NOT be 5 rows, since there are more rows with the same index
        # if there are indeed, it means it still ranges by "default index number" (i.e the default index numbers given to a DataFrame) and the test fails
        assert len(admin_sites["1":"5"].index) != 5
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
    
def test_admin_sites_types_ranging():
    """Tests whether ranging in DataFrame returned by icl.get_admin_sites_types works properly."""
    try:
        admin_sites_types = icl.get_admin_sites_types()
        # there should NOT be 5 rows, since there are more rows with the same index
        # if there are indeed, it means it still ranges by "default index number" (i.e the default index numbers given to a DataFrame) and the test fails
        assert len(admin_sites_types["1":"5"].index) != 5
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
    
def test_vaccine_general_summary_ranging():
    """Tests whether ranging in DataFrame returned by icl.get_vaccine_general_summary works properly."""
    try:
        vaccine_summary = icl.get_vaccine_general_summary()
        # there should be 6 rows
        assert len(vaccine_summary["1":"5"].index) == 6
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
    
def test_over_80_ranging():
    """Tests whether ranging in DataFrame returned by icl.get_over_80 works properly."""
    try:
        over_80 = icl.get_over_80()
        # there should be 4 rows
        assert len(over_80["1":"5"].index) == 4
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
        
def test_prepare_for_plotting_on_map_incompatibilities():
    """Tests whether icl.prepare_for_plotting_on_map raises the proper error when given a non compatible DataFrame (i.e. one missing a "region" or "province" column)."""
    try:
        equip_contracts = icl.get_equip_contracts()
        try:
            # equip_contracts has no regional data
            icl.prepare_for_plotting_on_map(equip_contracts, on="region")
        except Exception as e:
            assert isinstance(e, icl_e.ItaCovidLibKeyError)
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)

def test_prepare_for_plotting_on_map_incompatibilities_2():
    """Tests whether icl.prepare_for_plotting_on_map raises the proper error when given a compatible DataFrame but is asked to plot data on another kind of local subdivision (e.g. when asked to plot regional data on provinces)."""
    try:
        region_cases = icl.get_region_cases()
        try:
            # region_cases has no province data
            icl.prepare_for_plotting_on_map(region_cases, on="province")
        except Exception as e:
            assert isinstance(e, icl_e.ItaCovidLibKeyError)
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
        
def test_prepare_for_plotting_on_map_output_is_geodataframe():
    """Tests whether icl.prepare_for_plotting_on_map output is a GeoDataFrame."""
    try:
        region_cases_geodataframe = icl.prepare_for_plotting_on_map(source=icl.get_region_cases(), on="regions")
        assert isinstance(region_cases_geodataframe, geopandas.geodataframe.GeoDataFrame)
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
        
def test_tell_total_vaccinated_1():
    """Tests whether results returned by icl.tell_total_vaccinated with dose="1" and with ranging for date options make sense (i.e. the number of total vaccinated individuals is equal to the sum of the number of vaccinated individuals in three periods into which the whole vaccination timeline is divided)."""
    try:
        total_vaccinated_ever = icl.tell_total_vaccinated("1")
        vaccinated_first_group = icl.tell_total_vaccinated("1", stop_date="2020-10-01")
        vaccinated_second_group = icl.tell_total_vaccinated("1", start_date="2020-10-02", stop_date="2020-10-03")
        vaccinated_third_group = icl.tell_total_vaccinated("1", start_date="2020-10-04")
        assert total_vaccinated_ever == vaccinated_first_group+vaccinated_second_group+vaccinated_third_group
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
        
def test_tell_total_vaccinated_2():
    """Tests whether results returned by icl.tell_total_vaccinated with dose="2" and with ranging for date options make sense (i.e. the number of total vaccinated individuals is equal to the sum of the number of vaccinated individuals in three periods into which the whole vaccination timeline is divided)."""
    try:
        total_vaccinated_ever = icl.tell_total_vaccinated("2")
        vaccinated_first_group = icl.tell_total_vaccinated("2", stop_date="2020-10-01")
        vaccinated_second_group = icl.tell_total_vaccinated("2", start_date="2020-10-02", stop_date="2020-10-03")
        vaccinated_third_group = icl.tell_total_vaccinated("2", start_date="2020-10-04")
        assert total_vaccinated_ever == vaccinated_first_group+vaccinated_second_group+vaccinated_third_group
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
        
def test_tell_total_vaccinated_extra():
    """Tests whether results returned by icl.tell_total_vaccinated with dose="extra" and with ranging for date options make sense (i.e. the number of total vaccinated individuals is equal to the sum of the number of vaccinated individuals in three periods into which the whole vaccination timeline is divided)."""
    try:
        total_vaccinated_ever = icl.tell_total_vaccinated("extra")
        vaccinated_first_group = icl.tell_total_vaccinated("extra", stop_date="2020-10-01")
        vaccinated_second_group = icl.tell_total_vaccinated("extra", start_date="2020-10-02", stop_date="2020-10-03")
        vaccinated_third_group = icl.tell_total_vaccinated("extra", start_date="2020-10-04")
        assert total_vaccinated_ever == vaccinated_first_group+vaccinated_second_group+vaccinated_third_group
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
        
def test_tell_total_vaccinated_booster():
    """Tests whether results returned by icl.tell_total_vaccinated with dose="booster" and with ranging for date options make sense (i.e. the number of total vaccinated individuals is equal to the sum of the number of vaccinated individuals in three periods into which the whole vaccination timeline is divided)."""
    try:
        total_vaccinated_ever = icl.tell_total_vaccinated("booster")
        vaccinated_first_group = icl.tell_total_vaccinated("booster", stop_date="2020-10-20")
        vaccinated_second_group = icl.tell_total_vaccinated("booster", start_date="2020-10-21", stop_date="2020-10-22")
        vaccinated_third_group = icl.tell_total_vaccinated("booster", start_date="2020-10-23")
        assert total_vaccinated_ever == vaccinated_first_group+vaccinated_second_group+vaccinated_third_group
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)

def test_tell_manufacturer_delivered_doses_all():
    """Tests whether results returned by icl.tell_manufacturer_delivered_doses with manufacturer="all" and with ranging for date options make sense (i.e. the number of vaccinated individuals is equal to the sum of the number of vaccinated individuals in three periods into which the whole vaccination timeline is divided)."""
    try:
        manufacturer="all"
        total_delivered_ever = icl.tell_manufacturer_delivered_doses(manufacturer)
        delivered_first_group = icl.tell_manufacturer_delivered_doses(manufacturer, stop_date="2020-10-01")
        delivered_second_group = icl.tell_manufacturer_delivered_doses(manufacturer, start_date="2020-10-02", stop_date="2020-10-03")
        delivered_third_group = icl.tell_manufacturer_delivered_doses(manufacturer, start_date="2020-10-04")
        assert total_delivered_ever == delivered_first_group+delivered_second_group+delivered_third_group
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
        
def test_tell_manufacturer_delivered_doses_pfizer():
    """Tests whether results returned by icl.tell_manufacturer_delivered_doses with manufacturer="Pfizer/BioNTech" and with ranging for date options make sense (i.e. the number of vaccinated individuals with the given vaccine is equal to the sum of the number of vaccinated individuals with the given vaccine in three periods into which the whole vaccination timeline is divided)."""
    try:
        manufacturer="Pfizer/BioNTech"
        total_delivered_ever = icl.tell_manufacturer_delivered_doses(manufacturer)
        delivered_first_group = icl.tell_manufacturer_delivered_doses(manufacturer, stop_date="2020-10-01")
        delivered_second_group = icl.tell_manufacturer_delivered_doses(manufacturer, start_date="2020-10-02", stop_date="2020-10-03")
        delivered_third_group = icl.tell_manufacturer_delivered_doses(manufacturer, start_date="2020-10-04")
        assert total_delivered_ever == delivered_first_group+delivered_second_group+delivered_third_group
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
        
def test_tell_manufacturer_delivered_doses_moderna():
    """Tests whether results returned by icl.tell_manufacturer_delivered_doses with manufacturer="Moderna" and with ranging for date options make sense (i.e. the number of vaccinated individuals with the given vaccine is equal to the sum of the number of vaccinated individuals with the given vaccine in three periods into which the whole vaccination timeline is divided)."""
    try:
        manufacturer="Moderna"
        total_delivered_ever = icl.tell_manufacturer_delivered_doses(manufacturer)
        delivered_first_group = icl.tell_manufacturer_delivered_doses(manufacturer, stop_date="2020-10-01")
        delivered_second_group = icl.tell_manufacturer_delivered_doses(manufacturer, start_date="2020-10-02", stop_date="2020-10-03")
        delivered_third_group = icl.tell_manufacturer_delivered_doses(manufacturer, start_date="2020-10-04")
        assert total_delivered_ever == delivered_first_group+delivered_second_group+delivered_third_group
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
        
def test_tell_manufacturer_delivered_doses_astrazeneca():
    """Tests whether results returned by icl.tell_manufacturer_delivered_doses with manufacturer="Vaxzevria (AstraZeneca)" and with ranging for date options make sense (i.e. the number of vaccinated individuals with the given vaccine is equal to the sum of the number of vaccinated individuals with the given vaccine in three periods into which the whole vaccination timeline is divided)."""
    try:
        manufacturer="Vaxzevria (AstraZeneca)"
        total_delivered_ever = icl.tell_manufacturer_delivered_doses(manufacturer)
        delivered_first_group = icl.tell_manufacturer_delivered_doses(manufacturer, stop_date="2020-10-01")
        delivered_second_group = icl.tell_manufacturer_delivered_doses(manufacturer, start_date="2020-10-02", stop_date="2020-10-03")
        delivered_third_group = icl.tell_manufacturer_delivered_doses(manufacturer, start_date="2020-10-04")
        assert total_delivered_ever == delivered_first_group+delivered_second_group+delivered_third_group
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
        
def test_tell_manufacturer_delivered_doses_janssen():
    """Tests whether results returned by icl.tell_manufacturer_delivered_doses with manufacturer="Janssen" and with ranging for date options make sense (i.e. the number of vaccinated individuals with the given vaccine is equal to the sum of the number of vaccinated individuals with the given vaccine in three periods into which the whole vaccination timeline is divided)."""
    try:
        manufacturer="Janssen"
        total_delivered_ever = icl.tell_manufacturer_delivered_doses(manufacturer)
        delivered_first_group = icl.tell_manufacturer_delivered_doses(manufacturer, stop_date="2020-10-01")
        delivered_second_group = icl.tell_manufacturer_delivered_doses(manufacturer, start_date="2020-10-02", stop_date="2020-10-03")
        delivered_third_group = icl.tell_manufacturer_delivered_doses(manufacturer, start_date="2020-10-04")
        assert total_delivered_ever == delivered_first_group+delivered_second_group+delivered_third_group
    except Exception as e:
        assert isinstance(e, icl_e.ItaCovidLibConnectionError)
