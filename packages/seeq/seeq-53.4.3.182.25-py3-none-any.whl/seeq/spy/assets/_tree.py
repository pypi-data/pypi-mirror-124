import fnmatch
import re

import numpy as np
import pandas as pd

from seeq import spy
from seeq.sdk import *
from seeq.spy import _common
from seeq.spy import _config
from seeq.spy import _login
from seeq.spy import _metadata
from seeq.spy import _push
from seeq.spy import _search
from seeq.spy._errors import *

_reference_types = ['StoredSignal', 'StoredCondition']
_calculated_types = ['CalculatedScalar', 'CalculatedSignal', 'CalculatedCondition']
_data_types = _calculated_types + _reference_types
_supported_input_types = _data_types + ['Asset']
_supported_output_types = _calculated_types + ['Asset']

_dataframe_dtypes = {
    'ID': str,
    'Referenced ID': str,
    'Path': str,
    'Name': str,
    'Type': str,
    'Depth': int,
    'Description': str,
    'Formula': str,
    'Formula Parameters': (str, list, dict, pd.Series, pd.DataFrame),
    'Cache Enabled': bool
}
_dataframe_columns = list(_dataframe_dtypes.keys())

MAX_ERRORS_DISPLAYED = 3


class Tree:
    _dataframe = pd.DataFrame()
    _workbook = _common.DEFAULT_WORKBOOK_PATH
    _workbook_id = _common.EMPTY_GUID

    quiet = False
    errors = 'raise'

    def __init__(self, data, *, description=None, workbook=_common.DEFAULT_WORKBOOK_PATH,
                 quiet=False, errors='raise', status=None):
        """
        Utilizes a Python Class-based tree to produce a set of item definitions as
        a metadata DataFrame. Allows users to manipulate the tree using various functions.

        Parameters
        ----------
        data : {pandas.DataFrame, str}
            Defines which element will be inserted at the root.
            If an existing tree already exists in Seeq, the entire tree will be pulled recursively.
            If this tree doesn't already within the scope of the workbook, new tree elements
            will be created (by deep-copy or reference if applicable).
            The following options are allowed:
            1) A name string. If an existing tree with that name (case-insensitive) is found,
                all children will be recursively pulled in.
            2) An ID string of an existing item in Seeq. If that item is in a tree, all
                children will be recursively pulled in.
            3) spy.search results or other custom dataframes. The 'Path' column must be present
                and represent a single tree structure.

        description : str, optional
            The description to set on the root-level asset.

        workbook : str, default 'Data Lab >> Data Lab Analysis'
            The path to a workbook (in the form of 'Folder >> Path >> Workbook Name')
            or an ID that all pushed items will be 'scoped to'. You can
            push to the Corporate folder by using the following pattern:
            '__Corporate__ >> Folder >> Path >> Workbook Name'. A Tree currently
            may not be globally scoped. These items will not be visible/searchable
            using the data panel in other workbooks.

        quiet : bool, default False
            If True, suppresses progress output. This setting will be the default for all
            operations on this Tree. This option can be changed later using
            `tree.quiet = True` or by specifying the option for individual function calls.
            Note that when status is provided, the quiet setting of the Status object
            that is passed in takes precedent.

        errors : {'raise', 'catalog'}, default 'raise'
            If 'raise', any errors encountered will cause an exception. If 'catalog',
            errors will be added to a 'Result' column in the status.df DataFrame. The
            option chosen here will be the default for all other operations on this Tree.
            This option can be changed later using `tree.errors = 'catalog'` or by
            specifying the option for individual function calls.

        status : spy.Status, optional
            If specified, the supplied Status object will be updated as the command
            progresses. It gets filled in with the same information you would see
            in Jupyter in the blue/green/red table below your code while the
            command is executed. The table itself is accessible as a DataFrame via
            the status.df property.
        """
        _common.validate_argument_types([
            (data, 'data', (pd.DataFrame, str)),
            (description, 'description', str),
            (workbook, 'workbook', str),
            (quiet, 'quiet', bool),
            (errors, 'errors', str),
            (status, 'status', _common.Status)
        ])
        _common.validate_errors_arg(errors)
        self.quiet = quiet
        self.errors = errors
        status = _common.Status.validate(status, quiet)

        self._workbook = workbook if workbook else _common.DEFAULT_WORKBOOK_PATH
        self._find_workbook_id(quiet, status)

        # Since the constructor can't return a results dataframe, we collect any catalogued errors into
        # status.df so the user can still see them; filtered_items holds these temporarily
        filtered_items = []
        if isinstance(data, pd.DataFrame):
            if len(data) == 0:
                raise SPyValueError("A tree may not be created from a DataFrame with no rows")

            status.update('Constructing Tree object from dataframe input.', _common.Status.RUNNING)

            # Check user input for errors, filter if errors='catalog'
            df, bad_items = _validate_and_filter(data, status, errors, stage='input',
                                                 error_message='Errors were encountered before creating tree',
                                                 raise_if_all_filtered=True)
            filtered_items.append(bad_items)

            # If the dataframe specifies a root with ID and Name corresponding to a previously pushed SPy tree,
            # then we want this object to modify the same tree rather than create a copy of it. If such a tree
            # exists, then we store its current state in existing_tree_df
            existing_tree_df = _get_existing_spy_tree(df, self._workbook_id)

            # Sanitize data and pull in properties of items with IDs. Make items with IDs into references unless
            # they are contained in existing_tree_df
            df = _process_properties(df, existing_tree_df=existing_tree_df)
            modified_item_ids = df.modified_item_ids

            # Rectify paths
            df = _trim_unneeded_paths(df)
            df = _reify_missing_assets(df)

            # Pull children of items with IDs
            df = _pull_all_children_of_all_nodes(df, self._workbook_id, existing_tree_df,
                                                 item_ids_to_ignore=modified_item_ids)

            status_message = f"Tree successfully created from DataFrame."
            if existing_tree_df is not None:
                status_message += f' This tree modifies a pre-existing SPy-created tree with name ' \
                                  f'"{existing_tree_df.ID.iloc[0]}".'

        elif data and isinstance(data, str):
            if _common.is_guid(data):
                existing_node_id = data
            else:
                status.update(f'Searching for existing asset tree roots with name "{data}"', _common.Status.RUNNING)
                existing_node_id = _find_root_node_by_name(data, self._workbook_id, status)

            if existing_node_id:
                # Pull an existing tree. Detect whether it originated from SPy
                status.update(f'Pulling existing asset tree "{data}"', _common.Status.RUNNING)
                df = _pull_tree(existing_node_id, self._workbook_id)

                status_message = f"Recursively pulled {'SPy-created' if df.spy_tree else 'existing'} " \
                                 f"asset tree."
            else:
                # Define a brand new root asset
                df = pd.DataFrame([{
                    'Type': 'Asset',
                    'Path': '',
                    'Depth': 1,
                    'Name': data,
                    'Description': description if description else np.nan
                }], columns=_dataframe_columns)

                status_message = f'No existing root found. Tree created using new root "{data}".' \
                                 f'{"" if _login.client else " If an existing tree was expected, please log in."}'

        else:
            raise SPyTypeError("Input 'data' must be a name, Seeq ID, or Metadata dataframe when creating a Tree")

        _sort_by_node_path(df)
        if description:
            df.loc[0, 'Description'] = description

        # Unlike in Tree.insert(), this final validation step will catch some user errors such as including two roots
        df, bad_items = _validate_and_filter(df, status, errors, stage='final',
                                             error_message='Errors were encountered while creating tree',
                                             fatal_message='Errors were encountered while validating tree')
        filtered_items.append(bad_items)
        filtered_items = pd.concat(filtered_items, ignore_index=True)
        if not filtered_items.empty:
            _sort_by_node_path(filtered_items)
            status.df = filtered_items
            status.warn('Errors were encountered while creating tree. See dataframe below.')

        self._dataframe = df
        status.update(f'{status_message} {self.summarize(ret=True)}', _common.Status.SUCCESS)

    def insert(self, children, parent=None, *, friendly_name=None, formula=None, formula_params=None,
               errors=None, quiet=None, status=None):
        """
        Insert the specified elements into the tree.

        Parameters
        ----------
        children : {pandas.DataFrame, str, list, Tree}, optional
            Defines which element or elements will be inserted below each parent. If an existing
            node already existed at the level in the tree with that name (case-insensitive),
            it will be updated. If it doesn't already exist, a new node will be created
            (by deep-copy or reference if applicable).
            The following options are allowed:
            1) A basic string or list of strings to create a new asset.
            2) Another SPy Tree.
            3) spy.search results or other custom dataframes.

        parent : {pandas.DataFrame, str, int}, optional
            Defines which element or elements the children will be inserted below.
            If a parent match is not found and non-glob/regex string or path is used,
            the parent (or entire path) will be created too.
            The following options are allowed:
            1) No parent specified will insert directly to the root of the tree.
            2) String name match (case-insensitive equality, globbing, regex, column
                values) will find any existing nodes in the tree that match.
            3) String path match, including partial path matches.
            4) ID. This can either be the actual ID of the tree.push()ed node or the
                ID of the source item.
            5) Number specifying tree level. This will add the children below every
                node at the specified level in the tree (1 being the root node).
            6) spy.search results or other custom dataframe.

        friendly_name : str, optional
            Use this specified name rather than the referenced item's original name.

        formula : str, optional
            The formula for a calculated item. The `formula` and `formula_parameters` are
            used in place of the `children` argument.

        formula_params : dict, optional
            The parameters for a formula.

        errors : {'raise', 'catalog'}, optional
            If 'raise', any errors encountered will cause an exception. If 'catalog',
            errors will be added to a 'Result' column in the status.df DataFrame. This
            input will be used only for the duration of this function; it will default
            to the setting on the Tree if not specified.

        quiet : bool, optional
            If True, suppresses progress output. This input will be used only for the
            duration of this function; it will default to the setting on the Tree if
            not specified. Note that when status is provided, the quiet setting of
            the Status object that is passed in takes precedent.

        status : spy.Status, optional
            If specified, the supplied Status object will be updated as the command
            progresses. It gets filled in with the same information you would see
            in Jupyter in the blue/green/red table below your code while the
            command is executed. The table itself is accessible as a DataFrame via
            the status.df property.
        """

        if children is None:
            if formula and formula_params:
                # TODO CRAB-24291 Insert calculations
                raise SPyValueError('Inserting calculations is not currently supported')
            else:
                raise SPyValueError('Formula and formula parameters must be specified if no children argument is '
                                    'given.')
        else:
            if formula or formula_params:
                raise SPyValueError('Formula and formula parameters must be None if a children argument is given.')

        _common.validate_argument_types([
            (children, 'children', (pd.DataFrame, Tree, str, list)),
            (parent, 'parent', (pd.DataFrame, str, int)),
            (friendly_name, 'friendly_name', str),
            (formula, 'formula', str),
            (formula_params, 'formula_params', dict)
        ])
        errors = self._get_or_default_errors(errors)
        quiet = self._get_or_default_quiet(quiet)
        status = _common.Status.validate(status, quiet)

        if isinstance(children, str):
            children = [children]
        if isinstance(children, list):
            for child in children:
                if not isinstance(child, str):
                    raise SPyValueError(f'List input to children argument contained non-string data: {child}')
            children = pd.DataFrame([{'ID': child} if _common.is_guid(child) else
                                     {'Name': child, 'Type': 'Asset'} for child in children])
        elif isinstance(children, Tree):
            children = children._dataframe.copy()

        status.df = pd.DataFrame([{
            'Assets Inserted': 0,
            'Signals Inserted': 0,
            'Conditions Inserted': 0,
            'Scalars Inserted': 0,
            'Total Items Inserted': 0,
            'Errors Encountered': 0,
        }], index=['Status'])
        status.update('Processing item properties and finding children to be inserted.', _common.Status.RUNNING)

        # Check user input for errors, filter if errors='catalog'
        children, results_df = _validate_and_filter(children, status, errors, stage='input',
                                                    error_message='Errors were encountered before inserting')
        status.df['Errors Encountered'] = len(results_df)
        status.update()

        # Sanitize data and pull in properties of items with IDs
        children = _process_properties(children)

        # Pull children of items with pre-existing IDs
        children = _pull_all_children_of_all_nodes(children, self._workbook_id)

        # Pre-insertion validation. This should only validate that we didn't pull in any metrics. We use
        # errors='catalog' so that the user isn't screwed when inserting an asset with threshold metric children
        children, bad_rows = _validate_and_filter(children, status, errors='catalog', stage='pre-insert',
                                                  error_message='Errors were encountered before inserting')
        results_df = results_df.append(bad_rows, ignore_index=True)
        status.df['Errors Encountered'] = len(results_df)

        status.update('Inserting items into tree.', _common.Status.RUNNING)

        # A bool for each of the children, indicating that a parent was properly found
        parents_found = pd.Series(False, index=children.index)

        def _get_children_to_add(children_df, parent_node):
            children_to_add = children_df.copy()
            # TODO CRAB-24298: filter children by column names using the match object
            parents_found[:] = True
            parent_full_path = _get_full_path(parent_node)
            if 'Parent' in children_df.columns:
                # TODO CRAB-24290: Allow 'Parent' to be directly specified in the input dataframe
                raise SPyValueError("'Parent' input column is not yet supported.")
            elif 'Path' in children_df.columns and not pd.isna(children_df['Path']).all():
                # Simplify path while maintaining subtree structure
                children_to_add = _trim_unneeded_paths(children_to_add, parent_full_path)
                children_to_add = _reify_missing_assets(children_to_add, parent_full_path)
            else:
                # No path found in the input children DF. All children will be below this parent.
                children_to_add['Path'] = parent_full_path
                children_to_add['Depth'] = parent_node['Depth'] + 1
            return children_to_add

        # We concatenate all children to be inserted into one dataframe before
        # inserting them using a single pd.merge call
        # TODO CRAB-24290 Insert with parents defined by dataframes
        # TODO CRAB-24298 Insert using Column Values from a dataframe
        additions = []
        for _, parent_row in self._dataframe.iterrows():
            match = _is_node_match(parent, parent_row)
            if match:
                additions.append(_get_children_to_add(children, parent_row))
        additions = pd.concat(additions, ignore_index=True) if additions else pd.DataFrame()
        # Remove duplicate items in case the user has passed duplicate information to the children parameter
        _drop_duplicate_items(additions)

        # Merge the dataframes on case-insensitive 'Path' and 'Name' columns
        working_df = _upsert(self._dataframe.copy(), additions)
        additions['Result'] = 'Success'
        results_df = results_df.append(additions, ignore_index=True)

        _sort_by_node_path(working_df)

        # If errors occur during the following validation step, they are "our fault", i.e., we inserted into the tree
        # incorrectly. We ideally want all feasible user errors to be reported before this point
        working_df, bad_rows = _validate_and_filter(working_df, status, errors, stage='final',
                                                    error_message='Errors were encountered while inserting',
                                                    fatal_message='Errors were encountered while validating tree')
        results_df = _upsert(results_df, bad_rows)

        successful_results = results_df[results_df.Result == 'Success']
        if not successful_results.empty and not successful_results.Type.isnull().all():
            status.df['Assets Inserted'] = successful_results['Type'].str.contains('Asset').sum()
            status.df['Signals Inserted'] = successful_results['Type'].str.contains('Signal').sum()
            status.df['Conditions Inserted'] = successful_results['Type'].str.contains('Condition').sum()
            status.df['Scalars Inserted'] = successful_results['Type'].str.contains('Scalar').sum()
            status.df['Total Items Inserted'] = len(successful_results)
        status.df['Errors Encountered'] = len(results_df) - len(successful_results)
        status.update()

        # Include children with no matching parents found in the results_df
        children_with_no_parents_found = children[~parents_found]
        children_with_no_parents_found['Result'] = 'Ignored: No matching parent found.'
        results_df = results_df.append(children_with_no_parents_found, ignore_index=True)
        if not parents_found.any():
            status.warn('No matching parents found. Nothing was inserted.')

        _sort_by_node_path(results_df)

        self._dataframe = working_df
        status.update(f'Successfully completed element insertion. {self.summarize(ret=True)}', _common.Status.SUCCESS)

        return results_df

    def remove(self, elements, *, errors=None, quiet=None, status=None):
        """
        Remove the specified elements from the tree recursively.

        Parameters
        ----------
        elements : {pandas.DataFrame, str, int}
            Defines which element or elements will be removed.
            1) String name match (case-insensitive equality, globbing, regex, column
                values) will find any existing nodes in the tree that match.
            2) String path match, including partial path matches.
            3) ID. This can either be the actual ID of the tree.push()ed node or the
                ID of the source item.
            4) Number specifying tree level. This will add the children below every
                node at the specified level in the tree (1 being the root node).
            5) spy.search results or other custom dataframe.

        errors : {'raise', 'catalog'}, optional
            If 'raise', any errors encountered will cause an exception. If 'catalog',
            errors will be added to a 'Result' column in the status.df DataFrame. This
            input will be used only for the duration of this function; it will default
            to the setting on the Tree if not specified.

        quiet : bool, optional
            If True, suppresses progress output. This input will be used only for the
            duration of this function; it will default to the setting on the Tree if
            not specified. Note that when status is provided, the quiet setting of
            the Status object that is passed in takes precedent.

        status : spy.Status, optional
            If specified, the supplied Status object will be updated as the command
            progresses. It gets filled in with the same information you would see
            in Jupyter in the blue/green/red table below your code while the
            command is executed. The table itself is accessible as a DataFrame via
            the status.df property.
        """

        if isinstance(elements, pd.DataFrame):
            # TODO CRAB-24290 Remove by dataframe (requires same logic as insert with dataframe parent argument)
            raise SPyValueError('Removing using DataFrames is not currently supported')

        _common.validate_argument_types([
            (elements, 'elements', (pd.DataFrame, str, int)),
            (errors, 'errors', str),
            (quiet, 'quiet', bool),
            (status, 'status', _common.Status)
        ])

        errors = self._get_or_default_errors(errors)
        quiet = self._get_or_default_quiet(quiet)
        status = _common.Status.validate(status, quiet)

        working_df = self._dataframe.copy()
        results_df = pd.DataFrame(columns=_dataframe_columns + ['Result'])
        status.df = pd.DataFrame([{
            'Assets Removed': 0,
            'Signals Removed': 0,
            'Conditions Removed': 0,
            'Scalars Removed': 0,
            'Total Items Removed': 0,
            'Errors Encountered': 0,
        }], index=['Status'])
        status.update('Removing items from Tree', _common.Status.RUNNING)

        idx = 1
        while idx < len(working_df.index):
            node = working_df.iloc[idx]
            if _is_node_match(elements, node):
                # TODO CRAB-24296: Handle the validation output
                _validate_remove(working_df, idx)

                subtree_selector = (working_df['Path'].str.startswith(_get_full_path(node),
                                                                      na=False)) | (working_df.index == idx)
                dropped_nodes = working_df[subtree_selector].copy()
                working_df.drop(working_df.index[subtree_selector], inplace=True)
                working_df.reset_index(drop=True, inplace=True)
                dropped_nodes['Result'] = 'Removed'

                status.df['Assets Removed'] += sum(dropped_nodes['Type'].str.contains('Asset'))
                status.df['Signals Removed'] += sum(dropped_nodes['Type'].str.contains('Signal'))
                status.df['Conditions Removed'] += sum(dropped_nodes['Type'].str.contains('Condition'))
                status.df['Scalars Removed'] += sum(dropped_nodes['Type'].str.contains('Scalar'))
                status.df['Total Items Removed'] += len(dropped_nodes.index)
                status.update()

                results_df = results_df.append(dropped_nodes, ignore_index=True)
            else:
                idx += 1

        working_df, bad_rows = _validate_and_filter(working_df, status, errors, stage='final',
                                                    error_message='Errors were encountered while removing',
                                                    fatal_message='Errors were encountered while validating tree')

        results_df = _upsert(results_df, bad_rows)
        _sort_by_node_path(results_df)

        self._dataframe = working_df
        status.update(
            f'Successfully removed {status.df.loc["Status", "Total Items Removed"]} items from the tree. '
            f'{self.summarize(ret=True)}',
            _common.Status.SUCCESS
        )

        return results_df

    def move(self, source, *, destination=None, errors=None, quiet=None, status=None):
        """
        Move the specified elements (and all children) from one location in
        the tree to another.

        Parameters
        ----------
        source : {pandas.DataFrame, str}
            Defines which element or elements will be removed.
            1) String path match.
            2) ID. This can either be the actual ID of the tree.push()ed node or the
                ID of the source item.
            3) spy.search results or other custom dataframe.
            4) Another SPy Tree.

        destination : {pandas.DataFrame, str}; optional
            Defines which element or elements will be removed.
            1) No destination specified will move the elements to just below
              the root of the tree.
            2) String path match.
            3) ID. This can either be the actual ID of the tree.push()ed node or the
                ID of the source item.
            4) spy.search results or other custom dataframe.
            5) Another SPy Tree (root).

        errors : {'raise', 'catalog'}, optional
            If 'raise', any errors encountered will cause an exception. If 'catalog',
            errors will be added to a 'Result' column in the status.df DataFrame. This
            input will be used only for the duration of this function; it will default
            to the setting on the Tree if not specified.

        quiet : bool, optional
            If True, suppresses progress output. This input will be used only for the
            duration of this function; it will default to the setting on the Tree if
            not specified. Note that when status is provided, the quiet setting of
            the Status object that is passed in takes precedent.

        status : spy.Status, optional
            If specified, the supplied Status object will be updated as the command
            progresses. It gets filled in with the same information you would see
            in Jupyter in the blue/green/red table below your code while the
            command is executed. The table itself is accessible as a DataFrame via
            the status.df property.
        """
        errors = self._get_or_default_errors(errors)
        quiet = self._get_or_default_quiet(quiet)
        status = _common.Status.validate(status, quiet)
        # TODO CRAB-24293 Allow moving nodes
        _validate(self._dataframe)
        raise SPyValueError('Moving is not currently supported')
        self.summarize()

    @property
    def size(self):
        """
        Property that gives the number of elements currently in the tree.
        """
        return len(self._dataframe)

    def __len__(self):
        return self.size

    @property
    def height(self):
        """
        Property that gives the current height of the tree. This is the length
        of the longest item path within the tree.
        """
        return self._dataframe['Depth'].max()

    def items(self):
        return self._dataframe.copy()

    def count(self, item_type=None):
        """
        Count the number of elements in the tree of each Seeq type. If item_type
        is not specified, then returns a dictionary with keys 'Asset', 'Signal',
        'Condition', 'Scalar', and 'Unknown'. If item_type is specified, then
        returns an int.

        Parameters
        ----------
        item_type : {'Asset', 'Signal', 'Condition', 'Scalar', 'Uncompiled Formula'}, optional
            If specified, then the method will return an int representing the
            number of elements with Type item_type. Otherwise, a dict will be
            returned.
        """

        simple_types = ['Asset', 'Signal', 'Condition', 'Scalar', 'Uncompiled Formula']
        if item_type:
            if not isinstance(item_type, str) or item_type.capitalize() not in (simple_types + ['Formula',
                                                                                                'Uncompiled']):
                raise SPyValueError(f'"{item_type}" is not a valid node type. Valid types are: '
                                    f'{", ".join(simple_types)}')
            if item_type in ['Uncompiled Formula', 'Uncompiled', 'Formula']:
                return sum(pd.isnull(self._dataframe['Type']) | (self._dataframe['Type'] == ''))
            else:
                return sum(self._dataframe['Type'].str.contains(item_type.capitalize(), na=False))

        def _simplify_type(t):
            if not pd.isnull(t):
                for simple_type in simple_types:
                    if simple_type in t:
                        return simple_type
            return 'Uncompiled Formula'

        return self._dataframe['Type'] \
            .apply(_simplify_type) \
            .value_counts() \
            .to_dict()

    def summarize(self, ret=False):
        """
        Generate a human-readable summary of the tree.

        Parameters
        ----------
        ret : bool, default False
            If True, then this method returns a string summary of the tree. If
            False, then this method prints the summary and returns nothing.
        """
        counts = self.count()

        def _get_descriptor(k, v):
            singular_descriptors = {
                key: key.lower() if key != 'Uncompiled Formula' else 'calculation whose type has not '
                                                                     'yet been determined'
                for key in counts.keys()
            }
            plural_descriptors = {
                key: f'{key.lower()}s' if key != 'Uncompiled Formula' else 'calculations whose types have not '
                                                                           'yet been determined'
                for key in counts.keys()
            }
            if v == 1:
                return singular_descriptors[k]
            else:
                return plural_descriptors[k]

        nonzero_counts = {k: v for k, v in counts.items() if v != 0}
        if len(nonzero_counts) == 1:
            count_string = ''.join([f'{v} {_get_descriptor(k, v)}' for k, v in nonzero_counts.items()])
        elif len(nonzero_counts) == 2:
            count_string = ' and '.join([f'{v} {_get_descriptor(k, v)}' for k, v in nonzero_counts.items()])
        elif len(nonzero_counts) > 2:
            count_string = ', '.join([f'{v} {_get_descriptor(k, v)}' for k, v in nonzero_counts.items()])
            last_comma = count_string.rfind(',')
            count_string = count_string[:last_comma + 2] + 'and ' + count_string[last_comma + 2:]
        else:
            return

        root_name = self._dataframe.iloc[0]['Name']

        summary = f'The tree "{root_name}" has height {self.height} and contains {count_string}.'

        if ret:
            return summary
        else:
            print(summary)

    def missing_items(self, return_type='print'):
        """
        Identify elements that may be missing child elements based on the contents of other sibling nodes.

        Parameters
        ----------
        return_type : {'print', 'string', 'dict'}, default 'print'
            If 'print', then a string that enumerates the missing items will be
            printed. If 'string', then that same string will be returned and not
            printed. If 'dict', then a dictionary that maps element paths to lists
            of their potential missing children will be returned.
        """
        if return_type.lower() not in ['print', 'str', 'string', 'dict', 'dictionary', 'map']:
            raise SPyValueError(f"Illegal argument {return_type} for return_type. Acceptable values are 'print', "
                                f"'string', and 'dict'.")
        return_type = return_type.lower()

        if self.count(item_type='Asset') == self.size:
            missing_string = 'There are no non-asset items in your tree.'
            if return_type in ['dict', 'dictionary', 'map']:
                return dict()
            elif return_type == 'print':
                print(missing_string)
                return
            else:
                return missing_string

        repeated_grandchildren = dict()

        prev_row = None
        path_stack = []
        for _, row in self._dataframe.iterrows():
            if prev_row is None:
                pass
            elif row.Depth > prev_row.Depth:
                path_stack.append((prev_row, set()))
            else:
                path_stack = path_stack[:row.Depth - 1]
            if len(path_stack) > 1:
                grandparent, grandchildren_set = path_stack[-2]
                if row.Name in grandchildren_set:
                    repeated_grandchildren.setdefault(_get_full_path(grandparent), set()).add(row.Name)
                else:
                    grandchildren_set.add(row.Name)
            prev_row = row

        missing_item_map = dict()
        path_stack = []
        for _, row in self._dataframe.iterrows():
            if prev_row is None:
                pass
            elif row.Depth > prev_row.Depth:
                if path_stack and _get_full_path(path_stack[-1][0]) in repeated_grandchildren:
                    required_children = repeated_grandchildren[_get_full_path(path_stack[-1][0])].copy()
                else:
                    required_children = set()
                path_stack.append((prev_row, required_children))
            else:
                for parent, required_children in path_stack[row.Depth - 1:]:
                    if len(required_children) != 0:
                        missing_item_map[_get_full_path(parent)] = sorted(required_children)
                path_stack = path_stack[:row.Depth - 1]
            if len(path_stack) != 0:
                _, required_children = path_stack[-1]
                required_children.discard(row.Name)
            prev_row = row
        for parent, required_children in path_stack:
            if len(required_children) != 0:
                missing_item_map[_get_full_path(parent)] = sorted(required_children)

        if return_type in ['dict', 'dictionary', 'map']:
            return missing_item_map

        if len(missing_item_map):
            missing_string = 'The following elements appear to be missing:'
            for parent_path, missing_children in missing_item_map.items():
                missing_string += f"\n{parent_path} is missing: {', '.join(missing_children)}"
        else:
            missing_string = 'No items are detected as missing.'

        if return_type == 'print':
            print(missing_string)
        else:
            return missing_string

    def push(self, *, errors=None, quiet=None, status=None):
        """
        Imports the tree into Seeq Server.

        errors : {'raise', 'catalog'}, optional
            If 'raise', any errors encountered will cause an exception. If 'catalog',
            errors will be added to a 'Result' column in the status.df DataFrame. This
            input will be used only for the duration of this function; it will default
            to the setting on the Tree if not specified.

        quiet : bool, optional
            If True, suppresses progress output. This input will be used only for the
            duration of this function; it will default to the setting on the Tree if
            not specified. Note that when status is provided, the quiet setting of
            the Status object that is passed in takes precedent.

        status : spy.Status, optional
            If specified, the supplied Status object will be updated as the command
            progresses. It gets filled in with the same information you would see
            in Jupyter in the blue/green/red table below your code while the
            command is executed. The table itself is accessible as a DataFrame via
            the status.df property.
        """
        errors = self._get_or_default_errors(errors)
        quiet = self._get_or_default_quiet(quiet)
        status = _common.Status.validate(status, quiet)

        _validate_and_filter(self._dataframe, status, errors='raise', stage='final',
                             error_message='Errors encountered before pushing')

        push_results = _push.push(metadata=self._dataframe, workbook=self._workbook, archive=True,
                                  errors=errors, quiet=quiet, status=status)

        # make root only asset tree appear in Data -> Asset Trees in workbench
        if self.height == 1:
            trees_api = TreesApi(_login.client)
            item_id_list = ItemIdListInputV1()
            item_id_list.items = list(push_results.ID)
            trees_api.move_nodes_to_root_of_tree(body=item_id_list)

        successfully_pushed = push_results['Push Result'] == 'Success'
        self._dataframe.loc[successfully_pushed, 'ID'] = push_results.loc[successfully_pushed, 'ID']
        self._dataframe.loc[successfully_pushed, 'Type'] = push_results.loc[successfully_pushed, 'Type']

        return push_results

    def _repr_html_(self):
        # noinspection PyProtectedMember
        return self._dataframe._repr_html_()

    def __iter__(self):
        return self._dataframe.itertuples(index=False, name='Item')

    def _find_workbook_id(self, quiet, status):
        """
        Set the _workbook_id based on the workbook input. This will enable us to know whether we should set
        the `ID` or `Referenced ID` column when pulling an item.
        """
        if _common.is_guid(self._workbook):
            self._workbook_id = _common.sanitize_guid(self._workbook)
        elif _login.client:
            search_query, _ = _push.create_analysis_search_query(self._workbook)
            search_df = spy.workbooks.search(search_query,
                                             quiet=quiet,
                                             status=status.create_inner('Find Workbook', quiet=quiet))
            self._workbook_id = search_df.iloc[0]['ID'] if len(search_df) > 0 else _common.EMPTY_GUID
        else:
            self._workbook_id = _common.EMPTY_GUID

    def _get_or_default_errors(self, errors_input):
        if isinstance(errors_input, str):
            _common.validate_errors_arg(errors_input)
            return errors_input
        return self.errors

    def _get_or_default_quiet(self, quiet_input):
        if isinstance(quiet_input, bool):
            return quiet_input
        return self.quiet


def _get_full_path(node):
    if not isinstance(_common.get(node, 'Name'), str) or len(node['Name']) == 0:
        return ''
    if isinstance(_common.get(node, 'Path'), str) and len(node['Path']) != 0:
        return f"{node['Path']} >> {node['Name']}"
    return node['Name']


def _sort_by_node_path(df):
    _decorate_with_full_path(df)
    df.sort_values(by='Full Path List', inplace=True, ignore_index=True)
    _remove_full_path(df)


def _decorate_with_full_path(df):
    """
    From the 'Path' and 'Name' columns, add a 'Full Path List' column.
    """
    df['Full Path List'] = df.apply(_get_full_path, axis=1).apply(_common.path_string_to_list)


def _remove_full_path(df):
    """
    Remove the 'Full Path List' column.
    """
    df.drop('Full Path List', axis=1, inplace=True)


def _update_path_from_full_path_list(df):
    """
    From the 'Full Path List' column, set the 'Path' column.
    """
    df['Path'] = df.apply(lambda node: _common.path_list_to_string(node['Full Path List'][:-1]), axis=1)


def _trim_unneeded_paths(df, parent_full_path=None, maintain_last_shared_root=None):
    """
    Remove any leading parts of the path that are shared across all rows. Then add the parent_path back onto the
    front of the path.

    E.G. If all rows have a path of 'USA >> Texas >> Houston >> Cooling Tower >> Area {x} >> ...',
    'Cooling Tower' would become the root asset for this Tree. Then if parent_path was 'My Tree >> Cooling Tower',
    all rows would have a path 'My Tree >> Cooling Tower >> Area {x} >> ...'
    """
    if len(df) == 0:
        return df

    # Get the path of the first node. It doesn't matter which we start with since we're only removing paths that are
    # shared across ALL rows.
    _decorate_with_full_path(df)
    shared_root = _push.get_common_root(df['Full Path List'])
    # Trim the path until we're left with the last universally shared node.
    while shared_root:
        trimmed_full_path_list = df['Full Path List'].apply(lambda l: l[1:])
        remaining_shared_root = _push.get_common_root(trimmed_full_path_list)
        keep_last_shared_root = True
        if parent_full_path and remaining_shared_root:
            # We only want to remove the root-most path if it is already going to be the parent (due to insert)
            parent_name = _common.path_string_to_list(parent_full_path)[-1]
            keep_last_shared_root = remaining_shared_root != parent_name
        elif parent_full_path and shared_root and isinstance(maintain_last_shared_root, bool):
            # We explicitly want to remove the last shared root so it can be replaced.
            keep_last_shared_root = maintain_last_shared_root
        if not remaining_shared_root and keep_last_shared_root:
            # We need to keep the last shared root so do not save trimmed_full_path_list
            break
        df['Full Path List'] = trimmed_full_path_list
        if 'Depth' in df:
            df['Depth'] -= 1
        shared_root = remaining_shared_root

    if parent_full_path:
        # Prepend the parent path if applicable
        parent_path_list = _common.path_string_to_list(parent_full_path)
        parent_name = parent_path_list[-1]
        if _push.get_common_root(df['Full Path List']) == parent_name:
            parent_path_list.pop()
        if parent_path_list:
            df['Full Path List'] = df['Full Path List'].apply(lambda l: parent_path_list + l)
            if 'Depth' in df:
                df['Depth'] += len(parent_path_list)
    _update_path_from_full_path_list(df)
    _remove_full_path(df)
    return df


def _get_shared_root(full_path_series):
    """
    Returns the highest shared name in the input paths. If no such name exists, returns None
    """
    first_full_path_list = full_path_series.iloc[0]
    if not len(first_full_path_list):
        return None
    root_name = first_full_path_list[0]
    all_roots_same = full_path_series.apply(lambda l: len(l) and l[0] == root_name).all()
    return root_name if all_roots_same else None


def _reify_missing_assets(df, existing_parent_path=None):
    """
    Automatically generate any assets that are referred to by path only.
    E.G. If this tree were defined using a dataframe containing only leaf signals, but with a Path column of
    'Cooling Tower >> Area {x} >> {signal}', the 'Cooling Tower' and 'Area {x}' assets would be generated.

    If existing_parent_path is provided, the reification will not occur for any existing parents.
    E.G. 'Example >> Cooling Tower >> Area {x} >> {signal}' with existing_parent_path='Example'
     would only generate 'Cooling Tower' and 'Area {x}' assets, not 'Example'.
    """
    # Store the Full Path tuples of all possible Assets to be created in a set
    full_paths = set()
    for path_list in df.apply(_get_full_path, axis=1).apply(_common.path_string_to_list):
        full_paths.update([tuple(path_list[:i]) for i in range(1, len(path_list))])
    # Remove all Assets whose paths are contained in the existing_parent_path
    if existing_parent_path is not None:
        full_paths.difference_update([full_path for full_path in full_paths if
                                      _common.path_list_to_string(full_path) in existing_parent_path])
    # Create dataframe rows based on these paths, and use a single pd.merge call to update the dataframe
    new_assets = pd.DataFrame([{
        'Type': 'Asset',
        'Path': _common.path_list_to_string(full_path[:-1]),
        'Name': full_path[-1],
        'Depth': len(full_path)
    } for full_path in full_paths])
    _drop_duplicate_items(new_assets)
    return _upsert(df, new_assets, prefer_right=False)


def _pull_tree(node_id, workbook_id):
    """
    Given the ID of an Item, pulls that node and all children and returns the resulting sanitized dataframe
    """
    # Determine if node_id is root of pre-existing SPy tree
    existing_tree_df = _get_existing_spy_tree(pd.DataFrame([{'ID': node_id}]), workbook_id=workbook_id)

    # Get the requested node itself
    df = _process_properties(pd.DataFrame([{'ID': node_id}], columns=_dataframe_columns),
                             existing_tree_df=existing_tree_df)
    df = _pull_all_children_of_all_nodes(df, workbook_id, existing_tree_df)
    _common.add_properties_to_df(df, spy_tree=existing_tree_df is not None)
    return df


def _pull_all_children_of_all_nodes(df, workbook_id, existing_tree_df=None, item_ids_to_ignore=None):
    """
    For each node in the tree that contains an 'ID' or 'Referenced ID', pull in any asset tree children.
    If any nodes already exist in the dataframe (by case-insensitive Path+Name), the existing row will be kept.
    """
    if df.empty:
        return df

    for col in ['ID', 'Referenced ID']:
        if col not in df.columns:
            df[col] = pd.Series(np.nan, dtype='object')
    # Gather all Paths+IDs into a list upfront
    items_to_pull_children = df[(~pd.isnull(df['ID'])) | (~pd.isnull(df['Referenced ID']))]

    for _, row in items_to_pull_children.iterrows():
        # Pull based on ID if it exists, otherwise use Referenced ID
        if _common.present(row, 'ID'):
            node_id = row['ID']
            row_is_reference = False
        else:
            node_id = row['Referenced ID']
            row_is_reference = True
        node_full_path = _get_full_path(row)
        df = _pull_all_children_of_node(df, node_id, node_full_path, workbook_id,
                                        existing_tree_df=existing_tree_df if not row_is_reference else None,
                                        item_ids_to_ignore=item_ids_to_ignore)
    return df


def _pull_all_children_of_node(df, node_id, node_full_path, workbook_id, existing_tree_df, item_ids_to_ignore):
    """
    Given the ID of an Item in an asset tree, pulls all children and places them into the given dataframe.
    Does not overwrite existing data.
    """
    # Get all children of the requested asset
    search_results = _search.search(query={'Asset': node_id}, all_properties=True, workbook=workbook_id,
                                    order_by=['ID'], quiet=True)
    if len(search_results) == 0:
        return df

    if item_ids_to_ignore is not None:
        search_results = search_results[~search_results['ID'].isin(item_ids_to_ignore)]
        if len(search_results) == 0:
            return df

    # Step 1: Convert the search results dataframe into a Tree-style dataframe.
    insert_df = _process_properties(search_results, existing_tree_df=existing_tree_df, pull_nodes=False)

    # Step 2: If the node_id's original name does not match what the node's name is in the Tree, trim off any extra
    # path from the input.
    _decorate_with_full_path(insert_df)
    parent_name = _common.path_string_to_list(node_full_path)[-1]
    if parent_name:
        maintain_last_shared_root = parent_name in insert_df.iloc[0]['Full Path List']
        insert_df = _trim_unneeded_paths(insert_df, node_full_path, maintain_last_shared_root)

    # Step 3: Actually insert the nodes
    df = _upsert(df, insert_df, prefer_right=False)
    return df


def _upsert(df1, df2, prefer_right=True):
    """
    Upserts the data from df2 into df1 based on case-insensitive Path and Name values.
    If a row from df2 matches a row in df1, and the two have conflicting values, then preference
    is given as per the prefer_right parameter. Keeps the columns of df1
    """
    if len(df2) == 0:
        return df1
    if len(df1) == 0:
        return df2

    orig_columns = df1.columns
    df1 = df1.copy()
    df2 = df2.copy()
    for df in (df1, df2):
        df['path_nocase'] = df.Path.astype('object').str.casefold()
        df['name_nocase'] = df.Name.astype('object').str.casefold()
    df = df1.merge(df2, how='outer', on=['path_nocase', 'name_nocase'])
    wipe_ids = pd.Series(False, index=df.index)
    for column in orig_columns:
        prefer_right_column = prefer_right and column not in ['Path', 'Name']
        left_column = column + '_x'
        right_column = column + '_y'
        if right_column in df.columns:
            prefer_column = right_column if prefer_right_column else left_column
            backup_column = left_column if prefer_right_column else right_column
            df[column] = df[prefer_column]
            missing_values = pd.isnull(df[column])
            df.loc[missing_values, column] = df.loc[missing_values, backup_column]
            df[column] = df[column].apply(_safe_int_cast)
            if column == 'Type' and 'ID' in df.columns:
                wipe_ids = wipe_ids | df.apply(lambda row: _type_differs(row[prefer_column], row[backup_column]),
                                               axis=1)
    df.drop(columns=df.columns.difference(orig_columns), inplace=True)
    if 'ID' in df.columns:
        df.loc[wipe_ids, 'ID'] = np.nan
    return df


def _type_differs(t1, t2):
    if pd.isnull(t1) or pd.isnull(t2) or len(t1) == 0 or len(t2) == 0:
        return False
    if 'Calculated' in t1 and 'Stored' in t2:
        return False
    if 'Stored' in t1 and 'Calculated' in t2:
        return False
    for simple_type in ('Asset', 'Scalar', 'Signal', 'Condition'):
        if simple_type in t1 and simple_type in t2:
            return False
    return True


def _validate_remove(df, rmv_index):
    # TODO CRAB-24296: Validate calculation dependencies when removing nodes
    return


def _drop_duplicate_items(df):
    """
    Removes duplicate items (identified by case-insensitive Path and Name) from a dataframe.
    """
    if len(df) == 0:
        return
    df['path_nocase'] = df.Path.astype('object').str.casefold()
    df['name_nocase'] = df.Name.astype('object').str.casefold()
    df.drop_duplicates(subset=['path_nocase', 'name_nocase'], inplace=True, ignore_index=True)
    df.drop(columns=['path_nocase', 'name_nocase'], inplace=True)


def _safe_int_cast(x):
    return int(x) if isinstance(x, float) and not np.isnan(x) and x == int(x) else x


def _is_node_match(pattern, node):
    """
    General pattern matcher for tree methods that match on tree items. Pattern can be a tree depth; an ID;
    a dataframe; or a full- or partial- path regex, glob, or literal;
    """
    if pattern is None:
        return node['Depth'] == 1
    if isinstance(pattern, str):
        if _common.is_guid(pattern):
            if isinstance(node['ID'], str) and pattern.upper() == node['ID'].upper():
                return True
            if isinstance(node['Referenced ID'], str) and pattern.upper() == node['Referenced ID'].upper():
                return True
        else:
            pattern = _node_match_string_to_regex_list(pattern)
    if isinstance(pattern, list):
        return _is_node_match_via_regex_list(pattern, node)
    if isinstance(pattern, int):
        return node['Depth'] == pattern
    if isinstance(pattern, pd.DataFrame):
        # TODO CRAB-24290 Insert with parents & children defined by dataframes
        return False
    return False


def _node_match_string_to_regex_list(pattern):
    """
    :param pattern: String name match (case-insensitive equality, globbing, regex, column values)
                    or string path match (full or partial; case-insensitive equality, globbing, or regex)
    :return: A list of regular expressions that match the last n names in the full path of a node.
    """
    patterns = _common.path_string_to_list(pattern)
    return [_exact_or_glob_or_regex(p) for p in patterns]


def _exact_or_glob_or_regex(pat):
    try:
        re.compile(pat)
        return re.compile('(?i)' + '(' + ')|('.join([re.escape(pat), fnmatch.translate(pat), pat]) + ')')
    except re.error:
        return re.compile('(?i)' + '(' + ')|('.join([re.escape(pat), fnmatch.translate(pat)]) + ')')


def _is_node_match_via_regex_list(pattern_list, node):
    path_list = _common.path_string_to_list(_get_full_path(node))
    offset = len(path_list) - len(pattern_list)
    if offset < 0:
        return None
    out = []
    for i in range(len(pattern_list)):
        match = pattern_list[i].fullmatch(path_list[offset + i])
        if match is None:
            return None
        out.append(match)
    return out


def _find_root_nodes(workbook_id, matcher):
    trees_api = TreesApi(_login.client)
    matching_root_nodes = list()

    offset = 0
    limit = _config.options.search_page_size
    kwargs = dict()
    # Can't use get_tree_root_nodes()'s `properties` filter for scoped_to because the endpoint is case-sensitive and
    # we want both global and scoped nodes.
    if workbook_id and workbook_id is not _common.EMPTY_GUID:
        kwargs['scoped_to'] = workbook_id

    keep_going = True
    while keep_going:
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        root_nodes = trees_api.get_tree_root_nodes(**kwargs)  # type: AssetTreeOutputV1
        for root_node in root_nodes.children:  # type: TreeItemOutputV1
            if matcher(root_node):
                # A root node matching the name was already found. Choose a best_root_node based on this priority:
                # Workbook-scoped SPy assets > workbook-scoped assets > global SPy assets > global assets
                has_scope = hasattr(root_node, 'scoped_to') and _common.is_guid(root_node.scoped_to)
                workbook_scoped_score = 2 if has_scope is not None else 0
                spy_created_score = 1 if _item_output_has_sdl_datasource(root_node) else 0
                setattr(root_node, 'score', workbook_scoped_score + spy_created_score)
                matching_root_nodes.append(root_node)
        keep_going = root_nodes.next is not None
        offset = offset + limit
    return matching_root_nodes


def _find_root_node_by_name(name, workbook_id, status):
    """
    Finds the Seeq ID of a case-insensitive name match of existing root nodes.
    """
    if not _login.client:
        # User is not logged in or this is a unit test. We must create a new tree.
        return None
    status.update('Finding best root.', _common.Status.RUNNING)

    name_pattern = re.compile('(?i)^' + re.escape(name) + '$')
    matching_root_nodes = _find_root_nodes(workbook_id, lambda root_node: name_pattern.match(root_node.name))
    if len(matching_root_nodes) == 0:
        status.update(f"No existing root items were found matching '{name}'.", _common.Status.RUNNING)
        return None
    best_score = max([getattr(n, 'score') for n in matching_root_nodes])
    best_root_nodes = list(filter(lambda n: getattr(n, 'score') == best_score, matching_root_nodes))
    if len(best_root_nodes) > 1:
        e = SPyValueError(
            f"More than one existing tree was found with name '{name}'. Please use an ID to prevent ambiguities.")
        status.exception(e, throw=True)
    best_id = best_root_nodes[0].id
    if len(matching_root_nodes) > 1:
        status.update(f"{len(matching_root_nodes)} root items were found matching '{name}'. Selecting {best_id}.",
                      _common.Status.RUNNING)
    return best_id


def _process_properties(df, existing_tree_df=None, pull_nodes=True):
    """
    Sanitize and pull item properties into an input dataframe. Steps in order:
    -- Pulls missing properties for items with ID provided
    -- Filters out properties not in _dataframe_columns
    -- Determines tree depth
    -- Determines (if possible_tree_copy is True) if the input dataframe corresponds to an existing SPy tree
        -- If it is indeed a copy of a SPy tree, pulls in calculations from the original tree
        -- Otherwise, it converts all items with IDs into references
    """
    df = df.reset_index(drop=True)

    df = df.apply(_process_row_properties, axis=1, pull_nodes=pull_nodes)

    def _row_is_from_existing_tree(row):
        if existing_tree_df is None or not _common.present(row, 'ID'):
            return 'new'
        same_id_rows = existing_tree_df[existing_tree_df.ID.str.casefold() == row['ID'].casefold()]
        if len(same_id_rows) != 1:
            return 'new'
        if _common.present(row, 'Type') and row['Type'].casefold() != same_id_rows.Type.iloc[0].casefold():
            return 'new'
        if _common.present(row, 'Name') and row['Name'].casefold() != same_id_rows.Name.iloc[0].casefold():
            return 'modified'
        if _common.present(row, 'Path') and row['Path'].casefold() != same_id_rows.Path.iloc[0].casefold():
            return 'modified'
        return 'pre-existing'

    row_type = df.apply(_row_is_from_existing_tree, axis=1)
    modified_item_ids = df.loc[row_type == 'modified', 'ID'] if 'ID' in df.columns else list()

    # For the nodes that originated from the pre-existing SPy tree we are modifying, we want to pull
    # pre-existing calculations directly.
    formulas_api = FormulasApi(_login.client)
    df.loc[row_type == 'pre-existing', :] = df.loc[row_type == 'pre-existing', :].apply(_pull_calculation, axis=1,
                                                                                        formulas_api=formulas_api)

    # For the nodes that originate from places other than the pre-existing SPy tree we are modifying,
    # we want to build references so we create and modify *copies* and not the original items.
    df.loc[row_type != 'pre-existing', :] = df.loc[row_type != 'pre-existing', :].apply(_make_node_reference, axis=1)

    _common.add_properties_to_df(df, modified_item_ids=modified_item_ids)
    return df


def _process_row_properties(row, pull_nodes=True):
    if _common.present(row, 'ID') and pull_nodes:
        new_row = _pull_node(row['ID'])
    else:
        new_row = pd.Series(index=_dataframe_columns, dtype='object')

    # In case that properties are specified, but IDs are given, the user-given properties
    # override those pulled from Seeq
    for prop, value in row.items():
        if prop in ['Path', 'Asset']:
            prop = 'Path'
            value = _determine_path(row)
        if prop == 'Type' and _common.present(new_row, 'Type') and _type_differs(value, new_row['Type']):
            new_row['ID'] = np.nan
        _add_tree_property(new_row, prop, value)

    if not _common.present(new_row, 'Type') and not _common.present(new_row, 'Formula'):
        new_row['Type'] = 'Asset'

    if not _common.present(new_row, 'Path'):
        new_row['Path'] = ''
    new_row['Depth'] = new_row['Path'].count('>>') + 2 if new_row['Path'] else 1

    if _common.present(row, 'Friendly Name'):
        new_row['Name'] = row['Friendly Name']

    return new_row


def _make_node_reference(row):
    row = row.copy()
    if _common.present(row, 'ID'):
        if _common.get(row, 'Type') in _data_types and not is_reference(row):
            _metadata.build_reference(row)
        if _common.present(row, 'ID'):
            row['Referenced ID'] = row['ID']
    row['ID'] = np.nan
    return row


def is_reference(row):
    if not _common.get(row, 'Referenced ID') or not _common.get(row, 'Formula Parameters'):
        return False
    formula = _common.get(row, 'Formula')
    if formula is not None and re.match(r'^\$\w+$', formula):
        return True
    else:
        return False


def _pull_calculation(row, formulas_api):
    if _common.get(row, 'Type') in _calculated_types and _common.present(row, 'ID'):
        row = row.copy()
        formula_output = formulas_api.get_item(id=row['ID'])  # type: FormulaItemOutputV1
        row['Formula'] = formula_output.formula
        row['Formula Parameters'] = [
            '%s=%s' % (p.name, p.item.id if p.item else p.formula) for p in formula_output.parameters
        ]
    return row


def _pull_node(node_id):
    """
    Returns a dataframe row corresponding to the item given by node_id
    """
    items_api = _login.get_api(ItemsApi)

    item_output = items_api.get_item_and_all_properties(id=node_id)  # type: ItemOutputV1
    node = pd.Series(index=_dataframe_columns, dtype='object')

    # Extract only the properties we use
    node['Name'] = item_output.name
    node['Type'] = item_output.type
    node['ID'] = item_output.id  # If this should be a copy, it'll be converted to 'Referenced ID' later
    for prop in item_output.properties:  # type: PropertyOutputV1
        _add_tree_property(node, prop.name, prop.value)

    return node


def _add_tree_property(properties, key, value):
    """
    If the property is one which is used by SPy Trees, adds the key+value pair to the dict.
    """
    if key in _dataframe_columns:
        value = _common.none_to_nan(value)
        if isinstance(value, str) and key in ['Cache Enabled', 'Archived', 'Enabled', 'Unsearchable']:
            # Ensure that these are booleans. Otherwise Seeq Server will silently ignore them.
            value = (value.lower() == 'true')
        if key not in properties or not (pd.api.types.is_scalar(value) and pd.isnull(value)):
            properties[key] = value
    return properties


def _item_output_has_sdl_datasource(item_output):
    for prop in item_output.properties:  # type: PropertyOutputV1
        if prop.name == 'Datasource Class' and prop.value == _common.DEFAULT_DATASOURCE_CLASS:
            return True
    return False


def _get_existing_spy_tree(df, workbook_id):
    if 'ID' not in df.columns or not _login.client:
        return None

    df = df[df['ID'].notnull()]
    if 'Path' in df.columns:
        df = df[(df['Path'] == '') | (df['Path'].isnull())]

    def _spy_tree_root_filter(root):
        return root.scoped_to is not None and _item_output_has_sdl_datasource(root)

    existing_spy_trees = _find_root_nodes(workbook_id, _spy_tree_root_filter)

    def _row_is_spy_tree_root(_row, root_id, root_name):
        try:
            assert _common.present(_row, 'ID') and _row['ID'].casefold() == root_id.casefold()
            assert not _common.present(_row, 'Name') or _row['Name'].casefold() == root_name.casefold()
            assert not _common.get(_row, 'Path')
            return True
        except AssertionError:
            return False

    df_root_id = None
    for spy_tree in existing_spy_trees:
        for _, row in df.iterrows():
            if _row_is_spy_tree_root(row, spy_tree.id, spy_tree.name):
                if df_root_id is None:
                    df_root_id = row['ID']
                else:
                    return None
    if df_root_id is not None:
        existing_tree_df = spy.search([{'ID': df_root_id}, {'Asset': df_root_id}], workbook=workbook_id,
                                      order_by=['ID'], quiet=True)
        existing_tree_df['Path'] = existing_tree_df.apply(_determine_path, axis=1)
        existing_tree_df = existing_tree_df[['ID', 'Path', 'Name', 'Type']]
        return existing_tree_df
    else:
        return None


def _determine_path(row):
    """
    Gets the path from the Path and Asset columns
    """
    path = _common.get(row, 'Path')
    asset = _common.get(row, 'Asset')
    if not isinstance(path, str):
        path = None
    if not isinstance(asset, str):
        asset = None
    return ' >> '.join([s for s in (path, asset) if s is not None])


def _validate_and_filter(df_to_validate, status, errors, stage, error_message, fatal_message=None,
                         raise_if_all_filtered=False):
    """
    This is the main validation function. It takes a dataframe as input, and returns a dataframe containing the rows
    for which no errors were found, and a dataframe containing the rows for which errors were found.

    :param df_to_validate: DataFrame input
    :param status: Status object to raise exception to if error is found and errors='raise'
    :param errors: Determines whether errors raise an exception or are catalogued in the output

    :param stage: {'input', 'pre-insert', 'final'} This must be a key in _property_validations. Indicates which
    property validations we want to perform on df_to_validate, depending on whether it is a user-input
    dataframe, a dataframe about to be saved to Tree._dataframe, or some intermediary dataframe. Additionally,
    we only check the tree structure of the dataframe if stage='final'

    :param error_message: The error message header to pass to the exception if one is raised
    :param fatal_message: When stage='final' and errors='catalog', we always double check that validation is
    successful on a filtered dataframe. If not, then we raise an exception with fatal_message as the header

    :return filtered_df: A validated dataframe with invalid rows removed
    :return bad_results: The invalid rows of the input dataframe, with their errors stored in a 'Result' column
    """
    raise_if_all_filtered = raise_if_all_filtered or stage == 'final'
    error_summaries, error_series = _validate(df_to_validate, stage)
    if len(error_summaries) != 0:
        if errors == 'raise':
            df_to_validate['Result'] = error_series
            if len(df_to_validate) > 20 and (error_series.head(20) == '').all():
                # Filter status dataframe so rows with errors are visible
                status.df = df_to_validate[error_series != '']
            else:
                status.df = df_to_validate
            _raise_error_summaries(error_message, error_summaries, status)
        else:
            keep_items = error_series == ''
            bad_results = df_to_validate[~keep_items]
            bad_results['Result'] = _update_error_msg('Failure:', error_series[~keep_items])
            filtered_df = df_to_validate[keep_items]

            if raise_if_all_filtered and filtered_df.empty:
                status.df = bad_results
                status.warn('All rows encountered errors and tree could not be constructed')
                _raise_error_summaries(error_message, error_summaries, status)

            if stage == 'final':
                # We validate again to ensure that self._dataframe will stay valid. Something is fatally wrong
                # with validation if the following code is reached.
                further_error_summaries, error_series = _validate(filtered_df)
                if len(further_error_summaries) != 0:
                    filtered_df['Result'] = error_series
                    status.df = filtered_df
                    _raise_error_summaries(fatal_message if fatal_message else 'Tree validation failed',
                                           error_summaries, status)

            return _rectify_column_order(filtered_df), _rectify_column_order(bad_results)
    else:
        return _rectify_column_order(df_to_validate), pd.DataFrame()


def _validate(df, stage='final'):
    error_summaries_properties, error_series_properties = _validate_properties(df, stage)
    if stage == 'final':
        # Only do tree validation in the final validation step, i.e., when this df represents a tree
        # Don't do tree validation on rows that had property errors
        ignore_rows = error_series_properties != ''
        error_summaries_tree, error_series_tree = _validate_tree_structure(df, ignore_rows=ignore_rows)
    else:
        error_summaries_tree, error_series_tree = [], pd.Series('', index=df.index)

    error_summaries = error_summaries_properties + error_summaries_tree
    error_series = _update_error_msg(error_series_properties, error_series_tree)

    return error_summaries, error_series


def _raise_error_summaries(error_message, error_summaries, status):
    msg = error_message
    if len(error_summaries) == 1:
        msg += ': ' + error_summaries[0]
    else:
        msg += ':\n *** ' + '\n *** '.join(error_summaries[:MAX_ERRORS_DISPLAYED])
    if len(error_summaries) > MAX_ERRORS_DISPLAYED:
        additional_errors = len(error_summaries) - MAX_ERRORS_DISPLAYED
        msg += f'\n *** {additional_errors} additional issue{"s" if additional_errors > 1 else ""} found.'
    status.exception(SPyRuntimeError(msg), throw=True)


def _update_error_msg(old_msg, new_msg):
    if new_msg is None or isinstance(new_msg, str) and new_msg == '':
        return old_msg
    out = old_msg + ' ' + new_msg
    if isinstance(out, pd.Series):
        return out.str.strip()
    else:
        return out.strip()


def _validate_tree_structure(df, ignore_rows=None):
    # Asserts that:
    # - The tree is non-empty
    # - The root doesn't have a path, and is the only item with depth 1
    # - The dataframe is sorted by path
    # - There are no missing assets referenced in paths
    # - Paths reflect names of preceding items
    # - Depths reflects lengths of paths

    size = len(df)
    if size == 0:
        return ['Tree must be non-empty.'], pd.Series(dtype='string')

    error_series = pd.Series('', index=df.index)
    error_summaries = []
    if ignore_rows is None:
        ignore_rows = pd.Series(False, index=df.index)

    prev_path = list()
    _decorate_with_full_path(df)
    for i, row in df.iterrows():
        if error_series.iloc[i]:
            # Node has an error message already due to a bad ancestor
            continue

        depth = row.Depth
        this_path = row['Full Path List']

        try:
            if ignore_rows[i]:
                # Ignore tree errors on this row because of a property validation error
                # We still want invalidate its children if possible, so we raise an assertion error with no message
                assert False, ''

            assert depth == len(this_path), 'Item\'s depth does not match its path.'

            if i == 0:
                assert len(this_path) == 1, 'The root of the tree cannot be assigned a path.'
                # The following assertion will be handled differently to include node names in the error message
                assert (df['Full Path List'].iloc[1:].apply(len) != 1).all(), 'A tree can only have one root but ' \
                                                                              'multiple were given: '
            else:
                assert depth >= 1, 'Only depths greater or equal to 1 are valid.'

            if depth <= len(prev_path):
                assert prev_path[:depth - 1] == this_path[:depth - 1], 'Item\'s position in tree ' \
                                                                       'does not match its path.'
                assert prev_path[depth - 1] < this_path[depth - 1], 'Item is not stored in proper ' \
                                                                    'position sorted by path.'
            else:
                assert depth == len(prev_path) + 1, 'Item has an ancestor not stored in this tree.'
                assert prev_path[:depth - 1] == this_path[:depth - 1], 'Item\'s position in tree ' \
                                                                       'does not match its path.'

            prev_path = this_path

        except AssertionError as e:
            message = str(e)
            if message.startswith('A tree can only have one root'):
                roots = df.Depth == 1
                message += '"%s".' % '\", \"'.join(df.Name[roots])
                error_series[roots] = message
                error_series[~roots] = 'Item\'s parent is invalid.'
                error_summaries.append(message)
                break
            error_series[i] = message
            children = df['Full Path List'].apply(
                lambda path: len(path) > len(this_path) and path[:len(this_path)] == this_path)
            error_series[children] = 'Item\'s parent is invalid.'
            if message:
                error_summaries.append(f'Invalid item with path "{" >> ".join(this_path)}": ' + message)

    _remove_full_path(df)

    return error_summaries, error_series


def _validate_properties(df, stage):
    """
    :param df: The dataframe to be validated for errors related to presence of properties, type of properties,
    and ill-defined properties
    """
    error_series = pd.Series('', index=df.index)
    error_message_map = dict()  # maps error messages to the rows that encountered the error
    for index, node in df.iterrows():
        errors = _validate_node_properties(node, stage)
        for error in errors:
            _common.get(error_message_map, error, default=list(), assign_default=True).append((index, node))
        if errors:
            error_series[index] = ' '.join(errors)

    error_summaries = _collect_error_messages(error_message_map)

    # TODO CRAB-24296 Validate calculations better
    return error_summaries, error_series


def _collect_error_messages(error_message_map):
    def _get_row_description(index, row):
        description_properties = dict()
        # Prefer Friendly Name over Name
        if _common.present(row, 'Friendly Name'):
            description_properties['friendly name'] = row['Friendly Name']
        elif _common.present(row, 'Name'):
            description_properties['name'] = row['Name']
        # If a Name or Friendly Name has been found, add a Path too if it is present
        if len(description_properties) != 0 and (_common.present(row, 'Path') or _common.present(row, 'Asset')):
            description_properties['path'] = _determine_path(row)
        # Use ID next if it is present
        if len(description_properties) == 0 and _common.present(row, 'ID'):
            description_properties['ID'] = row['ID']

        # Use index if none of the above are present
        if len(description_properties) == 0:
            return f'row with index {index}'
        else:
            return 'row with ' + ' and '.join([f'{prop_name} "{prop_value}"' for prop_name, prop_value in
                                               description_properties.items()])

    def _get_row_descriptiveness_score(row):
        _, row = row
        if _common.present(row, 'Name') or _common.present(row, 'Friendly Name'):
            if _common.present(row, 'Path') or _common.present(row, 'Asset'):
                return 3
            else:
                return 2
        elif _common.present(row, 'ID'):
            return 1
        else:
            return 0

    def _get_most_descriptive_row(_rows):
        index, row = max(_rows, key=_get_row_descriptiveness_score)
        return _get_row_description(index, row)

    collected_messages = list()
    for message, rows in error_message_map.items():
        if len(collected_messages) >= MAX_ERRORS_DISPLAYED:
            # No need to fuss with error messaging formatting that won't be displayed. We pass in placeholder string
            collected_messages.extend(('' for _ in range(len(error_message_map) - MAX_ERRORS_DISPLAYED)))
            break
        if len(rows) == 1:
            collected_messages.append(f'Issue with {_get_row_description(*rows[0])}: {message}')
        else:
            collected_messages.append(f'Issue with {_get_most_descriptive_row(rows)} and '
                                      f'{len(rows) - 1} other row{"s" if len(rows) > 2 else ""}: {message}')
    return collected_messages


def _validate_node_properties(node, stage):
    def has_bad_type(column, dtype):
        if _common.present(node, column):
            datum = _safe_int_cast(node[column])
            try:
                _common.validate_argument_types([(datum, '', dtype)])
            except TypeError:
                return True
        return False

    def dtype_names(dtype):
        if isinstance(dtype, tuple):
            return tuple(x.__name__ for x in dtype)
        return dtype.__name__

    errors = [f"The property '{column}' must have one of the following types: {dtype_names(dtype)}."
              for column, dtype in _dataframe_dtypes.items() if has_bad_type(column, dtype)]

    # The conditions in _property_validations assume that values have the correct datatype
    # Therefore, return only type errors if they exist.
    if errors:
        return errors
    errors += [message for requirement, message in _property_validations[stage] if not requirement(node)]
    return errors


def _no_repeated_nested_paths(path_list, name, recurse=True):
    if len(path_list) == 0:
        return True
    if path_list[-1] == name:
        return False
    return _no_repeated_nested_paths(path_list[:-1], path_list[-1]) if recurse else True


def _rectify_column_order(df):
    standard_columns = [col for col in _dataframe_columns if col in df.columns]
    extra_columns = sorted([col for col in df.columns if col not in _dataframe_columns])
    columns = standard_columns + extra_columns
    return df[columns]


_property_validations = {
    'input': [
        (lambda node: _common.get(node, 'ID') or _common.get(node, 'Name') or _common.get(node, 'Friendly Name'),
         "The property 'Name' or 'Friendly Name' is required for all nodes without ID."),
        (lambda node: (not _common.get(node, 'Type') or _common.get(node, 'Formula') or
                       ('Condition' not in node['Type'] and 'Signal' not in node['Type']) or
                       _common.get(node, 'ID')),
         "Stored Signals and Conditions are not yet supported. "
         "All Signals and Conditions require either a formula or an ID."),
        (lambda node: (not _common.present(node, 'Formula') or '$' not in node['Formula'] or
                       _common.get(node, 'Formula Parameters')),
         "Calculations whose formulas use variables must be assigned a 'Formula Parameters' property."),
        # TODO CRAB-24637 check required properties for metrics and remove the below
        (lambda node: not _common.present(node, 'Type') or 'Metric' not in _common.get(node, 'Type'),
         "Threshold Metrics are not yet supported."),
        (lambda node: not (_common.present(node, 'ID') or _common.present(node, 'Referenced ID')) or _login.client,
         "Must log in via spy.login() before inserting an item via ID or Referenced ID."),
        (lambda node: not _common.present(node, 'ID') or _common.is_guid(node['ID']),
         "The given 'ID' property value is not a valid GUID."),
        (lambda node: not _common.present(node, 'Referenced ID') or _common.is_guid(node['Referenced ID']),
         "The given 'Referenced ID' property value is not a valid GUID."),
        (lambda node: (not (_common.get(node, 'Path') and _common.get(node, 'Name')) or
                       _no_repeated_nested_paths(_common.path_string_to_list(node['Path']), node['Name'])),
         "Paths with repeated names (e.g., 'Tree Root >> Location A >> Location A >> Cooling Tower') are not valid.")
    ],
    'pre-insert': [
        # TODO CRAB-24637 check required properties for metrics and remove the below
        (lambda node: not _common.present(node, 'Type') or 'Metric' not in _common.get(node, 'Type'),
         "Threshold Metrics are not yet supported.")
    ],
    'final': [
        (lambda node: _common.get(node, 'Formula') or _common.get(node, 'Type'),
         "The property 'Type' is required for all items without formulas."),
        (lambda node: (not _common.get(node, 'Type') or _common.get(node, 'Formula') or
                       ('Condition' not in node['Type'] and 'Signal' not in node['Type'])),
         "Stored Signals and Conditions are not yet supported. All Signals and Conditions require a formula."),
        (lambda node: (not _common.present(node, 'Formula') or '$' not in node['Formula'] or
                       _common.get(node, 'Formula Parameters')),
         "Calculations whose formulas use variables must be assigned a 'Formula Parameters' property."),
        # TODO CRAB-24637 check required properties for metrics and remove the below
        (lambda node: not _common.present(node, 'Type') or 'Metric' not in _common.get(node, 'Type'),
         "Threshold Metrics are not yet supported."),
        (lambda node: _common.present(node, 'Name'),
         "The property 'Name' is required."),
        (lambda node: _common.present(node, 'Path'),
         "The property 'Path' is required."),
        (lambda node: _common.present(node, 'Depth'),
         "The property 'Depth' is required."),
        (lambda node: (not _common.present(node, 'Name') or not _common.present(node, 'Path') or
                       _no_repeated_nested_paths(_common.path_string_to_list(node['Path']), node['Name'],
                                                 recurse=False)),
         "Paths with repeated names (e.g., 'Tree Root >> Location A >> Location A >> Cooling Tower') are not valid.")
    ]
}
