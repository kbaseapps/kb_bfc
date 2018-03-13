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
    GIT_URL = "https://github.com/psdehal/kb_bfc"
    GIT_COMMIT_HASH = "3f4234b860c40755dc6be1000939cadb546cc96f"

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
        :param params: instance of type "BFCParams". Initial version has no
        user parameters other than input reads and output reads name. 

        """

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

        p=subprocess.Popen(bfc_cmd, cwd=self.scratch, shell=False)
        retcode = p.wait()

        print('Return code: ' + str(retcode))

        output = {'report_name': None, 'report_ref': None}
        
        return [output]






    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
