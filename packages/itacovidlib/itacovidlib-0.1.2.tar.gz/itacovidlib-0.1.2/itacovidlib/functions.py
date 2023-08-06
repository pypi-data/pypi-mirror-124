import os.path
import itacovidlib.backend as icl_b
import itacovidlib.exceptions as icl_e
import numpy as np
import pandas as pd
import geopandas as gpd
import epyestim.covid19 as covid19


def get_vaccine_ages():
    """Returns DataFrame about COVID-19 vaccine administrations per age group in Italy.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with requested data.
    
    DataFrame Columns
    -----------------
    age_group : str (index)
        Age groups
    total : int64
        Total of administered vaccines
    males : int64
        Total of male persons to which vaccine has been administered
    females : int64
        Total of female persons to which vaccine has been administered
    first_dose : int64
        Number of first doses (excluding previously infected individuals)
    second_dose : int64
        Number of second doses
    previously_infected : int64
        Number of vaccine administrations to individuals infected between 3 and 6 months before, as such completing the vaccination cycle with a single dose
    extra_dose : int64
        Number of extra doses administered to individuals requiring it
    booster_dose : int64
        Number of booster doses administered to individuals requiring it
    last_update : datetime
        Date of last update"""
    
    data = icl_b._get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"fascia_anagrafica":"age_group","totale":"total","sesso_maschile":"males","sesso_femminile":"females","prima_dose":"first_dose","seconda_dose":"second_dose","pregressa_infezione":"previously_infected","dose_aggiuntiva":"extra_dose","dose_booster":"booster_dose","ultimo_aggiornamento":"last_update"}, inplace=True)
        # dates in last_update must be parsed into datetime objects
        data["last_update"] = pd.to_datetime(data["last_update"])
        data.set_index("age_group", inplace=True)
        return data

def get_vaccine_deliveries():
    """Returns DataFrame about COVID-19 vaccine deliveries in Italy.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with requested data.
    
    DataFrame Columns
    -----------------
    date_of_delivery : datetime (index)
        Date of delivery
    region_code : str
        Code of delivery region
    manufacturer : str
        Vaccine manufacturer name
    number_of_doses : int64
        Number of delivered doses on date date_of_delivery
    NUTS1_code : str
        European classification of territorial units NUTS: level NUTS1
    NUTS2_code : str
        European classification of territorial units NUTS: level NUTS2
    ISTAT_region_code : int
        ISTAT region code
    region : str
        Official region name"""
    
    data = icl_b._get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"area":"region_code","fornitore":"manufacturer","data_consegna":"date_of_delivery","numero_dosi":"number_of_doses","codice_NUTS1":"NUTS1_code","codice_NUTS2":"NUTS2_code","codice_regione_ISTAT":"ISTAT_region_code","nome_area":"region"}, inplace=True)
        # dates in column date_of_delivery must be parsed into datetime objects
        data["date_of_delivery"] = pd.to_datetime(data["date_of_delivery"])
        # since date_of_delivery is meant to be the index, it is reasonable returned DataFrame is sorted by date, also for proper ranging
        data.sort_values(by="date_of_delivery", inplace=True)
        data.set_index("date_of_delivery", inplace=True)
        return data

def get_eligible():
    """Returns DataFrame about eligible persons for COVID-19 vaccine administration in Italy.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with requested data.
    
    DataFrame Columns
    -----------------
    age_group : str (index)
        Age group
    region_code : str
        Region code
    region : str
        Official region name
    population : int64
        Total population per given age group
        
    See Also
    --------
    get_extra_dose_eligible : data about eligible persons for extra COVID-19 vaccine dose administration in Italy."""
    
    data = icl_b._get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"area":"region_code","nome_area":"region","fascia_anagrafica":"age_group","totale_popolazione":"population"}, inplace=True)
        data.set_index("age_group", inplace=True)
        return data
    
def get_extra_dose_eligible():
    """Returns DataFrame about eligible persons for extra COVID-19 vaccine dose administration in Italy.
    An extra dose is required for those individuals who cannot develop a proper protection after the usual vaccine administration(s).
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
        
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with requested data.
        
    DataFrame Columns
    -----------------
    region_code : str (index)
        Region code
    region : str
        Official region name
    prevailing_category : str
        Prevailing category of the vaccination group in the corresponding row
    population : int64
        Total population per given vaccination group (i.e. row)
    
    See Also
    --------
    get_eligible : data about eligible persons for COVID-19 vaccine administration in Italy.
    get_booster_dose_eligible : data about eligible persons for booster dose."""
        
    data = icl_b._get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea-dose-aggiuntiva.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"area":"region_code","nome_area":"region","categoria_prevalente":"prevailing_category","totale_popolazione":"population"}, inplace=True)
        data.set_index("region_code", inplace=True)
        return data
    
def get_booster_dose_eligible():
    """Returns DataFrame about eligible persons for booster COVID-19 vaccine dose administration in Italy.
    A booster dose is required for those individuals who have successfully developed a proper protection after the usual vaccine administration(s) but are considered in need of one extra dose to furtherly reinforce their protection.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
        
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with requested data.
        
    DataFrame Columns
    -----------------
    region_code : str (index)
        Region code
    region : str
        Official region name
    prevailing_category : str
        Prevailing category of the vaccination group in the corresponding row
    population : int64
        Total population per given vaccination group (i.e. row)
    
    See Also
    --------
    get_eligible : data about eligible persons for COVID-19 vaccine administration in Italy.
    get_extra_dose_eligible : data about eligible persons for extra dose."""
        
    data = icl_b._get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea-dose-booster.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"area":"region_code","nome_area":"region","categoria_prevalente":"prevailing_category","totale_popolazione":"population"}, inplace=True)
        data.set_index("region_code", inplace=True)
        return data
        

def get_admin_sites():
    """Returns DataFrame about COVID-19 vaccine administrations points in Italy.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with requested data.
    
    DataFrame Columns
    -----------------
    ISTAT_region_code : str (index)
        ISTAT region code
    region_code : str
        Region code
    province : str
        Province
    municipality : str
        Municipality
    place : str
        Name of place of administration
    NUTS1_code : str
        European classification of territorial units NUTS: level NUTS1
    NUTS2_code : str
        European classification of territorial units NUTS: level NUTS2
    region : str
        Official region name"""
    
    data = icl_b._get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/punti-somministrazione-latest.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"area":"region_code","provincia":"province","comune":"municipality","presidio_ospedaliero":"place","codice_NUTS1":"NUTS1_code","codice_NUTS2":"NUTS2_code","codice_regione_ISTAT":"ISTAT_region_code","nome_area":"region"}, inplace=True)
        # for proper indexing
        data.sort_values(by="ISTAT_region_code", inplace=True)
        # for proper ranging operations (i.e. data[x:y]). Ints have issues in this
        data["ISTAT_region_code"] = data["ISTAT_region_code"].apply(str)
        # for this dataset, this is the only reasonable choice, since ISTAT region codes are assigned from north to south, making a North-Centre-South distinction possible
        data.set_index("ISTAT_region_code", inplace=True)
        return data

def get_admin_sites_types():
    """Returns DataFrame on types of COVID-19 vaccine administration points in Italy.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with requested data.
    
    DataFrame Columns
    -----------------
    ISTAT_region_code : str (index)
        ISTAT region code
    region_code : str
        Region code
    place : str
        Name of place of administration
    type : str
        Type of administration place: OSPEDALIERO (hospital) or TERRITORIALE (local)
    NUTS1_code : str
        European classification of territorial units NUTS: level NUTS1
    NUTS2_code : str
        European classification of territorial units NUTS: level NUTS2
    region : str
        Official region name"""
    
    data = icl_b._get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/punti-somministrazione-tipologia.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"area":"region_code","denominazione_struttura":"place","tipologia":"type","codice_NUTS1":"NUTS1_code","codice_NUTS2":"NUTS2_code","codice_regione_ISTAT":"ISTAT_region_code","nome_area":"region"}, inplace=True)
        # for proper indexing
        data.sort_values(by="ISTAT_region_code", inplace=True)
        # for proper ranging operations (i.e. data[x:y]). Ints have issues in this
        data["ISTAT_region_code"] = data["ISTAT_region_code"].apply(str)
        # for this dataset, this is the only reasonable choice, since ISTAT region codes are assigned from north to south, making a North-Centre-South distinction possible
        data.set_index("ISTAT_region_code", inplace=True)
        return data

def get_vaccine_admin():
    """Returns DataFrame on COVID-19 vaccine administration in Italy.
    
    Parameters
    ----------
    None
    
    Raises
    -------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with requested data.
    
    DataFrame Columns
    -----------------
    date : datetime (index)
        Date of administration
    Manufacturer : str
        Vaccine manufacturer name
    region_code : str
        Region code
    age_group : str
        Age group
    males : int64
        Number of male individuals who have been given the vaccine
    females : int64
        Number of female individuals who have been given the vaccine
    first_dose : int64
        Number of first doses (excluding previously infected individuals)
    second_dose : int64
        Number of second doses
    previously_infected : int64
        Number of vaccine administrations to individuals who have already been infected by SARS-CoV-2 between 3 and 6 months before and as such completing the vaccination cycle with just one dose
    extra_dose : int64
        Number of extra doses administered to individuals requiring it
    booster_dose : int64
        Number of booster doses administered to individuals requiring it
    NUTS1_code : str
        European classification of territorial units NUTS: level NUTS1
    NUTS2_code : str
        European classification of territorial units NUTS: level NUTS2
    ISTAT_region_code : int64
        ISTAT region code
    region : str
        Official region name
    
    See Also
    --------
    get_vaccine_admin_summary : a concise version (summary) of this function"""
    
    data = icl_b._get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"data_somministrazione":"date","fornitore":"manufacturer","area":"region_code","fascia_anagrafica":"age_group","sesso_maschile":"males","sesso_femminile":"females","prima_dose":"first_dose","seconda_dose":"second_dose","pregressa_infezione":"previously_infected","dose_aggiuntiva":"extra_dose","dose_booster":"booster_dose","codice_NUTS1":"NUTS1_code","codice_NUTS2":"NUTS2_code","codice_regione_ISTAT":"ISTAT_region_code","nome_area":"region"}, inplace=True)
        # dates in column date must be parsed into datetime objects
        data["date"] = pd.to_datetime(data["date"])
        data.set_index("date", inplace=True)
        return data
    
def get_vaccine_admin_summary():
    """Returns DataFrame about COVID-19 vaccine administration in Italy (summary version)
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with requested data.
    
    DataFrame Columns
    -----------------
    date : datetime (index)
        Date of administration
    region_code : str
        Region code
    total : int64
        Total amount of doses
    males : int64
        Number of male individuals who have been given a vaccine dose
    females : int64
        Number of female individuals who have been given a vaccine dose
    first_dose : int64
        Number of first doses (excluding previously infected individuals)
    second_dose : int64
        Number of second doses
    previously_infected : int64
        Number of vaccine administrations to individuals who have already been infected by SARS-CoV-2 between 3 and 6 months before and as such completing the vaccination cycle with just one dose
    extra_dose : int64
        Number of extra doses administered to individuals requiring it
    booster_dose : int64
        Number of booster doses administered to individuals requiring it
    NUTS1_code : str
        European classification of territorial units NUTS: level NUTS1
    NUTS2_code : str
        European classification of territorial units NUTS: level NUTS2
    ISTAT_region_code : int64
        ISTAT region code
    region : str
        Official region name
    
    See Also
    --------
    get_vaccine_admin : a complete version of this function with more data"""
    
    data = icl_b._get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"data_somministrazione":"date","area":"region_code","totale":"total","sesso_maschile":"males","sesso_femminile":"females","prima_dose":"first_dose","seconda_dose":"second_dose","pregressa_infezione":"previously_infected","dose_aggiuntiva":"extra_dose","dose_booster":"booster_dose","codice_NUTS1":"NUTS1_code","codice_NUTS2":"NUTS2_code","codice_regione_ISTAT":"ISTAT_region_code","nome_area":"region"}, inplace=True)
        # dates in column date must be parsed into datetime objects
        data["date"] = pd.to_datetime(data["date"])
        data.set_index("date", inplace=True)
        return data
    
def get_vaccine_general_summary():
    """Returns DataFrame with a synthesis of COVID-19 vaccines deliveries and administrations in Italy.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with requested data.
    
    DataFrame Columns
    -----------------
    ISTAT_region_code : str (index)
        ISTAT region code
    region_code : str
        Region code
    administered_doses : int64
        Number of administered doses
    delivered_doses : int64
        Number of delivered doses
    administration_percent : float64
        Percentage of administered doses over delivered doses
    last_update : datetime
        Date and time of last update
    NUTS1_code : str
        European classification of territorial units NUTS: level NUTS1
    NUTS2_code : str
        European classification of territorial units NUTS: level NUTS2
    region : str
        Official region name
    
    See Also
    --------
    get_vaccine_deliveries : more info on COVID-19 vaccine deliveries
    get_vaccine_admin_summary : more info on COVID-19 vaccine administrations (concise version)
    get_vaccine_admin : more info on COVID-19 vaccine administrations (complete version)"""
    
    data = icl_b._get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"area":"region_code","dosi_somministrate":"administered_doses","dosi_consegnate":"delivered_doses","percentuale_somministrazione":"administration_percent","ultimo_aggiornamento":"last_update","codice_NUTS1":"NUTS1_code","codice_NUTS2":"NUTS2_code","codice_regione_ISTAT":"ISTAT_region_code","nome_area":"region"}, inplace=True)
        # dates in column last_update must be parsed into datetime objects
        data["last_update"] = pd.to_datetime(data["last_update"])
        # for proper indexing
        data.sort_values(by="ISTAT_region_code", inplace=True)
        # for proper ranging operations (i.e. data[x:y]). Ints have issues in this
        data["ISTAT_region_code"] = data["ISTAT_region_code"].apply(str)
        # for this dataset, this is the only reasonable choice, since ISTAT region codes are assigned from north to south, making a North-Centre-South distinction possible
        data.set_index("ISTAT_region_code", inplace=True)
        return data

def get_national_trend(latest=False):
    """Returns DataFrame about COVID-19 pandemic situation in Italy.
    
    Parameters
    ----------
    latest : bool
        Option for returning data referred to the current day only (default is False)
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame about COVID-19 pandemic situation in Italy
    
    DataFrame Columns
    -----------------
    date : datetime (index)
        Date
    country : str
        Country
    hospitalized_with_symptoms : int64
        Number of hospitalized individuals with COVID-19 symptoms
    intensive_care : int64
        Number of individuals in intensive care units
    hospitalized : int64
        Number of hospitalized individuals, either with symptoms or in intensive care unit
    isolation : int64
        Number of people placed into isolation
    cases : int64
        Number of COVID-19 cases
    cases_variation : int64
        Variation in the number of COVID-19 cases with respect to the previous day
    new_cases : int64
        Number of new individuals diagnosed with COVID-19
    recovered_released : int64
        Number of individuals released from hospital after recovery
    deaths : int64
        Number of dead individuals following COVID-19 infection
    cases_from_clinical_suspects : float64
        Number of positive cases found after report of COVID-19-like symptoms
    cases_from_screening : float64
        Number of positive cases found after screening (e.g. close contacts of a positive case)
    cumulative_cases : int64
        Total number of COVID-19 cases since the beginning of the pandemic
    swabs : int64
        Number of swabs performed
    tested : float64
        Number of tested individuals
    notes : str
        Notes
    intensive_care_in : float64
        Number of new accesses to intensive care units
    test_notes : float64
        Notes on testing
    case_notes : float64
        Notes on COVID-19 cases
    molecular_test_cases : float64
        Number of COVID-19 cases detected through molecular tests
    antigen_test_cases : float64
        Number of COVID-19 cases detected through antigen (so-called rapid) tests
    molecular_tests : float64
        Total number of molecular tests performed
    antigen_tests : float64
        Total number of antigen (so-called rapid) tests performed
    
    See Also
    --------
    tell_rt : returns the Rt index over time calculated from these data"""
    
    if latest == False:
        data = icl_b._get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
    elif latest == True:
        data = icl_b._get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-latest.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"data":"date","stato":"country","ricoverati_con_sintomi":"hospitalized_with_symptoms","terapia_intensiva":"intensive_care","totale_ospedalizzati":"hospitalized","isolamento_domiciliare":"isolation","totale_positivi":"cases","variazione_totale_positivi":"cases_variation","nuovi_positivi":"new_cases","dimessi_guariti":"recovered_released","deceduti":"deaths","casi_da_sospetto_diagnostico":"cases_from_clinical_suspects","casi_da_screening":"cases_from_screening","totale_casi":"cumulative_cases","tamponi":"swabs","casi_testati":"tested","note":"notes","ingressi_terapia_intensiva":"intensive_care_in","note_test":"test_notes","note_casi":"case_notes","totale_positivi_test_molecolare":"molecular_test_cases","totale_positivi_test_antigenico_rapido":"antigen_test_cases","tamponi_test_molecolare":"molecular_tests","tamponi_test_antigenico_rapido":"antigen_tests"}, inplace=True)
        # dates in column date must be parsed into datetime objects
        data["date"] = pd.to_datetime(data["date"])
        data.set_index("date", inplace=True)
        return data


def get_equip_contracts():
    """Returns data about COVID-19 pandemic equipment contracts for Italy.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with data about COVID-19 pandemic equipment contracts
    
    DataFrame Columns
    -----------------
    negotiation_date : datetime (index)
        Date of negotiation
    manufacturer : str
        Equipment manufacturer name
    country : str
        Country
    product_group : str
        Official product group
    article_subgroup : str
        Official article subgroup
    category : str
        Equipment category
    subcategory : str
        Equipment subcategory
    equipment_kind : str
        Equipment kind
    equipment : str
        Equipment name
    negotiation_protocol : str
        Name of negotiation protocol
    negotiation_file : str
        Negotiation file link
    errata : str
        Errata corrige
    errata_protocol : str
        Protocol errata corrige
    errata_date : str
        Date errata corrige
    errata_file : str
        File errata corrige
    tender_id_type : str
        Tender identification code type
    tender_id : str
        Tender identification code
    quantity : int64
        Item quantity
    unit_price : float64
        Price per unit
    total_price : float64
        Total price
    agreement_state : str
        State of agreement
    ceded : str
        State of cession to Special Commissioner for COVID-19 emergency (ITA: Commissario Straordinario)
    notes : float64
        Notes
    update_date : datetime
        Date of update
    
    See Also
    --------
    get_equip_contracts_payments : data about payments for COVID-19 pandemic equipment"""
    
    data = icl_b._get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-contratti-dpc-forniture/dpc-covid19-dati-contratti-dpc-forniture.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"fornitore":"manufacturer","stato_fornitore":"country","gruppo_articoli":"product_group","sottogruppo_articoli":"article_subgroup","categoria":"category","sottocategoria":"subcategory","tipologia_fornitura":"equipment_kind","fornitura":"equipment","protocollo_atto_negoziale":"negotiation_protocol","data_atto_negoziale":"negotiation_date","file_atto_negoziale":"negotiation_file","integrazione_rettifica":"errata","protocollo_integrazione_rettifica":"errata_protocol","data_integrazione_rettifica":"errata_date","file_integrazione_rettifica":"errata_file","tipologia_cig":"tender_id_type","cig":"tender_id","quantita":"quantity","prezzo_unitario":"unit_price","totale_articolo":"total_price","stato_contratto":"agreement_state","ceduti_commissario_straordinario":"ceded","note":"notes","data_aggiornamento":"update_date"}, inplace=True)
        # dates in column negotiation_date must be parsed into datetime objects
        data["negotiation_date"] = pd.to_datetime(data["negotiation_date"])
        # dates in column update_date must be parsed into datetime objects
        data["update_date"] = pd.to_datetime(data["update_date"])
        # for proper indexing
        data.sort_values(by="negotiation_date", inplace=True)
        data.set_index("negotiation_date", inplace=True)
        return data

def get_equip_contracts_payments():
    """Returns data about payments for COVID-19 equipment in Italy, as established by contracts.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame about payments for COVID-19 equipment
    
    DataFrame Columns
    -----------------
    negotiation_protocol : str (index)
        Name of negotiation protocol
    total_equipment : float64
        Total amount per given equipment
    total_paid : float64
        Total paid
    donations : float64
        Amount of donations
    other_funds : float64
        Amount of other funds used for that payment
    payment_fund : float64
        Amount of payment fund used for that payment
    ceded : str
        State of cession to Special Commissioner for COVID-19 emergency (ITA: Commissario Straordinario)
    notes : float64
        Notes
    update_date : datetime
        Date of update
    
    See Also
    --------
    get_equip_contracts : data about COVID-19 equipment contracts"""
    
    data = icl_b._get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-contratti-dpc-forniture/dpc-covid19-dati-pagamenti-contratti-dpc-forniture.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"protocollo_atto_negoziale":"negotiation_protocol","totale_fornitura":"total_equipment","totale_pagato":"total_paid","pagato_donazioni":"donations","pagato_altri_fondi":"other_funds","fondo_pagamento":"payment_fund","ceduti_commissario_straordinario":"ceded","note":"notes","data_aggiornamento":"update_date"}, inplace=True)
        # dates in column update_date must be parsed into datetime objects
        data["update_date"] = pd.to_datetime(data["update_date"])
        data.set_index("negotiation_protocol", inplace=True)
        return data

def get_province_cases(latest=False):
    """Returns DataFrame about COVID-19 cases per province in Italy.
    
    Parameters
    ----------
    latest : bool
        Option for returning data referred to the current day only (default is False) 
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame about COVID-19 cases per province
    
    DataFrame Columns
    -----------------
    date : datetime (index)
        Date
    country : str
        Country
    region_code : int64
        Region code number
    region : str
        Official region name
    province_code : int64
        Province code number
    province : str
        Province
    province_abbreviation : str
        Province two-letter abbreviation
    lat : float64
        Latitude
    long : float64
        Longitude
    cumulative_cases : int64
        Total number of COVID-19 cases since the beginning of the pandemic
    notes : str
        Notes
    NUTS1_code : str
        European classification of territorial units NUTS: level NUTS1
    NUTS2_code : str
        European classification of territorial units NUTS: level NUTS2
    NUTS3_code : str
        European classification of territorial units NUTS: level NUTS3
    
    See Also
    --------
    get_region_cases : returns data referred to regions"""
    
    if latest == False:
        data = icl_b._get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")
    elif latest == True:
        data = icl_b._get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-latest.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"data":"date","stato":"country","codice_regione":"region_code","denominazione_regione":"region","codice_provincia":"province_code","denominazione_provincia":"province","sigla_provincia":"province_abbreviation","lat":"lat","long":"long","totale_casi":"cumulative_cases","note":"notes","codice_nuts_1":"NUTS1_code","codice_nuts_2":"NUTS2_code","codice_nuts_3":"NUTS3_code"}, inplace=True)
        # dates in column date must be parsed into datetime objects
        data["date"] = pd.to_datetime(data["date"])
        data.set_index("date", inplace=True)
        return data
    

def get_region_cases(latest=False):
    """Returns DataFrame about COVID-19 cases per region in Italy.
    
    Parameters
    ----------
    latest : bool
        Option for returning data referred to the current day only (default is False)
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame about COVID-19 cases per region
    
    DataFrame Columns
    -----------------
    date : datetime (index)
        Date
    country : str
        Country
    region_code : int64
        Region code number
    region : str
        Official region name
    lat : float64
        Latitude
    long : float64
        Longitude
    hospitalized_with_symptoms : int64
        Number of hospitalized individuals with COVID-19 symptoms
    intensive_care : int64
        Number of individuals in intensive care units
    hospitalized : int64
        Number of hospitalized individuals, either with symptoms or in intensive care unit
    isolation : int64
        Number of people placed into isolation
    cases : int64
        Number of COVID-19 cases
    cases_variation : int64
        Variation in the number of COVID-19 cases with respect to the previous day
    new_cases : int64
        Number of new individuals diagnosed with COVID-19
    recovered_released : int64
        Number of individuals released from hospital after recovery
    deaths : int64
        Number of dead individuals following COVID-19 infection
    cases_from_clinical_suspects : float64
        Number of positive cases found after report of COVID-19-like symptoms
    cases_from_screening : float64
        Number of positive cases found after screening (e.g. close contacts of a positive case)
    cumulative_cases : int64
        Total number of COVID-19 cases since the beginning of the pandemic
    swabs : int64
        Number of swabs performed
    tested : float64
        Number of tested individuals
    notes : str
        Notes
    intensive_care_in : float64
        Number of new accesses to intensive care units
    test_notes : str
        Notes on testing
    case_notes : str
        Notes on COVID-19 cases
    molecular_test_cases : float64
        Number of COVID-19 cases detected through molecular tests
    antigen_test_cases : float64
        Number of COVID-19 cases detected through antigen (so-called rapid) tests
    molecular_tests : float64
        Total number of molecular tests performed
    antigen_tests : float64
        Total number of antigen (so-called rapid) tests performed
    NUTS1_code : str
        European classification of territorial units NUTS: level NUTS1
    NUTS2_code : str
        European classification of territorial units NUTS: level NUTS2
    
    See Also
    --------
    get_province_cases : returns data referred to provinces"""
    
    if latest == False:
        data = icl_b._get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")
    elif latest == True:
        data = icl_b._get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"data":"date","stato":"country","codice_regione":"region_code","denominazione_regione":"region","ricoverati_con_sintomi":"hospitalized_with_symptoms","terapia_intensiva":"intensive_care","totale_ospedalizzati":"hospitalized","isolamento_domiciliare":"isolation","totale_positivi":"cases","variazione_totale_positivi":"cases_variation","nuovi_positivi":"new_cases","dimessi_guariti":"recovered_released","deceduti":"deaths","casi_da_sospetto_diagnostico":"cases_from_clinical_suspects","casi_da_screening":"cases_from_screening","totale_casi":"cumulative_cases","tamponi":"swabs","casi_testati":"tested","note":"notes","ingressi_terapia_intensiva":"intensive_care_in","note_test":"test_notes","note_casi":"case_notes","totale_positivi_test_molecolare":"molecular_test_cases","totale_positivi_test_antigenico_rapido":"antigen_test_cases","tamponi_test_molecolare":"molecular_tests","tamponi_test_antigenico_rapido":"antigen_tests","codice_nuts_1":"NUTS1_code","codice_nuts_2":"NUTS2_code"}, inplace=True)
        # dates in column date must be parsed into datetime objects
        data["date"] = pd.to_datetime(data["date"])
        data.set_index("date", inplace=True)
        return data

def get_over_80():
    """Returns data on over 80 individuals in Italy
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with data on over 80 individuals
    
    DataFrame Columns
    -----------------
    region_code : str (index)
        Region code number
    NUTS1_code : str
        European classification of territorial units NUTS: level NUTS1
    NUTS1_description : str
        Description of level NUTS1 of the European classification of territorial units NUTS
    NUTS2_code : str
        European classification of territorial units NUTS: level NUTS2
    region : str
        Official region name
    age_range : str
        Age range
    males : int64
        Number of male individuals
    females : int64
        Number of female individuals
    total : int64
        Total number of over 80 individuals"""
    
    data = icl_b._get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-statistici-riferimento/popolazione-over80.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"codice_regione":"region_code","codice_nuts_1":"NUTS1_code","descrizione_nuts_1":"NUTS1_description","codice_nuts_2":"NUTS2_code","denominazione_regione":"region","range_eta":"age_range","totale_genere_maschile":"males","totale_genere_femminile":"females","totale_generale":"total"}, inplace=True)
        # for proper indexing
        data.sort_values(by="region_code", inplace=True)
        # for proper ranging operations (i.e. data[x:y]). Ints have issues in this
        data["region_code"] = data["region_code"].apply(str)
        # for this dataset, this is the only reasonable choice, since ISTAT region codes are assigned from north to south, making a North-Centre-South distinction possible
        data.set_index("region_code", inplace=True)
        return data

def get_istat_region_data(index="region_code"):
    """Returns data about Italian regions from ISTAT (Italian National Institute of Statistics).
    
    Parameters
    ----------
    index : str
        Choice of index for output DataFrame: region code numbers (options "r", "region", "region_code") or age ranges (options "a", "age", "age_range")(default is "region_code")
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    ItaCovidLibArgumentError
        Raised when improper arguments are passed to the function.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with data about Italian regions from ISTAT
    
    DataFrame Columns
    -----------------
    region_code : str (index with "r"/"region"/"region_code" option for index parameter)
        Region code number
    NUTS1_code : str
        European classification of territorial units NUTS: level NUTS1
    NUTS1_description : str
        Description of level NUTS1 of the European classification of territorial units NUTS
    NUTS2_code : str
        European classification of territorial units NUTS: level NUTS2
    region : str
        Official region name
    region_abbreviation: str
        Region name abbreviation
    lat : float64
        Latitude
    long : float64
        Longitude
    age_range : str (index with "a"/"age"/"age_range" option for index parameter)
        Age range
    males : int64
        Number of male individuals
    females : int64
        Number of female individuals
    total : int64
        Total number of individuals"""
    
    data = icl_b._get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-statistici-riferimento/popolazione-istat-regione-range.csv")
    if data is not None:
        # column names must be translated from Italian
        data.rename(columns={"codice_regione":"region_code","codice_nuts_1":"NUTS1_code","descrizione_nuts_1":"NUTS1_description","codice_nuts_2":"NUTS2_code","denominazione_regione":"region","sigla_regione":"region_abbreviation","latitudine_regione":"lat","longitudine_regione":"long","range_eta":"age_range","totale_genere_maschile":"males","totale_genere_femminile":"females","totale_generale":"total"}, inplace=True)
        # solves an issue with Trentino and South Tyrol region codes
        data["region_code"].replace({21:4, 22:4}, inplace=True)
        # there are two reasonable choices for this dataset DataFrame index. The user is let choose one of them.
        if index=="r" or index=="region" or index=="region_code":
            # for proper indexing
            data.sort_values(by="region_code", inplace=True)
            # for proper ranging operations (i.e. data[x:y]). Ints have issues in this
            data["region_code"] = data["region_code"].apply(str)
            data.set_index("region_code", inplace=True)
        elif index=="a" or index=="age" or index=="age_range":
            data["region_code"] = data["region_code"].apply(str)
            # for proper indexing
            data.sort_values(by="age_range", inplace=True)
            data.set_index("age_range", inplace=True)
        else:
            raise icl_e.ItaCovidLibArgumentError("invalid option for index. Please see documentation for help on possible options.")
        return data

def tell_total_administered_doses():
    """Returns the amount of all administered doses ever.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    int
        Integer with the amount of all administered doses ever
    
    See Also
    --------
    get_vaccine_general_summary : also includes regional data"""
    
    data = get_vaccine_general_summary()
    if data is not None:
        # get_vaccine_general_summary_latest also returns a column administered_doses, with the amount of all doses ever administered per region. Sum is performed on all regional values.
        return int(data["administered_doses"].sum())

def tell_total_vaccinated(dose, option="n", start_date="2020", stop_date="2030"):
    """Depending on the str provided as dose:
    dose = "1": returns the number of individuals who have been injected at least one vaccine dose in Italy (independently of it being enough for vaccination cycle completion, as is the case with Janssen vaccine or for individuals with recent COVID-19 injection, for whom only one dose is required);
    dose = "2": returns the number of individuals who have completed the vaccination cycle in Italy (with double dose for Pfizer/BioNTech, Moderna and Vaxzevria (AstraZeneca), with single dose for Janssen, with single dose for individuals previously infected with SARS-CoV-2 between 3 and 6 months before vaccination);
    dose = "extra" or "e": returns the number of individuals who have been injected an extra dose of vaccine in Italy, being eligible for it depending on their medical condition (commonly referred to as "third dose" in media);
    dose = "booster" or "b": returns the number of individuals who have been injected a booster dose of vaccine in Italy, being eligible for it to furtherly reinforce their fully acquired protection (also commonly referred to as "third dose" in media).
    
    Numbers refer to the period between start_date and stop_date. If start_date and stop_date are not specified, returned numbers refer to all time.
    
    Result is returned, depending on the str value provided as option:
    no option or option = "n" or "number": just returns the requested number (default option);
    option = "o" or "over12": returns the requested number as a fraction of the Italian population aged over 12;
    option = "p" or "population": returns the requested number as a fraction of the whole Italian population;
    option = "e" or "eligible": (ONLY FOR dose = "extra"/"e"/"booster"/"b") returns the requested number as a fraction of eligible individuals for extra or booster dose.
    
    Parameters
    ----------
    dose : str
        Dose type of interest. See above for the meaning of the various options. Other str values raise an error.
    option : str
        Output option. See above for the meaning of the various option codes. Other str values raise an error.
    start_date : datetime or datetime-like formatted str
        Starting date of the period of interest (default is beginning of vaccination cycle).  
    stop_date : datetime or datetime-like formatted str
        Ending date of the period of interest (default is current day)
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    ItaCovidLibArgumentError
        Raised when improper arguments are passed to the function.
    
    Returns
    -------
    FOR THE DEFAULT option OPTION:
    int64
        64-bit integer (see above for its meaning, depending on dose code).
    
    FOR THE OTHER option OPTIONS:
    float64
        64-bit floating point (see above for its meaning, depending on dose code and option code).
    
    See Also
    --------
    get_vaccine_admin : full data about vaccine administration in Italy"""

    # checks on options are performed first, otherwise get_vaccine_admin might run uselessly
    if option!="number" and option!="n" and option!="over12" and option!="o" and option!="population" and option!="p" and option!="eligible" and option!="e":
        raise icl_e.ItaCovidLibArgumentError("invalid option for option. Please see documentation for help on possible options.")
    elif dose!="1" and dose!="2" and dose!="extra" and dose!="e" and dose!="booster" and dose!="b":
        raise icl_e.ItaCovidLibArgumentError("invalid option for dose. Please see documentation for help on possible options.")
    # option "eligible" is not available with dose options "1" and "2"
    elif (dose=="1" or dose=="2") and (option=="eligible" or option=="e"):
        raise icl_e.ItaCovidLibArgumentError("invalid option for option. Please see documentation for help on possible options.")
    else:
        # default parameters for start_date and stop_date are respectively "2020" and "2030": this since syntax necessarily requires such default arguments. "2020" covers everything since the beginning, while "2030" covers all future runs of this software (hoping the pandemic ends much earlier!).
        vaccine_admin = get_vaccine_admin()[start_date:stop_date]
        if vaccine_admin is not None:
            if dose == "1":
                # Previously infected individuals data are also added, since the DataFrame returned by get_vaccine_admin keeps them separate from first doses count
                vaccinated = vaccine_admin.sum()["first_dose"]+vaccine_admin.sum()["previously_infected"]
                if option=="number" or option=="n":
                    return vaccinated
                elif option=="over12" or option=="o":
                    total_over_12 = get_eligible().sum()["population"]
                    return vaccinated/total_over_12
                elif option=="population" or option=="p":
                    total_population = get_istat_region_data().sum()["total"]
                    return vaccinated/total_population
            elif dose == "2":
                # For vaccines requiring two doses data on second doses are taken, for vaccines requiring one single dose data on first doses are taken, for all vaccines data on previously infected individuals, completing the vaccination cycle with one single dose, are also taken, since their data are kept separate from first and second doses data
                vaccinated = vaccine_admin[vaccine_admin["manufacturer"]!="Janssen"].sum()["second_dose"]+vaccine_admin[vaccine_admin["manufacturer"]=="Janssen"].sum()["first_dose"]+vaccine_admin.sum()["previously_infected"]
                if option=="number" or option=="n":
                    return vaccinated
                elif option=="over12" or option=="o":
                    total_over_12 = get_eligible().sum()["population"]
                    return vaccinated/total_over_12
                elif option=="population" or option=="p":
                    total_population = get_istat_region_data().sum()["total"]
                    return vaccinated/total_population
            elif dose == "extra" or dose == "e":
                vaccinated = vaccine_admin.sum()["extra_dose"]
                if option=="number" or option=="n":
                    return vaccinated
                elif option=="over12" or option=="o":
                    total_over_12 = get_eligible().sum()["population"]
                    return vaccinated/total_over_12
                elif option=="population" or option=="p":
                    total_population = get_istat_region_data().sum()["total"]
                    return vaccinated/total_population
                elif option=="eligible" or option=="e":
                    total_eligible = get_extra_dose_eligible().sum()["population"]
                    return vaccinated/total_eligible
            elif dose == "booster" or dose == "b":
                vaccinated = vaccine_admin.sum()["booster_dose"]
                if option=="number" or option=="n":
                    return vaccinated
                elif option=="over12" or option=="o":
                    total_over_12 = get_eligible().sum()["population"]
                    return vaccinated/total_over_12
                elif option=="population" or option=="p":
                    total_population = get_istat_region_data().sum()["total"]
                    return vaccinated/total_population
                elif option=="eligible" or option=="e":
                    total_eligible = get_booster_dose_eligible().sum()["population"]
                    return vaccinated/total_eligible

def tell_total_admin_points():
    """Returns the number of all vaccine administration points in Italy.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    int
        Integer with the number of all vaccine administration points in Italy
    
    See Also
    --------
    get_admin_sites : returns specific info on vaccine administration points
    get_admin_sites_types : returns vaccine administration points types"""

    # get_admin_sites_types returns all administration points, one per row
    data = get_admin_sites_types()
    if data is not None:
        return len(data.index)

def tell_manufacturer_delivered_doses(manufacturer="all", start_date="2020", stop_date="2030"):
    """Returns the number of delivered vaccine doses from the manufacturer given as a parameter in Italy. If string "all" or no string is provided as parameter, it returns the number of delivered vaccine doses from all manufacturers.
    
    Numbers refer to the period between start_date and stop_date. If start_date and stop_date are not specified, returned numbers refer to all time.
    
    Parameters
    ----------
    manufacturer : str
        Vaccine manufacturer name or str "all". ONLY ACCEPTED MANUFACTURERS AND SPELLINGS ARE "Pfizer/BioNTech", "Moderna", "Vaxzevria (AstraZeneca)" AND "Janssen". Str "all" triggers return of number of delivered doses from all manufacturers (default is "all").
    start_date : datetime or datetime-like formatted str
        Starting date of the period of interest (default is beginning of vaccination cycle).
    stop_date : datetime or datetime-like formatted str
        Ending date of the period of interest (default is current day).

    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    ItaCovidLibArgumentError
        Raised when improper arguments are passed to the function.
    
    Returns
    -------
    int64
        Number of delivered vaccine doses from chosen manufacturer or all manufacturers, according to parameter "manufacturer"
    
    See Also
    --------
    get_vaccine_deliveries : full data about vaccine deliveries per manufacturer"""

    # get_vaccine_deliveries returns all delivered doses per day and per manufacturer in a DataFrame. A sum must be performed over days for the chosen manufacturer. np.int64() to avoid a numpy.float64 obj being produced in case of null result. If str "all" is provided, the function returns all delivered doses for all manufacturers.
    # default parameters for start_date and stop_date are respectively "2020" and "2030": this since syntax necessarily requires such default arguments. "2020" covers everything since the beginning, while "2030" covers all future runs of this software (hoping the pandemic ends much earlier!).
    data = get_vaccine_deliveries()[start_date:stop_date]
    if data is not None:
        if manufacturer=="all":
            all_delivered_doses = np.int64(data.sum()["number_of_doses"])
            return all_delivered_doses
        elif manufacturer=="Pfizer/BioNTech" or manufacturer=="Moderna" or manufacturer=="Vaxzevria (AstraZeneca)" or manufacturer=="Janssen":
            manufacturer_delivered_doses = np.int64(data[data["manufacturer"]==manufacturer].sum()["number_of_doses"])
            return manufacturer_delivered_doses
        else:
            raise icl_e.ItaCovidLibArgumentError('no vaccine manufacturer recognized with name "{}". Only accepted names and spellings are "Pfizer/BioNTech", "Moderna", "Vaxzevria (AstraZeneca)" and "Janssen".'.format(manufacturer))

def prepare_for_plotting_on_map(source, on):
    """Makes any Italian COVID Library generated DataFrame with geographical data compatible with geopandas, for subsequent plotting on a map with Italian regions or provinces (depending on the option "on" specified).
    
    Parameters
    ----------
    source : pandas.core.frame.DataFrame
        Pandas DataFrame, with the data to plot, to make compatible with geopandas. Only Italian COVID Library generated DataFrames with geographical data compatible with the option "on" provided are guaranteed to work.
    on : str
        Option for choosing local subdivisions for plotting: regions (options "region", "regions" or "r") or provinces (options "province", "provinces" or "p")
    
    Raises
    ------
    ItaCovidLibKeyError
        Raised when DataFrame cannot be converted into GeoDataFrame (because the required "region" or "province" column with local subdivision data is missing).
    
    ItaCovidLibArgumentError
        Raised when improper arguments are passed to the function.
    
    Returns
    -------
    geopandas.geodataframe.GeoDataFrame
        GeoPandas DataFrame, the Pandas DataFrame given as an argument made compatible with GeoPandas.
    
    See Also
    --------
    plot_on_map : plots directly the DataFrame given as an argument on a map with Italian regions or provinces. Use this function to instantly have the plot, with the possibility of basic customization. Use prepare_for_plotting_on_map if you need the full customization and editing potential of GeoPandas."""
    if on=="region" or on=="regions" or on=="r":
        # file contains Italian regions with their borders
        italy_with_subdivisions = gpd.read_file(str(os.path.join(os.path.dirname(__file__), "regions_map.geojson")))
        try:
            # in this way, input DataFrame includes regional borders
            source_with_geometry = gpd.GeoDataFrame(pd.merge(source, italy_with_subdivisions, on="region", how="inner"))
            return source_with_geometry
        except KeyError:
            raise icl_e.ItaCovidLibKeyError("could not convert source object into GeoDataFrame with regions.") from None
    elif on=="province" or on=="provinces" or on=="p":
        # file contains Italian provinces with their borders
        italy_with_subdivisions = gpd.read_file(str(os.path.join(os.path.dirname(__file__), "provinces_map.geojson")))
        # the following solves an issue with Sardinian provinces, which are not optimally described by the provinces file
        italy_with_subdivisions = italy_with_subdivisions.dissolve(by="province")
        try:
            # in this way, input DataFrame includes province borders
            source_with_geometry = gpd.GeoDataFrame(pd.merge(source, italy_with_subdivisions, on="province", how="inner"))
            return source_with_geometry
        except KeyError:
            raise icl_e.ItaCovidLibKeyError("could not convert source object into GeoDataFrame with provinces.") from None
    else:
        raise icl_e.ItaCovidLibArgumentError("invalid option on. Please see documentation for help on possible options.")

def plot_on_map(source, on, column, title="", legend=True, cmap="Reds"):
    """Plots data on a map of Italy with regions or provinces, depending on the option "on" specified.
    
    Parameters
    ----------
    source : pandas.core.frame.DataFrame
        Pandas DataFrame with the data to plot. Only Italian COVID Library generated DataFrames with geographical data compatible with the option "on" provided are guaranteed to work.
    on : str
        Option for choosing local subdivisions for plotting: regions (options "region", "regions" or "r") or provinces (options "province", "provinces" or "p")
    column : str
        Name of the column with the data to plot
    title : str
        Title to give the plot (default is a null title)
    legend : bool
        Displays or not a legend (default is True)
    cmap : str
        Code name of the color palette for plotting (for the list of codes please see matplotlib.org/stable/tutorials/colors/colormaps)(default is "Reds")
    
    Raises
    ------ 
    ItaCovidLibKeyError
        Raised when DataFrame cannot be converted into GeoDataFrame (because the required "region" or "province" column with local subdivision data is missing).
        
    ItaCovidLibArgumentError
        Raised when improper arguments are passed to the function.
    
    Returns
    -------
    matplotlib.axes._subplots.AxesSubplot
        Map of data by region or province.
    
    See Also
    --------
    prepare_for_plotting_on_map: only turns the Pandas DataFrame given as an argument to a GeoPandas compatible GeoDataFrame, for subsequent plotting. Use this function if you need the full customization and editing potential of GeoPandas."""
    # with the following function, input DataFrame can be plotted on a map correctly
    data_to_plot = prepare_for_plotting_on_map(source, on)
    plot = data_to_plot.plot(column, legend=legend, cmap=cmap)
    # plot returned by plot function also includes anti-aesthetic latitude and longitude axes
    plot.set_axis_off()
    plot.set_title(title)
    return plot

def tell_rt():
    """Returns a DataFrame with Rt values over time in Italy.
    
    Parameters
    ----------
    None
    
    Raises
    ------
    ItaCovidLibConnectionError
        Raised when there are issues with Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame containing Rt values over time.
    
    DataFrame Columns
    -----------------
    date : datetime (index)
        Date
    cases : float64
        Number of new cases on given date
    R_mean : float64
        Rt best value
    R_var : float64
        Variance on R_mean
    Q0.025 : float64
        Rt quantile at 0.025
    Q0.5 : float64
        Rt quantile at 0.5
    Q0.975 : float64
        Rt quantile at 0.975
    
    See Also
    --------
    get_national_trend : returns cases and the general situation of the epidemic in Italy over time"""
    # cases per day are returned by get_national_trend
    trend = get_national_trend()
    # covid19.r_covid, the function calculating Rt index, requires dates without hours, minutes and seconds
    trend.index = trend.index.date
    rt_data = covid19.r_covid(trend["new_cases"])
    # index column must be given a name
    rt_data.index.name = "date"
    # for proper indexing and ranging
    rt_data.index = pd.to_datetime(rt_data.index)
    return rt_data
