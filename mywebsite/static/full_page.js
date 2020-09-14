$(document).ready(function () {
    $(".md-trigger").on("click", function () {
        $(".md-modal").addClass("full-page-show");
    });

    $(".player-close").on("click", function () {
        $(".full-page-modal").removeClass("full-page-show");
    });
});
