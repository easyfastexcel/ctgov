# ctgov modules
* ctgov.py 
* ctgov_zip.py

## ctgov.py
#### This module includes functions and a class to query www.ClinicalTrials.gov, extract study data, and facilitate utilization.  

### Examples
#### Example 1: extract study data of the first 10 studies from all studies in www.ClinicalTrials.gov
<code>
  import ctgov

  data = ctgov.DataExtract()
</code>

##### DataExtract() has the following parameters with default values; in this example, the default parameters are not altered to search through all studies in www.clinicaltrials.gov and return the study data of the first 10 studies in the search results

<code>down_count=10<i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;download count; options: 10, 100, 1000, or 10000</i></code><br/>
<code>down_flds='default'<i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;download fields; options: 'all' or 'default'</i></code><br/>
<code>down_chunk=1 <i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;download chunck; chunk 1 is 1-10, chunk 2 is 11-20, chunk 3  is 21-30,...</i></code><br/>
<code>param_term=None<i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;terms; free text</i></code><br/>
<code>param_type=None<i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;study type; options: 'Intr', 'Obsr', 'PReg', 'Expn'</i></code><br/>
<code>param_rslt=None<i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;study results; options: 'With', 'Without'</i></code><br/>
<code>param_status=None<i>&nbsp;&nbsp;&nbsp;&nbsp;status; options: 'b', 'a', 'f', 'd', 'g', 'h', 'e', 'i', 'm', 'c', 'j', 'k', 'l' (footnote1)</i></code><br/>
<code>param_cond=None<i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;conditions; free text</i></code><br/>
<code>param_intr=None<i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;intervention treatment(s); free text</i></code><br/>
<code>param_spons=None<i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sponsor(s); free text</i></code><br/>
<code>param_phase=None<i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;study phase; options: 4 (early P1), 0 (P1), 1 (P2), 2 (P3), 3 (P4)</i></code><br/>
<code>param_fund=None<i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;funder type; options: 0 (NIH), 1 (Other US), 2 (Industry), 3 (all others; univ, indiv, org)</i></code><br/>
###### (footnote1: 'b' is Not yet recruiting, 'a' is Recruiting, 'f' is Enrolling by invitation, 'd' is Active, not recruiting, 'g' is Suspended, 'h' is Terminated, 'e' is Completed, 'i' is Withdrawn, 'm' is Unknown status, 'c' is Available, 'j' is No longer available, 'k' is Temporarily not available, 'l' is Approved for marketing)

##### get_list_of_studies_in_json() will return the study data in json format
<code>
  data.get_list_of_studies_in_json()
</code>

### Dependencies
#### The following modules (note: some of these libs are already built-in python) must be installed for ctgov to work properly 
##### os, sys, json, xmltodict, datetime, requests, urllib, bs4, pprint

### Project Goals
#### Add addtional classes to:
#####     - deliver and store data into SQL/NoSQL DBs
#####     - transform and visualize data


## ctgov_zip.py
development in progress
