# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import subprocess
import shutil
import uuid
import time

from pprint import pprint
from ReadsUtils.ReadsUtilsClient import ReadsUtils as _ReadsUtils
from KBaseReport.KBaseReportClient import KBaseReport as _KBaseReport
from Workspace.WorkspaceClient import Workspace as _Workspace

def log(message, prefix_newline=False):
    """
    Logging function, provides a hook to suppress or redirect log messages.
    """
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))

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
    GIT_URL = "https://github.com/kbaseapps/kb_bfc"
    GIT_COMMIT_HASH = "4116d523524eea68bcc5bf9e0aae301a6dd624b7"

    #BEGIN_CLASS_HEADER
    BFC = '/kb/module/bfc/bfc'
    SEQTK = '/kb/module/seqtk/seqtk'

    THREADS = 8

    def run_command(self, command):
        """
        _run_command: run command and print result
        """

        log('Start executing command:\n{}'.format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        output = pipe.communicate()[0]
        exitCode = pipe.returncode

        if (exitCode == 0):
            log('Executed command:\n{}\n'.format(command) +
                'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
        else:
            error_msg = 'Error running command:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)
            raise ValueError(error_msg)
        return output

    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR

        self.scratch = os.path.abspath(config['scratch'])
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.ws_url = config['workspace-url']
        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)

        #END_CONSTRUCTOR
        pass


    def run_bfc(self, ctx, params):
        """
        BFC (Bloom Filter) error correcting app for sequencing errors in llluminia short reads.
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportBFCResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: results
        #BEGIN run_bfc

        log('Running run_bfc with params=')
        pprint(params)
        bfc_cmd = [self.BFC]
        shared_dir = "/kb/module/work/tmp"

        # validate parameters
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'input_reads_upa' not in params:
            raise ValueError('input_reads_upa parameter is required')
        if 'output_reads_name' not in params:
            raise ValueError('output_reads_name parameter is required')

        if 'drop_unique_kmer_reads' in params:
            if params['drop_unique_kmer_reads']:
                bfc_cmd.append(str('-1'))

        if 'est_genome_size' in params:
            if params['est_genome_size']:
                if 'est_genome_size_units' in params:
                    if params['est_genome_size_units'] in ["G", "M", "K", "g", "m", "k"]:
                        bfc_cmd.append('-s')
                        bfc_cmd.append(str(params['est_genome_size']) +
                                       str(params['est_genome_size_units']))
                    else:
                        raise ValueError('est_genome_size_units must be G, M or K')
                else:
                    raise ValueError('est_genome_size_units must be set')

        if 'kmer_size' in params:
            if params['kmer_size']:
                if params['kmer_size'] < 64:
                    bfc_cmd.append('-k')
                    bfc_cmd.append(str(params['kmer_size']))
                else:
                    raise ValueError('kmer_size must be <= 63')

        input_reads_upa = params['input_reads_upa']
        output_reads_name = params['output_reads_name']
        os.chdir(shared_dir)

        output_reads_file = output_reads_name + ".fq"
        bfc_output_file = "bfc_" + output_reads_name + ".fq"
        seqtk_output_file = "seqtk_bfc_" + output_reads_name + ".fq"
        workspace_name = params['workspace_name']

        # get the reads library as gzipped interleaved file
        reads_params = {'read_libraries': [input_reads_upa], 'interleaved': 'true',
                        'gzipped': 'true'}

        ru = _ReadsUtils(self.callbackURL)
        reads = ru.download_reads(reads_params)['files']
        log(reads)
        input_reads_file = os.path.basename(reads[input_reads_upa]['files']['fwd'])
        log('Input reads files:')
        log('     ' + input_reads_file)

        # hardcoding a couple parameters
        bfc_cmd.append('-t')
        bfc_cmd.append(str(self.THREADS))

        bfc_cmd.append(input_reads_file)

        bfc_cmd.append('>')
        bfc_cmd.append(bfc_output_file)

        log('Running BFC:')
        log('     ' + ' '.join(bfc_cmd))

        bfc_cmd_output = self.run_command(' '.join(bfc_cmd))

        # drop non-paired reads using seqtk

        seqtk_cmd = [self.SEQTK, "dropse", bfc_output_file, ">", seqtk_output_file]
        self.run_command(' '.join(seqtk_cmd))

        # upload reads output
        shutil.copy(seqtk_output_file, output_reads_file)

        out_reads_upa = ru.upload_reads({'fwd_file': os.path.join(shared_dir, output_reads_file),
                                         'interleaved': 1, 'wsname': workspace_name,
                                         'name': output_reads_name,
                                         'source_reads_ref': input_reads_upa})
        # create report
        ws = _Workspace(self.ws_url)

        input_meta = ws.get_objects2({'objects': [
                                      {'ref': input_reads_upa}], 'no_data': 1})['data'][0]
        input_reads_name = input_meta['info'][1]
        input_reads_count = input_meta['info'][10]['read_count']

        output_meta = ws.get_objects2({'objects': [
                                      {'ref': out_reads_upa['obj_ref']}], 'no_data': 1})['data'][0]
        output_reads_count = output_meta['info'][10]['read_count']

        # get total filtered reads
        filtered_reads = int(input_reads_count) - int(output_reads_count)
        filtered_reads = str(filtered_reads)
        k_mer_size = str(params['kmer_size'])

        bfc_main = '\n'.join([l for l in bfc_cmd_output.split('\n') if l.startswith('[M::main')])

        report = 'Successfully ran bfc, on input reads: {}\n'.format(input_reads_name)
        report += 'with command: {}\n\n{}\n'.format(' '.join(bfc_cmd), bfc_main)
        report += 'created object: {}({})\n\n'.format(output_reads_name, out_reads_upa['obj_ref'])
        report += 'input reads: {}\n k-mer size: {}\n filtered reads: {}\n output reads: {}'.format(input_reads_count, k_mer_size, filtered_reads, output_reads_count )

        log('Saving report')
        kbr = _KBaseReport(self.callbackURL)
        report_info = kbr.create_extended_report({
            'message': report,
            'objects_created': [{'ref': out_reads_upa['obj_ref'],
                                 'description': 'Corrected reads'}],
            'workspace_name': workspace_name,
            'report_object_name': 'bfc_report_' + str(uuid.uuid4())
            })

        results = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

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
