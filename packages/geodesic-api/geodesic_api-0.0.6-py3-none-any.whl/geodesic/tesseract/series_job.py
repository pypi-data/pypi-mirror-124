from geodesic.bases import reset_attr
from typing import List
from geodesic import Dataset
from shapely.geometry import shape
from geodesic.stac import Item
from geodesic.client import get_client, raise_on_error
from geodesic.tesseract.job import Job
from geodesic.tesseract.global_properties import GlobalProperties
from geodesic.tesseract.asset_spec import AssetSpec


#############################################################################
# Series Job Root Class
#############################################################################

class SeriesJob(Job):
    """SeriesJob represents a tesseract process that produces time series.

    Args:
        desc(dict): A dictionary representing the job request.
        job_id(str): The job ID of a previously submitted job. This will reinitialize this object by querying tesseract.

    """
    def __init__(self, spec: dict = None, job_id: str = None):
        self._geometries = None
        self._geometry_epsg = None
        self._series_format = None
        self._global_properties = None
        self._asset_specs = None
        super().__init__(spec, job_id)

    def submit(self):
        """Submits a job to be processed by tesseract

        This function will take the job defined by this class and submit it to the tesserct api for processing.
        Once submitted the dataset and items fields will be populated containing the SeerAI dataset and STAC items
        respectively. Keep in mind that even though the links to files in the STAC item will be populated, the job
        may not yet be completed and so some of the chunks may not be finished.
        """
        if self._submitted:
            raise Exception("this job has already been submitted. \
                            Create a new SeriesJob if you would like to submit a new job")

        client = get_client()

        res = raise_on_error(client.post('/tesseract/api/v1/series', **self)).json()

        self.job_id = res.get("job_id", None)
        if self.job_id is None:
            raise ValueError("no job_id was returned, something went wrong")

        ds = res.get('dataset', None)
        if ds is not None:
            self._dataset = Dataset(**ds)

        si = res.get('stac_item', None)
        if si is not None:
            self._item = Item(obj=si, dataset=self._dataset)

        self.status(return_quark_geoms=True)
        self._submitted = True
        return f"created job: {self.job_id}"

    @property
    def geometries(self):
        if self._geometries is not None:
            return self._geometries
        gj = self.get("geometries", [])
        self._geometries = [shape(g) for g in gj]

        return self._geometries

    @geometries.setter
    @reset_attr
    def geometries(self, v: list):
        if isinstance(v, list):
            # If its a dict of geojson then store it internally
            if isinstance(v[0], dict):
                self['geometries'] = v
                return

            geoms = []
            for g in v:
                try:
                    geoms.append(g.__geo_interface__)
                except AttributeError:
                    raise ValueError("input does not appear to be a geometry")
            self._geometries = geoms
        else:
            raise ValueError("input must be a list of geometries")

    @property
    def series_format(self) -> str:
        if self._series_format is not None:
            return self._series_format
        self._series_format = self.get("series_format", None)
        return self._series_format

    @series_format.setter
    @reset_attr
    def series_format(self, v: str):
        if not isinstance(v, str):
            raise ValueError("series format must be a string and one of ['netcdf', 'json']")
        if v not in ['netcdf', 'json']:
            raise ValueError("series_format must be one of ['netcdf', 'json']")
        self["series_format"] = v

    @property
    def geometry_epsg(self):
        if self._geometry_epsg is not None:
            return self._geometry_epsg

        self._geometry_epsg = self.get("geometry_epsg", None)
        return self._geometry_epsg

    @geometry_epsg.setter
    @reset_attr
    def geometry_epsg(self, epsg: int):
        assert isinstance(epsg, int)
        self["geometry_epsg"] = epsg

    @property
    def global_properties(self):
        if self._global_properties is not None:
            return self._global_properties
        p = self.get("global_properties", {})
        self._global_properties = GlobalProperties(p)
        return self._global_properties

    @global_properties.setter
    @reset_attr
    def global_properties(self, v):
        self['global_properties'] = v

    @property
    def asset_specs(self):
        if self._asset_specs is not None:
            return self._asset_specs
        a = self.get("asset_specs", {})
        self._asset_specs = AssetSpec(a)
        return self._asset_specs

    @asset_specs.setter
    @reset_attr
    def asset_specs(self, specs: List[dict]):
        self['asset_specs'] = specs
