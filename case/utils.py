def upload_to_case_files(instance, filename):
    """
    Generates a dynamic upload path for files.
    The path is formatted as: case_files/%Y/%m/%d/case_<case_name>
    """
    case_name = instance.case.name or "unknown_case"
    sanitized_case_name = "".join(
        c if c.isalnum() or c in (" ", "_") else "" for c in case_name
    ).replace(" ", "_")
    return f"case_files/{instance.created_at:%Y/%m/%d}/case_{sanitized_case_name}/{filename}"
