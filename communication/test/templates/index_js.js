const new_btn = document.getElementById("new_btn")
const image = document.getElementById("image")

const url = '{{url_for("video_feed")}}'

function take_a_photo(){
    //image.setAttribute("src", "{{ url_for('video_feed') }}")
    location.reload();
    console.log("A new photo has been taken.")
}

new_btn.addEventListener("click", take_a_photo)