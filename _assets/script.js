window.onscroll = function() {
    scrollFunction()
};

function scrollFunction() {
  if (document.body.scrollTop > 70 || document.documentElement.scrollTop > 70) {
    document.getElementById("scrollingInteraction").className = "headerSpecificPage";
    document.getElementById("container").style.marginTop = "145px";
  } else {
    document.getElementById("scrollingInteraction").className = "headerIndexPage";
    document.getElementById("container").style.marginTop = "320px";
  }
} 
