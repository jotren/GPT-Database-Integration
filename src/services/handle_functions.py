def handle_function_call(api, function_name, function_args):
    """
    Handles API function calls based on the function name and arguments.
    Updates the context with the data collected and determines the next steps.
    
    Args:
        function_name (str): The name of the function to call.
        function_args (dict): Arguments needed for the API function.
        context (dict): Context of the conversation to be updated.
    
    Returns:
        tuple: The response from the function and the updated context.
    """
    function_response = None
    break_loop = False

    try:
        if function_name == "get_asset_ids_names":
            asset_data = api.get_asset_ids_names()
            function_response = asset_data        

        elif function_name == "get_single_report_data":
            if 'reportID' in function_args:
                report_data = api.get_single_report_data(function_args['reportID'])
                function_response = report_data
          
            else:
                function_response = "Report ID missing."
                
        elif function_name == "get_all_report_data_from_asset_names":
            if 'assetName' in function_args:
                reports_data = api.get_all_report_data_from_asset_names(function_args['assetName'])
                function_response = reports_data

        elif function_name == "get_all_report_data_from_asset_names_full":
            if 'assetName' in function_args:
                reports_data = api.get_all_report_data_from_asset_names_full(function_args['assetName'])
                function_response = reports_data
            
        elif function_name == "get_all_system_severity_data":
            severity_data = api.get_all_system_severity_data()
            function_response = severity_data
        

        elif function_name == "get_number_of_assets":
            num_assets = api.get_number_of_assets()
            function_response = num_assets

        elif function_name == "get_asset_ids_names":
            asset_ids_names = api.get_asset_ids_names()
            function_response = asset_ids_names
        

        elif function_name == "get_number_of_reports":
            num_reports = api.get_number_of_reports()
            function_response = num_reports
        

        elif function_name == "get_all_asset_severity_data":
            severity_data = api.get_all_asset_severity_data()
            function_response = severity_data

        elif function_name == "get_asset_comments":
            if 'assetID' in function_args:
                function_response = api.get_asset_comments(function_args['entityId'])
            else:
                function_response = "Entity ID missing for asset comments."

        elif function_name == "get_report_comments":
            if 'reportID' in function_args:
                function_response = api.get_report_comments(function_args['entityId'])
            else:
                function_response = "Entity ID missing for report comments."

        elif function_name == "get_all_report_comments":
            function_response = api.get_all_report_comments()

        else:
            function_response = "Function not recognized."

    except Exception as e:
        function_response = f"An error occurred: {str(e)}"

    return function_response, break_loop
