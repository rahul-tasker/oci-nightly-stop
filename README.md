# oci-nigthly-stop
Stop your OCI instances at night.

# Supported instances for stop
- Compute Instances
- Autonomous Databases
- Database nodes of database systems (VM and Baremetal)
- Analytics Cloud Instances

This script will start and stop all compute, Autonomous, database and analytics instances within a tenancy. Specific resources can be tagged so that they will not be started and stopped, or the lines for the specific types of resources can be removed from the botton of the `start.py` and `stop.py` files

# Prerequisites
- oci-cli (https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
- Pre-created oci-cli config file (~/.oci/config). 
- You can create by `oci setup config` command and assumed DEFAULT profile in the `~/.oci` path. To use a different path and profile, the `start.py` and `stop.py` files must be edited to reflect those changes.
- Python 3 and above (https://realpython.com/installing-python/)
- oci python SDK (https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/installation.html)


# How to use
1. Clone this repository.

2. Open stop.py and start.py files and edit # Specify your config file section accordingly.

3. `python3 stop.py` will start stopping transactions. `python3 start.py` will start starting transactions

4. Errors will be emitted to the standard output.  Redirect it to the file if you need record logs.

5. There is no scheduler included in the script. Please use cron or othe scheduler as you need. 
    - Exapmple of crontab entry to revoke every 0 am 
    ```
    0 * * * cd /home/opc; python3 -u /home/opc/oci-nightly-stop/stop.py > /home/opc/log/stop_date +%Y%m%d-%H%M%S.log 2>&1
    ```

6. If you want to exclude instances from stopping, set defined tags below for individual compute, db-systems or autnoumous database instances.
    - Tag Namespace : control
    - Defined tag ： nightly_stop
    - Tag value : false
