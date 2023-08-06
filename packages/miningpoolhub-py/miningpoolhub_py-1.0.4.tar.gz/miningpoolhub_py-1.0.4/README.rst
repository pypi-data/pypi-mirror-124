
miningpoolhub_py
----------------
.. image:: https://github.com/CoryKrol/miningpoolhub_py/workflows/CI/badge.svg?branch=master
     :target: https://github.com/CoryKrol/miningpoolhub_py/actions?workflow=CI
     :alt: CI Status

A Python wrapper for the Mining Pool Hub REST API

Installation
------------
Install with pip:

.. code-block:: bash

   pip install miningpoolhub_py

Usage
------------

Universal Endpoints
-------------------
Mining Pool Hub supports auto switching between coins. Obtain statistics for all coins with the following methods

.. code-block:: python

   from miningpoolhub_py import Pool

   pool_instance = Pool('ethereum')
   pool_instance.get_all_user_balances()
   pool_instance.get_auto_switching_and_profits_statistics()
   pool_instance.get_mining_profit_and_statistics()


Pool Selection
-------------------
Mining Pool Hub has different base urls for each coin they offer. Create a new pool object for every coin you are
interested in mining statistics for

.. code-block:: python

   from miningpoolhub_py import Pool
   pool_instance = Pool('ethereum')
   pool_instance.get_dashboard()

Authentication
-------------------

Environment File
--------------------------------
.. code-block::

   MPH_API_KEY=<api_key>

Pass API Key to Pool Constructor
--------------------------------
.. code-block:: python

   from miningpoolhub_py import Pool
   pool_instance = Pool('ethereum', '<api_key>')

References
------------

Mining Pool Hub
---------------------------------------------
- `Mining Pool Hub <https://miningpoolhub.com/>`_
- `API Reference <https://github.com/miningpoolhub/php-mpos/wiki/API-Reference>`_
- `Mining Pool Hub API Key <https://miningpoolhub.com/?page=account&action=edit>`_

Python API Wrapper & and CI/CD Pipeline
---------------------------------------------
- `Building and Testing an API Wrapper in Python <https://semaphoreci.com/community/tutorials/building-and-testing-an-api-wrapper-in-python>`_
- `Creating a Python API Wrapper \(Ally Invest API\) <https://medium.com/analytics-vidhya/creating-a-python-api-wrapper-ally-invest-api-568934a1411c>`_
- `Publishing a Package to PyPI with Poetry <https://www.ianwootten.co.uk/2020/10/20/publishing-a-package-to-pypi-with-poetry/>`_
- `Publishing to PyPI Using GitHub Actions <https://www.ianwootten.co.uk/2020/10/23/publishing-to-pypi-using-github-actions/>`_
   - `Code Repo <https://github.com/niftydigits/ftrack-s3-accessor/tree/master/.github/workflows>`_

Contribute
----------

- `Issue Tracker <https://github.com/CoryKrol/miningpoolhub_py/issues>`_
- `Source Code <https://github.com/CoryKrol/miningpoolhub_py>`_

Support
-------

`Open an issue <https://github.com/CoryKrol/miningpoolhub_py/issues/new>`_

License
-------

The project is licensed under the Apache 2 license