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
from dataclasses import dataclass, field
from itertools import combinations
from typing import List

import hist
import numpy
import uproot
from hist import Hist


@dataclass
class CheckResult:
    """Class for representing the return result of ntuple checks"""

    passed: bool
    messages: List[str] = field(default_factory=list)
    histograms: List[Hist] = field(default_factory=list)
    tree_names: List[str] = field(default_factory=list)
    count_events: List[float] = field(default_factory=list)


def num_entries(
    filepath,
    count,
    tree_pattern=r"(.*/DecayTree)|(.*/MCDecayTree)",
):
    """Check that all matching TTree objects contain a minimum number of entries.

    :param filepath: Path to a file to analyse
    :param count: The minimum number of entries required
    :param tree_pattern: A regular expression for the TTree objects to check
    :returns: A CheckResult object
    """
    result = CheckResult(False)
    with uproot.open(filepath) as f:
        for key, obj in f.items(cycle=False):
            if not isinstance(obj, uproot.TTree):
                continue
            if re.fullmatch(tree_pattern, key):
                num_entries = obj.num_entries
                result.passed |= num_entries >= count
                result.messages += [f"Found {num_entries} in {key}"]
                result.tree_names += [f"{key}"]
    # If no matches were found the check should be marked as failed
    if len(result.messages) == 0:
        result.passed = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
    return result


def range_check(
    filepath,
    expression,
    limits,
    blind_ranges,
    tree_pattern=r"(.*/DecayTree)|(.*/MCDecayTree)",
    exp_mean=0.0,
    exp_std=0.0,
    mean_tolerance=0.0,
    std_tolerance=0.0,
):
    """Check if there is at least one entry in the TTree object with a specific
    variable falling in a pre-defined range. The histogram is then produced as output.
    If the expected mean and standard deviation values are given in input, they are compared with the observed ones
    and their agreement within the provided *_tolerance is checked. If the check is passed, the fraction of events falling in the
    exp_mean +- exp_std region is given in output.
    It is possible to blind some regions.

    :param filepath: Path to a file to analyse
    :param expression: Name of the variable (or expression depending on varibales in the TTree) to be checked
    :param limits: Pre-defined range
    :param blind_ranges: regions to be blinded in the histogram
    :param exp_mean: Expected mean value (optional)
    :param exp_std: Expected standard deviation (optional)
    :param mean_tolerance: Maximum shift tolerated between expected and observed mean values (optional)
    :param std_tolerance: Maximum shift tolerated between expected and observed values of standard deviation (optional)
    :param tree_pattern: A regular expression for the TTree object to check
    :returns: A CheckResult object
    """
    result = CheckResult(False)
    with uproot.open(filepath) as f:
        for key, obj in f.items(cycle=False):
            if not isinstance(obj, uproot.TTree):
                continue
            if not re.fullmatch(tree_pattern, key):
                continue

            values_obj = {}
            # Check if the branch is in the Tree or if the expression is correctly written
            try:
                values_obj = obj.arrays(expression, library="np")
            except uproot.exceptions.KeyInFileError as e:
                result.messages += [f"Missing branch in {key!r} with {e!r}"]
                result.passed |= False
                result.tree_names += [f"{key}"]
                continue
            except Exception as e:
                result.messages += [
                    f"Failed to apply {expression!r} to {key!r} with error: {e!r}"
                ]
                result.passed |= False
                result.tree_names += [f"{key}"]
                continue
            test_array = values_obj[expression]
            test_array = test_array[
                numpy.where((test_array < limits["max"]) & (test_array > limits["min"]))
            ]
            if isinstance(blind_ranges, dict):
                blind_ranges = [blind_ranges]
                # Take into account that there could be multiple regions to blind
            for blind_range in blind_ranges:
                lower, upper = blind_range["min"], blind_range["max"]
                test_array = test_array[~((lower < test_array) & (test_array < upper))]
            if len(test_array) == 0:
                result.passed |= False
                result.messages += [f"No events found in range for Tree {key}"]
                result.tree_names += [f"{key}"]
                continue
            result.messages += [f"Found at least one event in range in Tree {key} "]
            result.tree_names += [f"{key}"]
            axis0 = hist.axis.Regular(50, limits["min"], limits["max"], name=expression)
            h = Hist(axis0)
            h.fill(test_array)
            result.histograms += [h]
            if (
                (exp_mean == 0.0)
                & (exp_std == 0.0)
                & (mean_tolerance == 0.0)
                & (std_tolerance == 0.0)
            ):
                result.passed |= True
            else:
                delta_mean = abs(test_array.mean() - exp_mean)
                delta_std = abs(test_array.std() - exp_std)
                if (delta_mean > mean_tolerance) & ~(
                    (exp_mean == 0.0) & (mean_tolerance == 0.0)
                ):
                    result.passed |= False
                    result.messages += [
                        f"The observed mean differs from the expected value by {delta_mean}"
                    ]
                elif (delta_std > std_tolerance) & ~(
                    (exp_std == 0.0) & (std_tolerance == 0.0)
                ):
                    result.passed |= False
                    result.messages += [
                        f"The observed standard deviation differs from the expected value by {delta_std}"
                    ]
                else:
                    result.passed |= True
                    # Return also the fraction of events falling in the exp_mean +- exp_std region
                    events_in_exp_region = test_array[
                        (exp_mean - exp_std < test_array)
                        & (test_array < exp_mean + exp_std)
                    ]
                    frac_events = events_in_exp_region.size / test_array.size
                    result.count_events += [frac_events]
    # If no matches are found the check should be marked as failed
    if len(result.messages) == 0:
        result.passed = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
    return result


def range_check_nd(
    filepath,
    expression,
    limits,
    blind_ranges,
    tree_pattern=r"(.*/DecayTree)|(.*/MCDecayTree)",
):
    """Produce 2-dimensional histograms of variables taken from a TTree object.

    :param filepath: Path to a file to analyse
    :param expression: Name of the variables (or expression) to be checked.
    :param limits: Pre-defined ranges
    :param blind_ranges: regions to be blinded in the histogram
    :param tree_pattern: A regular expression for the TTree object to check
    :returns: A CheckResult object
    """
    result = CheckResult(False)
    # Check if the number of variables matches expectations
    lenght_expr = len(expression)
    lenght_limits = len(limits)
    if lenght_expr < 2 or lenght_expr > 4:
        result.messages += ["Expected at least two variables, but not more than four."]
        result.passed |= False
        return result
    if lenght_expr != lenght_limits:
        result.messages += [
            "For each variable, a corresponding range should be defined."
        ]
        result.passed |= False
        return result
    with uproot.open(filepath) as f:
        for key, obj in f.items(cycle=False):
            if not isinstance(obj, uproot.TTree):
                continue
            if not re.fullmatch(tree_pattern, key):
                continue
            values_obj = {}
            list_expressions = list(expression.values())
            # Check if the branch is present in the TTree or if the expression is correctly written
            try:
                values_obj = obj.arrays(list_expressions, library="pd")
            except uproot.exceptions.KeyInFileError as e:
                result.messages += [f"Missing branch in {key!r} with {e!r}"]
                result.passed |= False
                result.tree_names += [f"{key}"]
                continue
            except Exception as e:
                result.messages += [
                    f"Failed to apply the expressions to {key!r} with error: {e!r}"
                ]
                result.passed |= False
                result.tree_names += [f"{key}"]
                continue
            # Check if there are regions to blind
            for k, ranges in blind_ranges.items():
                if isinstance(ranges, dict):
                    ranges = [ranges]
                # Take into account that there could be multiple regions to blind
                for blind_range in ranges:
                    lower, upper = blind_range["min"], blind_range["max"]
                    values_obj = values_obj.loc[
                        ~(
                            (lower < values_obj[expression[k]])
                            & (values_obj[expression[k]] < upper)
                        )
                    ]
            if values_obj.size == 0:
                result.passed |= False
                result.messages += [f"No events found in range for Tree {key}"]
                result.tree_names += [f"{key}"]
                continue
            # Fill the histograms
            list_keys = list(expression.keys())
            for key_i, key_j in combinations(list_keys, 2):
                axis0 = hist.axis.Regular(
                    50,
                    limits[key_i]["min"],
                    limits[key_i]["max"],
                    name=expression[key_i],
                )
                axis1 = hist.axis.Regular(
                    50,
                    limits[key_j]["min"],
                    limits[key_j]["max"],
                    name=expression[key_j],
                )
                h = Hist(axis0, axis1)
                h.fill(values_obj[expression[key_i]], values_obj[expression[key_j]])
                if not h.empty():
                    result.histograms += [h]
                    result.messages += [
                        f"Found at least one event in range in Tree {key} "
                    ]
                    result.passed |= True
                    result.tree_names += [f"{key}"]
                else:
                    var1 = expression[key_i]
                    var2 = expression[key_j]
                    result.messages += [
                        f"No events found in range for Tree {key} and variables {var1}, {var2} "
                    ]
                    result.passed |= False
                    result.tree_names += [f"{key}"]
    # If no matches are found the check should be marked as failed
    if len(result.messages) == 0:
        result.passed = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
    return result


def num_entries_per_invpb(
    filepath,
    count_per_invpb,
    tree_pattern=r"(.*/DecayTree)",
    lumi_pattern=r"(.*/LumiTuple)",
):
    """Check that the matching TTree objects contain a minimum number of entries per unit luminosity (pb-1).

    :param filepath: Path to a file to analyse
    :param count_per_invpb: The minimum number of entries per unit luminosity required
    :param tree_pattern: A regular expression for the TTree objects to check
    :param lumi_pattern: A regular expression for the TTree object containing the luminosity information
    :returns: A CheckResult object
    """
    result = CheckResult(False)
    check_tree_pattern = 0
    with uproot.open(filepath) as f:
        num_entries = {}
        lumi = 0.0
        for key, obj in f.items(cycle=False):
            if not isinstance(obj, uproot.TTree):
                continue
            if re.fullmatch(tree_pattern, key):
                check_tree_pattern = 1
                num_entries[key] = obj.num_entries
            if re.fullmatch(lumi_pattern, key):
                try:
                    lumi_arr = obj["IntegratedLuminosity"].array(library="np")
                except uproot.exceptions.KeyInFileError as e:
                    result.messages += [
                        f"Missing luminosity branch in {key!r} with error {e!r}"
                    ]
                    result.passed |= False
                    result.tree_names += [f"{key}"]
                    break
                lumi = numpy.sum(lumi_arr)
        if lumi == 0:
            result.passed |= False
            result.messages += ["Failed to get luminosity information"]
        else:
            for key, entries in num_entries.items():
                entries_per_lumi = round(entries / lumi, 2)
                result.passed |= entries_per_lumi >= count_per_invpb
                result.messages += [
                    f"Found {entries_per_lumi} entries per unit luminosity (pb-1) in {key}"
                ]
                result.tree_names += [f"{key}"]
    # If no matches were found the check should be marked as failed
    if check_tree_pattern == 0:
        result.passed = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
    return result


def range_check_bkg_subtracted(
    filepath,
    expression,
    limits,
    expr_for_subtraction,
    mean_sig,
    background_shift,
    background_window,
    signal_window,
    blind_ranges,
    tree_pattern=r"(.*/DecayTree)|(.*/MCDecayTree)",
):
    """Check if there is at least one entry in the TTree object with a specific
    variable falling in a pre-defined range. The background-subtracted histogram is then produced as output.
    Background is subtracted assuming a linear distribution. In particular, signal ([m-s, m+s])
    and background ([m-b-delta, m-b] U [m+b, m+b+delta]) windows have to be defined on a control variable.
    Then, one histogram is created for events falling in the signal region and another histogram is created
    for events falling in the background region.
    The subtraction, using the proper scaling factor, is finally performed.
    It is possible to blind some regions.

    :param filepath: Path to a file to analyse
    :param expression: Name of the variable (or expression depending on varibales in the TTree) to be checked
    :param limits: Pre-defined range
    :param expr_for_subtraction: Name of the control variable (or expression depending on varibales in the TTree)
    to be used to perform background subtraction
    :param mean_sig: expected mean value of expr_for_subtraction variable. The signal window will be centered around this value.
    :param background_shift:  Shift, w.r.t the "mean_sig" value, used to define the two background regions.
    :param background_window:  Lenght of the background windows (of expr_for_subtraction variable).
    :param signal_window: Lenght of the signal window (of expr_for_subtraction variable) used for background subtraction.
    The window is centered around the value of "mean_sig".
    :param blind_ranges: regions to be blinded in the histogram
    :param tree_pattern: A regular expression for the TTree object to check
    :returns: A CheckResult object
    """
    result = CheckResult(False)
    with uproot.open(filepath) as f:
        for key, obj in f.items(cycle=False):
            if not isinstance(obj, uproot.TTree):
                continue
            if not re.fullmatch(tree_pattern, key):
                continue
            values_obj = {}
            # Check if the branch is in the Tree or if the expressions are correctly written
            try:
                values_obj = obj.arrays(
                    [expr_for_subtraction, expression], library="np"
                )
            except uproot.exceptions.KeyInFileError as e:
                result.messages += [f"Missing branch in {key!r} with {e!r}"]
                result.passed |= False
                result.tree_names += [f"{key}"]
                continue
            except Exception as e:
                result.messages += [
                    f"Failed to apply {expr_for_subtraction!r} or {expression!r} to {key!r} with error: {e!r}"
                ]
                result.passed |= False
                result.tree_names += [f"{key}"]
                continue
            # Caluclate the min and max values of each of the two background regions.
            # By construction, the two intervals have the same lenght
            background_range_low = {
                "min": mean_sig - background_shift - background_window,
                "max": mean_sig - background_shift,
            }
            background_range_high = {
                "min": mean_sig + background_shift,
                "max": mean_sig + background_shift + background_window,
            }
            # Caluclate the min and max values of each of the signal region
            signal_range = {
                "min": mean_sig - signal_window / 2.0,
                "max": mean_sig + signal_window / 2.0,
            }
            # Create the histogram for the control variable used to perform background subtraction
            var_for_bkgsub_array = values_obj[expr_for_subtraction]
            axis0 = hist.axis.Regular(
                50,
                background_range_low["min"],
                background_range_high["max"],
                name=expr_for_subtraction,
            )
            h = Hist(axis0)
            # Add ranges to histogram metadata. Signal and background regions can be then highlighted in the final plot.
            h.metadata = [
                background_range_low["min"],
                background_range_low["max"],
                background_range_high["min"],
                background_range_high["max"],
                signal_range["min"],
                signal_range["max"],
            ]
            h.fill(var_for_bkgsub_array)
            result.histograms += [h]
            # Assume linear background distribution and evaluate fraction of background in the signal region
            alpha = 2.0 * background_window / signal_window
            # Select events in signal region
            cut_string = (
                "("
                + expr_for_subtraction
                + ">"
                + str(signal_range["min"])
                + ") & ("
                + expr_for_subtraction
                + "<"
                + str(signal_range["max"])
                + ")"
            )
            values_sig = obj.arrays([expression], cut_string, library="np")
            test_array_sig = values_sig[expression]
            test_array_sig = test_array_sig[
                numpy.where(
                    (test_array_sig < limits["max"]) & (test_array_sig > limits["min"])
                )
            ]
            # Select events in background region
            cut_string = (
                "( ("
                + expr_for_subtraction
                + ">"
                + str(background_range_low["min"])
                + ") & ("
                + expr_for_subtraction
                + "<"
                + str(background_range_low["max"])
                + ") ) | ( ("
                + expr_for_subtraction
                + ">"
                + str(background_range_high["min"])
                + ") & ("
                + expr_for_subtraction
                + "<"
                + str(background_range_high["max"])
                + ") )"
            )
            values_bkg = obj.arrays([expression], cut_string, library="np")
            test_array_bkg = values_bkg[expression]
            test_array_bkg = test_array_bkg[
                numpy.where(
                    (test_array_bkg < limits["max"]) & (test_array_bkg > limits["min"])
                )
            ]
            if isinstance(blind_ranges, dict):
                blind_ranges = [blind_ranges]
                # Take into account that there could be multiple regions to blind
            for blind_range in blind_ranges:
                lower, upper = blind_range["min"], blind_range["max"]
                test_array_sig = test_array_sig[
                    ~((lower < test_array_sig) & (test_array_sig < upper))
                ]
                test_array_bkg = test_array_bkg[
                    ~((lower < test_array_bkg) & (test_array_bkg < upper))
                ]

            if len(test_array_sig) == 0 | len(test_array_bkg) == 0:
                result.passed |= False
                result.messages += [
                    f"Not enough events for background subtraction found in range for Tree {key}"
                ]
                result.tree_names += [f"{key}"]
                continue
            result.messages += [f"Found at least one event in range in Tree {key} "]
            result.passed |= True
            result.tree_names += [f"{key}"]

            # Histograms subtraction
            axis0 = hist.axis.Regular(50, limits["min"], limits["max"], name=expression)
            hs = Hist(axis0)
            hb = Hist(axis0)
            hs.fill(test_array_sig)
            hb.fill(test_array_bkg)
            hsub = hs + (-1 * alpha) * hb
            result.histograms += [hsub]
    # If no matches are found the check should be marked as failed
    if len(result.messages) == 0:
        result.passed = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
    return result
