# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import shutil


from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_bfc.kb_bfcImpl import kb_bfc
from kb_bfc.kb_bfcServer import MethodContext
from kb_bfc.authclient import KBaseAuth as _KBaseAuth
from ReadsUtils.ReadsUtilsClient import ReadsUtils


class kb_bfcTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_bfc'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_bfc',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = kb_bfc(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_bfc_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def getPairedEndLibInfo(self):
        input_reads_file = '/kb/module/test/data/small_test_reads.fastq'
        #input_reads_file = '/kb/module/test/data/12040.half_million.fastq'
        shared_dir = "/kb/module/work/tmp"
        input_file = os.path.join(shared_dir, os.path.basename(input_reads_file))
        shutil.copy(input_reads_file, input_file)

        ru = ReadsUtils(os.environ['SDK_CALLBACK_URL'])

        paired_end_ref = ru.upload_reads({'fwd_file': input_file,
                                            'sequencing_tech': 'artificial reads',
                                            'interleaved': 1, 'wsname': self.getWsName(),
                                            'name': 'test.pe.reads'})['obj_ref']

        new_obj_info = self.wsClient.get_object_info_new({'objects': [{'ref': paired_end_ref}]})
        return new_obj_info[0]


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa

    def test_missing_params(self):
        impl = self.serviceImpl
        ctx = self.ctx
        ws = self.wsName
        # figure out where the test data lives
        pe_lib_info = self.getPairedEndLibInfo()
        pprint(pe_lib_info)

        # Missing input_reads, output_reads, workspacename
        with self.assertRaises(ValueError):
            impl.run_bfc(ctx, {'workspace_name': ws,
                               "output_reads_name": "test_out", "kmer_size": 30,
                                "drop_unique_kmer_reads" : "1", "est_genome_size": 20,
                                "est_genome_size_units": "M" })
        with self.assertRaises(ValueError):
            impl.run_bfc(ctx, {'input_reads_upa': pe_lib_info[7] + '/' + pe_lib_info[1], 'workspace_name': ws,
                                "kmer_size": 30, "drop_unique_kmer_reads": "1",
                                "est_genome_size": 20,
                                "est_genome_size_units": "M"})
        with self.assertRaises(ValueError):
            impl.run_bfc(ctx, {'input_reads_upa': pe_lib_info[7] + '/' + pe_lib_info[1],
                               "output_reads_name": "test_out",
                                "kmer_size": 30, "drop_unique_kmer_reads": "1",
                                "est_genome_size": 20,
                                "est_genome_size_units": "M"})

        with self.assertRaises(ValueError):
            impl.run_bfc(ctx, {'input_reads_upa': pe_lib_info[7] + '/' + pe_lib_info[1], 'workspace_name': ws,
                               "output_reads_name": "test_out",
                                "kmer_size": 30, "drop_unique_kmer_reads": "1",
                                "est_genome_size": 20 })

    def test_invalid_params(self):
        impl = self.serviceImpl
        ctx = self.ctx
        ws = self.wsName
        # figure out where the test data lives
        pe_lib_info = self.getPairedEndLibInfo()
        pprint(pe_lib_info)

        with self.assertRaises(ValueError):
            impl.run_bfc(ctx, {'input_reads_upa': pe_lib_info[7] + '/' + pe_lib_info[1],
                               'workspace_name': ws,
                               "output_reads_name": "test_out", "kmer_size": 30,
                               "drop_unique_kmer_reads": "1", "est_genome_size": 20,
                               "est_genome_size_units": "F"})

        with self.assertRaises(ValueError):
            impl.run_bfc(ctx, {'input_reads_upa': pe_lib_info[7] + '/' + pe_lib_info[1],
                               'workspace_name': ws,
                               "output_reads_name": "test_out", "kmer_size": 64,
                               "drop_unique_kmer_reads": "1", "est_genome_size": 20,
                               "est_genome_size_units": "M"})


    def test_bfc(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

        # figure out where the test data lives
        pe_lib_info = self.getPairedEndLibInfo()
        pprint(pe_lib_info)


        params = {'input_reads_upa': pe_lib_info[7] + '/' + pe_lib_info[1],
                  'workspace_name': self.getWsName(),
                  'output_reads_name':'test_out', 'kmer_size':33,
                  'drop_unique_kmer_reads': '1',
                  'est_genome_size':20, 'est_genome_size_units':'M' }

        self.getImpl().run_bfc(self.getContext(), params)
        pass
