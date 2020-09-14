
$(document).ready(function () {
    var hideFunction = (el) => {
        $(el).css(
            {
                "display": "none"
            }
        )
    }

    $(".play-btn").on("click", function (e) {
        var parent = $(this).parent().parent()
        var parentId = $(parent).data("id")

        hideFunction(this)
        hideFunction($(".thumbnail-overlay"))
        hideFunction($(".thumbnail-container"))

        document.querySelector("#video-" + parentId).play()
    })
});
