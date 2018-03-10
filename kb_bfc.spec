/*
A KBase module: kb_bfc
*/

module kb_bfc {
    /*
        Insert your typespec information here.
    */

    typedef string reads_upa;

    typedef structure {
    	reads_upa input_reads_upa;
    	string workspace_name;
    	string output_reads_name;
    } BFCParams;

    typedef structure {
    	string report_name;
    	string report_ref;
    } BFCResults;

    funcdef run_bfc (BFCParams params)
    	returns (BFCResults results) authentication required;
};
