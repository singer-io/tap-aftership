# tap-aftership

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).

This tap:

- Pulls raw data from the [aftership API].
- Extracts the following resources:
    - [Trackings](https://www.aftership.com/docs/tracking/jh865r66gc6hi-get-trackings)

    - [Couriers](https://www.aftership.com/docs/tracking/ukw8ouy82dp1k-get-couriers)

    - [CourierConnections](https://www.aftership.com/docs/tracking/2ar6bpph8n7ye-get-courier-connections)

    - [ItemReturns](https://www.aftership.com/docs/returns/wpx1lk91k5ima-get-returns)

    - [ItemTags](https://www.aftership.com/docs/returns/sxu3emct2h6is-get-item-tags)

    - [QueryClaims](https://www.aftership.com/docs/protection/e99b7b198fd97-query-claims)

    - [QueryCoverages](https://www.aftership.com/docs/protection/0202765fded3f-query-coverages)

    - [Stores](https://www.aftership.com/docs/commerce/yc24p1srfyqiv-get-stores)

    - [Orders](https://www.aftership.com/docs/commerce/kr3dy6e5ma49n-get-orders)

    - [Products](https://www.aftership.com/docs/commerce/rloip27l58tm1-get-products)

    - [Fulfillments](https://www.aftership.com/docs/commerce/6dafeb354dd2b-get-fulfillments)

    - [Memberships](https://www.aftership.com/docs/members/50fa1b4e7b871-get-memberships)

    - [Roles](https://www.aftership.com/docs/members/bb5124963ea73-get-roles)

    - [ShippingRates](https://www.aftership.com/docs/shipping/99f88b084657b-get-rates)

    - [ShippingLabels](https://www.aftership.com/docs/shipping/c056230c3b6c4-get-labels)

    - [ShippingManifests](https://www.aftership.com/docs/shipping/8ba86e501d12e-get-manifests)

    - [ShippingCouriers](https://www.aftership.com/docs/shipping/89c99df22fcd7-get-all-couriers)

    - [CancelLabels](https://www.aftership.com/docs/shipping/24ec02f862c50-get-the-cancelled-labels)

    - [Pickups](https://www.aftership.com/docs/shipping/x8mxu5wa7m6y3-get-pickups)

    - [CancelPickups](https://www.aftership.com/docs/shipping/35p8o3dsqpaqc-get-the-cancelled-pickups)

    - [ShipperAccounts](https://www.aftership.com/docs/shipping/5742112a2c755-get-shipper-accounts)

    - [Locations](https://www.aftership.com/docs/shipping/bdb851fc7dfdc-get-locations)

- Outputs the schema for each resource
- Incrementally pulls data based on the input state


## Streams


**[trackings](https://www.aftership.com/docs/tracking/jh865r66gc6hi-get-trackings)**
- Data Key = trackings
- Primary keys: id
- Replication strategy: INCREMENTAL

**[couriers](https://www.aftership.com/docs/tracking/ukw8ouy82dp1k-get-couriers)**
- Data Key = couriers
- Primary keys: ['slug']
- Replication strategy: FULL_TABLE

**[courier_connections](https://www.aftership.com/docs/tracking/2ar6bpph8n7ye-get-courier-connections)**
- Data Key = courier_connections
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[item_returns](https://www.aftership.com/docs/returns/wpx1lk91k5ima-get-returns)**
- Data Key = returns
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[item_tags](https://www.aftership.com/docs/returns/sxu3emct2h6is-get-item-tags)**
- Data Key = item_tags
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[query_claims](https://www.aftership.com/docs/protection/e99b7b198fd97-query-claims)**
- Data Key = claims
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[query_coverages](https://www.aftership.com/docs/protection/0202765fded3f-query-coverages)**
- Data Key = coverages
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[stores](https://www.aftership.com/docs/commerce/yc24p1srfyqiv-get-stores)**
- Data Key = stores
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[orders](https://www.aftership.com/docs/commerce/kr3dy6e5ma49n-get-orders)**
- Data Key = orders
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[products](https://www.aftership.com/docs/commerce/rloip27l58tm1-get-products)**
- Data Key = products
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[fulfillments](https://www.aftership.com/docs/commerce/6dafeb354dd2b-get-fulfillments)**
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[memberships](https://www.aftership.com/docs/members/50fa1b4e7b871-get-memberships)**
- Data Key = memberships
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[roles](https://www.aftership.com/docs/members/bb5124963ea73-get-roles)**
- Data Key = roles
- Primary keys: ['code']
- Replication strategy: FULL_TABLE

**[shipping_rates](https://www.aftership.com/docs/shipping/99f88b084657b-get-rates)**
- Data Key = rates
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[shipping_labels](https://www.aftership.com/docs/shipping/c056230c3b6c4-get-labels)**
- Data Key = labels
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[shipping_manifests](https://www.aftership.com/docs/shipping/8ba86e501d12e-get-manifests)**
- Data Key = manifests
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[shipping_couriers](https://www.aftership.com/docs/shipping/89c99df22fcd7-get-all-couriers)**
- Data Key = couriers
- Primary keys: ['slug']
- Replication strategy: FULL_TABLE

**[cancel_labels](https://www.aftership.com/docs/shipping/24ec02f862c50-get-the-cancelled-labels)**
- Data Key = cancel_labels
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[pickups](https://www.aftership.com/docs/shipping/x8mxu5wa7m6y3-get-pickups)**
- Data Key = pickups
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[cancel_pickups](https://www.aftership.com/docs/shipping/35p8o3dsqpaqc-get-the-cancelled-pickups)**
- Data Key = cancel_pickups
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[shipper_accounts](https://www.aftership.com/docs/shipping/5742112a2c755-get-shipper-accounts)**
- Data Key = shipper_accounts
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[locations](https://www.aftership.com/docs/shipping/bdb851fc7dfdc-get-locations)**
- Data Key = locations
- Primary keys: ['location_id']
- Replication strategy: FULL_TABLE



## Authentication

## Quick Start

1. Install

    Clone this repository, and then install using setup.py. We recommend using a virtualenv:

    ```bash
    > virtualenv -p python3 venv
    > source venv/bin/activate
    > python setup.py install
    OR
    > cd .../tap-aftership
    > pip install -e .
    ```
2. Dependent libraries. The following dependent libraries were installed.
    ```bash
    > pip install singer-python
    > pip install target-stitch
    > pip install target-json

    ```
    - [singer-tools](https://github.com/singer-io/singer-tools)
    - [target-stitch](https://github.com/singer-io/target-stitch)

3. Create your tap's `config.json` file.  The tap config file for this tap should include these entries:
   - `start_date` - the default value to use if no bookmark exists for an endpoint (rfc3339 date string)
   - `user_agent` (string, optional): Process and email for API logging purposes. Example: `tap-aftership <api_user_email@your_company.com>`
   - `request_timeout` (integer, `300`): Max time for which request should wait to get a response. Default request_timeout is 300 seconds.

    ```json
    {
        "start_date": "2019-01-01T00:00:00Z",
        "user_agent": "tap-aftership <api_user_email@your_company.com>",
        "request_timeout": 300
    }

    ```
    Optionally, also create a `state.json` file. `currently_syncing` is an optional attribute used for identifying the last object to be synced in case the job is interrupted mid-stream. The next run would begin where the last job left off.

    ```json
    {
        "currently_syncing": "dummy_stream1",
        "bookmarks": {
            "dummy_stream1": "2019-09-27T22:34:39.000000Z",
            "dummy_stream2": "2019-09-28T15:30:26.000000Z",
            "dummy_stream3": "2019-09-28T18:23:53Z"
        }
    }
    ```

4. Run the Tap in Discovery Mode
    This creates a catalog.json for selecting objects/fields to integrate:
    ```bash
    tap-aftership --config config.json --discover > catalog.json
    ```
   See the Singer docs on discovery mode
   [here](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode).

5. Run the Tap in Sync Mode (with catalog) and [write out to state file](https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#running-a-singer-tap-with-a-singer-target)

    For Sync mode:
    ```bash
    > tap-aftership --config tap_config.json --catalog catalog.json > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    To load to json files to verify outputs:
    ```bash
    > tap-aftership --config tap_config.json --catalog catalog.json | target-json > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    To pseudo-load to [Stitch Import API](https://github.com/singer-io/target-stitch) with dry run:
    ```bash
    > tap-aftership --config tap_config.json --catalog catalog.json | target-stitch --config target_config.json --dry-run > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```

6. Test the Tap
    While developing the aftership tap, the following utilities were run in accordance with Singer.io best practices:
    Pylint to improve [code quality](https://github.com/singer-io/getting-started/blob/master/docs/BEST_PRACTICES.md#code-quality):
    ```bash
    > pylint tap_aftership -d missing-docstring -d logging-format-interpolation -d too-many-locals -d too-many-arguments
    ```
    Pylint test resulted in the following score:
    ```bash
    Your code has been rated at 9.67/10
    ```

    To [check the tap](https://github.com/singer-io/singer-tools#singer-check-tap) and verify working:
    ```bash
    > tap_aftership --config tap_config.json --catalog catalog.json | singer-check-tap > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```

    #### Unit Tests

    Unit tests may be run with the following.

    ```
    python -m pytest --verbose
    ```

    Note, you may need to install test dependencies.

    ```
    pip install -e .'[dev]'
    ```
---

Copyright &copy; 2019 Stitch
