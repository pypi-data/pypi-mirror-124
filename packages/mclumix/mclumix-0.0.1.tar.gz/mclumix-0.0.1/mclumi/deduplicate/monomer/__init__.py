# ## /*** block. remote ***/
from .Adjacency import *
from .Build import *
from .DedupBasic import *
from .Cluster import *
from .Directional import *
from .MarkovClustering import *


# ## /*** block. local ***/
# try:
#     from mclumi.deduplicate.monomer.Adjacency import *
#     from mclumi.deduplicate.monomer.Parse import *
#     from mclumi.deduplicate.monomer.DedupBasic import *
#     from mclumi.deduplicate.monomer.Cluster import *
#     from mclumi.deduplicate.monomer.Directional import *
#     from mclumi.deduplicate.monomer.MarkovClustering import *
# except ImportError:
#     pass