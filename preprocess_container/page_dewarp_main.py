#!/usr/bin/python3
import page_dewarp as p
import numpy as np
import cv2
import os

def dewarp(filename):

    print("    Image on processing.\n")

    img = cv2.imread(filename)

    small = p.resize_to_screen(img)
    basename = os.path.basename(filename)
    name, _ = os.path.splitext(basename)

    pagemask, page_outline = p.get_page_extents(small)

    cinfo_list = p.get_contours(name, small, pagemask, 'text')
    spans = p.assemble_spans(name, small, pagemask, cinfo_list)

    if len(spans) < 3:
        cinfo_list = p.get_contours(name, small, pagemask, 'line')
        spans2 = p.assemble_spans(name, small, pagemask, cinfo_list)
        if len(spans2) > len(spans):
            spans = spans2

    span_points = p.sample_spans(small.shape, spans)

    corners, ycoords, xcoords = p.keypoints_from_samples(name, small,
                                                            pagemask,
                                                            page_outline,
                                                            span_points)

    rough_dims, span_counts, params = p.get_default_params(corners,
                                                                ycoords, xcoords)

    dstpoints = np.vstack((corners[0].reshape((1, 1, 2)),) +
                                tuple(span_points))

    params = p.optimize_params(name, small,
                                    dstpoints,
                                    span_counts, params)

    page_dims = p.get_page_dims(corners, rough_dims, params)

    outfile = p.remap_image(name, img, small, page_dims, params)

    print()
    print("    Image processing is done.\n")
    print("    Sending the processed image to tesseract container\n")

    return outfile