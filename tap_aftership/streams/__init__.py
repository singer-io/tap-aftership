from tap_aftership.streams.trackings import Trackings
from tap_aftership.streams.couriers import Couriers
from tap_aftership.streams.courier_connections import CourierConnections
from tap_aftership.streams.item_returns import ItemReturns
from tap_aftership.streams.item_tags import ItemTags
from tap_aftership.streams.query_claims import QueryClaims
from tap_aftership.streams.query_coverages import QueryCoverages
from tap_aftership.streams.stores import Stores
from tap_aftership.streams.orders import Orders
from tap_aftership.streams.products import Products
from tap_aftership.streams.fulfillments import Fulfillments
from tap_aftership.streams.memberships import Memberships
from tap_aftership.streams.roles import Roles
from tap_aftership.streams.shipping_rates import ShippingRates
from tap_aftership.streams.shipping_labels import ShippingLabels
from tap_aftership.streams.shipping_manifests import ShippingManifests
from tap_aftership.streams.shipping_couriers import ShippingCouriers
from tap_aftership.streams.cancel_labels import CancelLabels
from tap_aftership.streams.pickups import Pickups
from tap_aftership.streams.cancel_pickups import CancelPickups
from tap_aftership.streams.shipper_accounts import ShipperAccounts
from tap_aftership.streams.locations import Locations

STREAMS = {
    "trackings": Trackings,
    "couriers": Couriers,
    "courier_connections": CourierConnections,
    "item_returns": ItemReturns,
    "item_tags": ItemTags,
    "query_claims": QueryClaims,
    "query_coverages": QueryCoverages,
    "stores": Stores,
    "orders": Orders,
    "products": Products,
    "fulfillments": Fulfillments,
    "memberships": Memberships,
    "roles": Roles,
    "shipping_rates": ShippingRates,
    "shipping_labels": ShippingLabels,
    "shipping_manifests": ShippingManifests,
    "shipping_couriers": ShippingCouriers,
    "cancel_labels": CancelLabels,
    "pickups": Pickups,
    "cancel_pickups": CancelPickups,
    "shipper_accounts": ShipperAccounts,
    "locations": Locations,
}

