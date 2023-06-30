$(document).ready(function() {
    $(".like-dislike").click(function(event) {
        event.preventDefault();
        var id = $(this).attr("value");
        var url = "/post/" + id + "/like/";
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'id': id,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
                console.log("Success!", response);
                if (response.is_liked) {
                    $(`#like-${id}`).text('Dislike');
                    $(`#like-${id}`).removeClass("like-dislike btn btn-primary");
                    $(`#like-${id}`).addClass("like-dislike btn btn-danger");
                    $(`#total_likes-${id}`).text(response.total_likes);
                    $(`#like-${id}`).attr('id', `dislike-${id}`);
                } else {
                    $(`#dislike-${id}`).text('Like');
                    $(`#dislike-${id}`).removeClass("like-dislike btn btn-danger");
                    $(`#dislike-${id}`).addClass("like-dislike btn btn-primary");
                    $(`#dislike-${id}`).attr('id', `like-${id}`);
                    $(`#total_likes-${id}`).text(response.total_likes);
                }
            },
            error: function(rs, e) {
                console.log(rs.responseText);
            },
        })
    })
    $("#submit-comment").click(function(event) {
        event.preventDefault();
        var id = $(this).attr("value");
        var url = "/post/comment/" + id + "/";
        var dataPosted = $("#mainSubmit").serialize();
        $.ajax({
            type: 'POST',
            url: url,
            data: dataPosted,
            success: function(data) {
                $('#comments-' + data.post).prepend(`<div class="col-lg-6 offset-lg-3">
                                                    <div class="card p-2">
                                                        <div class="row">
                                                            <div class="col-12">
                                                                <strong>${data.user}</strong>
                                                            </div>
                                                            <div class="col-12">
                                                                <p class="m-1 mt-3">${data.content}</p>
                                                                <p class="text-right text-muted"><small>${data.created}</small></p>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>`)
                $(`#comment-count-${data.post}`).html(data.count)
            },
            error: function(rs, e) {
                alert("!error...")
            },
        });
    });

})