if(document.getElementById("q")){
let cat="all";const q=document.getElementById("q");
function apply(){const s=q.value.toLowerCase();document.querySelectorAll(".card").forEach(c=>{c.style.display=(cat==="all"||c.dataset.cat===cat)&&c.dataset.text.includes(s)?"":"none"})}
document.querySelectorAll(".f").forEach(b=>b.onclick=()=>{document.querySelectorAll(".f").forEach(x=>x.classList.remove("on"));b.classList.add("on");cat=b.dataset.c;apply()});q.oninput=apply;
}
document.querySelectorAll("#signup-form").forEach(f=>f.addEventListener("submit",async ev=>{ev.preventDefault();const m=f.querySelector("small"),b=f.querySelector("button"),email=f.email.value.trim();
if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){m.textContent="Please enter a valid email address.";m.style.color="#ff7a7a";return}
b.disabled=true;m.style.color="#889";m.textContent="Subscribing…";
try{const r=await fetch("/api/subscribe",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email,website:f.website.value})});const j=await r.json().catch(()=>({}));
if(r.ok&&j.ok){m.textContent="You're in! Check your inbox 🎉";m.style.color="#b48cff";f.reset()}else{m.textContent=j.error||"Something went wrong. Please try again.";m.style.color="#ff7a7a"}}
catch(e){m.textContent="Network error. Please try again.";m.style.color="#ff7a7a"}finally{b.disabled=false}}));
