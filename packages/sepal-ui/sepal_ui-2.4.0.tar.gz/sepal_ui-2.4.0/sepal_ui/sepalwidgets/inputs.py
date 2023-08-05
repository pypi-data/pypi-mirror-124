from pathlib import Path
import json

import ipyvuetify as v
from traitlets import link, Int, Any, List, observe, Dict, Unicode
from ipywidgets import jslink
import pandas as pd
import ee
import geopandas as gpd
from natsort import humansorted


from sepal_ui.message import ms
from sepal_ui.frontend.styles import *
from sepal_ui.scripts import utils as su
from sepal_ui.scripts import gee
from sepal_ui.sepalwidgets.sepalwidget import SepalWidget
from sepal_ui.sepalwidgets.btn import Btn

__all__ = [
    "DatePicker",
    "FileInput",
    "LoadTableField",
    "AssetSelect",
    "PasswordField",
    "NumberField",
    "VectorField",
]


class DatePicker(v.Layout, SepalWidget):
    """
    Custom input widget to provide a reusable DatePicker. It allows to choose date as a string in the following format YYYY-MM-DD

    Args:
        label (str, optional): the label of the datepicker field

    Attributes:
        menu (v.Menu): the menu widget to display the datepicker

    """

    def __init__(self, label="Date", **kwargs):

        date_picker = v.DatePicker(no_title=True, v_model=None, scrollable=True)

        date_text = v.TextField(
            v_model=None,
            label=label,
            hint="YYYY-MM-DD format",
            persistent_hint=True,
            prepend_icon="event",
            readonly=True,
            v_on="menuData.on",
        )

        self.menu = v.Menu(
            min_width="290px",
            transition="scale-transition",
            offset_y=True,
            value=False,
            close_on_content_click=False,
            children=[date_picker],
            v_slots=[
                {
                    "name": "activator",
                    "variable": "menuData",
                    "children": date_text,
                }
            ],
        )

        super().__init__(
            v_model=None,
            row=True,
            class_="pa-5",
            align_center=True,
            children=[v.Flex(xs10=True, children=[self.menu])],
            **kwargs,
        )

        jslink((date_picker, "v_model"), (date_text, "v_model"))
        jslink((date_picker, "v_model"), (self, "v_model"))

        # close the datepicker on click
        # date_text.observe(lambda _: setattr(self.menu, 'value', False), 'v_model')


class FileInput(v.Flex, SepalWidget):
    """
    Custom input field to select a file in the sepal folders.

    Args:
        extentions ([str]): the list of the allowed extentions. the FileInput will only display these extention and folders
        folder (str | pathlib.Path): the starting folder of the file input
        label (str): the label of the input
        v_model (str, optional): the default value
        clearable (bool, optional): wether or not to make the widget clearable. default to False

    Attributes:
        extentions ([str]): the extention list
        folder (str | pathlib.Path): the current folder
        selected_file (v.TextField): the textfield where the file pathname is stored
        loading (v.ProgressLinear): loading top bar of the menu component
        file_list (v.List): the list of files and folder that are available in the current folder
        file_menu (v.Menu): the menu that hide and show the file_list
        reload (v.Btn): reload btn to reload the file list on the current folder
        clear (v.Btn): clear btn to remove everything and set back to the ini folder
    """

    file = Any("")
    v_model = Unicode(None, allow_none=True).tag(sync=True)

    def __init__(
        self,
        extentions=[],
        folder=Path.home(),
        label="search file",
        v_model=None,
        clearable=False,
        **kwargs,
    ):

        if type(folder) == str:
            folder = Path(folder)

        self.extentions = extentions
        self.folder = folder

        self.selected_file = v.TextField(
            readonly=True, label="Selected file", class_="ml-5 mt-5", v_model=None
        )

        self.loading = v.ProgressLinear(
            indeterminate=False,
            background_color="grey darken-3",
            color=COMPONENTS["PROGRESS_BAR"]["color"],
        )

        self.file_list = v.List(
            dense=True,
            color="grey darken-3",
            flat=True,
            max_height="300px",
            style_="overflow: auto; border-radius: 0 0 0 0;",
            children=[v.ListItemGroup(children=self._get_items(), v_model="")],
        )

        self.file_menu = v.Menu(
            min_width=300,
            children=[self.loading, self.file_list],
            close_on_content_click=False,
            v_slots=[
                {
                    "name": "activator",
                    "variable": "x",
                    "children": Btn(
                        icon="mdi-file-search", v_model=False, v_on="x.on", text=label
                    ),
                }
            ],
        )

        self.reload = v.Btn(
            icon=True, color="primary", children=[v.Icon(children=["mdi-cached"])]
        )

        self.clear = v.Btn(
            icon=True, color="primary", children=[v.Icon(children=["mdi-close"])]
        )
        if not clearable:
            su.hide_component(self.clear)

        super().__init__(
            row=True,
            class_="d-flex align-center mb-2",
            align_center=True,
            children=[
                self.clear,
                self.reload,
                self.file_menu,
                self.selected_file,
            ],
            **kwargs,
        )

        link((self.selected_file, "v_model"), (self, "file"))
        link((self.selected_file, "v_model"), (self, "v_model"))

        self.file_list.children[0].observe(self._on_file_select, "v_model")
        self.reload.on_event("click", self._on_reload)
        self.clear.on_event("click", self.reset)

    def reset(self, *args):
        """
        Clear the File selection and move to the root folder if something was selected

        Return:
            self
        """

        root = Path("~").expanduser()

        if self.v_model is not None:

            # move to root
            self._on_file_select({"new": root})

            # remove v_model
            self.v_model = None

        return self

    def select_file(self, path):
        """
        Manually select a file from it's path. No verification on the extension is performed

        Params:
            path (str|pathlib.Path): the path to the file

        Return:
            self
        """

        # cast to Path
        path = Path(path)

        # test file existence
        if not path.is_file():
            raise Exception(f"{path} is not a file")

        # set the menu to the folder of the file
        self._on_file_select({"new": path.parent})

        # select the appropriate file
        self._on_file_select({"new": path})

        return self

    def _on_file_select(self, change):
        """Dispatch the behavior between file selection and folder change"""

        if not change["new"]:
            return self

        new_value = Path(change["new"])

        if new_value.is_dir():
            self.folder = new_value
            self._change_folder()

        elif new_value.is_file():
            self.file = str(new_value)

        return self

    def _change_folder(self):
        """Change the target folder"""
        # reset files
        self.file_list.children[0].children = self._get_items()

        return

    def _get_items(self):
        """Return the list of items inside the folder"""

        self.loading.indeterminate = True

        folder = self.folder

        list_dir = [el for el in folder.glob("*/") if not el.name.startswith(".")]

        if self.extentions:
            list_dir = [
                el for el in list_dir if el.is_dir() or el.suffix in self.extentions
            ]

        folder_list = []
        file_list = []

        for el in list_dir:

            if el.suffix in ICON_TYPES.keys():
                icon = ICON_TYPES[el.suffix]["icon"]
                color = ICON_TYPES[el.suffix]["color"]
            else:
                icon = ICON_TYPES["DEFAULT"]["icon"]
                color = ICON_TYPES["DEFAULT"]["color"]

            children = [
                v.ListItemAction(children=[v.Icon(color=color, children=[icon])]),
                v.ListItemContent(
                    children=[v.ListItemTitle(children=[el.stem + el.suffix])]
                ),
            ]

            if el.is_dir():
                folder_list.append(v.ListItem(value=str(el), children=children))
            else:
                file_size = su.get_file_size(el)
                children.append(v.ListItemActionText(children=[file_size]))
                file_list.append(v.ListItem(value=str(el), children=children))

        folder_list = humansorted(folder_list, key=lambda x: x.value)
        file_list = humansorted(file_list, key=lambda x: x.value)

        parent_item = v.ListItem(
            value=str(folder.parent),
            children=[
                v.ListItemAction(
                    children=[
                        v.Icon(
                            color=ICON_TYPES["PARENT"]["color"],
                            children=[ICON_TYPES["PARENT"]["icon"]],
                        )
                    ]
                ),
                v.ListItemContent(
                    children=[v.ListItemTitle(children=[f"..{folder.parent}"])]
                ),
            ],
        )

        folder_list.extend(file_list)
        folder_list.insert(0, parent_item)

        self.loading.indeterminate = False

        return folder_list

    def _on_reload(self, widget, event, data):

        # force the update of the current folder
        self._change_folder()

        return


class LoadTableField(v.Col, SepalWidget):
    """
    A custom input widget to load points data. The user will provide a csv or txt file containing labeled dataset.
    The relevant columns (lat, long and id) can then be identified in the updated select. Once everything is set, the widget will populate itself with a json dict.
    {pathname, id_column, lat_column,lng_column}

    Attributes:
        fileInput (sw.FileInput): the file input to select the .csv or .txt file
        v_model (Traitlet): the json saved v_model shaped as {'pathname': xx, 'id_column': xx, 'lat_column': xx, 'lng_column': xx} The values can be accessed separately with the appropriate getter methods
        IdSelect (v.Select): input to select the id column
        LngSelect (v.Select): input to select the lng column
        LatSelect (v.Select): input to select the lat column
    """

    default_v_model = {
        "pathname": None,
        "id_column": None,
        "lat_column": None,
        "lng_column": None,
    }

    def __init__(self, label="Table file"):

        self.fileInput = FileInput([".csv", ".txt"], label=label)

        self.IdSelect = v.Select(
            _metadata={"name": "id_column"}, items=[], label="Id", v_model=None
        )
        self.LngSelect = v.Select(
            _metadata={"name": "lng_column"}, items=[], label="Longitude", v_model=None
        )
        self.LatSelect = v.Select(
            _metadata={"name": "lat_column"}, items=[], label="Latitude", v_model=None
        )

        super().__init__(
            v_model=self.default_v_model,
            children=[self.fileInput, self.IdSelect, self.LngSelect, self.LatSelect],
        )

        # link the dropdowns
        jslink((self.IdSelect, "items"), (self.LngSelect, "items"))
        jslink((self.IdSelect, "items"), (self.LatSelect, "items"))

        # link the widget with v_model
        self.fileInput.observe(self._on_file_input_change, "v_model")
        self.IdSelect.observe(self._on_select_change, "v_model")
        self.LngSelect.observe(self._on_select_change, "v_model")
        self.LatSelect.observe(self._on_select_change, "v_model")

    def reset(self):
        """
        Clear the values and return to the empty default json

        Return:
            self
        """

        # clear the fileInput
        self.fileInput.reset()

    @su.switch("loading", on_widgets=["IdSelect", "LngSelect", "LatSelect"])
    def _on_file_input_change(self, change):
        """Update the select content when the fileinput v_model is changing"""

        # clear the selects
        self._clear_select()

        # set the path
        path = change["new"]
        self.v_model["pathname"] = path

        # exit if none
        if not path:
            return self

        df = pd.read_csv(path, sep=None, engine="python")

        if len(df.columns) < 3:
            self._clear_select()
            self.fileInput.selected_file.error_messages = (
                ms.widgets.load_table.too_small
            )
            return

        # set the items
        self.IdSelect.items = df.columns.tolist()

        # pre load values that sounds like what we are looking for
        # it will only keep the first occurence of each one
        for name in reversed(df.columns.tolist()):
            lname = name.lower()
            if "id" in lname:
                self.IdSelect.v_model = name
            elif any(
                ext in lname
                for ext in ["lng", "long", "longitude", "x_coord", "xcoord", "lon"]
            ):
                self.LngSelect.v_model = name
            elif any(ext in lname for ext in ["lat", "latitude", "y_coord", "ycoord"]):
                self.LatSelect.v_model = name

        return self

    def _clear_select(self):
        """clear the selects components"""

        self.fileInput.selected_file.error_messages = None
        self.IdSelect.items = []  # all the others are listening to this one
        self.IdSelect.v_model = self.LngSelect.v_model = self.LatSelect.v_model = None

        return self

    def _on_select_change(self, change):
        """change the v_model value when a select is changed"""

        name = change["owner"]._metadata["name"]
        self.v_model[name] = change["new"]

        return self


class AssetSelect(v.Combobox, SepalWidget):
    f"""
    Custom widget input to select an asset inside the asset folder of the user

    Args:
        label (str): the label of the input
        folder (str): the folder of the user assets
        default_asset (str, List): the id of a default asset or a list of defaults
        types ([str]): the list of asset type you want to display to the user. type need to be from: ['IMAGE', 'FOLDER', 'IMAGE_COLLECTION', 'TABLE','ALGORITHM'. Default to 'IMAGE' & 'TABLE'

    Attributes:
        folder (str): the folder of the user assets
        valid (Bool): whether the selected asset is valid (user has access) or not
        type (TYPES): Type of the selected asset if is valid. None if is not accessible.
        asset_info (dict): The selected asset informations
        default_asset (str, List): the id of a default asset or a list of default assets
    """

    TYPES = {
        "IMAGE": ms.widgets.asset_select.types[0],
        "TABLE": ms.widgets.asset_select.types[1],
        "IMAGE_COLLECTION": ms.widgets.asset_select.types[2],
        "ALGORITHM": ms.widgets.asset_select.types[3],
        "FOLDER": ms.widgets.asset_select.types[4],
        # UNKNOWN type is ignored
    }

    default_asset = Any().tag(sync=True)

    @su.need_ee
    def __init__(
        self,
        label=ms.widgets.asset_select.label,
        folder=None,
        types=["IMAGE", "TABLE"],
        **kwargs,
    ):
        self.valid = False
        self.asset_info = None

        # Validate the input as soon as the object is insantiated
        self.observe(self._validate, "v_model")

        # save the types
        self.types = [el for el in types if el in self.TYPES.keys()]

        # if folder is not set use the root one
        self.folder = folder if folder else ee.data.getAssetRoots()[0]["id"]

        self.label = label

        self.v_model = None
        self.clearable = True
        self.dense = True
        self.prepend_icon = "mdi-cached"

        self.class_ = "my-5"
        self.placeholder = "users/someCustomUser/customAsset"

        self._get_items()

        super().__init__(**kwargs)

        self.on_event("click:prepend", self._get_items)

    @observe("default_asset")
    def _add_default(self, change=None):
        """Add default element(s) to item list"""

        new_val = change["new"]

        if new_val:

            new_items = self.items.copy()

            if isinstance(new_val, str):
                new_val = [new_val]

            self.v_model = new_val[0]

            default_items = [
                {"divider": True},
                {"header": ms.widgets.asset_select.custom},
            ] + [default for default in new_val]

            # Check if there are previously custom items and replace them, instead
            # of append them

            if {"header": ms.widgets.asset_select.custom} in self.items:

                next_div_index = new_items.index({"divider": True}, 1)
                new_items[0:next_div_index] = default_items

            else:
                new_items = default_items + self.items

            self.items = new_items

        return

    @su.switch("loading")
    def _validate(self, change):
        """Validate the selected access. Throw an error message if is not accesible."""

        self.error = False
        self.error_messages = None

        if change["new"]:

            try:
                self.asset_info = ee.data.getAsset(change["new"])
                self.valid = True

            except Exception:

                self.asset_info = None
                self.valid = False
                self.error = True
                self.error_messages = ms.widgets.asset_select.no_access

        return

    @su.switch("loading", "disabled")
    def _get_items(self, *args):

        # get the list of user asset
        raw_assets = gee.get_assets(self.folder)

        assets = {
            k: sorted([e["id"] for e in raw_assets if e["type"] == k])
            for k in self.types
        }

        self.items = []
        for k in self.types:
            if len(assets[k]):
                self.items += [
                    {"divider": True},
                    {"header": self.TYPES[k]},
                    *assets[k],
                ]

        return self


class PasswordField(v.TextField, SepalWidget):
    """
    Custom widget to input passwords in text area and
    toggle its visibility.

    Args:
        label (str, optional): Header displayed in text area. Defaults to Password.
    """

    def __init__(self, **kwargs):

        # default behavior
        self.label = "Password"
        self.class_ = "mr-2"
        self.v_model = ""
        self.type = "password"
        self.append_icon = "mdi-eye-off"

        # init the widget with the remaining kwargs
        super().__init__(**kwargs)

        # bind the js behavior
        self.on_event("click:append", self._toggle_pwd)

    def _toggle_pwd(self, widget, event, data):
        """Toggle password visibility when append button is clicked"""

        if self.type == "text":
            self.type = "password"
            self.append_icon = "mdi-eye-off"
        else:
            self.type = "text"
            self.append_icon = "mdi-eye"


class NumberField(v.TextField, SepalWidget):
    """
    Custom widget to input numbers in text area and add/substract with single increment.

    Args:
        max_ (int, optional): Maximum selectable number. Defaults to 10.
        min_ (int, optional): Minimum selectable number. Defaults to 0.

    """

    max_ = Int(10).tag(sync=True)
    min_ = Int(0).tag(sync=True)

    def __init__(self, **kwargs):

        self.type = "number"
        self.append_outer_icon = "mdi-plus"
        self.prepend_icon = "mdi-minus"
        self.v_model = 0
        self.readonly = True

        super().__init__(**kwargs)

        self.on_event("click:append-outer", self.increment)
        self.on_event("click:prepend", self.decrement)

    def increment(self, widget, event, data):
        """Adds 1 to the current v_model number"""
        if self.v_model < self.max_:
            self.v_model += 1

    def decrement(self, widget, event, data):
        """Substracts 1 to the current v_model number"""
        if self.v_model > self.min_:
            self.v_model -= 1


class VectorField(v.Col, SepalWidget):
    """
    A custom input widget to load vector data. The user will provide a vector file compatible with fiona or a GEE feature collection.
    The user can then select a specific shape by setting column and value fields.

    Args:
        label (str): the label of the file input field, default to 'vector file'.
        gee (bool, optional): whether to use GEE assets or local vectors.
        **asset_select_kwargs: When gee=True, extra args will be used for AssetSelect

    Attributes:
        original_gdf (geopandas.gdf): The originally selected dataframe
        gdf (geopandas.gdf): The selected dataframe.
        v_model (Traitlet): The json saved v_model shaped as {'pathname': xx, 'column': xx, 'value': xx} The values can be accessed separately with the appropriate getter methods
        w_file (sw.FileInput): The file selector widget
        w_column (v.Select): The Select widget to select the column
        w_value (v.Select): The Select widget to select the value in the selected column
    """

    v_model = Dict(
        {
            "pathname": None,
            "column": None,
            "value": None,
        }
    )

    def __init__(self, label="vector_file", gee=False, **kwargs):

        # save the df for column naming (not using a gdf as geometry are useless)
        self.df = None
        self.feature_collection = None

        self.column_base_items = [
            {"text": "Use all features", "value": "ALL"},
            {"divider": True},
        ]

        # set the 3 wigets
        if not gee:
            self.w_file = FileInput([".shp", ".geojson", ".gpkg", ".kml"], label=label)
        else:
            # Don't care about 'types' arg. It will only work with tables.
            asset_select_kwargs = {k: v for k, v in kwargs.items() if k in ["folder"]}
            self.w_file = AssetSelect(types=["TABLE"], **asset_select_kwargs)

        self.w_column = v.Select(
            _metadata={"name": "column"},
            items=self.column_base_items,
            label="Column",
            v_model="ALL",
        )
        self.w_value = v.Select(
            _metadata={"name": "value"}, items=[], label="Value", v_model=None
        )
        su.hide_component(self.w_value)

        # create the Col Field
        self.children = [self.w_file, self.w_column, self.w_value]

        super().__init__(**kwargs)

        # events
        self.w_file.observe(self._update_file, "v_model")
        self.w_column.observe(self._update_column, "v_model")
        self.w_value.observe(self._update_value, "v_model")

    def reset(self):
        """
        Return the field to its initial state

        Return:
            self
        """

        self.w_file.reset()

        return self

    @su.switch("loading", on_widgets=["w_column", "w_value"])
    def _update_file(self, change):
        """update the file name, the v_model and reset the other widgets"""

        # reset the widgets
        self.w_column.items = self.w_value.items = []
        self.w_column.v_model = self.w_value.v_model = None
        self.df = None
        self.feature_collection = None

        # set the pathname value
        self.v_model["pathname"] = change["new"]

        # exit if nothing
        if not change["new"]:
            return self

        if isinstance(self.w_file, FileInput):
            # read the file
            self.df = gpd.read_file(change["new"], ignore_geometry=True)
            columns = self.df.columns.to_list()

        elif isinstance(self.w_file, AssetSelect):
            self.feature_collection = ee.FeatureCollection(change["new"])
            columns = self.feature_collection.first().getInfo()["properties"]
            columns = [
                str(col) for col in columns if col not in ["system:index", "Shape_Area"]
            ]

        # update the columns
        self.w_column.items = self.column_base_items + sorted(set(columns))

        self.w_column.v_model = "ALL"

        return self

    @su.switch("loading", on_widgets=["w_value"])
    def _update_column(self, change):
        """Update the column name and empty the value list"""

        # reset value widget
        self.w_value.items = []
        self.w_value.v_model = None

        # set the value
        self.v_model["column"] = change["new"]

        # hide value if "ALL" or none
        if change["new"] in ["ALL", None]:
            su.hide_component(self.w_value)
            return self

        # read the colmun
        if isinstance(self.w_file, FileInput):
            values = self.df[change["new"]].to_list()

        elif isinstance(self.w_file, AssetSelect):
            values = (
                self.feature_collection.distinct(change["new"])
                .aggregate_array(change["new"])
                .getInfo()
            )

        self.w_value.items = sorted(set(values))

        su.show_component(self.w_value)

        return self

    def _update_value(self, change):
        """Update the value name and reduce the gdf"""

        # set the value
        self.v_model["value"] = change["new"]

        return self
