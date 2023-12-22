import re
import folder_paths
import numpy as np
import json
import os.path

from copy import deepcopy
from PIL import Image, ImageDraw
from comfy.cli_args import args
from PIL.PngImagePlugin import PngInfo
from .grid_types import Annotation

static_x = 1
static_y = 1

reset_registry = {}

class GridFloats:
    @classmethod
    def INPUT_TYPES(s):
        return { 
            "required": {
                "index": ( "INT", {"default": 1, "min": 1 } ),
                "float1": ("FLOAT", {"default": 1.0, "step": 0.01}),
                "float2": ("FLOAT", {"default": 1.0, "step": 0.01}),
                "float3": ("FLOAT", {"default": 1.0, "step": 0.01}),
                "float4": ("FLOAT", {"default": 1.0, "step": 0.01}),
                "float5": ("FLOAT", {"default": 1.0, "step": 0.01}),
                "float6": ("FLOAT", {"default": 1.0, "step": 0.01}),
            },
             }

    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "ReturnFloat"
    CATEGORY = "EasyGrids"

    def ReturnFloat( self, index: int, float1 : float, float2 : float, float3 : float, float4 : float, float5 : float, float6: float ):
        #TODO: probably a more pythonic way to do this
        ret_list = [float1, float2, float3, float4, float5, float6]
        if ( index > len(ret_list) ):
            return ( ret_list[len(ret_list) - 1], )
        return (ret_list[ index - 1 ], )

class GridFloatList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ( "INT", {"default": 1, "min": 1, "max": 100 } ),
                "float_list": ("STRING", {"multiline": True}),
        }}

    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "ParseAndReturnFloat"
    CATEGORY = "EasyGrids"

    def __init__(self):
        self.static_text = "" 
        self.static_out_arr = []

    def ParseAndReturnFloat( self, index: int, float_list: str ):
        if float_list != self.static_text:
            split_str = re.split( ",|;|\s|:", float_list )
            out_arr = []
            for val in split_str:
                # let the exception happen if invalid
                out_arr.append(float(val))
            self.static_text = float_list
            self.static_out_arr = deepcopy( out_arr )
        if ( index > len(self.static_out_arr) ):
            return ( self.static_out_arr[len(self.static_out_arr) - 1], )
        return (self.static_out_arr[ index - 1 ],)

class GridInts:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ( "INT", {"default": 1, "min": 1 }),
                "int1": ("INT", {"default": 1, "step": 1 }),
                "int2": ("INT", {"default": 1, "step": 1}),
                "int3": ("INT", {"default": 1, "step": 1}),
                "int4": ("INT", {"default": 1, "step": 1}),
                "int5": ("INT", {"default": 1, "step": 1}),
                "int6": ("INT", {"default": 1, "step": 1}),
            },
             }

    RETURN_TYPES = ("INT",)
    FUNCTION = "ReturnInt"
    CATEGORY = "EasyGrids"

    def ReturnInt( self, index: int, int1 : int, int2 : int, int3 : int, int4 : int, int5 : int, int6: int ):
        ret_list = [int1, int2, int3, int4, int5, int6]
        if ( index > len(ret_list) ):
            return ( ret_list[len(ret_list) - 1], )
        return (ret_list[ index - 1 ], )

class GridIntList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ( "INT", {"default": 1, "min": 1, "max": 100 } ),
                "int_list": ("STRING", {"multiline": True}),
        }}

    RETURN_TYPES = ("INT",)
    FUNCTION = "ParseAndReturnInt"
    CATEGORY = "EasyGrids"

    def __init__(self):
        self.static_text = "" 
        self.static_out_arr = []

    def ParseAndReturnInt( self, index: int, int_list: str ):
        if int_list != self.static_text:
            split_str = re.split( ",|;|\s|:", int_list )
            out_arr = []
            for val in split_str:
                # let the exception happen if invalid
                out_arr.append(int(val))
            self.static_text = int_list
            self.static_out_arr = deepcopy( out_arr )
        if ( index > len(self.static_out_arr) ):
            return ( self.static_out_arr[len(self.static_out_arr) - 1], )
        return (self.static_out_arr[ index - 1 ],)

class GridStrings:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ( "INT", {"default": 1, "min": 1 }),
                "string1": ("STRING", {"default": ""}),
                "string2": ("STRING", {"default": ""}),
                "string3": ("STRING", {"default": ""}),
                "string4": ("STRING", {"default": ""}),
                "string5": ("STRING", {"default": ""}),
                "string6": ("STRING", {"default": ""}),
            },
             }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "ReturnString"
    CATEGORY = "EasyGrids"

    def ReturnString( self, index: int, string1 : str, string2 : str, string3 : str, string4 : str, string5 : str, string6: str ):
        ret_list = [string1, string2, string3, string4, string5, string6]
        if ( index > len(ret_list) ):
            return ( ret_list[len(ret_list) - 1], )
        return (ret_list[ index - 1 ], )

class GridStringList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ( "INT", {"default": 1, "min": 1, "max": 100 } ),
                "string_list": ("STRING", {"multiline": True}), 
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "SplitAndReturnStrings"
    CATEGORY = "EasyGrids"

    def __init__(self):
        self.static_text = "" 
        self.static_out_arr = []

    def SplitAndReturnStrings( self, index: int, string_list: str ):
        if string_list != self.static_text:
            # unlike the numeric list nodes, we only want to split on newlines
            # TODO: support manual delimiter specification?
            split_str = re.split( "\n", string_list )
            self.static_text = string_list
            self.static_out_arr = deepcopy( split_str )
        if ( index > len(self.static_out_arr) ):
            return ( self.static_out_arr[len(self.static_out_arr) - 1], )
        return (self.static_out_arr[ index - 1 ],)

class ImageGridCommander:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { "x_count": ("INT", {"default": 1, "min": 1, "max": 12, "step": 1}),
                          "y_count": ("INT", {"default": 1, "min": 1, "max": 12, "step": 1}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("INT","INT","INT","INT",)
    RETURN_NAMES = ("x_index", "y_index", "x_size", "y_size",)
    FUNCTION = "queue_batch"
    CATEGORY = "EasyGrids"

    def __init__(self):
        self.curr_x_index = 1
        self.curr_y_index = 1
        self.last_x_count = 0
        self.last_y_count = 0
        self.unique_id = None
    
    def __del__(self):
        if self.unique_id is not None and self is reset_registry.get(self.unique_id, None):
            reset_registry.pop(self.unique_id, None)

    def queue_batch(self, x_count, y_count, unique_id ):
        #wish we could do this on init but there doesn't seem to be a way to get the unique_id at that point
        #there shouldn't be any need to reset before the first run in any case
        if unique_id is not None:
            if unique_id != self.unique_id:
                if self.unique_id is not None and self is reset_registry.get(self.unique_id, None):
                    reset_registry.pop(self.unique_id, None)
                self.unique_id = unique_id
        if self.unique_id not in reset_registry and self.unique_id is not None:
            reset_registry[unique_id] = self
        if x_count != self.last_x_count or y_count != self.last_y_count:
            self.last_x_count = x_count
            self.last_y_count = y_count
            self.curr_x_index = 1
            self.curr_y_index = 1
        last_x_index = self.curr_x_index
        last_y_index = self.curr_y_index
        self.curr_x_index += 1
        if self.curr_x_index > x_count:
            self.curr_x_index = 1
            self.curr_y_index += 1
            if self.curr_y_index > y_count:
                self.curr_y_index = 1
        return (last_x_index, last_y_index, x_count, y_count,)

    # This node will always be run
    @classmethod
    def IS_CHANGED( s, x_count, y_count ):
        return float("NaN")

    def reset(self):
        self.curr_x_index = 1
        self.curr_y_index = 1
        self.last_x_count = 0
        self.last_y_count = 0

class TextConcatenator:
    @classmethod
    def INPUT_TYPES(s):
        return { "required" : { "text_1": ("STRING", {"multiline": True}),
                                "text_2": ("STRING", {"multiline": True}), } }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "concat_text"
    CATEGORY = "EasyGrids"

    def concat_text( self, text_1, text_2 ):
        #simple as!
        return ((text_1 + text_2), )

class FloatToText:
    @classmethod
    def INPUT_TYPES(s):
        return { "required": { "float_input": ("FLOAT", {"default": 1.0, "step": 0.01}), 
                               "decimal_places": ("INT", {"default": 3, "min": 1, "max": 10 }), }}

    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert_to_str"
    CATEGORY = "EasyGrids"

    def convert_to_str(self, float_input : float, decimal_places : int):
        # if this doesn't work, blame Copilot
        formatted_float = "{:.{}f}".format(float_input, decimal_places)
        return (formatted_float,)

class IntToText:
    @classmethod
    def INPUT_TYPES(s):
        return { "required": { "int_input": ("INT", {"default": 1}), }}

    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert_to_str"
    CATEGORY = "EasyGrids"

    def convert_to_str(self, int_input : int):
        return (str(int_input),)

class SaveImageGrid:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.image_grid = []
        self.curr_x_size = 1
        self.curr_x_idx = 0
        self.curr_y_size = 1
        self.curr_y_idx = 0
        self.done_flag = False
        self.unique_id = None
    
    def __del__(self):
        if self.unique_id is not None and self is reset_registry.get(self.unique_id, None):
            reset_registry.pop(self.unique_id, None)

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"images": ("IMAGE", ),
                     "x_size": ("INT", {"default": 1, "min": 1, "max": 12, "step": 1}),
                     "y_size": ("INT", {"default": 1, "min": 1, "max": 12, "step": 1}),
                     "filename_prefix": ("STRING", {"default": "ComfyUI"})},
                "optional" : { "annotations": ("GRID_ANNOTATION",)}, 
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID" },
                }

    RETURN_TYPES = ()
    FUNCTION = "accumulate_images"

    OUTPUT_NODE = True

    CATEGORY = "EasyGrids"

    def accumulate_images(self, images, x_size, y_size, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None, annotations=None, unique_id=None):
        if unique_id is not None:
            if unique_id != self.unique_id:
                if self.unique_id is not None and self is reset_registry.get(self.unique_id, None):
                    reset_registry.pop(self.unique_id, None)
                self.unique_id = unique_id
        if self.unique_id not in reset_registry and self.unique_id is not None:
            reset_registry[unique_id] = self
        filename_prefix += self.prefix_append
        if x_size != self.curr_x_size or y_size != self.curr_y_size or self.done_flag:
            self.curr_x_size = x_size
            self.curr_y_size = y_size
            self.reset()
        for image in images:
            self.image_grid.append(image)
            self.curr_x_idx += 1
            if self.curr_x_idx >= self.curr_x_size:
                self.curr_y_idx += 1
                self.curr_x_idx = 0
                
        if len( self.image_grid ) >= self.curr_x_size * self.curr_y_size:
            #complete grid
            grid_image = self.assemble_grid( annotations )
            return self.save_grid( grid_image, filename_prefix, prompt, extra_pnginfo )
        return { "ui": { "images": [] } }
    
    def assemble_grid( self, annotations: Annotation | None = None ):
        space_height = max( [ len(image) for image in self.image_grid ] )
        space_width = max( [ len(image[0]) for image in self.image_grid ] )
        total_width = space_width * self.curr_x_size
        total_height = space_height * self.curr_y_size
        width_padding = 0
        height_padding = 0
        if annotations is not None:
            width_padding = int(max( [ annotations.font.getlength( text ) for text in annotations.row_texts ] ) * 1.5)
            height_padding = int(max( [ ( annotations.font.getbbox( text )[3] - annotations.font.getbbox( text )[1] ) for text in annotations.column_texts ] )  * 1.5)
        total_width += width_padding
        total_height += height_padding
        with Image.new("RGB", (total_width, total_height), color="#ffffff") as grid_canvas:
            draw = ImageDraw.Draw( grid_canvas )
            for y_idx in range( self.curr_y_size ):
                if annotations is not None and y_idx < len( annotations.column_texts ):
                    row_x_anchor = width_padding / 2
                    row_y_anchor = height_padding + space_height * y_idx + ( space_height / 2 )
                    draw.text((row_x_anchor, row_y_anchor), annotations.row_texts[y_idx], anchor="mm", font=annotations.font, fill="#000000")
                for x_idx in range( self.curr_x_size ):
                    if y_idx == 0:
                        if annotations is not None and x_idx < len( annotations.row_texts ):
                            col_x_anchor = width_padding + space_width * x_idx + ( space_width / 2 )
                            col_y_anchor = height_padding / 2
                            draw.text((col_x_anchor, col_y_anchor), annotations.column_texts[x_idx], anchor="mm", font=annotations.font, fill="#000000")
                    pil_image = Image.fromarray( np.clip( ( self.image_grid[ ( y_idx * self.curr_x_size ) + x_idx].cpu().numpy() * 255. ), 0, 255 ).astype( np.uint8 ) )
                    grid_canvas.paste(pil_image, ((x_idx * space_width) + width_padding, (y_idx * space_height) + height_padding ))
            return grid_canvas


    def save_grid( self, grid_image, filename_prefix, prompt=None, extra_pnginfo=None ):
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, grid_image.width, grid_image.height)
        results = list()
        metadata = None
        if not args.disable_metadata:
            metadata = PngInfo()
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add_text(x, json.dumps(extra_pnginfo[x]))

        file = f"{filename}_{counter:05}_.png"
        grid_image.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=4)
        results.append({
            "filename": file,
            "subfolder": subfolder,
            "type": self.type
        })
        self.done_flag = True
        return { "ui": { "images": results } }

    def reset( self ):
        self.curr_x_idx = 0
        self.curr_y_idx = 0
        self.image_grid = []
        self.done_flag = False


NODE_CLASS_MAPPINGS = {
    "ImageGridCommander": ImageGridCommander,
    "GridFloats": GridFloats,
    "GridFloatList": GridFloatList,
    "GridInts": GridInts,
    "GridIntList": GridIntList,
    "GridStrings": GridStrings,
    "GridStringList": GridStringList,
    "TextConcatenator": TextConcatenator,
    "FloatToText": FloatToText,
    "IntToText": IntToText,
    "SaveImageGrid": SaveImageGrid,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageGridCommander": "Create Image Grid",
    "GridFloats" : "Float List",
    "GridFloatList": "Float List fom Text Field",
    "GridInts": "Int List",
    "GridIntList": "Int List from Text Field",
    "GridStrings": "String List",
    "GridStringList": "String List from Text Field",
    "TextConcatenator": "Text Concatenator",
    "FloatToText": "Float to Text",
    "IntToText": "Int to Text",
    "SaveImageGrid": "Save Image Grid",
}