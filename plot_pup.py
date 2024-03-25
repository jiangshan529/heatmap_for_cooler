
import pandas as pd
import h5sparse
import re
import os
import numpy as np
import matplotlib.pyplot as plt

import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Plot heatmap from a given file.")
# Add an argument
parser.add_argument('--input', type=str, help='The file path to the data file.')

# Argument parser setup
parser = argparse.ArgumentParser(description="Plot heatmaps from given files and customize color scales.")
parser.add_argument('--input', type=str, help='The file paths to the data files, separated by commas.')
parser.add_argument('--vmin', type=float, default=0.6, help='Minimum value for the color scale of the first matrix.')
parser.add_argument('--vmax', type=float, default=1.4, help='Maximum value for the color scale of the first matrix.')
parser.add_argument('--vmin_diff', type=float, default=-0.2, help='Minimum value for the color scale of the difference matrix.')
parser.add_argument('--vmax_diff', type=float, default=0.2, help='Maximum value for the color scale of the difference matrix.')
args = parser.parse_args()

# Now args.file_path holds the input file path
file_path = args.input
vmin = args.vmin
vmax = args.vmax
base_name = os.path.splitext(os.path.basename(file_path))[0]
output_file = f'{base_name}_heatmap.pdf'

__version__ = "1.1.0"
def load_pileup_df(filename, quaich=False, skipstripes=False):
    """
    Loads a dataframe saved using `save_pileup_df`

    Parameters
    ----------
    filename : str
        File to load from.
    quaich : bool, optional
        Whether to assume standard quaich file naming to extract sample name and bedname.
        The default is False.

    Returns
    -------
    annotation : pd.DataFrame
        Pileups are in the "data" column, all metadata in other columns

    """
    with h5sparse.File(filename, "r", libver="latest") as f:
        metadata = dict(zip(f["attrs"].attrs.keys(), f["attrs"].attrs.values()))
        dstore = f["data"]
        data = []
        for chunk in dstore.iter_chunks():
            chunk = dstore[chunk]
            data.append(chunk)
        annotation = pd.read_hdf(filename, "annotation")
        annotation["data"] = data
        vertical_stripe = []
        horizontal_stripe = []
        coordinates = []
        if not skipstripes:
            try:
                for i in range(len(data)):
                    vstripe = "vertical_stripe_" + str(i)
                    hstripe = "horizontal_stripe_" + str(i)
                    coords = "coordinates_" + str(i)
                    vertical_stripe.append(f[vstripe][:].toarray())
                    horizontal_stripe.append(f[hstripe][:].toarray())
                    coordinates.append(f[coords][:].astype("U13"))
                annotation["vertical_stripe"] = vertical_stripe
                annotation["horizontal_stripe"] = horizontal_stripe
                annotation["coordinates"] = coordinates
            except KeyError:
                pass
    for key, val in metadata.items():
        if key != "version":
            annotation[key] = val
        elif val != __version__:
            logger.debug(
                f"pileup generated with v{val}. Current version is v{__version__}"
            )
    if quaich:
        basename = os.path.basename(filename)
        sample, bedname = re.search(
            "^(.*)-(?:[0-9]+)_over_(.*)_(?:[0-9]+-shifts|expected).*\.clpy", basename
        ).groups()
        annotation["sample"] = sample
        annotation["bedname"] = bedname
    matrix_to_plot = annotation.loc[0, 'data']
    return matrix_to_plot


 

# print(np.array2string(annotation, threshold=np.inf, max_line_width=np.inf))



file_paths = args.input.split(',')
matrices = [load_pileup_df(file_path) for file_path in file_paths]

# Calculate the difference if two matrices are provided

# Plotting based on the number of matrices
if len(matrices) == 1:
    # Single matrix case
    base_name = os.path.splitext(os.path.basename(file_paths[0]))[0]
    output_file = f'{base_name}_heatmap.pdf'
    matrix_to_plot = matrices[0]
    plt.figure(figsize=(10, 8))
    plt.imshow(matrix_to_plot, aspect='auto', cmap="coolwarm", vmin=args.vmin, vmax=args.vmax)
    plt.colorbar()
    plt.title('Matrix Heatmap')
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.savefig(output_file, format='pdf', bbox_inches='tight')

    plt.show()  # Show the plot
elif len(matrices) == 2:
    difference_matrix = matrices[0] - matrices[1]
    np.fill_diagonal(difference_matrix, np.nan)
    matrices.append(difference_matrix)
    base_name = os.path.splitext(os.path.basename(file_paths[0]))[0]
    output_file = f'{base_name}_combined_heatmap.pdf'

    # Plotting
    fig, axs = plt.subplots(1, len(matrices), figsize=(10 * len(matrices), 8))
    # Color scales and limits
    # Color scales and limits
    color_scales = ["coolwarm", "coolwarm", "RdBu_r"]
    vmins = [args.vmin, args.vmin, args.vmin_diff]
    vmaxs = [args.vmax, args.vmax, args.vmax_diff]

    titles = ['Matrix 1', 'Matrix 2', 'Difference Matrix']

    for i, matrix in enumerate(matrices):
        ax = axs[i]
        cax = ax.imshow(matrix, aspect='auto', cmap=color_scales[i], vmin=vmins[i], vmax=vmaxs[i])
        fig.colorbar(cax, ax=ax, orientation='vertical')
        ax.set_title(titles[i])
        ax.set_xlabel('X-axis Label')
        ax.set_ylabel('Y-axis Label')

    plt.tight_layout()
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close(fig)



