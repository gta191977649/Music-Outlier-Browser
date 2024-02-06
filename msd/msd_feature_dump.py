
import h5.hdf5_getters as h5

file = h5.open_h5_file_read("/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/blue_oyster_cult/h5/TRNJREN128F4267C9B.h5")
feature = h5.get_beats_start(file)