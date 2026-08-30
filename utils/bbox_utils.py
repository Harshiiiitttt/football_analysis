def get_centre_of_bbox(bbox):
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int(y2)

def get_bbox_width(bbox):
    return int(bbox[2] - bbox[0])
