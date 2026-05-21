def classify_severity(x1, y1, x2, y2):
    area = (x2 - x1) * (y2 - y1)
    if area < 5000:
        return "small"
    elif area < 20000:
        return "medium"
    else:
        return "large"