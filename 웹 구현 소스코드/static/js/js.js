/*타이핑 효과 
const content = "무슨 내용이 들어가야 할지 모르겠당s(￣▽￣)/"
const text = document.querySelector('#text')
let i = 0;

    function typing() {
        let txt =  content[i++]
        text.innerHTML += txt=== "\n" ? "<br/>" : txt;
        if(i > content.length) {
            text.textContent = ""
            i = 0;
        }

    }
    setInterval(typing, 100)*/

    /* 타이핑효과 적고 지우기 
   let i = 0,
   j = 0;

 const textArray = ["경험해보세요", "체험해보세요", "느껴보세요"],
   speed = 100,
   target = document.getElementByid("text");

 function txtnum() {
   j == textArray.length - 1
   ? j = 0
   : j++
 }

 function type() {
   i < textArray[j].length
   ? (target.innerHTML += textArray[j].charAt(i), i++, setTimeout(type, speed))
   : remove()
 }

 function remove() {
   0 <= i
   ? (target.innerHTML = target.innerHTML.slice(0, i), i--, setTimeout(remove, speed))
   : (type(), txtnum())
 }

 type();*/

 var slides = document.querySelector('.slides'),
 slide = document.querySelectorAll('.slides li'),
 currentIdx = 0,
 slideCount = slide.length,
 prevBtn =document.querySelector('.prev'),
 slidewidth = 928,
 slideMargin = 10,
 nextBtn =document.querySelector('.next');

 slides.style.width = (slidewidth + slideMargin) *slideCount - slideMargin + 'px';

function moveSlide(num) {
 slides.style.left = -num * 610 + 'px'
 currentIdx = num;
}
nextBtn.addEventListener('click', function() {
if(currentIdx < slideCount -1 ) {
 moveSlide(currentIdx +1);}else{moveSlide(0)}
})
prevBtn.addEventListener('click', function() {
 if(currentIdx > 0 ) {
  moveSlide(currentIdx - 1);}else{moveSlide(slideCount -1)}
})

/*휠이벤트
window.onload = function(){
 const elm = document.querySelectorAll('.section');
 const elmCount = elm.length;
 elm.forEach(function(item, index){
   item.addEventListener('mousewheel', function(event){
     event.preventDefault();
     let delta = 0;

     if (!event) event = window.event;
     if (event.wheelDelta) {
         delta = event.wheelDelta / 5;
         if (window.opera) delta = -delta;
     } 
     else if (event.detail)
         delta = -event.detail / 2;

     let moveTop = window.scrollY;
     let elmSelector = elm[index];

     // wheel down : move to next section
     if (delta < 0){
       if (elmSelector !== elmCount-1){
         try{
           moveTop = window.pageYOffset + elmSelector.nextElementSibling.getBoundingClientRect().top;
         }catch(e){}
       }
     }
     
     // wheel up : move to previous section
     else{
       if (elmSelector !== 0){
         try{
           moveTop = window.pageYOffset + elmSelector.previousElementSibling.getBoundingClientRect().top;
           
         }catch(e){}
       }
     }

     const body = document.querySelector('body');
     window.scrollTo({top:moveTop, left:0, behavior:'smooth'});
   });
 });
}*/