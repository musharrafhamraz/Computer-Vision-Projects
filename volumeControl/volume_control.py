import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class VolumeControl:
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.min_vol, self.max_vol = self.volume.GetVolumeRange()[0], self.volume.GetVolumeRange()[1]

    def set_volume_by_distance(self, distance, min_distance=25, max_distance=250):
        """Set the volume based on the hand distance."""
        volume_level = np.interp(distance, [min_distance, max_distance], [self.min_vol, self.max_vol])
        self.volume.SetMasterVolumeLevel(volume_level, None)
