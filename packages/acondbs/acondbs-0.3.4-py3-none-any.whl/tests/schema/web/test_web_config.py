import pytest

from ..funcs import assert_query

QUERY = """
{ webConfig {
    configId
    headTitle
    toolbarTitle
    devtoolLoadingstate
    productCreationDialog
    productUpdateDialog
    productDeletionDialog
  }
}
"""


##__________________________________________________________________||
params = [
    pytest.param(
        {"query": QUERY},
        id="query",
    ),
]


##__________________________________________________________________||
@pytest.mark.parametrize("data", params)
@pytest.mark.asyncio
async def test_schema(app, snapshot, data):
    await assert_query(app, snapshot, data)

##__________________________________________________________________||
