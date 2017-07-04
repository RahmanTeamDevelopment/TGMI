import copy
import tgmi.interval
import unittest


class TestUniquifyRegionNames(unittest.TestCase):
    def test_returns_empty_list_when_given_empty_list(self):
        assert tgmi.interval.uniquify_region_names([]) == []

    def test_returns_list_of_one_interval_when_given_list_of_one_interval(self):
        interval = tgmi.interval.GenomicInterval("1", 100, 200, "REGION")
        assert tgmi.interval.uniquify_region_names([interval]) == [interval]

    def test_returns_identical_copy_of_inputs_when_inputs_have_different_names(self):
        interval_1 = tgmi.interval.GenomicInterval("1", 100, 200, "REGION")
        interval_2 = tgmi.interval.GenomicInterval("1", 500, 600, "OTHER_REGION")
        inputs = [interval_1, interval_2]
        assert tgmi.interval.uniquify_region_names(inputs) == inputs

    def test_returns_copy_with_unique_names_if_identical_names_in_input(self):
        interval_1 = tgmi.interval.GenomicInterval("1", 100, 200, "REGION")
        interval_2 = tgmi.interval.GenomicInterval("1", 500, 600, "REGION")
        inputs = [interval_1, interval_2]

        expected_outputs = [
            tgmi.interval.GenomicInterval("1", 100, 200, "REGION_1"),
            tgmi.interval.GenomicInterval("1", 500, 600, "REGION_2"),
        ]

        assert tgmi.interval.uniquify_region_names(inputs) == expected_outputs

    def test_returns_sorted_copy_with_unique_names_if_identical_names_in_input_and_inputs_unsorted(self):
        interval_1 = tgmi.interval.GenomicInterval("1", 500, 600, "REGION")
        interval_2 = tgmi.interval.GenomicInterval("1", 100, 200, "REGION")
        inputs = [interval_1, interval_2]

        expected_outputs = [
            tgmi.interval.GenomicInterval("1", 100, 200, "REGION_1"),
            tgmi.interval.GenomicInterval("1", 500, 600, "REGION_2"),
        ]

        assert tgmi.interval.uniquify_region_names(inputs) == expected_outputs


class TestGenpmicInterval(unittest.TestCase):
    def test_raises_assertion_if_constructed_with_negative_position(self):
        self.assertRaises(
            AssertionError,
            tgmi.interval.GenomicInterval,
            chromosome="1",
            start_pos=-1,
            end_pos=100,
            name=None
        )

        self.assertRaises(
            AssertionError,
            tgmi.interval.GenomicInterval,
            chromosome="1",
            start_pos=100,
            end_pos=-1,
            name=None
        )

    def test_interval_size_is_end_minus_start(self):
        interval_1 = tgmi.interval.GenomicInterval(None, 100, 200)
        interval_2 = tgmi.interval.GenomicInterval(None, 0, 0)
        assert interval_1.size() == 100
        assert interval_2.size() == 0

    def test_intervals_compare_equal_if_chromosomes_and_coordinates_are_identical(self):
        interval_1 = tgmi.interval.GenomicInterval("1", 0, 100)
        interval_2 = tgmi.interval.GenomicInterval("1", 0, 100)
        assert interval_1 == interval_2

    def test_intervals_do_not_compare_equal_if_chromosomes_are_different(self):
        interval_1 = tgmi.interval.GenomicInterval("1", 0, 100)
        interval_2 = tgmi.interval.GenomicInterval("2", 0, 100)
        assert interval_1 != interval_2

    def test_intervals_do_not_compare_equal_if_start_positions_are_different(self):
        interval_1 = tgmi.interval.GenomicInterval("1", 0, 100)
        interval_2 = tgmi.interval.GenomicInterval("1", 10, 100)
        assert interval_1 != interval_2

    def test_intervals_do_not_compare_equal_if_end_positions_are_different(self):
        interval_1 = tgmi.interval.GenomicInterval("1", 0, 100)
        interval_2 = tgmi.interval.GenomicInterval("1", 0, 150)
        assert interval_1 != interval_2

    def test_overlap_of_identical_intervals_is_same_interval_again(self):
        interval_1 = tgmi.interval.GenomicInterval("1", 0, 100)
        interval_2 = copy.deepcopy(interval_1)
        assert interval_1.overlap(interval_2) == interval_1

    def test_overlap_of_intervals_on_different_chromosomes_is_zero(self):
        interval_1 = tgmi.interval.GenomicInterval("1", 0, 100)
        interval_2 = tgmi.interval.GenomicInterval("2", 0, 100)
        assert interval_1.overlap(interval_2).size() == 0

    def test_overlap_of_non_overlapping_intervals_on_same_chromosome_is_zero(self):
        interval_1 = tgmi.interval.GenomicInterval("1", 0, 100)

        interval_2 = tgmi.interval.GenomicInterval(
            interval_1.chromosome,
            interval_1.end_pos + 1,
            interval_1.end_pos + 2
        )

        assert interval_1.overlap(interval_2).size() == 0

    def test_overlap_of_small_interval_entirely_contained_in_larger_interval_is_small_interval(self):
        small_interval = tgmi.interval.GenomicInterval("1", 100, 200)

        larger_interval = tgmi.interval.GenomicInterval(
            small_interval.chromosome,
            small_interval.start_pos - 100,
            small_interval.end_pos + 100
        )

        assert small_interval.overlap(larger_interval) == small_interval


class TestGetClustersOfRegionsFromBEDFile(unittest.TestCase):
    def test_raises_exception_if_there_are_no_regions(self):

        # Generator functiond won't raise an exception until we start iterating
        # through the results
        clusters = tgmi.interval.cluster_genomic_intervals(
            []
        )

        self.assertRaises(
            StandardError,
            clusters.next
        )


if __name__ == "__main__":
    unittest.main()