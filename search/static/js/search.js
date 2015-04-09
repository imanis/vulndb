$(function () {
    $(".feed-results li").click(function () {
        var feed = $(this).attr("feed-id");
        location.href = "/feeds/" + feed + "/";
    });

    $(".projects-results li").click(function () {
        var p = $(this).attr("project-slug");
        location.href = "/projects/" + p + "/";
    });

    $(".clients-results li").click(function () {
        var c = $(this).attr("client-id");
        location.href = "/projects/client/" + c + "/";
    });

    $(".vulnerabilities-results li").click(function () {
        var v = $(this).attr("vuln-slug");
        location.href = "/vulns/" + v + "/";
    });

    $(".vulnerabilitiesinst-results li").click(function () {
        var v = $(this).attr("vuln-id");
        location.href = "/projects/show/" + v + "/";
    });

});