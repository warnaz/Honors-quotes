function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {

    $('.like-form').submit(function (event) {
        event.preventDefault()
        const post_id = $(this).attr('id')

        let res;
        const likes = $(`.like-count${post_id}`).text()
        const trimCount = parseInt(likes)

        const csrftoken = getCookie('csrftoken');
        $.ajax({
            method: "POST",
            url: "{% url 'love:like_urls' %}",
            headers: { 'X-CsrfToken': csrftoken },
            data:
            {
                'post_id': post_id,
            },
            success: function (response) {
                selector = $(`.like_btn${post_id}`);
                if (response.liked) {
                    $(selector).css('color', 'green')
                    res = trimCount + 1
                }
                else {
                    $(selector).css('color', 'black')
                    res = trimCount - 1
                }
                $(`.like-count${post_id}`).text(res)
            },
            error: function (er, response) {
                console.log(er, response)
            }


        });

    })
})

