if(document.getElementById("q")){
let cat="all";const q=document.getElementById("q");
function apply(){const s=q.value.toLowerCase();document.querySelectorAll(".card").forEach(c=>{c.style.display=(cat==="all"||c.dataset.cat===cat)&&c.dataset.text.includes(s)?"":"none"})}
document.querySelectorAll(".f").forEach(b=>b.onclick=()=>{document.querySelectorAll(".f").forEach(x=>x.classList.remove("on"));b.classList.add("on");cat=b.dataset.c;apply()});q.oninput=apply;
}
