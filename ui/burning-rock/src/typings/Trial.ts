/**
 * Define interface for trial in DB
 */

export interface Trial {
    record_verification_date: string;
    nci_id: number;
    official_title: string;
    lead_org: string;
    current_trial_status: string;
    start_date: string;
    completion_date: string;
    brief_summary: string;
    detail_description: string;
    primary_purpose: string;
    phase: string;
    nct_id: string;
    eligibility: object;
    sites: string[];
    found_genes: string[];
    found_strings: string[];
}

