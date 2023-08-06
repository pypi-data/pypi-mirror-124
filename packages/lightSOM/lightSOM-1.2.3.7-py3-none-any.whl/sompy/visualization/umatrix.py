from .mapview import MapView
from .plot_tools import plot_hex_map
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from skimage.feature import blob_log

from warnings import warn
from math import sqrt
import numpy as np
import scipy


# def rectxy_to_hexaxy(coord, X, Y):
#     """Convert rectangular grid xy coordinates to hexagonal grid xy coordinates.
#     Useful for plotting additional data on top of hexagonal grid.
#
#     Args:
#         coord (array): array with rectangular grid xy coordinates
#         X (array): mapsize shaped array with hexagonal grid x coordinates
#         Y (array): mapsize shaped array with hexagonal grid y coordinates
#
#     Returns:
#         [array]: array of coord's shape with hexagonal grid xy coordinates
#     """
#     out = np.vstack(([X[tuple(i)] for i in coord], [Y[tuple(i)] for i in coord])).T
#     return out

class UMatrixView(MapView):
    def _set_labels(self, cents, ax, labels, onlyzeros, fontsize, hex=False):
        for i, txt in enumerate(labels):
            if onlyzeros == True:
                if txt > 0:
                    txt = ""
            c = cents[i] if hex else (cents[i, 1], cents[-(i + 1), 0])
            ax.annotate(txt, c, va="center", ha="center", size=fontsize)
    def build_u_matrix(self, som, distance=1, row_normalized=False):
        UD2 = som.calculate_map_dist()
        Umatrix = np.zeros((som.codebook.nnodes, 1))
        codebook = som.codebook.matrix
        if row_normalized:
            vector = som._normalizer.normalize_by(codebook.T, codebook.T).T
        else:
            vector = codebook

        for i in range(som.codebook.nnodes):
            codebook_i = vector[i][np.newaxis, :]
            neighborbor_ind = UD2[i][0:] <= distance
            neighborbor_codebooks = vector[neighborbor_ind]
            neighborbor_dists = scipy.spatial.distance_matrix(
                codebook_i, neighborbor_codebooks)
            Umatrix[i] = np.sum(neighborbor_dists) / (neighborbor_dists.shape[1] - 1)

        return Umatrix.reshape(som.codebook.mapsize)

    def show(self, som, data=None, anotate=True, onlyzeros=False, labelsize=7, cmap="jet"):
        org_w = self.width
        org_h = self.height
        (self.width, self.height, indtoshow, no_row_in_plot, no_col_in_plot,
         axis_num) = self._calculate_figure_params(som, 1, 1)
        self.width /= (self.width / org_w) if self.width > self.height else (self.height / org_h)
        self.height /= (self.width / org_w) if self.width > self.height else (self.height / org_h)
        try:
            clusters = getattr(som, 'cluster_labels')
        except:
            clusters = som.cluster()

        # codebook = getattr(som, 'cluster_labels', som.cluster())
        msz = som.codebook.mapsize

        self.prepare()
        if som.codebook.lattice == "rect":
            ax = self._fig.add_subplot(111)

            if data:
                proj = som.project_data(data)
                cents = som.bmu_ind_to_xy(proj)
                if anotate:
                    # TODO: Fix position of the labels
                    self._set_labels(cents, ax, clusters[proj], onlyzeros, labelsize, hex=False)

            else:
                cents = som.bmu_ind_to_xy(np.arange(0, msz[0]*msz[1]))
                if anotate:
                    # TODO: Fix position of the labels
                    self._set_labels(cents, ax, clusters, onlyzeros, labelsize, hex=False)

            plt.imshow(np.flip(clusters.reshape(msz[0], msz[1])[::],axis=0), alpha=0.5)

        elif som.codebook.lattice == "hexa":
            umat = self.build_u_matrix(som, distance=2, row_normalized=False)

            ax, cents = plot_hex_map(umat,  fig=self._fig, colormap=cmap, colorbar=True)
            if anotate:
                self._set_labels(cents, ax, reversed(clusters), onlyzeros, labelsize, hex=True)

#        plt.show()

#         # Setting figure parameters
#         org_w = self.width
#         org_h = self.height
#         (self.width, self.height, indtoshow, no_row_in_plot, no_col_in_plot,
#             axis_num) = self._calculate_figure_params(som, 1, 1)
#         self.width /= (self.width/org_w) if self.width > self.height else (self.height/org_h)
#         self.height /= (self.width / org_w) if self.width > self.height else (self.height / org_h)
#         self.prepare()
# #        plt.rc('figure', titlesize=self.text_size)
#         colormap = plt.get_cmap('RdYlBu_r')
#
#         # Setting figure data
#         if som.codebook.lattice == "hexa" and distance < sqrt(3):
#             warn("For hexagonal lattice, distance < sqrt(3) produces a null U-matrix.")
#         umat = self.build_u_matrix(som, distance=distance, row_normalized=row_normalized)
#         # msz = som.codebook.mapsize
#         # proj = som._bmu[0]
#         # coord = som.bmu_ind_to_xy(proj)[:, :2]
#         sel_points = list()
#
#         if som.codebook.lattice == "rect":
#             ax = self._fig.add_subplot(111)
#             ax.imshow(umat, cmap=colormap, alpha=1)
#             divider = make_axes_locatable(ax)
#             cax = divider.append_axes("right", size="5%", pad=0.05)
#             plt.colorbar(cm.ScalarMappable(cmap=colormap), cax=cax, orientation='vertical')
#             coord = np.flip(coord, axis=1)
#
#             if contour:
#                 self._set_contour(umat, ax, hex=False)
#
#             if blob:
#                 self._set_blob(umat, coord, ax, hex=False)
#         elif som.codebook.lattice == "hexa":
#             ax, cents = plot_hex_map(umat, colormap=colormap, fig=self._fig, colorbar=True)
#             # X = np.flip(np.array(cents)[:, 0].reshape(msz[0], msz[1]), axis=1)
#             # Y = np.flip(np.array(cents)[:, 1].reshape(msz[0], msz[1]), axis=1)
#             # coord = rectxy_to_hexaxy(coord, X, Y)
#
#             if contour:
#                 self._set_contour(umat, ax, X, Y, hex=True)
#
#             if blob:
#                 self._set_blob(umat, coord, ax, X, Y, hex=True)
#         else:
#             raise ValueError(
#                 'lattice argument of SOM object should be either "rect" or "hexa".')
#
#         if show_data:
#             self._set_show_data(coord[:, 0], coord[:, 1], ax)
#
#         if labels:
#             labels = som.build_data_labels()
#             self._set_labels(labels, coord[:, 0], coord[:, 1], ax)
#
#         # ratio = float(msz[0])/(msz[0]+msz[1])
#         # self._fig.set_size_inches((1-ratio)*15, ratio*15)
#         # plt.tight_layout()
#         # plt.subplots_adjust(top=0.80, hspace=.00, wspace=.000)
#
#         plt.show()
#  #       return sel_points, umat
