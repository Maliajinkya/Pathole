def get_gps_tag():
    """
    Returns (lat, lng).
    For live GPS hardware (Raspberry Pi), replace with gpsd logic.
    For now returns None — user provides location via map pin or form.
    """
    return (None, None)