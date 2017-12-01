from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.characteristics.characteristics_names import *
from Source.Model.main.delineation.morfology_point import *
import numpy as np
from hrv.classical import frequency_domain
from hrv.utils import open_rri


class QRSPlotData:

    def __init__(self, lead):

        rr_dist = []
        bins_centers = []
        hist = []
        pdf = []

        rate = lead.rate
        qrs_dels = lead.qrs_dels

        if qrs_dels:

            if len(qrs_dels) > 1:

                for qrs_id in range(0, len(qrs_dels) - 1):
                    current_rr = (qrs_dels[qrs_id + 1].peak_index - qrs_dels[qrs_id].peak_index) / rate
                    rr_dist.append(current_rr)

            if rr_dist:

                rr_diffs = []
                for rr_id in range(0, len(rr_dist) - 1):
                    rr_diffs.append((rr_dist[rr_id + 1] - rr_dist[rr_id]))

                bins_borders = np.arange(0.0, 3.0, 0.0078125)
                bins_borders.tolist()
                hist_data = np.histogram(rr_dist, bins_borders)

                bins_centers = []
                for bin_id in range(0, len(bins_borders) - 1):
                    bins_centers.append((bins_borders[bin_id + 1] + bins_borders[bin_id]) * 0.5)


                hist = hist_data[0].tolist()
                pdf = (hist_data[0] / (sum(hist_data[0]) * (bins_borders[1] - bins_borders[0]))).tolist()

        plot_data_dict = {
            QRSPlotDataNames.rr_dist : rr_dist,
            QRSPlotDataNames.rr_bins_centers : bins_centers,
            QRSPlotDataNames.rr_hist : hist,
            QRSPlotDataNames.rr_pdf : pdf
        }

        self.dict = plot_data_dict


class QRSPlotDataNames(Enum):
    rr_dist = 'rr_dist'
    rr_bins_centers = 'rr_bins_centers'
    rr_hist = 'rr_hist'
    rr_pdf = 'rr_pdf'
