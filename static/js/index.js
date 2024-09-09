
document.addEventListener("DOMContentLoaded", function () {
    const videos = document.querySelectorAll("video");

    videos.forEach(video => {
        video.addEventListener('ended', function () {
            video.currentTime = 0;
            video.play();
        });

        setInterval(() => {
            if (video.paused) {
                video.currentTime = 0;
                video.play();
            }
        }, 1000); // Check every 30 seconds (adjust as needed)
    });
});

$(document).ready(()=>{
    var stop_video_interval = setInterval(()=>{
        $("#demoVideo").get(0).currentTime = 0;
    }, 100);

    $("#videoplayBtn").click(()=>{
        $("#demo-player-cover").fadeOut(400);
        clearInterval(stop_video_interval);
        $("#demoVideo").get(0).play();
    })

    $("#demoVideo").click(()=>{
        $("#demo-player-cover").fadeIn(400);
        $("#demoVideo").get(0).pause();
        $('#demoVideo').get(0).currentTime = 0;
        stop_video_interval = setInterval(()=>{
            $("#demoVideo").get(0).currentTime = 0;
        }, 100);
    })
});



const animateValue = (obj, start, end, duration) => {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const target = entry.target;
            const endValue = parseInt(target.getAttribute('data-target'));
            animateValue(target, 0, endValue, 2000);
            observer.unobserve(target);
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.number-counter').forEach(counter => {
    observer.observe(counter);
});




// const headings = [
//     "Empower",
//     "Enhance",
//     "Elevate"
// ];
// let currentHeadingIndex = 0;
// const slideContainer = document.getElementById('slide-container');

// function createSlides() {
//     headings.forEach(heading => {
//         const slideItem = document.createElement('div');
//         slideItem.className = 'slide-item';
//         slideItem.innerHTML = `<h1>${heading}</h1>`;
//         slideContainer.appendChild(slideItem);
//     });
//     // Duplicate the first slide at the end for smooth looping
//     const firstSlideClone = slideContainer.children[0].cloneNode(true);
//     slideContainer.appendChild(firstSlideClone);
// }

// function slideUp() {
//     currentHeadingIndex++;
//     const slideHeight = slideContainer.children[0].offsetHeight;
//     slideContainer.style.transform = `translateY(-${currentHeadingIndex * slideHeight}px)`;
//     slideContainer.style.transition = 'transform 0.5s ease';

//     if (currentHeadingIndex >= headings.length) {
//         setTimeout(() => {
//             slideContainer.style.transition = 'none';
//             slideContainer.style.transform = 'translateY(0)';
//             currentHeadingIndex = 0;
//         }, 500);
//     }
// }

// createSlides();
// setInterval(slideUp, 3000); // Change slide every 3 seconds