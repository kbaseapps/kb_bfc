# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import subprocess
from pprint import pprint
#END_HEADER


class kb_bfc:
    '''
    Module Name:
    kb_bfc

    Module Description:
    A KBase module: kb_bfc
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/psdehal/kb_bfc.git"
    GIT_COMMIT_HASH = "99aa29cad215a86450da6d03d9b62d15a95d484c"

    #BEGIN_CLASS_HEADER
    BFC = '/kb/module/kb_bfc/bfc/bfc'
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR

        self.scratch = os.path.abspath(config['scratch'])
        self.callbackURL = os.environ['SDK_CALLBACK_URL']

        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)

        #END_CONSTRUCTOR
        pass


    def run_bfc(self, ctx, params):
        """
        :param params: instance of type "BFCParams" -> structure: parameter
           "input_reads_upa" of type "reads_upa" (Insert your typespec
           information here.), parameter "workspace_name" of String,
           parameter "output_reads_name" of String
        :returns: instance of type "BFCResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: results
        #BEGIN run_bfc
        
        print('Running run_bfc with params=')
        pprint(params)
        bfc_cmd = [self.BFC]

        #hardcoding a couple parameters
        bfc_cmd.append('-t')
        bfc_cmd.append('8')

        bfc_cmd.append('/kb/module/kb_bfc/test/data/small_test_reads.fastq.gz')

        bfc_cmd.append('>')
        bfc_cmd.append('output_reads.fastq')

        print('Running BFC:')
        print('     ' + ' '.join(bfc_cmd))

        p=subprocess.Popen(" ".join(bfc_cmd), cwd=self.scratch, shell=True)
        retcode = p.wait()

        print('Return code: ' + str(retcode))

        results = {'report_name': None, 'report_ref': None}

        #END run_bfc

        # At some point might do deeper type checking...
        if not isinstance(results, dict):
            raise ValueError('Method run_bfc return value ' +
                             'results is not type dict as required.')
        # return the results
        return [results]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
