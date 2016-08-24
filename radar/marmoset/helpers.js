function date(x) {
    // js2py doesn't support ISO8601 dates so we manually extract
    // the year, month, and day.
    // See: https://github.com/PiotrDabkowski/Js2Py/issues/42
    var y = x.slice(0, 4);
    var m = x.slice(5, 7);
    var d = x.slice(8, 10);
    return new Date(y, m, d);
}