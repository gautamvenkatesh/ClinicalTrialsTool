/**
 * Display trial table row
 */
import { Table } from 'semantic-ui-react'
import { Trial } from '../typings/Trial';

interface TrialRowProps {
    trials: Trial;
}

const LENGTH = 100;

 const TrialRow: React.FC<TrialRowProps> = ({trials}) => {
   //console.log(trials)
    return (
        <Table.Row> 
            <Table.Cell>{trials.record_verification_date}</Table.Cell>
            <Table.Cell>{trials.nci_id}</Table.Cell>
            <Table.Cell>{trials.official_title}</Table.Cell>
            <Table.Cell>{trials.lead_org}</Table.Cell>
            <Table.Cell>{trials.current_trial_status}</Table.Cell>
            <Table.Cell>{trials.start_date}</Table.Cell>
            <Table.Cell>{trials.completion_date}</Table.Cell>
            <Table.Cell>{trials.brief_summary.substring(0, LENGTH) + '...'}</Table.Cell>
            <Table.Cell>{trials.phase}</Table.Cell>
            <Table.Cell><a href={'https://clinicaltrials.gov/ct2/show/' + trials.nct_id}>{trials.nct_id}</a></Table.Cell>
            <Table.Cell>{trials.sites.join(', ')}</Table.Cell>
            <Table.Cell>{trials.found_genes.join(', ')}</Table.Cell>
            <Table.Cell>{trials.found_strings.join(', ')}</Table.Cell>
        </Table.Row>
    );
}

export default TrialRow;
