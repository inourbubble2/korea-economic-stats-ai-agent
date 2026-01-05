def format_date(date_str: str, cycle: str) -> str:
    """
    Format date string to match ECOS API requirements based on cycle.
    Removes non-alphanumeric characters.
    """
    if not date_str:
        return ""

    # Remove separators (., -, /)
    cleaned = "".join(c for c in date_str if c.isalnum())

    # Basic validation/truncation based on cycle
    if cycle == "A":
        return cleaned[:4]  # YYYY
    elif cycle == "Q":
        return cleaned[:6]  # YYYYQn
    elif cycle == "M":
        return cleaned[:6]  # YYYYMM
    elif cycle == "D":
        return cleaned[:8]  # YYYYMMDD

    return cleaned
