# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from django.db.models import DecimalField
from django.db.models.lookups import (
    Contains, EndsWith, Exact, GreaterThan, GreaterThanOrEqual, IContains,
    IEndsWith, IExact, IRegex, IStartsWith, LessThan, LessThanOrEqual, Regex,
    StartsWith,
)


def contains(self, compiler, connection):
    """contains and icontains"""
    lhs_sql, params = self.process_lhs(compiler, connection)
    rhs_sql, rhs_params = self.process_rhs(compiler, connection)
    params.extend(rhs_params)
    rhs_sql = self.get_rhs_op(connection, rhs_sql)
    # Chop the leading and trailing percent signs that Django adds to the
    # param since this isn't a LIKE query as Django expects.
    params[0] = params[0][1:-1]
    # Add the case insensitive flag for icontains.
    if self.lookup_name.startswith('i'):
        params[0] = '(?i)' + params[0]
    # rhs_sql is REGEXP_CONTAINS(%s, %%s), and lhs_sql is the column name.
    return rhs_sql % lhs_sql, params


def iexact(self, compiler, connection):
    lhs_sql, params = self.process_lhs(compiler, connection)
    rhs_sql, rhs_params = self.process_rhs(compiler, connection)
    params.extend(rhs_params)
    rhs_sql = self.get_rhs_op(connection, rhs_sql)
    # Wrap the parameter in ^ and $ to restrict the regex to an exact match.
    if params:
        params[0] = '^(?i)%s$' % params[0]
    else:
        # If no params, then lhs_sql is the expression/column to use as the
        # regular expression. Use concat to make the value case-insensitive.
        lhs_sql = "CONCAT('^(?i)', " + lhs_sql + ", '$')"
        rhs_sql = rhs_sql.replace('%%s', '%s')
    # rhs_sql is REGEXP_CONTAINS(%s, %%s), and lhs_sql is the column name.
    return rhs_sql % lhs_sql, params


def regex(self, compiler, connection):
    """regex and iregex"""
    lhs_sql, params = self.process_lhs(compiler, connection)
    rhs_sql, rhs_params = self.process_rhs(compiler, connection)
    params.extend(rhs_params)
    rhs_sql = self.get_rhs_op(connection, rhs_sql)
    if self.lookup_name.startswith('i'):
        params[0] = '(?i)%s' % params[0]
    else:
        params[0] = str(params[0])
    # rhs_sql is REGEXP_CONTAINS(%s, %%s), and lhs_sql is the column name.
    return rhs_sql % lhs_sql, params


def startswith_endswith(self, compiler, connection):
    """startswith, endswith, istartswith, and iendswith lookups."""
    lhs_sql, params = self.process_lhs(compiler, connection)
    rhs_sql, rhs_params = self.process_rhs(compiler, connection)
    params.extend(rhs_params)
    rhs_sql = self.get_rhs_op(connection, rhs_sql)
    # Chop the leading (endswith) or trailing (startswith) percent sign that
    # Django adds to the param since this isn't a LIKE query as Django expects.
    if 'endswith' in self.lookup_name:
        params[0] = str(params[0][1:]) + '$'
    else:
        params[0] = '^' + str(params[0][:-1])
    # Add the case insentiive flag for istartswith or iendswith.
    if self.lookup_name.startswith('i'):
        params[0] = '(?i)' + params[0]
    # rhs_sql is REGEXP_CONTAINS(%s, %%s), and lhs_sql is the column name.
    return rhs_sql % lhs_sql, params


def cast_param_to_float(self, compiler, connection):
    sql, params = self.as_sql(compiler, connection)
    if params:
        # Cast to DecimaField lookup values to float because
        # google.cloud.spanner_v1._helpers._make_value_pb() doesn't serialize
        # decimal.Decimal.
        if isinstance(self.lhs.output_field, DecimalField):
            params[0] = float(params[0])
        # Cast remote field lookups that must be integer but come in as string.
        elif (hasattr(self.lhs.output_field, 'target_field') and
                self.lhs.output_field.target_field.rel_db_type(connection) == 'INT64' and
                isinstance(params[0], str)):
            params[0] = int(params[0])
    return sql, params


def register_lookups():
    Contains.as_spanner = contains
    IContains.as_spanner = contains
    IExact.as_spanner = iexact
    Regex.as_spanner = regex
    IRegex.as_spanner = regex
    EndsWith.as_spanner = startswith_endswith
    IEndsWith.as_spanner = startswith_endswith
    StartsWith.as_spanner = startswith_endswith
    IStartsWith.as_spanner = startswith_endswith
    Exact.as_spanner = cast_param_to_float
    GreaterThan.as_spanner = cast_param_to_float
    GreaterThanOrEqual.as_spanner = cast_param_to_float
    LessThan.as_spanner = cast_param_to_float
    LessThanOrEqual.as_spanner = cast_param_to_float
