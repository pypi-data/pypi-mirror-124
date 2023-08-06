import pandas as pd
import requests
import io
import itacovidlib.exceptions as icl_e


def _get(url):
    """Returns a DataFrame from the .csv file at which the URL provided as a parameter points, properly parsing it. Meant to be invoked by get_<resource_name> functions.
    
    Parameters
    ----------
    url : str
        URL at which the required .csv file is.
    
    Raises
    ------
    ItaCovidLibConnectionError
        Connection error coming from Italian COVID Library, making it clear to the user it comes from this library and not other ones. This error is raised when the library fails to get data from the Internet, e.g. for lack of Internet connection.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas DataFrame with the data from the .csv file at which url points.
    
    See Also
    --------
    Any function whose name begins with "get_" : uses _get"""

    try:
        downloaded_content = requests.get(url).content
        dataframe = pd.read_csv(io.StringIO(downloaded_content.decode('utf-8')))
        return dataframe
    # error reraising makes it clear to the user the error was actually raised by Italian COVID Library and not other libraries.
    except requests.exceptions.ConnectionError:
        raise icl_e.ItaCovidLibConnectionError("connection failure. Most probable cause is lack of Internet connection.") from None

