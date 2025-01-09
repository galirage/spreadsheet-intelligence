from dataclasses import dataclass
from typing import Optional, Union
from spreadsheet_intelligence.models.common.common_data import Color


@dataclass
class SrgbClr:
    """
    Represents an sRGB color.

    Attributes:
        val (Color): The sRGB color value.
    
    XMLReference:
        val: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme
    """
    val: Color


@dataclass
class SysClr:
    """
    Represents a system color with a fallback color.

    Attributes:
        val (str): The system color value.
        last_clr (Color): The fallback color.
    """
    val: str
    last_clr: Color  # Fallback color


@dataclass
class ClrScheme:
    """
    Represents a color scheme with various color roles.

    Attributes:
        dk1: Union[SysClr, SrgbClr]
        lt1: Union[SysClr, SrgbClr]
        dk2: Union[SysClr, SrgbClr]
        lt2: Union[SysClr, SrgbClr]
        accent1: Union[SysClr, SrgbClr]
        accent2: Union[SysClr, SrgbClr]
        accent3: Union[SysClr, SrgbClr]
        accent4: Union[SysClr, SrgbClr]
        accent5: Union[SysClr, SrgbClr]
        accent6: Union[SysClr, SrgbClr]
        hlink: Union[SysClr, SrgbClr]
        folHlink: Union[SysClr, SrgbClr]
    
    XMLReference:
        dk1: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:dk1
        lt1: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:lt1
        dk2: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:dk2
        lt2: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:lt2
        accent1: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:accent1
        accent2: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:accent2
        accent3: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:accent3
        accent4: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:accent4
        accent5: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:accent5
        accent6: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:accent6
        hlink: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:hlink
        folHlink: xl/theme/themeX.xml/a:theme/a:themeElements/a:clrScheme/a:folHlink
    """
    dk1: Union[SysClr, SrgbClr]
    lt1: Union[SysClr, SrgbClr]
    dk2: Union[SysClr, SrgbClr]
    lt2: Union[SysClr, SrgbClr]
    accent1: Union[SysClr, SrgbClr]
    accent2: Union[SysClr, SrgbClr]
    accent3: Union[SysClr, SrgbClr]
    accent4: Union[SysClr, SrgbClr]
    accent5: Union[SysClr, SrgbClr]
    accent6: Union[SysClr, SrgbClr]
    hlink: Union[SysClr, SrgbClr]
    folHlink: Union[SysClr, SrgbClr]

    @staticmethod
    def map_color(val: str) -> str:
        """Maps a color role to its corresponding attribute name.

        Args:
            val (str): The color role to map.

        Returns:
            str: The mapped attribute name.
        """
        map_dir = {"tx1": "dk1", "tx2": "dk2", "bg1": "lt1", "bg2": "lt2"}
        if val in map_dir:
            return map_dir[val]
        else:
            return val

    def get_color(self, val: str) -> Color:
        """Retrieves the color associated with a given role.

        Args:
            val (str): The color role to retrieve.

        Returns:
            Color: The color associated with the role.

        Raises:
            ValueError: If the color type is invalid.
        """
        clr = getattr(self, self.map_color(val))
        if isinstance(clr, SysClr):
            return clr.last_clr
        elif isinstance(clr, SrgbClr):
            return clr.val
        else:
            raise ValueError(f"Invalid color type: {type(clr)}")


@dataclass
class Theme:
    """
    Represents a theme with a color scheme.

    Attributes:
        clr_scheme: ClrScheme
        # Other schemes can be implemented if needed
    """
    clr_scheme: ClrScheme
    # Other schemes can be implemented if needed


@dataclass
class SchemeClr:
    """
    Represents a scheme color with optional adjustments.

    Attributes:
        val (str): The theme name such as dk1, lt1, dk2, lt2, tx1, tx2, accent1, accent2, accent3, accent4, accent5, accent6
        lum_mod (Optional[int]): The luminance modifier.
        lum_off (Optional[int]): The luminance offset.
        shade (Optional[int]): The shade value.
    """
    val: str  # Theme name such as dk1, lt1, dk2, lt2, tx1, tx2, accent1, accent2, accent3, accent4, accent5, accent6
    lum_mod: Optional[int]
    lum_off: Optional[int]
    shade: Optional[int]

    def get_color(self, theme: Theme) -> Color:
        """Gets the adjusted color from the theme.

        Args:
            theme (Theme): The theme to retrieve the color from.

        Returns:
            Color: The adjusted color.
        """
        clr = theme.clr_scheme.get_color(self.val)
        adjusted_clr = clr.adjust_color(self.lum_mod, self.lum_off, self.shade)
        return adjusted_clr


@dataclass
class StyleBaseRef:
    """
    Represents a base reference for a style.

    Attributes:
        idx (str): The index of the style.
        ref_clr (Union[SchemeClr, SrgbClr]): The reference color.
    """
    idx: str
    ref_clr: Union[SchemeClr, SrgbClr]


@dataclass
class StyleRefs:
    """
    Represents style references for line, fill, effect, and font.

    Attributes:
        ln_ref (StyleBaseRef): The reference for the line style.
        fill_ref (StyleBaseRef): The reference for the fill style.
        effect_ref (Optional[StyleBaseRef]): The reference for the effect style.
        font_ref (Optional[StyleBaseRef]): The reference for the font style.
    
    XMLReference:
        ln_ref: xl/drawingX.xml/xdr:twoCellAnchor/xdr:style/a:lnRef
        fill_ref: xl/drawingX.xml/xdr:twoCellAnchor/xdr:style/a:fillRef
        effect_ref: xl/drawingX.xml/xdr:twoCellAnchor/xdr:style/a:effectRef
        font_ref: xl/drawingX.xml/xdr:twoCellAnchor/xdr:style/a:fontRef
    
    TODO:
        effect_ref: xl/drawingX.xml/xdr:twoCellAnchor/xdr:style/a:effectRef
        font_ref: xl/drawingX.xml/xdr:twoCellAnchor/xdr:style/a:fontRef
    """
    ln_ref: StyleBaseRef
    fill_ref: StyleBaseRef
    effect_ref: Optional[StyleBaseRef]
    font_ref: Optional[StyleBaseRef]
