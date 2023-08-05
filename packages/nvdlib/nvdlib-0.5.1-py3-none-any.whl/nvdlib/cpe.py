import datetime

from datetime import datetime
from .get import __get
from .classes import __convert

def searchCPE(**kwargs):
    """Build and send GET request then return list of objects containing a collection of CPEs.
    
    :param modStartDate: CPE modification start date
    :type modStartDate: ISO 8601 date/time
        Example: '2020-06-28 00:00'

    :param modEndDate: CPE modification end date
    :type modEndDate: ISO 8601 date/time
        Example: '2020-06-28 00:00'

    :param includeDeprecated: Include deprecated CPE names that have been replaced.
    :type includeDeprecated: Bool True

    :param keyword: Free text keyword search.
    :type keyword: str

    :param cpeMatchString: CPE match string search.
    :type cpeMatchString: str

    :param cves: Return vulnerabilities. 
        **Warning**: This parameter may incur large amounts of results causing delays.
    :type cves: bool True

    :param limit: Limits the number of results of the search.
    :type limit: int

    """


    def __buildCPECall(kwargs):
        parameters = []

        if 'modStartDate' in kwargs:
            date = str(datetime.strptime(kwargs['modStartDate'], '%Y-%m-%d %H:%M').isoformat()) + ':000 UTC-00:00'
            modStartDate = 'modStartDate=' + date
            parameters.append(modStartDate)

        if 'modEndDate' in kwargs:
            date = str(datetime.strptime(kwargs['modEndDate'], '%Y-%m-%d %H:%M').isoformat()) + ':000 UTC-00:00'
            modEndDate = 'modEndDate=' + date
            parameters.append(modEndDate)     
        
        if 'includeDeprecated' in kwargs:
            includeDeprecated = 'includeDeprecated=true'
            parameters.append(includeDeprecated)
        
        if 'keyword' in kwargs:
            keyword = 'keyword=' + kwargs['keyword']
            parameters.append(keyword)

        if 'cpeMatchString' in kwargs:
            cpeMatchString = 'cpeMatchString=' + kwargs['cpeMatchString']
            parameters.append(cpeMatchString)

        if 'cves' in kwargs:
            if kwargs['cves'] == True:
                cves = 'addOns=cves'
                parameters.append(cves)
            else:
                raise TypeError("cves parameter can only be boolean True.")

        if 'limit' in kwargs:
            limit = 'resultsPerPage=' + str(kwargs['limit'])
            if kwargs['limit'] > 5000 or kwargs['limit'] < 1:
                raise ValueError('Limit parameter must be between 1 and 5000')
            parameters.append(limit)

        return parameters

    # Build the URL for the request
    parameters = __buildCPECall(kwargs)

    # Send the GET request for the JSON and convert to dictionary
    raw = __get('cpe', parameters, kwargs)

    cpes = []
    # Generates the CVEs into objects for easy referencing and appends them to self.cves
    for eachCPE in raw['result']['cpes']:
        cpe = __convert('cpe', eachCPE)
        cpe.getvars() # Generates cpe.title and cpe.name
        cpes.append(cpe)
    return cpes