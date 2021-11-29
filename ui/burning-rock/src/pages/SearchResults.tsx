/**
 * Display search result trials
 */
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";


const INCLUDE_PARAMETERS = ['total', 'record_verification_date', 'nci_id', 'lead_org', 'official_title', 'current_trial_status', 'start_date',
'completion_date', 'brief_summary', 'detail_description', 'primary_purpose', 'phase', 'nct_id']
    
 const SearchResults: React.FC = () => {

    const axiosProps = useLocation().state
    const [currPage, setCurrPage] = useState(0)
    const [results, setResults] = useState(Array())
    const axios = require('axios')

    useEffect(() => {
        generateResults(currPage)
    }, [currPage])

    const generateResults = async (start: number) => {
        console.log('props are : ', axiosProps)
        //Constructing URL with parameters 
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