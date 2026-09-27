
## ERGONOMICS
found api documentation: [EUDAMED API](https://developer.datalake.sante.service.ec.europa.eu/api-details#api=94b9e658-d721-4b58-8d96-022c490f7a17&operation=411c8f92-26fa-4451-9377-7a13b5d17915). The EUDAMED site does not seem to link to this, and only offers manual search from portal or download.


The 1000 rows cap is a problem.
Doc says that when using GET in JSON format, a continuation link is provided (if the returned data is incomplete) to query the following 1000. EXPE CONFIRMED



## SEMANTICS

From sources\exploration\EUDAMED Public API - user guide.pdf it can be inferred that CA_name valid field values are the subset of name field values where actor_type = "Competent Authority" (analogously for CA_actor_id).

UDI = unique device identifier

udi/NOMENCLATURE_CODE is the medical categorization of the device - crucial to the project. References:

https://health.ec.europa.eu/medical-devices-topics-interest/european-medical-devices-nomenclature-emdn_en

https://webgate.ec.europa.eu/dyna2/emdn/