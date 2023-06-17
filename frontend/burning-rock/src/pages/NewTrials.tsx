/**
 * Display new clinical trials
 */
import { Table, Loader, Card } from 'semantic-ui-react'
import {Trial} from "../typings/Trial";
import TrialRow from "../components/TrialRow";
import React, { useState, useEffect } from 'react';

const HEADERS = [
  'Date',
  'NCI ID',
  'Title',
  'Lead Org',
  'Status',
  'Start Date',
  'Completion Date',
  'Summary',
  'Phase',
  'URL',
  'Sites',
  'Genes',
  'Flagged words'
]

const NewTrials: React.FC = () => {

  const [trials, setTrials] = useState<Trial[]>([])

  useEffect(() => {
    async function response(){
        const r = await fetch("https://1apsty3a4h.execute-api.us-east-1.amazonaws.com/staging/trials")
        const data = await r.json()
        setTrials(data);
    };

    response();
  },
  []
);

  if (trials.length === 0) {
    return (
      <Loader/>
    );
  }

  return (
      <Table celled={true}>
        <Table.Header>
          <Table.Row>
            {HEADERS.map((header) => (<Table.HeaderCell>{header}</Table.HeaderCell>))}
          </Table.Row>
        </Table.Header>
        {trials.map((t : Trial) => (<TrialRow trials = {t}/>))}
      </Table>
  );
}

export default NewTrials;
