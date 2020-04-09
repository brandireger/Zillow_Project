import numpy as np
import pandas as pd
from env import get_db_url

sql_MVP = """
SELECT parcelid, bathroomcnt AS bathrooms, bedroomcnt AS bedrooms, 
calculatedfinishedsquarefeet AS square_feet, fips, taxvaluedollarcnt AS value, taxamount AS tax_amount
FROM properties_2017
JOIN predictions_2017 USING (parcelid)
WHERE propertylandusetypeid = 261
AND (transactiondate LIKE '2017-05%%' OR transactiondate LIKE '2017-06%%')
"""

sql_all = """
SELECT *
FROM properties_2017
JOIN predictions_2017 USING (parcelid)
WHERE propertylandusetypeid = 261
AND (transactiondate LIKE '2017-05%%' OR transactiondate LIKE '2017-06%%')
"""

sql_FE = """
SELECT parcelid, regionidneighborhood, basementsqft, fireplaceflag, poolcnt, decktypeid, 
hashottuborspa, fips, taxamount, taxvaluedollarcnt, bathroomcnt, 
bedroomcnt, calculatedfinishedsquarefeet, lotsizesquarefeet
FROM properties_2017
JOIN predictions_2017 USING (parcelid)
WHERE propertylandusetypeid = 261
AND (transactiondate LIKE '2017-05%%' OR transactiondate LIKE '2017-06%%')
"""

def get_data_from_sql(sql):
    url = get_db_url('zillow')
    zillow_df = pd.read_sql(sql, url)
    return zillow_df

def wrangle_zillow(sql):
    zillow = get_data_from_sql(sql)
    zillow.fips = zillow.fips.astype(int)
    zillow['county'] = np.where(zillow.fips == 6037, 'Los_Angeles',
                           np.where(zillow.fips == 6059, 'Orange', 
                                   'Ventura'))
    zillow['state'] = 'CA'
    zillow = zillow.dropna(how='any',axis=0)
    zillow = zillow[zillow.bathrooms != 0]
    zillow = zillow[zillow.bedrooms != 0]
    zillow = zillow.drop(columns='fips')
    zillow['tax_rate'] = zillow.tax_amount / zillow.value
    return zillow

def wrangle_zillow_FE(sql):
    zillow = get_data_from_sql(sql)
    with pd.option_context('mode.use_inf_as_na', True):
        zillow = zillow.dropna(subset=['calculatedfinishedsquarefeet'])
    zillow = zillow.fillna(0)
    zillow['is_extra'] = np.where(zillow.basementsqft > 0, '1',
                              np.where(zillow.fireplaceflag > 0, '1',
                                       np.where(zillow.poolcnt > 0, '1',
                                                np.where(zillow.decktypeid > 0, '1',
                                                         np.where(zillow.hashottuborspa > 0, '1', '0')))))
    zillow.fips = zillow.fips.astype(int)
    zillow['county'] = np.where(zillow.fips == 6037, 'Los_Angeles',
                            np.where(zillow.fips == 6059, 'Orange', 
                                    'Ventura'))
    zillow['state'] = 'CA'
    zillow['tax_rate'] = (zillow.taxamount / zillow.taxvaluedollarcnt).round(4)
    zillow['size_ratio'] = (zillow.calculatedfinishedsquarefeet / zillow.lotsizesquarefeet).round(4)
    zillow = zillow.rename(columns={
    "calculatedfinishedsquarefeet": "home_sf",
    "taxvaluedollarcnt": "value",
    "bathroomcnt": "baths",
    "bedroomcnt": "beds",
    "regionidneighborhood": "neighborhood"})
    zillow.value = zillow.value.astype(int)
    zillow.beds = zillow.beds.astype(int)
    zillow.home_sf = zillow.home_sf.astype(int)
    zillow.neighborhood = zillow.neighborhood.astype(int)
    zillow = zillow.drop(columns=['fips', 'basementsqft', 'fireplaceflag',
    'poolcnt', 'decktypeid', 'hashottuborspa', 'taxamount', 'lotsizesquarefeet'])
    zillow = zillow.dropna(how='any',axis=0)
    return zillow