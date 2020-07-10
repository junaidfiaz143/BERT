from planet import api
import sys
client = api.ClientV1("18272744a851407eb14b599ce28ad2eb")

# https://tiles.planet.com/data/v1/item-types/PSScene3Band/items/20160223_174714_0c72/thumb?api_key=18272744a851407eb14b599ce28ad2eb

aoi = {
  "type": "Polygon",
  "coordinates": [
    [
            [
              34.1015625,
              7.36246686553575
            ],
            [
              81.9140625,
              7.36246686553575
            ],
            [
              81.9140625,
              37.996162679728116
            ],
            [
              34.1015625,
              37.996162679728116
            ],
            [
              34.1015625,
              7.36246686553575
            ]
    ]
  ]
}

# build a filter for the AOI
query = api.filters.and_filter(
  api.filters.geom_filter(aoi),
  api.filters.range_filter('cloud_cover', gt=0),    
  api.filters.date_range('acquired', gt='2020-06-13T00:00:00Z', lte="2020-06-16T00:00:00Z"),
  api.filters.permission_filter('assets:download')
)

# we are requesting PlanetScope 4 Band imagery
item_types = ['PSScene4Band']
request = api.filters.build_search_request(query, item_types)

# this will cause an exception if there are any API related errors
results = client.quick_search(request)
dd = api.downloader.create(client, mosaic=False, order=False, **kw)

# items_iter returns an iterator over API response pages
for item in results.items_iter(10):
  # each item is a GeoJSON feature
  print("ID -> ", item["id"], "DATE -> ", item["properties"]["acquired"])
  assets = client.get_assets(item).get()
  # activation = client.activate(assets['analytic'])
  # wait for activation
  # assets = client.get_assets(item).get()
  # callback = api.write_to_file()
  # body = client.download(assets['analytic'], callback=callback)
  # body.await()