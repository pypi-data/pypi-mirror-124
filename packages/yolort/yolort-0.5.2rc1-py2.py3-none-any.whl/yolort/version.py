__version__ = '0.5.2rc1'
git_version = '01403bf785f8b17ffbf2f823e84efc3d24a6fcc3'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
