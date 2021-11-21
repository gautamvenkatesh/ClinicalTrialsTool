/**
 * Display trial table row
 */
import { Table } from 'semantic-ui-react'
import { Trial } from '../typings/Trial';

interface TrialRowProps {
    trials: Trial;
}

 const TrialRow: React.FC<TrialRowProps> = ({trials}) => {
    return (
        <Table.Row>
            {Object.keys(trials).map((value) => {
                <Table.Cell>
                    value
                </Table.Cell>
            })}
        </Table.Row>
    );
}

export default TrialRow;