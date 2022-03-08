from iautil import io
from iautil.plotting.image_tool import ImageTool
import os

scans_vti_path = os.path.abspath("tests/test_files")
scans_iau_path = os.path.abspath("tests/test_files/scans40-42.iau")

io.vti_to_iau(
    vti_path=scans_vti_path,
    iau_path=scans_iau_path,
    dims=["H", "K", "L", "V"]
)

da = io.iau_to_data_array(scans_iau_path)
os.remove(scans_iau_path)

it = ImageTool(da)
it.show()