import tgmi.bed
import tgmi.interval
import unittest


class TestBEDParser(unittest.TestCase):
    def test_raises_standard_error_if_line_in_file_has_less_than_three_columns(self):
        parser = tgmi.bed.BedFileParser(iter([
            "chr1\t100\n"
        ]))

        self.assertRaises(
            StandardError,
            parser.next
        )

    def test_returns_genomic_interval_from_well_formatted_line(self):
        parser = tgmi.bed.BedFileParser(iter([
            "chr1\t100\t200\tREGION_1\n",
            "chr1\t300\t400\tREGION_2\n",
        ]))

        assert parser.next() == tgmi.interval.GenomicInterval(
            "chr1",
            100,
            200,
            "REGION_1"
        )

        assert parser.next() == tgmi.interval.GenomicInterval(
            "chr1",
            300,
            400,
            "REGION_2"
        )

    def test_iterating_over_parser_gives_instances_of_genomic_interval_class(self):
        parser = tgmi.bed.BedFileParser(iter([
            "chr1\t100\t200\tREGION_1\n"
        ]))

        for interval in parser:
            self.assertIsInstance(interval, tgmi.interval.GenomicInterval)


if __name__ == "__main__":
    unittest.main()
