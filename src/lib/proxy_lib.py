import os, sys
from PIL import Image

from src.lib.request_lib import get_image_by_url


def load_image(path, origin='local'):
    if origin == 'web':
        return get_image_by_url(path)
    elif origin == 'local':
        return Image.open(path)
    else:
        raise ValueError('Invalid Origin', origin)


def imgs_from_paths(df):
    return [load_image(row['path'], origin=row['origin']) for idx, row in df.iterrows()]


def get_paper_size_300DPI(paper, orientation):
    if paper == 'A4':
        size = (2480, 3508)
    elif paper == 'A3':
        size = (3508, 4960)
    else:
        raise ValueError("Unknown Paper", paper)

    if orientation == 'portrait':
        return size
    else:
        return (size[1], size[0])



def stack_imgs_pdf(imgs, outpath, paper='A4', orientation='portrait'):
    shape300dpiPaper = get_paper_size_300DPI(paper, orientation)
    shape300dpiCard = (744, 1039)
    # dx = (62, 98)

    nFigX = shape300dpiPaper[0] // shape300dpiCard[0]
    nFigY = shape300dpiPaper[1] // shape300dpiCard[1]
    nFigPerPage = nFigX * nFigY

    dx = (shape300dpiPaper[0] - shape300dpiCard[0] * nFigX) // (nFigX + 1)
    dy = (shape300dpiPaper[1] - shape300dpiCard[1] * nFigY) // (nFigY + 1)

    groups1D = [imgs[i:i + nFigPerPage] for i in range(0, len(imgs), nFigPerPage)]

    for iPage, group1D in enumerate(groups1D):
        print("Doing page", iPage, "of", len(groups1D))

        page = Image.new('RGB', shape300dpiPaper, 'white')
        for i in range(nFigY):
            for j in range(nFigX):
                idx1D = nFigY * i + j
                if idx1D < len(group1D):
                    box = (
                        dx * (j + 1) + shape300dpiCard[0] * j,
                        dy * (i + 1) + shape300dpiCard[1] * i
                    )
                    img = group1D[idx1D]
                    img = img.resize(shape300dpiCard, Image.BICUBIC)
                    page.paste(img, box=box)

        outfile = outpath + str(iPage) + '.pdf'
        page.save(outfile)
