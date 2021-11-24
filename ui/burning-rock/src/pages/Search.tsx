/**
 * Search page for trials
 */
import React, { useState } from 'react'
import { Button, Dropdown, DropdownProps, Form } from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'

const SORT_TYPES = [
    { key: 'start_date', text: 'Start Date', value: 'start_date'},
    { key: 'nci_id', text: 'nci_id', value: 'nci_id'},
    { key: 'relevance', text: 'Relevance', value: 'relevance'}
]
// Note that these are possible values for the current_trial_status and NOT trial_status
const TRIAL_STATUS_FILTERS = [
    { key: 'active', text: 'Active', value: 'active' },
    { key: 'administratively complete', text: 'Administratively Complete', value: 'administratively complete' },
    { key: 'approved', text: 'Approved', value: 'approved' },
    { key: 'closed to accrual', text: 'Closed to Accrual', value: 'closed to accrual' },
    { key: 'closed to accrual and intervention', text: 'Closed to Accrual and Intervention', value: 'closed to accrual and intervention' },
    { key: 'complete', text: 'Complete', value: 'complete' },
    { key: 'inactive', text: 'INACTIVE', value: 'inactive' },
    { key: 'enrolling by invitation', text: 'Enrolling by Invitation', value: 'enrolling by invitation' },
    { key: 'temporarily closed to accrual and intervention', text: 'Temporarily Closed to Accrual and Intervention', value: 'temporarily closed to accrual and intervention' },
    { key: 'in review', text: 'In Review', value: 'in review' },
    { key: 'withdrawn', text: 'Withdrawn', value: 'withdrawn' },
]

const PHASE_FILTERS = [
    { key: 'I', text: 'I', value: 'I'},
    { key: 'II', text: 'II', value: 'II'},
    { key: 'II_III', text: 'II_III', value: 'II_III'}, 
    { key: 'III', text: 'III', value: 'III'}
]

const DropdownMenu = (options: Array<{}>, multiple: boolean, onChangeMethod: ((event: React.SyntheticEvent<HTMLElement, Event>, data: DropdownProps) => void) | undefined) => (
    <Dropdown
        placeholder=""
        clearable
        fluid
        multiple= {multiple}
        search
        inline
        selection
        options={options}
        onChange = {onChangeMethod}
    />
    )


const Search = () => {
    const [searchString, setSearchString] = useState("")
    const [trialStatuses, setTrialStatuses] = useState(Array())
    const [sortType, setSortType] = useState('Relevance')
    const [phaseTypes, setPhaseTypes] = useState(Array())

    const onChangeSearchString = (event: { target: { value: React.SetStateAction<string> } }) => {
        setSearchString(event.target.value)
    }

    const onChangeTrialStatus = (event:React.SyntheticEvent<HTMLElement, Event>, data: DropdownProps) => {
        const updatedTrialPref = Array(data.value)
        setTrialStatuses(updatedTrialPref)
    }
    const onChangeSortType = (event:React.SyntheticEvent<HTMLElement, Event>, data: DropdownProps) => {
        const updatedSortPref = String(data.value)
        setSortType(updatedSortPref)
    }
    const onChangePhaseTypes = (event:React.SyntheticEvent<HTMLElement, Event>, data: DropdownProps) => {
        const updatedPhasePref = Array(data.value)
        setPhaseTypes(updatedPhasePref)
    }

    return (
        <>
        <Form style ={{display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', marginTop: '50' }}>
            <Form.Field>
                <label>Keywords</label>
                    <input placeholder='ex. cancer' onChange={onChangeSearchString}/>
            </Form.Field>
            <Form.Field style={{minWidth: '250px'}}>
                <label>Trial Status</label>
                {DropdownMenu(TRIAL_STATUS_FILTERS, true, onChangeTrialStatus)}
            </Form.Field>
            <Form.Field>
                <label>Phase</label>
                {DropdownMenu(PHASE_FILTERS, true, onChangePhaseTypes)}
            </Form.Field>
            <Form.Field style = {{minWidth: '250px'}}>
                <label>Sort Type</label>
                {DropdownMenu(SORT_TYPES, false,  onChangeSortType )} 
            </Form.Field>
            <Form.Field>
                <Button type='submit'>Submit</Button>
            </Form.Field>
        </Form>
    
        </>
    );
}
 

export default Search;
 




