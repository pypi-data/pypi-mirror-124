import click

from tirf_ob import version
from tirf_ob.utils.load_data import *


@click.command()
@click.option('-dir_img', '--dir_img',
              help='Directory to the image in *.tif format.',
              show_default=True)
@click.option('-dir_csv', '--dir_csv',
              help='Directory to the coordinates in *.csv format.',
              show_default=True)
@click.option('-m', '--mask_size',
              default=256,
              help='Size of the cropping mask',
              show_default=True)
@click.version_option(version=version)
def main(dir_img: str,
         dir_csv: str,
         mask_size: int):
    image = load_image_to_numpy(dir_img)
    coord = load_csv_to_numpy(dir_csv)

    # TODO interpolation
    size = image.shape
    corped_image = np.zeros((size[0], mask_size, mask_size))

    """ Main loop to corp image """
    for i in range(size[0]):
        idx = np.where(coord[:, 2] == (i + 1))[0]

        if len(idx) == 1:
            idx = idx
        elif len(idx) == 0:
            # ToDo interpolation
            assert i != 0 or i != (size[0] - 1), 'For the interpolation first and the last point are needed!'
            past = np.where(coord[:, 2] == i)[0]
            feature = np.where(coord[:, 2] == (i + 2))[0]
            idx = (coord[past, ] + coord[feature, ]) / 2
        else:
            idx = np.array(int(round(idx.mean(), 0)))

        if idx.size == 1:
            crop_y_start, crop_y_stop = coord[idx, 0] - mask_size / 2, coord[idx, 0] + mask_size / 2
            crop_x_start, crop_x_stop = coord[idx, 1] - mask_size / 2, coord[idx, 1] + mask_size / 2
        if idx.size == 3:
            crop_y_start, crop_y_stop = idx[0, 0] - mask_size / 2, idx[0, 0] + mask_size / 2
            crop_x_start, crop_x_stop = idx[0, 1] - mask_size / 2, idx[0, 1] + mask_size / 2

        corped_image[i, :, :] = image[
                                i,
                                int(crop_x_start):int(crop_x_stop),
                                int(crop_y_start): int(crop_y_stop)
                                ]

    tifffile.imsave('output.tif',
                    corped_image)


if __name__ == '__main__':
    main()
