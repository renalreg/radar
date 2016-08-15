function date(x) {
    var y = x.slice(0, 4);
    var m = x.slice(5, 7);
    var d = x.slice(8, 10);
    return new Date(y, m, d);
}