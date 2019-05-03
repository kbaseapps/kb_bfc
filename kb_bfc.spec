/*
A KBase module: kb_bfc
*/

   module kb_bfc {
       typedef structure {
    	string report_name;
    	string report_ref;
    } ReportBFCResults;

    /*
    BFC (Bloom Filter) error correcting app for sequencing errors in llluminia short reads.
    */
    funcdef run_bfc(mapping<string,UnspecifiedObject>  params)
    	returns (ReportBFCResults results) authentication required;
};
