from geodesic.bases import reset_attr
from typing import List
from geodesic import Dataset
from shapely.geometry import box
from geodesic.stac import Item
from geodesic.client import get_client, raise_on_error
from geodesic.tesseract.job import Job
from geodesic.tesseract.global_properties import GlobalProperties
from geodesic.tesseract.asset_spec import AssetSpec


class RasterJob(Job):
    """RasterJob represents a tesseract process that produces a raster.

    Args:
        desc(dict): A dictionary representing the job request.

    """
    def __init__(self, job_id: str = None, **spec):
        self._bbox = None
        self._bbox_epsg = None
        self._raster_format = None
        self._output_epsg = None
        self._global_properties = None
        self._asset_specs = None

        self.global_properties = GlobalProperties()
        self.bbox_epsg = 4326
        self.output_epsg = 3857

        if job_id is None:
            super().__init__(**spec)
            for k, v in spec.items():
                setattr(self, k, v)
        else:
            super().__init__(job_id=job_id)

    def submit(self):
        """Submits a job to be processed by tesseract

        This function will take the job defined by this class and submit it to the tesserct api for processing.
        Once submitted the dataset and items fields will be populated containing the SeerAI dataset and STAC items
        respectively. Keep in mind that even though the links to files in the STAC item will be populated, the job
        may not yet be completed and so some of the chunks may not be finished.
        """
        if self._submitted:
            raise Exception("this job has already been submitted. \
                            Create a new RasterJob if you would like to submit a new job")

        client = get_client()

        res = raise_on_error(client.post('/tesseract/api/v1/raster', **self)).json()

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
    def bbox(self):
        if self._bbox is not None:
            return self._bbox
        bb = self.get("bbox", [])
        if len(bb) >= 4:
            self._bbox = box(bb[0], bb[1], bb[2], bb[3])
        return self._bbox

    @bbox.setter
    @reset_attr
    def bbox(self, b):
        if isinstance(b, (list, tuple)):
            self._set_item('bbox', b)
            return
        try:
            self._set_item('bbox', b.__geo_interface__)
            try:
                self._set_item('bbox', b.bounds)
            except AttributeError:
                try:
                    self._set_item('bbox', b.extent)
                except Exception:
                    pass
            return
        except AttributeError:
            raise ValueError("unknown bbox or geometry type")

    @property
    def raster_format(self) -> str:
        if self._raster_format is not None:
            return self._raster_format
        self._raster_format = self.get("raster_format", None)
        return self._raster_format

    @raster_format.setter
    @reset_attr
    def raster_format(self, f: str):
        assert isinstance(f, str)
        self._set_item('raster_format', f)

    @property
    def bbox_epsg(self):
        if self._bbox_epsg is not None:
            return self._bbox_epsg

        self._bbox_epsg = self.get("bbox_epsg", None)
        return self._bbox_epsg

    @bbox_epsg.setter
    @reset_attr
    def bbox_epsg(self, epsg: int):
        assert isinstance(epsg, int)
        self._set_item("bbox_epsg", epsg)

    @property
    def output_epsg(self):
        if self._output_epsg is not None:
            return self._output_epsg

        self._output_epsg = self.get("output_epsg", None)
        return self._output_epsg

    @output_epsg.setter
    @reset_attr
    def output_epsg(self, epsg: int):
        assert isinstance(epsg, int)
        self._set_item("output_epsg", epsg)

    @property
    def global_properties(self):
        if self._global_properties is not None:
            return self._global_properties
        p = self.get("global_properties", {})
        self._global_properties = GlobalProperties(**p)
        return self._global_properties

    @global_properties.setter
    @reset_attr
    def global_properties(self, v):
        self._set_item('global_properties', dict(GlobalProperties(**v)))

    @property
    def asset_specs(self):
        if self._asset_specs is not None:
            return self._asset_specs
        a = self.get("asset_specs", [])
        self._asset_specs = [AssetSpec(**_) for _ in a]
        return self._asset_specs

    @asset_specs.setter
    @reset_attr
    def asset_specs(self, specs: List[dict]):
        self._set_item('asset_specs', [dict(AssetSpec(**_)) for _ in specs])
