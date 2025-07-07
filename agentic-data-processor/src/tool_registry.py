# TODO - so that agent_config.yaml only needs to list tool names, no manual wiring - need to fix

from src.transformations import drop_nulls, convert_to_datetime, filter_by_value, redact_column, rename_column, standardize_text

TOOL_REGISTRY = {
    'drop_nulls': drop_nulls,
    'convert_to_datetime': convert_to_datetime,
    'filter_by_value': filter_by_value,
    'redact_column': redact_column,
    'rename_column': rename_column,
    'standardize_text': standardize_text,
}
