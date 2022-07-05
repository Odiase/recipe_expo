const navbar = document.querySelector(".navbar");
const slides = document.querySelectorAll(".slide");
const slider_container = document.querySelector(".sliders");

const mobile_search_bar = document.getElementById("mobile-search");

// mobile menu toggle functionality
function toggle_menu(){
    if(navbar.style.top != "75px"){
        navbar.style.top = "75px"
    }
    else{
        navbar.style.top = "-100vh"
    }
}


let show_mobile_search_bar = () =>{
    if(mobile_search_bar.style.top != "70px"){
        mobile_search_bar.style.top = "70px"
    }else{
        mobile_search_bar.style.top = "-100%"
    }
}












let height = window.innerHeight // gets the initial height of the window
if(slides && slider_container){
    function slide_down(){
        /*scrolls the slide container by the current value of the height variablee ( i.e the height of the window)*/
        slider_container.scroll(0,height);
        height += window.innerHeight // increment the height variable by the height of the window
        let slide_up_interval;
    
        // checking if the slide has scrolled to the last image, and if it has call the slide up function
        if (height == window.innerHeight * 4){
            clearInterval(slide_down_interval)  
            slide_up_interval = setInterval(slide_up,2000);
        }
    
        function slide_up(){
            // checking if the slide is in the first image, and if it is call the slide down function
            if(height == window.innerHeight){
                clearInterval(slide_up_interval);
                slide_down_interval = setInterval(slide_down,2000);
            }
            height -= window.innerHeight; // decrementing the height variable by the height of the window
            slider_container.scroll(0,height);
        }
        
    } 
    let slide_down_interval = setInterval(slide_down,3000)
}