import numpy as np
import pandas as pd
from env import get_db_url

def get_data_from_sql():
    sql = """
    SELECT parcelid, bathroomcnt AS bathrooms, bedroomcnt AS bedrooms, 
    calculatedfinishedsquarefeet AS square_feet, fips, taxvaluedollarcnt AS value, taxamount AS tax_amount
    FROM properties_2017
    JOIN predictions_2017 USING (parcelid)
    WHERE propertylandusetypeid = 261
    AND (transactiondate LIKE '2017-05%%' OR transactiondate LIKE '2017-06%%')
    """
    url = get_db_url('zillow')
    zillow_df = pd.read_sql(sql, url)
    return zillow_df

def wrangle_zillow():
    zillow = get_data_from_sql()
    zillow.fips = zillow.fips.astype(int)
    zillow['county'] = np.where(zillow.fips == 6037, 'Los_Angeles',
                           np.where(zillow.fips == 6059, 'Orange', 
                                   'Ventura'))
    zillow['state'] = 'CA'
    zillow = zillow.dropna(how='any',axis=0)
    zillow = zillow[zillow.bathrooms != 0]
    zillow = zillow[zillow.bedrooms != 0]
    zillow = zillow.drop(columns='fips')
    zillow = zillow.set_index('parcelid')
    zillow['tax_rate'] = zillow.tax_amount / zillow.value
    return zillow


