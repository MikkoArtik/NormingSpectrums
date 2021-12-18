import argparse
import os

import numpy as np


SPECTRUM_EXTENSION = 'ssc'
NORMING_EXTENSION = 'nssc'


def load_norming_curve(path: str) -> np.ndarray:
    return np.loadtxt(path, skiprows=1, delimiter='\t')


def load_spectrum(path: str) -> np.ndarray:
    return np.loadtxt(path, delimiter=' ')


def get_norming_spectrum(spectrum_data: np.ndarray,
                         norming_curve: np.ndarray) -> np.ndarray:
    norming_spectrum = np.zeros(shape=(spectrum_data.shape[0], 2))
    norming_spectrum[:, 0] = spectrum_data[:, 0]
    for i, row in enumerate(spectrum_data):
        freq, amplitude = row
        coefficient = np.interp(freq, norming_curve[:, 0],
                                norming_curve[:, 1])
        norming_spectrum[i, 1] = amplitude * coefficient
    return norming_spectrum


if __name__ == '__main__':
    utility = argparse.ArgumentParser(
        description='Утилита для нормирования спектров')
    utility.add_argument('spectrum_root', type=str,
                         help='Путь к папке со спектрами')
    utility.add_argument('norming_curve', type=str,
                         help='Путь к файлу нормировочной кривой')
    utility.add_argument('export_root', type=str,
                         help='Путь для экспорта нормированных спектров')

    args = utility.parse_args()

    spectrum_root = args.spectrum_root
    norming_curve_path = args.norming_curve
    export_root = args.export_root

    spectrum_folder_name = os.path.basename(spectrum_root)
    export_folder = os.path.join(export_root,
                                 spectrum_folder_name + '_norming')

    norming_curve = load_norming_curve(norming_curve_path)

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    for root, _, files in os.walk(spectrum_root):
        for filename in files:
            basename = ''.join(filename.split('.')[:-1])
            extension = filename.split('.')[-1]
            if extension != SPECTRUM_EXTENSION:
                continue

            spectrum_data = load_spectrum(os.path.join(root, filename))
            norm_spectrum = get_norming_spectrum(spectrum_data, norming_curve)

            export_filename = basename + '.' + NORMING_EXTENSION
            export_file_path = os.path.join(export_folder, export_filename)
            header = 'Frequency\tAmplitude'
            np.savetxt(export_file_path, norm_spectrum, '%f', '\t',
                       header=header, comments='')

