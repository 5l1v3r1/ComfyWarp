from PIL import Image, ImageOps 
import torch
import hashlib
import numpy as np
import glob

class LoadFrameSequence:
    @classmethod
    def INPUT_TYPES(self):
        return {"required":
                    {
                        "file_path": ("STRING", {"multiline": True, 
                                                 "default":"C:\code\warp\19_cn_venv\images_out\stable_warpfusion_0.20.0\videoFrames\650571deef_0_0_1"})
                    }
                }
    
    CATEGORY = "WarpFusion"
    OUTPUT_IS_LIST = (True,False)
    RETURN_TYPES = ("FRAMES", "INT")
    RETURN_NAMES = ("Frames", "Total_frames")
    FUNCTION = "get_frames"

    def get_frames(self, file_path):
        print(file_path)
        self.frames = glob.glob(file_path+'/**/*.*', recursive=True)
        self.max_frames = len(self.frames)
        print(f'Found {len(self.frames)} frames.')
        out = [{'image':frame, 'max_frames':self.max_frames}for frame in self.frames]
        return (out,self.max_frames)

    @classmethod
    def IS_CHANGED(self, file_path):
        self.get_frames(self, file_path)

    @classmethod
    def VALIDATE_INPUTS(self, file_path):
        self.get_frames(self, file_path)
        if len(self.frames)==0:
            return f"Found 0 frames in path {file_path}"

        return True
    
class LoadFrame:
    @classmethod
    def INPUT_TYPES(self):
        return {"required":
                    {
                        "file_paths": ("FRAMES",),
                        "seed": ("INT", {"default": 0, "min": 0, "max": 9999999999}),
                        "total_frames":("INT", {"default": 0, "min": 0, "max": 9999999999})
                    }
                }
    
    CATEGORY = "WarpFusion/Frames"

    INPUT_IS_LIST = True
    RETURN_TYPES = ("IMAGE","INT")
    RETURN_NAMES = ("Image","Frame number")
    FUNCTION = "load_frame"
    #validation fails here for some reason 

    def load_frame(self, file_paths, seed, total_frames):
        frame_number = seed
        print(file_paths[:10], frame_number, total_frames)
        frame_number = frame_number[0]
        total_frames = total_frames[0]
        frame_number = min(min(frame_number, total_frames), len(file_paths)-1)
        print(frame_number)
        image_path = file_paths[frame_number]['image']

        i = Image.open(image_path)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        print(image.shape, frame_number, total_frames)
        
        return (image, frame_number)

NODE_CLASS_MAPPINGS = {
    "LoadFrameSequence": LoadFrameSequence,
    "LoadFrame": LoadFrame
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadFrameSequence": "Load Frame Sequence",
    "LoadFrame":"Load Frame"
}
