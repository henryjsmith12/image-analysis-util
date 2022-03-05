from iautil import io
from iautil.plotting.image_tool import ImageTool
import os


scan40_vti_path = os.path.abspath("tests/test_files/scan40.vti")
scan40_iau_path = os.path.abspath("tests/test_files/scan40.iau")

io.vti_to_iau(
    vti_path=scan40_vti_path,
    iau_path=scan40_iau_path,
    dims=["H", "K", "L"]
)

da = io.iau_to_data_array(scan40_iau_path)[:, :, 100]

os.remove(scan40_iau_path)

it = ImageTool(da)
it.show()