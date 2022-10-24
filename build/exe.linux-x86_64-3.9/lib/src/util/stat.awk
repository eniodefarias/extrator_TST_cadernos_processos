BEGIN {
    print "<!--<html><body>--><table  border=\"1\" cellpadding=\"3\"  style=\"border-collapse: collapse\">"

    print "<!--<tr>"
    print "<th bgcolor=turquoise colspan="6">BEFORE_USAGE</th>"
    print "</tr>-->"
    print "<tr>"
    print "<th bgcolor=\"#51596a\" > <font color=\"#fff\" > Sistema de Arq </font></th>"
    print "<th bgcolor=\"#51596a\" > <font color=\"#fff\" > Tamanho </font></th>"
    print "<th bgcolor=\"#51596a\" > <font color=\"#fff\" > Usado </font></th>"
    print "<th bgcolor=\"#51596a\" > <font color=\"#fff\" > Disponivel </font></th>"
    print "<th bgcolor=\"#51596a\" > <font color=\"#fff\" > Em uso% </font></th>"
    print "<th bgcolor=\"#51596a\"> <font color=\"#fff\" > Ponto de montagem </font></th>"
    print "</tr>"
}

NR > 1 {
    bgcolor=""



    if ($5+0 > 80) {
        bgcolor=" bgcolor=#f7f5dd"

            if ($5+0 > 90) {
                bgcolor=" bgcolor=#f7e4e4"
            }

    }







    print "<tr><td"bgcolor">"$1"</td><td"bgcolor">"$2"</td><td"bgcolor">"$3"</td><td"bgcolor">"$4"</td><td"bgcolor">"$5"</td><td"bgcolor">"$6"</td></tr>"
}

END {
    print "</table><!--</body></html>-->"
}