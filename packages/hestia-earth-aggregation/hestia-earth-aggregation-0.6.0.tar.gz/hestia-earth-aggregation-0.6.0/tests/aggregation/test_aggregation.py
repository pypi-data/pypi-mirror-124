from unittest.mock import patch
from hestia_earth.schema import NodeType

from tests.utils import PRODUCT, SOURCE, WORLD
from hestia_earth.aggregation import aggregate

class_path = 'hestia_earth.aggregation'


@patch(f"{class_path}.find_nodes", return_value=[])
@patch(f"{class_path}._call_aggregate_by_type", return_value={})
def test_aggregate(mock_aggregate, *args):
    # aggregate by country
    aggregate(NodeType.IMPACTASSESSMENT.value, WORLD, PRODUCT, 2000, 2009, SOURCE)
    mock_aggregate.assert_called_once()
