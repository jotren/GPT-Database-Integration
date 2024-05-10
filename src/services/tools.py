def define_tools():
    """
    Dynamically define the list of tools available based on the context of the conversation.
    Args:
    context (dict): The context dictionary containing keys like 'data_collected' and 'data_needed'.
    
    Returns:
    list: A list of tool definitions that should be available for the next step.
    """
    tools = []
    
    tools.append({
        "type": "function",
        "function": {
            "name": "get_all_system_severity_data",
            "description": "Fetch high level details on the severities of all the systems in the site. Severity2 is advanced warning, Severity1 is early warning, and Severity0 is no warning.",
            "parameters": {},
        }
    })

    tools.append({
        "type": "function",
        "function": {
            "name": "get_number_of_assets",
            "description": "Get number of assets at the site.",
            "parameters": {},
        }
    })

    tools.append({
        "type": "function",
        "function": {
            "name": "get_number_of_reports",
            "description": "Get number of reports at the site.",
            "parameters": {},
        }
    })

    tools.append({
        "type": "function",
        "function": {
            "name": "get_all_asset_severity_data",
            "description": "Asset information sorted from most severe to least severe.",
            "parameters": {},
        }
    })

    tools.append({
        "type": "function",
        "function": {
            "name": "get_all_report_data_from_asset_names",
            "description": "Fetch all reports for a given asset name. You can use the assetName here to find the specific report IDs for specific systems and feed it into get_single_report_data",
            "parameters": {
                "type": "object",
                "properties": {
                    "assetName": {"type": "string", "description": "Asset name to fetch reports for"},
                },
                "required": ["assetName"],
            }
        }
    })

    tools.append({
        "type": "function",
        "function": {
            "name": "get_all_report_data_from_asset_names_full",
            "description": "Fetch all reports for a given asset name. You can use the assetName here to find the specific report IDs for specific systems and feed it into get_single_report_data. You only need this data if you require reports older than the most recent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "assetName": {
                        "type": "string",
                        "description": "The name of the asset in the format e.g. F2",
                    },
                },
                "required": ["assetName"],
            },
        }
    })

    tools.append({
        "type": "function",
        "function": {
            "name": "get_single_report_data",
            "description": "Fetch details of a single report that relates to a single asset and system. This call provides mode information on what is causing problems.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reportID": {"type": "string", "description": "The ID of the report to fetch"},
                },
                "required": ["reportID"],
            }
        }
    })

    tools.append({
        "type": "function",
        "function": {
            "name": "get_asset_ids_names",
            "description": "Provides information on all the asset names and IDs. Useful to getting the paramaters for hyperlinks",
            "parameters": {},
        }
    })

    
    tools.append({
        "type": "function",
        "function": {
            "name": "get_asset_comments",
            "description": "Fetch all comments made against a specific asset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "entityId": {
                        "type": "string",
                        "description": "The ID of the asset to fetch comments for."
                    },
                },
                "required": ["assetID"]
            }
        }
    })

    tools.append({
        "type": "function",
        "function": {
            "name": "get_report_comments",
            "description": "Return all user comments made against a specific report.",
            "parameters": {
                "type": "object",
                "properties": {
                    "entityId": {
                        "type": "string",
                        "description": "The ID of the report to fetch comments for."
                    },
                },
                "required": ["reportID"]
            }
        }
    })

    tools.append({
        "type": "function",
        "function": {
            "name": "get_all_report_comments",
            "description": "Get all comments for reports within the site.",
            "parameters": {}
        }
    })

    return tools
