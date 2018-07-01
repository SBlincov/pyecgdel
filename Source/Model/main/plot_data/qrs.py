from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.characteristics.characteristics_names import *
from Source.Model.main.delineation.morfology_point import *
import numpy as np
from hrv.classical import frequency_domain
from hrv.utils import open_rri
from Source.Model.main.plot_data.utils import *

class QRSPlotData:

    def __init__(self, lead):

        rr_dist = []
        bins_centers = []
        hist = []
        pdf = []
        ellipse_pca = []
        ellipse_bis = []

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

                if (len(rr_dist) > 2):

                    # PCA ellipse
                    x = np.asarray(rr_dist[:-1])
                    y = np.asarray(rr_dist[1:])

                    X = np.vstack((x, y))
                    Xcentered = (X[0] - x.mean(), X[1] - y.mean())
                    m = [x.mean(), y.mean()]
                    covmat = np.cov(Xcentered)
                    vals, vecs = np.linalg.eig(covmat)
                    angle = angle_between(np.asarray([1.0, 0.0]), vecs[1]) * 57.2958
                    a = 3.0 * np.sqrt(vals[0])
                    b = 3.0 * np.sqrt(vals[1])

                    ellipse_pca_center_x = m[0]
                    ellipse_pca_center_y = m[1]
                    ellipse_pca_a = a
                    ellipse_pca_b = b
                    ellipse_pca_angle = angle

                    ellipse_pca = [float(ellipse_pca_center_x),
                                   float(ellipse_pca_center_y),
                                   float(ellipse_pca_a),
                                   float(ellipse_pca_b),
                                   float(ellipse_pca_angle)]

                    # Bisector ellipse
                    x_c = np.mean(x)
                    y_c = np.mean(y)
                    x_center = (x_c + y_c) * 0.5
                    y_center = (x_c + y_c) * 0.5
                    point_center = [x_center, y_center]

                    x_45 = x_center + 1.0
                    y_45 = y_center + 1.0
                    point_45 = [x_45, y_45]

                    x_135 = x_center - 1.0
                    y_135 = y_center + 1.0
                    point_135 = [x_135, y_135]

                    dist_45 = []
                    dist_135 = []
                    for point_id in range(0, len(x)):
                        point = [x[point_id], y[point_id]]
                        curr_dist_45 = distance_point_to_line(point, point_center, point_45)
                        dist_45.append(curr_dist_45)
                        curr_dist_135 = distance_point_to_line(point, point_center, point_135)
                        dist_135.append(curr_dist_135)

                    mean_45 = np.mean(dist_45)
                    std_45 = np.std(dist_45)
                    mean_135 = np.mean(dist_135)
                    std_135 = np.std(dist_135)
                    ellipse_bis_center_x = x_center
                    ellipse_bis_center_y = y_center
                    ellipse_bis_a = 2.0 * mean_45 + 6.0 * std_45
                    ellipse_bis_b = 2.0 * mean_135 + 6.0 * std_135
                    ellipse_bis_angle = 45.0

                    ellipse_bis = [float(ellipse_bis_center_x),
                                   float(ellipse_bis_center_y),
                                   float(ellipse_bis_a),
                                   float(ellipse_bis_b),
                                   float(ellipse_bis_angle)]

        plot_data_dict = {
            QRSPlotDataNames.rr_dist : list(map(float, rr_dist)),
            QRSPlotDataNames.rr_bins_centers : list(map(float, bins_centers)),
            QRSPlotDataNames.rr_hist : list(map(float, hist)),
            QRSPlotDataNames.rr_pdf : list(map(float, pdf)),
            QRSPlotDataNames.rr_ellipse_pca : list(map(float, ellipse_pca)),
            QRSPlotDataNames.rr_ellipse_bis : list(map(float, ellipse_bis))
        }

        self.dict = plot_data_dict


class QRSPlotDataNames:
    rr_dist = 'rr_dist'
    rr_bins_centers = 'rr_bins_centers'
    rr_hist = 'rr_hist'
    rr_pdf = 'rr_pdf'
    rr_ellipse_pca = 'rr_ellipse_pca'
    rr_ellipse_bis = 'rr_ellipse_bis'
