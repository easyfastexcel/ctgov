# ctgov
#### This module includes functions and a class to query www.ClinicalTrials.gov, extract study data, and facilitate utilization.  

## Examples
#### Example 1: extract study data of the first 10 studies from all studies in www.ClinicalTrials.gov
<code>
  import ctgov

  data = ctgov.DataExtract()
</code>

###### DataExtract() has the following parameters with default values; in this example, the default parameters are not altered to search through all studies in www.clinicaltrials.gov and return the study data of the first 10 studies in the search results

<code>down_count=10</code><br/>
<code>down_flds='default'</code><br/>
<code>down_fmt='xml'</code><br/>
<code>down_chunk=1</code><br/>
<code>param_term=None</code><br/>
<code>param_type=None</code><br/>
<code>param_rslt=None</code><br/>
<code>param_status=None</code><br/>
<code>param_cond=None</code><br/>
<code>param_intr=None</code><br/>
<code>param_spons=None</code><br/>
<code>param_phase=None</code><br/>
<code>param_fund=None</code><br/>

###### get_list_of_studies_in_json() will return the study data in json format
<code>
  data.get_list_of_studies_in_json()
</code>

## Dependencies
#### os, sys, json, xmltodict, datetime, requests, urllib, bs4, pprint

## Project Goals
#### Add addtional classes to:
####     - deliver and store data into SQL/NoSQL DBs
####     - transform and visualize data
