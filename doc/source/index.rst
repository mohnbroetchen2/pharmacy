.. anishare documentation master file, created by
   sphinx-quickstart on Tue May 29 13:02:59 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation of pharmacy !
==========================================

.. toctree::
   :maxdepth: 3
   :caption: Contents:

Introduction
------------

**pharmacy** is a webservice for research institutes to manage there pharmacy stock and the submissions to the animal caretakers.

It has been developed at the `Leibniz institute for aging research <http://www.leibniz-fli.de>`_ in
Jena. This django app is meant to be used by Veterinarians who are responsible for the pharmacy. The system should help documentation and
to have a quick overview over the pharmacy stock.

.. image:: images/start.png
    :width: 99%
 

Contact
-------

Technical and application support: Fabian Monheim (CF Life Science Computing), fabian.monheim@leibniz-fli.de, 03641-65-6872

Content support: Animal Facility and Animal Welfare Officer

License
-------
The software was developed at the Leibniz Institute on Aging - Fritz Lipmann Institute (FLI; http://www.leibniz-fli.de/) under a mixed licensing model. 
Researchers at academic and non-profit organizations can use pharmacy using the included license, while for-profit organizations are required to purchase a license. 
By downloading the package you agree with conditions of the FLI Software License Agreement for Academic Non-commercial Research (LICENSE.pdf).

Sitemap
-------
* Start: http://pharmacy.leibniz-fli.de
* Full overview: http://pharmacy.leibniz-fli.de/all
* Passwort change: http://pharmacy.fli-leibniz.de/accounts/password_change/
* Add pup directly from PyRAT: http://pharmacy.leibniz-fli.de/changes
* Administration / Add pharmacy and add order: https://pharmcy.leibniz-fli.de/admin
.. User types
----------
* User: FLI employee from the animal facility  Veterinarians and the Animal Welfare Officer.
* Manager: this person is appointed within the research group and coordinates the offering/sharing of animals. 
* Person who perform euthanasia: this person will be named in anishare by the manager (relevant only for organ sharing).
* Superuser: this person is administrator of the database and has the full control of the function (IT, animal welfare officers, veterinarians and heads of animal facilities).

Main user interface
-------------------

Overview
""""""""

The home page shows the stock which is currently available.

.. image:: images/start.png
    :width: 60%

It is possible to export the available stock as .csv file using the Button ``Options`` and ``Export``. Furthermore it's possible to export all 
submissions within a period of time using the button ``Export advanced``.

.. image:: images/options.png
    :width: 80%

Use the link of the pharmacy name column to see all submissions belonging to a pharmacy (ignoring a a single order) 
The ``more`` link (last coloumn) shows all orders concerning the pharmacy. 
To create a submissions you can use the ``submit`` link (second last coloumn). If there are containers from several orders available the user has to select
an order from which the pharmacy is taken. 

Full Overview
"""""""""""""

The full overview shows also pharmacy which isn't available

Entities
-------------------

Persons
"""""""
`Persons <http://pharmacy.leibniz-fli.de/admin/pharmadoc/person/>`_.
Persons are members of the institute and can apply for a pharmacy

Pharmacy
""""""""
`Pharmacy <http://pharmacy.scinet.fli-leibniz.de/admin/pharmadoc/pharmacy/>`_.
The pharmacy is the medicine. The name is composed of the name of the pharmacy and the dose of the active molecule

Order
"""""
`Order <http://pharmacy.scinet.fli-leibniz.de/admin/pharmadoc/order/>`_.
An Order increase the stock of a pharmacy. Every order gets an identifier from the system. 
The identifier is composed of the first three letters of the name of the pharmacy and the delivery date. If there is already an order with the designated
identifier the new identifier gets a ongoing number as last character.
Every order belongs to a pharmacy and have a state ``active`` or ``deactivated``. It turns automatically to ``deactivated`` if all containers are submitted.
In case of reaching the expiry date or something else the status can be set manually. It isn't possible to create a new submissions from a order which is set to ``deactivated``.

Company
"""""""
`Company <http://pharmacy.scinet.fli-leibniz.de/admin/pharmadoc/company/>`_.
A Company is the manufacturer of the pharmacy.

Drug class
""""""""""
`Drug class <http://pharmacy.scinet.fli-leibniz.de/admin/pharmadoc/drugclass/>`_.
The drug class helps to classify the pharmacy into several groups like ``Antibiotika`` or ``Anästhetikum``


Molecules
"""""""""
`Molecule <http://pharmacy.scinet.fli-leibniz.de/admin/pharmadoc/molecule/>`_.
The molecule is the active substance of a pharmacy

