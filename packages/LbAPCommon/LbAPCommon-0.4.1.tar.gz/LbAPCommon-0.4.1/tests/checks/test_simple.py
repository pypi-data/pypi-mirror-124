###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import re
from pathlib import Path

import pytest

from LbAPCommon import checks

pytest.importorskip("XRootD")


def test_num_entries_passing():
    result = checks.num_entries(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        1000,
        "DecayTree",
    )
    assert result.passed
    assert result.messages == ["Found 5135823 in DecayTree"]
    assert result.histograms == []


def test_num_entries_failing():
    result = checks.num_entries(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        1000000000,
        "DecayTree",
    )
    assert not result.passed
    assert result.messages == ["Found 5135823 in DecayTree"]
    assert result.histograms == []


def test_num_entries_failing_tree_name():
    result = checks.num_entries(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        1000000000,
        "RandomName",
    )
    assert not result.passed
    assert result.messages == ["No TTree objects found that match RandomName"]
    assert result.histograms == []


def test_num_entries_per_invpb_passing():
    file_name = Path(__file__).parent.absolute() / "example_tuple_with_lumi.root"
    result = checks.num_entries_per_invpb(file_name, 10000, "DecayTree", "LumiTuple")
    assert result.passed
    assert result.messages == [
        "Found 23026.2 entries per unit luminosity (pb-1) in DecayTree"
    ]
    assert result.histograms == []


def test_num_entries_per_invpb_failing():
    file_name = Path(__file__).parent.absolute() / "example_tuple_with_lumi.root"
    result = checks.num_entries_per_invpb(file_name, 100000, "DecayTree", "LumiTuple")
    assert not result.passed
    assert result.messages == [
        "Found 23026.2 entries per unit luminosity (pb-1) in DecayTree"
    ]
    assert result.histograms == []


def test_num_entries_per_invpb_failing_MC():
    result = checks.num_entries_per_invpb(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        10000,
        "DecayTree",
    )
    assert not result.passed
    assert result.messages == ["Failed to get luminosity information"]
    assert result.histograms == []


def test_num_entries_per_invpb_failing_MC_nameTTree():
    result = checks.num_entries_per_invpb(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        10000,
        "RandomName",
    )
    assert not result.passed
    assert result.messages == [
        "Failed to get luminosity information",
        "No TTree objects found that match RandomName",
    ]
    assert result.histograms == []


def test_range_check_passing():
    result = checks.range_check(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        "H1_PZ",
        {"min": 0.0, "max": 500000.0},
        [],
        "DecayTree",
    )
    assert result.passed
    assert result.messages == ["Found at least one event in range in Tree DecayTree "]
    assert result.tree_names == ["DecayTree"]
    assert not result.histograms == []


def test_range_check_failing_range():
    result = checks.range_check(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        "H1_PZ",
        {"min": -100000.0, "max": -99999.0},
        [],
        "DecayTree",
    )
    assert not result.passed
    assert result.messages == ["No events found in range for Tree DecayTree"]
    assert result.tree_names == ["DecayTree"]
    assert result.histograms == []


def test_range_check_failing_missing_branch():
    result = checks.range_check(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        "Dst_M",
        {"min": 1800.0, "max": 2300.0},
        [],
        "DecayTree",
    )
    message = result.messages[0]
    pattern = r"Missing branch in "
    matched = False
    if re.match(pattern, message):
        matched = True
    assert not result.passed
    assert matched
    assert result.tree_names == ["DecayTree"]
    assert result.histograms == []


def test_range_check_failing_tree_name():
    result = checks.range_check(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        "H1_PZ",
        {"min": 0.0, "max": 500000.0},
        [],
        "RandomName",
    )
    assert not result.passed
    assert result.messages == ["No TTree objects found that match RandomName"]
    assert result.tree_names == []
    assert result.histograms == []


def test_range_check_nd_passing():
    result = checks.range_check_nd(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        {"x": "H1_PZ", "y": "H2_PZ"},
        {"x": {"min": 0.0, "max": 500000.0}, "y": {"min": 0.0, "max": 500000.0}},
        {"x": [], "y": []},
        "DecayTree",
    )
    assert result.passed
    assert result.messages == ["Found at least one event in range in Tree DecayTree "]
    assert result.tree_names == ["DecayTree"]
    assert not result.histograms == []


def test_range_check_nd_failing_num_var():
    result = checks.range_check_nd(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        {"x": "H1_PZ"},
        {"x": {"min": 0.0, "max": 500000.0}},
        {"x": [], "y": []},
        "DecayTree",
    )
    assert not result.passed
    assert result.messages == [
        "Expected at least two variables, but not more than four."
    ]
    assert result.tree_names == []
    assert result.histograms == []


def test_range_check_nd_failing_missing_limit():
    result = checks.range_check_nd(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        {"x": "H1_PZ", "y": "H2_PZ"},
        {"x": {"min": 0.0, "max": 500000.0}},
        {"x": [], "y": []},
        "DeacyTree",
    )
    assert not result.passed
    assert result.messages == [
        "For each variable, a corresponding range should be defined."
    ]
    assert result.tree_names == []
    assert result.histograms == []


def test_range_check_nd_failing_missing_branch():
    result = checks.range_check_nd(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        {"x": "H1_PZ", "y": "Dst_M-D0_M"},
        {"x": {"min": 0.0, "max": 500000.0}, "y": {"min": 138.0, "max": 150.0}},
        {"x": [], "y": []},
        "DecayTree",
    )
    message = result.messages[0]
    pattern = r"Missing branch in "
    matched = False
    if re.match(pattern, message):
        matched = True
    assert not result.passed
    assert matched
    assert result.tree_names == ["DecayTree"]
    assert result.histograms == []


def test_range_check_nd_failing_range():
    result = checks.range_check_nd(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        {"x": "H1_PZ", "y": "H2_PZ"},
        {
            "x": {"min": -1000000.0, "max": -999999.0},
            "y": {"min": -1000000.0, "max": -999999.0},
        },
        {"x": [], "y": []},
        "DecayTree",
    )
    assert not result.passed
    assert result.messages == [
        "No events found in range for Tree DecayTree and variables H1_PZ, H2_PZ "
    ]
    assert result.tree_names == ["DecayTree"]
    assert result.histograms == []


def test_range_check_nd_failing_tree_name():
    result = checks.range_check_nd(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        {"x": "H1_PZ", "y": "H2_PZ"},
        {"x": {"min": 0.0, "max": 1.0}, "y": {"min": 0.0, "max": 1.0}},
        {"x": [], "y": []},
        "RandomName",
    )
    assert not result.passed
    assert result.messages == ["No TTree objects found that match RandomName"]
    assert result.tree_names == []
    assert result.histograms == []


def test_range_check_bkg_subtracted_passing():
    result = checks.range_check_bkg_subtracted(
        "root://eospublic.cern.ch//eos/opendata/lhcb/MasterclassDatasets/D0lifetime/2014/MasterclassData.root",
        "D0_PT",
        {"min": 0.0, "max": 500000.0},
        "D0_MM",
        1865.0,
        30.0,
        10.0,
        20.0,
        [],
        "DecayTree",
    )
    assert result.passed
    assert result.messages[0] == "Found at least one event in range in Tree DecayTree "
    assert result.tree_names[0] == "DecayTree"
    assert not result.histograms == []


def test_range_check_bkg_subtracted_failing_range():
    result = checks.range_check_bkg_subtracted(
        "root://eospublic.cern.ch//eos/opendata/lhcb/MasterclassDatasets/D0lifetime/2014/MasterclassData.root",
        "D0_PT",
        {"min": -1000000.0, "max": -99999.0},
        "D0_MM",
        1865.0,
        30.0,
        10.0,
        20.0,
        [],
        "DecayTree",
    )
    assert not result.passed
    assert (
        result.messages[0]
        == "Not enough events for background subtraction found in range for Tree DecayTree"
    )
    assert result.tree_names[0] == "DecayTree"


def test_range_check_bkg_subtracted_failing_missing_branch():
    result = checks.range_check_bkg_subtracted(
        "root://eospublic.cern.ch//eos/opendata/lhcb/MasterclassDatasets/D0lifetime/2014/MasterclassData.root",
        "D0_PT",
        {"min": -1000000.0, "max": -99999.0},
        "Dst_M",
        1865.0,
        30.0,
        10.0,
        20.0,
        [],
        "DecayTree",
    )
    message = result.messages[0]
    print(message)
    pattern = r"Missing branch in "
    matched = False
    if re.match(pattern, message):
        matched = True
    assert not result.passed
    assert matched
    assert result.tree_names[0] == "DecayTree"
    assert result.histograms == []


def test_range_check_bkg_subtracted_failing_tree_name():
    result = checks.range_check_bkg_subtracted(
        "root://eospublic.cern.ch//eos/opendata/lhcb/MasterclassDatasets/D0lifetime/2014/MasterclassData.root",
        "D0_PT",
        {"min": -1000000.0, "max": -99999.0},
        "D0_MM",
        1865.0,
        30.0,
        10.0,
        20.0,
        [],
        "RandomName",
    )
    assert not result.passed
    assert result.messages == ["No TTree objects found that match RandomName"]
    assert result.tree_names == []
    assert result.histograms == []
