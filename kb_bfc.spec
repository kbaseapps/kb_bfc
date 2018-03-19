/*
A KBase module: kb_bfc
*/

module kb_bfc {
    /*
        Insert your typespec information here.
    */

    /* A boolean. 0 = false, anything else = true. */
    typedef int bool;

    /* unique permanent address of reads object */
    typedef string reads_upa;

    typedef structure {
    	reads_upa input_reads_upa;
    	string workspace_name;
    	string output_reads_name;
      int kmer_size;
      bool drop_unique_kmer_reads;
      int est_genome_size;
      string est_genome_size_units;
    } BFCParams;

    typedef structure {
    	string report_name;
    	string report_ref;
    } BFCResults;

    funcdef run_bfc (BFCParams params)
    	returns (BFCResults results) authentication required;
};
