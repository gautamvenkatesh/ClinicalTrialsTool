/**
 * Display new clinical trials
 */
import { Table, Loader } from 'semantic-ui-react'
import {Trial} from "../typings/Trial";
import TrialRow from "../components/TrialRow";
import React, { useState, useEffect } from 'react';



const NewTrials: React.FC = () => {

  const [trials, setTrials] = useState<Trial[]>([])

  // Similar to componentDidMount and componentDidUpdate:

  useEffect(() => {
    // this.state.trials = fetch("https://1apsty3a4h.execute-api.us-east-1.amazonaws.com/staging/trials");
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
      <Table>
          {Object.keys(trials[0]).map((header) => (<Table.HeaderCell>{header}</Table.HeaderCell>))}
          {trials.map((t : Trial) => (<TrialRow trials = {t}/>))}
      </Table>
  );
}

export default NewTrials;
