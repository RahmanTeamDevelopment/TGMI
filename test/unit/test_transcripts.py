"""Unit tests for the transcripts module"""

import gzip
import os
import uuid
from unittest import TestCase
from tgmi.transcripts import Transcript, Exon, TranscriptDB, TranscriptDBWriter


class TestTranscript(TestCase):
    """Tests for the Transcript class"""


    def test_read_from_database_record(self):
        record = {'one': 'x', 'two': 'y', 'start': '12345', 'exons': '10000-20000,30000-40000'}
        transcript = Transcript()
        transcript.read_from_database_record(record)

        for key in record:
            assert key in transcript.__dict__

        assert transcript.one == 'x'
        assert transcript.two == 'y'
        assert transcript.start == 12345

        for exon in transcript.exons:
            assert type(exon) == Exon

        assert transcript.exons[0].start == 10000
        assert transcript.exons[1].end == 40000


    def test_set_info(self):
        transcript = Transcript(strand='-', start=10000, end=19600)
        transcript.exons = [Exon('1-2'), Exon('3-4'), Exon('5-6')]
        transcript.cdna_length = 8100
        transcript.prot_length = 1200

        transcript.set_info()
        assert transcript.info == '-/9.6kb/3/8.1kb/1200'


    def test_cds_regions(self):
        transcript = Transcript()
        record = {'strand': '+', 'exons': '10000-20000,30000-40000,50000-60000', 'coding_start': '12000', 'coding_end': '53000' }
        transcript.read_from_database_record(record)

        cds_regions = transcript.cds_regions()
        assert cds_regions[0] == (12000, 20000)
        assert cds_regions[1] == (30000, 40000)
        assert cds_regions[2] == (50000, 53001)

        transcript = Transcript()
        record = {'strand': '-', 'exons': '50-60, 30-40, 10-20', 'coding_start': '55', 'coding_end': '15'}
        transcript.read_from_database_record(record)

        cds_regions = transcript.cds_regions()
        assert cds_regions[0] == (50, 56)
        assert cds_regions[1] == (30, 40)
        assert cds_regions[2] == (15, 20)


    def test_get_cdna_length(self):
        transcript = Transcript()
        record = {'strand': '+', 'exons': '10-20,100-200,1000-2000'}
        transcript.read_from_database_record(record)
        assert transcript.get_cdna_length() == 1110


    def test_get_cds_length(self):
        transcript = Transcript()
        record = {'strand': '+', 'exons': '10-20,30-40,50-60', 'coding_start': '16', 'coding_end': '53'}
        transcript.read_from_database_record(record)
        assert transcript.get_cds_length() == 18

        transcript = Transcript()
        record = {'strand': '-', 'exons': '50-60,30-40,10-20', 'coding_start': '55', 'coding_end': '15'}
        transcript.read_from_database_record(record)
        assert transcript.get_cds_length() == 21


    def test_get_protein_length(self):
        transcript = Transcript()
        record = {'strand': '+', 'exons': '10-20,30-40,50-60', 'coding_start': '16', 'coding_end': '53'}
        transcript.read_from_database_record(record)
        assert transcript.get_protein_length() == 5

        transcript = Transcript()
        record = {'strand': '-', 'exons': '50-60,30-40,10-20', 'coding_start': '55', 'coding_end': '15'}
        transcript.read_from_database_record(record)
        assert transcript.get_protein_length() == 6


    def test_finalize(self):

        transcript = Transcript(strand='+', coding_start=16, coding_end=53)
        transcript.exons = [Exon('10-20'), Exon('30-40'), Exon('50-60')]
        transcript.finalize()
        assert transcript.cdna_length == 30
        assert transcript.prot_length == 5
        assert transcript.start == 10
        assert transcript.end == 60

        transcript = Transcript(strand='-', coding_start=55, coding_end=15)
        transcript.exons = [Exon('50-60'), Exon('30-40'), Exon('10-20')]
        transcript.finalize()
        assert transcript.cdna_length == 30
        assert transcript.prot_length == 6
        assert transcript.start == 10
        assert transcript.end == 60


    def test_any_unset(self):
        transcript = Transcript()
        assert transcript._any_unset(['start','end'])
        transcript.start = 1
        transcript.end = 2
        assert not transcript._any_unset(['start', 'end'])



class TestExon():
    """Tests for the Exon class"""


    def test_get_cds_forward_stranded(self):
        coding_start = 1000
        coding_end = 2000

        assert Exon('300-400').get_cds(coding_start, coding_end) is None
        assert Exon('3000-4000').get_cds(coding_start, coding_end) is None
        assert Exon('1500-1600').get_cds(coding_start, coding_end) == (1500, 1600)
        assert Exon('800-2200').get_cds(coding_start, coding_end) == (1000, 2001)
        assert Exon('700-1500').get_cds(coding_start, coding_end) == (1000, 1500)
        assert Exon('1900-2300').get_cds(coding_start, coding_end) == (1900, 2001)
        assert Exon('1000-2001').get_cds(coding_start, coding_end) == (1000, 2001)
        assert Exon('1000-3000').get_cds(coding_start, coding_end) == (1000, 2001)
        assert Exon('500-2001').get_cds(coding_start, coding_end) == (1000, 2001)


    def test_get_cds_reverse_stranded(self):
        coding_start = 2000
        coding_end = 1000

        assert Exon('300-400').get_cds(coding_start, coding_end) is None
        assert Exon('3000-4000').get_cds(coding_start, coding_end) is None
        assert Exon('1500-1600').get_cds(coding_start, coding_end) == (1500, 1600)
        assert Exon('800-2200').get_cds(coding_start, coding_end) == (1000, 2001)
        assert Exon('700-1500').get_cds(coding_start, coding_end) == (1000, 1500)
        assert Exon('1900-2300').get_cds(coding_start, coding_end) == (1900, 2001)
        assert Exon('1000-2001').get_cds(coding_start, coding_end) == (1000, 2001)
        assert Exon('1000-3000').get_cds(coding_start, coding_end) == (1000, 2001)
        assert Exon('500-2001').get_cds(coding_start, coding_end) == (1000, 2001)



class TestTranscriptDBWriter(TestCase):
    """Tests for the TranscriptDBWriter class"""


    def setUp(self):
        self.fn = str(uuid.uuid4())
        self.tdb_writer = TranscriptDBWriter(self.fn, source='ToolName x.x.x', build='GRCh37', columns=['id', 'chrom', 'exons', 'START', 'end'])


    def tearDown(self):
        if os.path.isfile(self.fn + '.gz'):
            os.remove(self.fn + '.gz')
            os.remove(self.fn + '.gz.tbi')


    def test_init(self):
        assert self.tdb_writer.idx_chrom == 1
        assert self.tdb_writer.idx_start == 3
        assert self.tdb_writer.idx_end == 4

        for k in ['1', '14', '22', 'X', 'MT']:
            assert k in self.tdb_writer._records
        assert len(self.tdb_writer._records['7']) == 0


    def test_add(self):
        transcript = Transcript(id='xyz', chrom='11', strand='+', start=130, end=580)
        transcript.exons = [Exon('100-200'), Exon('300-400'), Exon('500-600')]
        self.tdb_writer.add(transcript)

        assert self.tdb_writer._records['11'][0] == ['xyz', '11', '100-200,300-400,500-600', 130, 580]


    def test_sort_records(self):

        t1 = Transcript(id='1', chrom='8', strand='+', start=130, end=580, exons=[])
        t2 = Transcript(id='2', chrom='8', strand='+', start=800, end=900, exons=[])
        t3 = Transcript(id='3', chrom='8', strand='+', start=800, end=880, exons=[])
        t4 = Transcript(id='4', chrom='8', strand='+', start=30, end=40, exons=[])

        self.tdb_writer.add(t1)
        self.tdb_writer.add(t2)
        self.tdb_writer.add(t3)
        self.tdb_writer.add(t4)

        self.tdb_writer._sort_records()

        assert self.tdb_writer._records['8'][0][-1] == 40
        assert self.tdb_writer._records['8'][1][-1] == 580
        assert self.tdb_writer._records['8'][2][-1] == 880


    def test_index_with_tabix(self):
        out = open('.' + self.tdb_writer._fn + '_tmp', 'w')
        out.write('#header\n')
        self.tdb_writer._index_with_tabix()
        assert os.path.isfile(self.fn + '.gz')
        assert os.path.isfile(self.fn + '.gz.tbi')
        os.remove('.' + self.tdb_writer._fn + '_tmp')


    def test_finalize(self):
        t1 = Transcript(id='1', chrom='8', strand='+', start=130, end=580, exons=[])
        t2 = Transcript(id='2', chrom='8', strand='+', start=800, end=900, exons=[])
        t3 = Transcript(id='3', chrom='8', strand='+', start=800, end=880, exons=[])
        t4 = Transcript(id='4', chrom='8', strand='+', start=30, end=40, exons=[])

        self.tdb_writer.add(t1)
        self.tdb_writer.add(t2)
        self.tdb_writer.add(t3)
        self.tdb_writer.add(t4)

        self.tdb_writer.finalize()

        assert os.path.isfile(self.fn + '.gz')
        assert os.path.isfile(self.fn + '.gz.tbi')

        order = []
        for line in gzip.open(self.fn + '.gz'):
            line = line.strip()
            if line.startswith('#'):
                continue
            cols = line.split('\t')
            order.append(int(cols[-1]))

        assert order == [40, 580, 880, 900]



class TestTranscriptDB(TestCase):
    """Tests for the TranscriptDB class"""


    def setUp(self):
        self.fn = str(uuid.uuid4())
        tdb_writer = TranscriptDBWriter(self.fn, source='xyz', build='GRCh37', columns=['id', 'chrom', 'strand', 'start', 'end'])

        tdb_writer.add(Transcript(id='t1', chrom='8', strand='+', start=130, end=580))
        tdb_writer.add(Transcript(id='t2', chrom='8', strand='+', start=800, end=900))
        tdb_writer.add(Transcript(id='t3', chrom='8', strand='+', start=800, end=880))
        tdb_writer.add(Transcript(id='t4', chrom='8', strand='+', start=30, end=40))
        tdb_writer.finalize()

        self.tdb = TranscriptDB(self.fn + '.gz')


    def tearDown(self):
        os.remove(self.fn + '.gz')
        os.remove(self.fn + '.gz.tbi')


    def test_read(self):
        assert len(self.tdb._data) == 0
        self.tdb.read()
        assert len(self.tdb._data) == 4
        assert self.tdb._data['t4'] == '\t'.join(['t4','8', '+', '30', '40'])


    def test_contains(self):
        self.tdb.read()
        assert self.tdb.contains('t2')
        assert not self.tdb.contains('t7')


    def test_by_id(self):
        self.tdb.read()
        assert self.tdb.by_id('t3').chrom == '8'
        assert self.tdb.by_id('t2').end == 900
        assert self.tdb.by_id('t1').start == 130
        assert self.tdb.by_id('t4').strand == '+'


    def test_search_position(self):
        hits = [t.id for t in self.tdb.search_position('8', 850)]
        hits.sort()
        assert hits == ['t2', 't3']
        assert [t.id for t in self.tdb.search_position('8', 33)] == ['t4']


    def test_generator(self):
        order = [t.id for t in self.tdb.generator()]
        assert order == ['t4', 't1', 't3', 't2']


    def test_read_header(self):
        self.tdb.source = ''
        self.tdb.build = ''
        self.tdb._read_header()
        assert self.tdb.source == 'xyz'
        assert self.tdb.build == 'GRCh37'


    def test_to_dict(self):
        d = self.tdb._to_dict('\t'.join(['t4','8', '+', '30', '40']))
        assert d == {'id': 't4', 'chrom': '8', 'strand': '+', 'start': '30', 'end': '40'}