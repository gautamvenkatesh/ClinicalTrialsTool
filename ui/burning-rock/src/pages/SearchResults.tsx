/**
 * Display search result trials
 */
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

//Default parameters to include in data
const INCLUDE_PARAMETERS = ['total', 'record_verification_date', 'nci_id', 'lead_org', 'official_title', 'current_trial_status', 'start_date',
'completion_date', 'brief_summary', 'detail_description', 'primary_purpose', 'phase', 'nct_id']


//TO-DO: 
    // 1. Debug generateResults. As of now, it seems that the URl isn't properly being constructed in the string 
    // 2. Add the UI table to display search results (take ex. from NewTrials) from the 'results' state variable
    // 3. Use react semantic ui pagination. Create a function to update currPage when you load the next page
    //      - Updating currPage should trigger a useEffect to update the next 50 results 

 const SearchResults: React.FC = () => {
    //use axiosProps to access GET request metadata (.searchString, .trialStatuses, .phaseTypes, .sortType)
    const axiosProps = useLocation().state
    const [currPage, setCurrPage] = useState(0)
    const [results, setResults] = useState(Array())
    const axios = require('axios')

    //Update the results state if we change page
    useEffect(() => {
        generateResults()
    }, [currPage])
    // Start is the starting index for the api call 
    const generateResults = async () => {
        console.log('props are : ', axiosProps)

        //Starting index for page search (pagination should be every 50 searches)
        var start = currPage*50
        var apiCall = 'https://clinicaltrialsapi.cancer.gov/api/v2/trials?size=50&from' + start.toString() + '&'
        var headers = {'x-api-key': 'T0GzvGRulK6fFeFVzjmeo1Est2KbWeW25OXpyszf'}
        if (axiosProps.sortType == 'nci_id') {
            apiCall += 'sort=nci_id&'
        }
        if (axiosProps.searchString) {
            apiCall = apiCall + 'keyword=' + axiosProps.searchString + '&' 
        }
        if (axiosProps.trialStatuses) {
            axiosProps.trialStatuses.forEach((trial_status: string, index: any) => {
                apiCall = apiCall + 'trial_status=' + trial_status + '&'
                console.log('apicall is: ', apiCall)
            })
        }
        if (axiosProps.phaseTypes) {
            axiosProps.phaseTypes.forEach((phase_type: string, index: any) => {
                apiCall = apiCall + 'phase=' + phase_type + '&'
            })
        }
        INCLUDE_PARAMETERS.forEach((param, index) => {
            apiCall = apiCall + param
        })

        const res = await axios.get(apiCall, {
            headers: {headers}
        })
        setResults(res)
    
    }

    return (
        <>
        Table Here
        </>
    );
}
export default SearchResults;