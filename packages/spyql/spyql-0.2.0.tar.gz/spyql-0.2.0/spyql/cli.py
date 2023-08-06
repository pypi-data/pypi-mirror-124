from spyql.processor import Processor
from spyql.quotes_handler import QuotesHandler
import spyql.utils
import spyql.log
import logging
import re
import click


query_struct_keywords = [
    "import",
    "select",
    "from",
    "explode",
    "where",
    "order by",
    "limit",
    "offset",
    "to",
]


def clean_query(q):
    """makes sure that queries start with a space (required for parse_structure)"""
    q = " " + q.strip()
    return q


def parse_structure(q):
    """parse the supported keywords, which must follow a given order"""
    keys = query_struct_keywords
    last_pos = 0
    key_matches = []
    for key in keys:
        entry = re.compile(fr"\s+{key}\s+".replace(" ", r"\s+"), re.IGNORECASE).search(
            q, last_pos
        )
        if entry:
            entry = entry.span()
            last_pos = entry[1]
        key_matches.append(entry)

    # # Alternative code where order is not enforced:
    # key_matches = [re.search(fr"\s+{key}\s+", q, re.IGNORECASE) for key in keys]
    # key_matches = [(m.span() if m else None)  for m in key_matches]

    d = {}
    for i in range(len(query_struct_keywords)):
        if not key_matches[i]:
            d[keys[i]] = None
            continue
        st = key_matches[i][1]
        nd = len(q)
        for j in range(i + 1, len(keys)):
            if key_matches[j]:
                nd = key_matches[j][0]
                break

        # this list should be empty, otherwise order of clauses was not respected
        misplaced_keys = list(
            filter(
                None,
                [
                    re.compile(
                        fr"\s+{k}\s+".replace(" ", r"\s+"), re.IGNORECASE
                    ).search(q[st:nd])
                    for k in keys
                ],
            )
        )
        if misplaced_keys:
            spyql.log.user_error(
                "could not parse query",
                SyntaxError(f"misplaced '{misplaced_keys[0][0].strip()}' clause"),
            )
        d[keys[i]] = q[st:nd]

    return d


def pythonize(s):
    """replaces sql/custom syntax by python syntax"""
    # TODO check for special SQL stuff such as in, is, like
    # s = re.compile(r"([^=<>])={1}([^=])").sub(r"\1==\2", s)
    # DECISION: expressions are PURE python code :-)

    # make sure the `as` keyword is always lowcase
    # (currently only needed for imports)
    s = re.compile(r"\s+AS\s+", re.IGNORECASE).sub(" as ", s)

    # easy shortcut for navigating through dics (of dics)
    # e.g.   `json->hello->'planet hearth'` converts into
    #       `json['hello']['planet hearth']`

    # first replace quoted keys (they do not need quotes)
    s = re.compile(r"->(%s)" % (QuotesHandler.string_placeholder_re())).sub(r"[\1]", s)
    # then replace unquoted keys (they need quotes)
    s = re.compile(r"->([^\d\W]\w*)").sub(r"['\1']", s)

    return s


def split_multi_expr_clause(s):
    """
    Transforms "abc, (123 + 1) * 2, f(a,b)"
    into ["abc", "(123 + 1) * 2", "f(a,b)"]
    """
    sin = list(s)
    sep = [-1]
    rb = 0  # ()
    cb = 0  # {}
    sb = 0  # []
    for i in range(len(sin)):
        c = sin[i]
        if c == "(":
            rb = rb + 1
        elif c == ")":
            rb = rb - 1
        elif c == "{":
            cb = cb + 1
        elif c == "}":
            cb = cb - 1
        elif c == "[":
            sb = sb + 1
        elif c == "]":
            sb = sb - 1
        elif c == "," and rb == 0 and cb == 0 and sb == 0:
            sep.append(i)
    sep.append(None)
    parts = [s[sep[i] + 1 : sep[i + 1]].strip() for i in range(len(sep) - 1)]

    return parts


def parse_select(sel, strings):
    """splits the SELECT clause into columns and find their names"""
    # TODO support column alias without AS

    sel = [c.strip() for c in split_multi_expr_clause(sel)]
    new_sel = []
    as_pattern = re.compile(r"\s+AS\s+", re.IGNORECASE)
    for i in range(len(sel)):
        c = sel[i]
        sas = re.search(as_pattern, c)
        name = ""
        if sas:
            name = c[(sas.span()[1]) :].strip()
            c = c[: (sas.span()[0])]
        else:
            # automatic output column name from expresopm
            # removes json 'variable' reference (visual garbage)
            name = re.compile(r"(\s|^)json(->|\[)").sub(r"\1", c)
            # makes the string a valid python variable name
            name = spyql.utils.make_str_valid_varname(strings.put_strings_back(name))

        if c.strip() == "*":
            c = "*"
            name = "*"
        else:
            name = strings.put_strings_back(name, quote=False)
            c = f"{make_expr_ready(c, strings)}"

        new_sel.append({"name": name, "expr": c})

    return new_sel


def parse_orderby(clause, strings):
    """splits the ORDER BY clause and handles modifiers"""

    exprs = [e.strip() for e in split_multi_expr_clause(clause)]
    res = []
    mod_pattern = re.compile(r"(?:\s+(DESC|ASC))?(?:\s+NULLS\s+(FIRST|LAST)\s*)?$")
    for i in range(len(exprs)):
        expr = exprs[i]
        modifs = re.search(mod_pattern, expr.upper())
        rev = "DESC" in modifs.groups()
        rev_nulls = ((not rev) and "FIRST" in modifs.groups()) or (
            rev and "LAST" in modifs.groups()
        )
        expr = expr[: (modifs.span()[0])]  # remove modifiers
        try:
            expr = int(expr)  # special case: expression is output column number
        except ValueError:
            expr = make_expr_ready(expr, strings)

        res.append({"expr": expr, "rev": rev, "rev_nulls": rev_nulls})

    return res


def make_expr_ready(expr, strings):
    return pythonize(expr).strip()


def parse(query):
    """parses the spyql query"""
    strings = QuotesHandler()
    query = strings.extract_strings(query)

    prs = parse_structure(query)

    if not prs["select"]:
        spyql.log.user_error(
            "could not parse query", SyntaxError("SELECT keyword is missing")
        )

    prs["select"] = parse_select(prs["select"], strings)

    for clause in set(query_struct_keywords) - {
        "select",
        "limit",
        "offset",
        "order by",
    }:
        if prs[clause]:
            prs[clause] = make_expr_ready(prs[clause], strings)

    for clause in {"order by"}:
        if prs[clause]:
            prs[clause] = parse_orderby(prs[clause], strings)

    for clause in {"limit", "offset"}:
        if prs[clause]:
            try:
                val = int(prs[clause])
                prs[clause] = val if val > 0 else 0
            except ValueError:
                prs[clause] = None

    return (prs, strings)


def parse_options(ctx, param, options):
    options = [opt.split("=", 1) for opt in options]
    for opt in options:
        if len(opt) < 2:
            raise click.BadParameter(
                f"bad format for option '{opt[0]}', format must be 'option=value'"
            )
    return {kv[0]: spyql.utils.try2eval(kv[1], globals()) for kv in options}


###############
# run
###############
def run(query, input_opt={}, output_opt={}):
    query = clean_query(query)

    prs, strings = parse(query)

    spyql.log.user_debug_dict("Parsed query", prs)
    spyql.log.user_debug_dict("Strings", strings.strings)

    processor = Processor.make_processor(prs, strings, input_opt)

    processor.go(output_opt)


@click.command()
@click.argument("query")
@click.option(
    "-I",
    "input_opt",
    type=click.UNPROCESSED,
    callback=parse_options,
    multiple=True,
    help=(
        "Set input options in the format 'option=value'. Example: -Idelimiter=,"
        " -Iheader=False"
    ),
)
@click.option(
    "-O",
    "output_opt",
    type=click.UNPROCESSED,
    callback=parse_options,
    multiple=True,
    help=(
        "Set output options in the format 'option=value'. Example: -Odelimiter=,"
        " -Oheader=False"
    ),
)
@click.option(
    "--verbose",
    "-v",
    "verbose",
    default=0,
    help=(
        "Set verbose level: -2 to supress errors and warnings; -1 to supress warnings;"
        " 0 to only show errors and warnings (default); 1 to show additional info"
        " messages; 2 to show additional debug messages."
    ),
)
@click.option(
    "-W",
    "warning_flag",
    type=click.Choice(["default", "error"]),
    default="default",
    help=(
        "Set if warnings are turned into errors or if warnings do not halt execution"
        " (default)."
    ),
)
@click.version_option(version="0.1.0")
def main(query, warning_flag, verbose, input_opt, output_opt):
    """
    Tool to run a SpyQL QUERY over text data.
    For more info visit: https://github.com/dcmoura/spyql

    \b
    [ IMPORT python_module [ AS identifier ] [, ...] ]
    SELECT
        [ * | python_expression [ AS output_column_name ] [, ...] ]
        [ FROM csv | spy | text | python_expression | json [ EXPLODE path ] ]
        [ WHERE python_expression ]
        [ ORDER BY output_column_number | python_expression
            [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] ]
        [ LIMIT row_count ]
        [ OFFSET num_rows_to_skip ]
        [ TO csv | json | spy | sql | pretty | plot ]
    """

    logging.basicConfig(level=(3 - verbose) * 10, format="%(message)s")
    spyql.log.error_on_warning = warning_flag == "error"

    run(query, input_opt, output_opt)


if __name__ == "__main__":
    main()
