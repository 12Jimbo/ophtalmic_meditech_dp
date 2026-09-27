## Links
[EUDAMED API Portal](https://developer.datalake.sante.service.ec.europa.eu/api-details#api=94b9e658-d721-4b58-8d96-022c490f7a17&operation=411c8f92-26fa-4451-9377-7a13b5d17915)

[EUDAMED InfoCenter](https://webgate.ec.europa.eu/eudamed-help/en/documentation/user-guides-and-templates.html)
--> a list of pdf documents, including sources\EUDAMED\API\Public API - user guide.pdf

[EUDAMED Tech Doc](https://webgate.ec.europa.eu/eudamed-help/en/documentation/technical-documentation.html)
--> most pertinent to semantic field descriptions

[Public Health Topics](https://health.ec.europa.eu/medical-devices-topics-interest_en)
--> [European Medical Devices Nomenclature (EMDN)](https://health.ec.europa.eu/medical-devices-topics-interest/european-medical-devices-nomenclature-emdn_en)
--> [download list](https://webgate.ec.europa.eu/dyna2/emdn/M90#title)
--> sources\EUDAMED\data dictionaries\EMDN\EMDN v2026_EN.csv


## ERGONOMICS

#### Pagination
The 1000 rows cap is a problem.
Doc says that when using GET in JSON format, a continuation link is provided (if the returned data is incomplete) to query the following 1000. EXPE CONFIRMED


## Semanics
From sources\EUDAMED\API\Public API - user guide.pdf - user guide.pdf it can be inferred that CA_name valid field values are the subset of name field values where actor_type = "Competent Authority" (analogously for CA_actor_id).

Device identifiers - see sources\EUDAMED\downloaded docs\md_eudamed-udi-concept_en.pdf
UDI means unique device identifier.
`Basic UDI-DI`: Main key in the database and relevant documentation, groups devices with same intended purpose, risk class and essential design and manufacturing characteristics. 
`UDI-DI`: Specific to a model/variation/version
`Package UDI-DI`: groups devices that are packaged together in serving a medical purpose (es: collirium + tomographer)

In the relationship between 'Basic UDI-DI' and 'UDI-DI', one or multiple UDI-DIs can be linked to one Basic UDI-DI. 
The registration of a Basic UDI-DI must always be accompanied by at least one UDI-DI.
Each UDI-DI inherits the attributes of its linked Basic UDI-DI. Package definition is not required.


udi/NOMENCLATURE_CODE is the medical categorization of the device, to be matched in EMDN map


## Tech Doc

#### Data dictionaries (Excel files)
Common

EUD Common - data dictionary | 

Actor

ACT - data dictionary | 

UDI/Devices

UDI Devices - data dictionary | 

Certificates

CRF - certificates - data dictionary | 

CRF - Refused certificates and applications - data dictionary

CRF - varia - data dictionary

CRF - CECP - data dictionary

Market Surveillance

MSU - data dictionary


#### Business rules/enumerations
These seem to apply to actors who want to insert data into the database rather than pulling data from it.

Common

EUD Common - business rules | This purpose of this document is to provide an overview of the scope and conditions data needs to be provided to be valid information for EUDAMED.
Business rules describe a required set of conditions that will be validated when submitting information.

EUD Common - enumerations | This purpose of this document is to provide an overview of the possible values fields can contain to be valid information for EUDAMED throughout the releases. 

Actor

AIM - enumerations |

ACT - business rules |

ACT - enumerations | 

AIM - business rules |

Certificates

CRF - business rules | 

CRF - enumerations | 

Market Surveillance |

MSU - business rules | 

MSU - enumerations | 

UDI/Devices

UDI Devices - business rules | 

UDI Devices - enumerations | 