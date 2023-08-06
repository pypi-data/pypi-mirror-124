import datetime as pydatetime
from geodesic.bases import APIObject

from geodesic.service import ServiceClient
from dateutil.parser import parse

from collections import defaultdict

from geodesic.client import raise_on_error
from geodesic.entanglement import Object
from geodesic.stac import FeatureCollection
from geodesic.widgets import get_template_env, jinja_available

from shapely.geometry import shape, box

from typing import Optional, Union, List, Tuple

datasets_client = ServiceClient('entanglement', 1, 'datasets')
stac_client = ServiceClient('spacetime', 1, 'stac')


def list_datasets(ids: Union[List, str] = [], search: str = None):

    params = {}
    if ids:
        if isinstance(ids, str):
            ids = ids.split(",")
        params['ids'] = ",".join(ids)

    if search is not None:
        params['search'] = search

    resp = datasets_client.get('', **params)
    raise_on_error(resp)

    ds = [Dataset(**r) for r in resp.json()["datasets"]]
    datasets = DatasetList(ds)
    return datasets


class Dataset(Object):
    """Allows interaction with SeerAI datasets.

    Dataset provides a way to interact with datasets in the SeerAI.

    Args:
        **spec (dict): Dictionary with all properties in the dataset
    """

    def __init__(self, **obj):
        o = {'class': "dataset"}
        # If this came from the dataset API, this needs to be built as an object
        if 'item' not in obj:
            o['item'] = obj
            uid = obj.get('uid')
            if uid is not None:
                o['uid'] = uid
            o['name'] = obj.get('name', None)

            o['class'] = "dataset"
            o['domain'] = obj.get('domain', "*")
            o['category'] = obj.get('category', "*")
            o['type'] = obj.get('type', "*")
            o['description'] = obj.get('description', '')
            o['keywords'] = obj.get('keywords', [])

            # geom from extent
            e = obj.get('extent', {})
            se = e.get('spatial', None)
            if se is not None:
                g = box(*se, ccw=False)
                self.geometry = g

            o.update(obj.get('entanglement', {}))

        # Otherwise, parse as object
        else:
            obj['item']['uid'] = obj['uid']
            o = obj

        super(Dataset, self).__init__(**o)

    @property
    def object_class(self):
        return "Dataset"

    @object_class.setter
    def object_class(self, v):
        if v.lower() != "dataset":
            raise ValueError("shouldn't happen")
        self._set_item('class', 'dataset')

    @property
    def dataset_type(self):
        return self.item['type']

    @dataset_type.setter
    def dataset_type(self, v: str):
        if not isinstance(v, str):
            raise ValueError("dataset_type must be a string")
        self.item['type'] = v

    @property
    def dataset_subtype(self):
        return self.item["subtype"]

    @dataset_subtype.setter
    def dataset_subtype(self, v: str):
        if not isinstance(v, str):
            raise ValueError("dataset_subtype must be a string")
        self.item['subtype'] = v

    @property
    def stac(self):
        stac = self.item.get("stac", {})
        if not stac:
            self.item['stac'] = stac
        return stac

    @stac.setter
    def stac(self, v: dict):
        if not isinstance(v, dict):
            raise ValueError("stac must be a dict")
        self.item['stac'] = v

    @property
    def clients(self):
        return self.item.get("clients", [])

    @clients.setter
    def clients(self, v: list):
        if not isinstance(v, list):
            raise ValueError("clients must be a list of strings")
        self.item['clients'] = v

    @property
    def alias(self):
        return self.item.get("alias", self.name)

    @alias.setter
    def alias(self, v: str):
        if not isinstance(v, str):
            raise ValueError('alias must be a string')
        self.item["alias"] = v

    @property
    def item_assets(self):
        return ItemAssets(item_assets=self.stac['itemAssets'], ds_name=self.alias)

    @item_assets.setter
    def item_assets(self, v: dict):
        if not isinstance(v, dict):
            raise ValueError("item assets must be a dict")
        self.stac['itemAssets'] = v

    @property
    def bands(self):
        """
        Alias for item_assets
        """
        return self.item_assets

    def _repr_html_(self, add_style=True):
        if not jinja_available():
            return self.__repr__()

        template = get_template_env().get_template("dataset_template.html.jinja")
        # Make this look like dataset list but with a single entry so one template can be used for both
        dataset = {self.name: self}
        return template.render(datasets=dataset)

    def query(
        self,
        bbox: Optional[List] = None,
        datetime: Union[List, Tuple] = None,
        limit: Optional[Union[bool, int]] = 10,
        intersects=None,
        **kwargs
    ):
        """ Query the dataset for items.

        Query this service's OGC Features or STAC API.

        Args:
            bbox: The spatial extent for the query as a bounding box. Example: [-180, -90, 180, 90]
            datetime: The temporal extent for the query formatted as a list: [start, end].
            limit: The maximum number of items to return in the query.

        Returns:
            A :class:`geodesic.stac.FeatureCollection` with all items in the dataset matching the query.

        Examples:
            A query on the `sentinel-2-l2a` dataset with a given bouding box and time range. Additionally it
            you can apply filters on the parameters in the items.

            >>> bbox = geom.bounds
            >>> date_range = (datetime.datetime(2020, 12,1), datetime.datetime.now())
            >>> ds.query(
            ...          bbox=bbox,
            ...          datetime=date_range,
            ...          query={'properties.eo:cloud_cover': {'lte': 10}}
            ... )
        """
        api = kwargs.pop("api", None)
        # clients = self.clients

        if api is None:
            api = "stac"

        else:
            if api not in ["features", "stac"]:
                raise ValueError("query with api '{0}' not supported.".format(api))

        query_all = False
        if not limit:
            limit = 500
            query_all = True

        # Request query/body
        params = {"limit": limit}

        if api == "features":
            url = f"collections/{self.name}/items"

        elif api == "stac":
            params["collections"] = [self.name]
            url = "search"

        # If the bounding box only provided.
        if bbox is not None and intersects is None:
            if api == "stac":
                params["bbox"] = bbox
            else:
                params["bbox"] = ",".join(map(str, bbox))
        # If a intersection geometry was provided
        if intersects is not None:
            # Geojson
            if isinstance(intersects, dict):
                try:
                    g = shape(intersects)
                except ValueError:
                    try:
                        g = shape(intersects['geometry'])
                    except Exception as e:
                        raise ValueError('could not determine type of intersection geometry') from e

            elif hasattr(intersects, "__geo_interface__"):
                g = intersects

            else:
                raise ValueError("intersection geometry must be either geojson or object with __geo_interface__")

            # If STAC, use the geojson
            if api == "stac":
                params["intersects"] = g.__geo_interface__
            # Bounding box is all that's supported for OAFeat
            else:
                try:
                    # Shapely
                    params["bbox"] = g.bounds
                except AttributeError:
                    # ArcGIS
                    params["bbox"] = g.extent

        # STAC search specific
        if api == "stac":
            ids = kwargs.pop("ids", None)
            if ids is not None:
                params["ids"] = ids
            query = kwargs.pop("query", None)
            if query is not None:
                for k, v in query.items():

                    gt = v.get("gt")
                    if gt is not None and isinstance(gt, pydatetime.datetime):
                        v["gt"] = gt.isoformat()
                    lt = v.get("lt")
                    if lt is not None and isinstance(lt, pydatetime.datetime):
                        v["lt"] = lt.isoformat()
                    gte = v.get("gte")
                    if gte is not None and isinstance(gte, pydatetime.datetime):
                        v["gte"] = gte.isoformat()
                    lte = v.get("lte")
                    if lte is not None and isinstance(lte, pydatetime.datetime):
                        v["lte"] = lte.isoformat()
                    eq = v.get("eq")
                    if eq is not None and isinstance(eq, pydatetime.datetime):
                        v["eq"] = eq.isoformat()
                    neq = v.get("neq")
                    if neq is not None and isinstance(neq, pydatetime.datetime):
                        v["neq"] = neq.isoformat()
                    query[k] = v

                params["query"] = query
            sortby = kwargs.pop("sortby", None)
            if sortby is not None:
                params["sortby"] = sortby

            fields = kwargs.pop("fields", None)
            if fields is not None:
                fieldsObj = defaultdict(list)
                # fields with +/-
                if isinstance(fields, list):
                    for field in fields:
                        if field.startswith("+"):
                            fieldsObj["include"].append(field[1:])
                        elif field.startswith("-"):
                            fieldsObj["exclude"].append(field[1:])
                        else:
                            fieldsObj["include"].append(field)
                else:
                    fieldsObj = fields
                params["fields"] = fieldsObj

        if datetime is not None:
            params["datetime"] = "/".join([parsedate(d).isoformat() for d in datetime])

        if api == "features":
            res = raise_on_error(stac_client.get(url, **params))
        elif api == "stac":
            res = raise_on_error(stac_client.post(url, **params))

        collection = FeatureCollection(obj=res.json(), dataset=self, query=params)

        if query_all:
            collection.get_all()

        if api == "stac":
            collection._is_stac = True

        return collection


def parsedate(dt):
    try:
        return parse(dt)
    except TypeError:
        return dt


class DatasetList(APIObject):
    def __init__(self, datasets):
        for dataset in datasets:
            self._set_item(dataset.name, dataset)

    def _repr_html_(self):
        if not jinja_available():
            return self.__repr__()
        template = get_template_env().get_template("dataset_template.html.jinja")
        return template.render(datasets=self)


class ItemAssets(dict):
    def __init__(self, item_assets=None, ds_name=None):
        self.update(item_assets)
        self._ds_name = ds_name

    def _repr_html_(self, add_style=True):
        if not jinja_available():
            return self.__repr__()
        template = get_template_env().get_template("item_assets_template.html.jinja")
        return template.render(assets=self)
