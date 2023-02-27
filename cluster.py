import pandas as pd

import outlier.outlier as OutlierDetection

import outlier.data as dataset
import outlier.helper as helper
import outlier.result as result
import outlier.cluster as cluster
import numpy as np
import outlier.result as output
import pandas as pd
import outlier.config as CONF
from tqdm import tqdm

if __name__ == '__main__':
    artist_list = [
        "Blue Oyster Cult",
        "MNEMIC",
        "Colin Meloy",
        "Rod Lee",
        "Blue Six"
    ]
    #cluster.clusterSongsByArtist("Rod Lee", x_discriminator="tempo", y_discriminator="loudness")
    cluster.clusterSongsByArtist("Audio Bullys", x_discriminator="tempo", y_discriminator="loudness")
